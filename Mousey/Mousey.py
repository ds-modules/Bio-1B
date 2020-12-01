import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import time
import multiprocessing

output = widgets.Output()

migration_const = 1.0 / (1.0 - np.exp(-1.0))
    
class Geno(Enum):
    dd = 0
    Dd = 1
    DD = 2

def geno_to_pheno(geno):
    pheno = np.array(geno)
    pheno[geno == Geno.dd] = 'white'
    pheno[geno != Geno.dd] = 'black'
    return pheno

def report_geno_before_counts(geno, lava):
    sand_before_DD.value = sum(geno[~lava] == Geno.DD)
    sand_before_Dd.value = sum(geno[~lava] == Geno.Dd)
    sand_before_dd.value = sum(geno[~lava] == Geno.dd)
    lava_before_DD.value = sum(geno[lava] == Geno.DD)
    lava_before_Dd.value = sum(geno[lava] == Geno.Dd)
    lava_before_dd.value = sum(geno[lava] == Geno.dd)

def report_geno_after_counts_and_get_geno_dist(geno, lava, mortality_mask, settings):
    sand_after_DD.value = sum((geno[~lava] == Geno.DD) & ~mortality_mask[~lava])
    sand_after_Dd.value = sum((geno[~lava] == Geno.Dd) & ~mortality_mask[~lava])
    sand_after_dd.value = sum((geno[~lava] == Geno.dd) & ~mortality_mask[~lava])
    lava_after_DD.value = sum((geno[lava] == Geno.DD) & ~mortality_mask[lava])
    lava_after_Dd.value = sum((geno[lava] == Geno.Dd) & ~mortality_mask[lava])
    lava_after_dd.value = sum((geno[lava] == Geno.dd) & ~mortality_mask[lava])
    m = settings['mutation_rate']
    def apply_mutation_to_dist(p):
        nonlocal m
        return p * (1-m) + (1-p) * m
    s = settings['num_mice'] - (2*settings['mortality_count'])
    sand_D = apply_mutation_to_dist((2 * sand_after_DD.value + sand_after_Dd.value) / s)
    sand_d = apply_mutation_to_dist((2 * sand_after_dd.value + sand_after_Dd.value) / s)
    lava_D = apply_mutation_to_dist((2 * lava_after_DD.value + lava_after_Dd.value) / s)
    lava_d = apply_mutation_to_dist((2 * lava_after_dd.value + lava_after_Dd.value) / s)
    def hardy_weinberg(D, d):
        return (d ** 2, 2 * D * d, D ** 2)
    return (hardy_weinberg(sand_D, sand_d), hardy_weinberg(lava_D, lava_d))
    
def iterate_generation(x, y, geno, pheno, settings):
    # MOVEMENT
    lava = x > 0.5
    x += (np.random.random(settings['num_mice']) >= 0.95) * (np.random.random(settings['num_mice']) - 0.5) * 0.1
    y += (np.random.random(settings['num_mice']) >= 0.95) * (np.random.random(settings['num_mice']) - 0.5) * 0.1
    # Keep within bounding box
    x += (x < 0) * (~lava) * 2 * (0 - x)
    x -= (x > 0.5) * (~lava) * 2 * (x - 0.5)
    x += (x < 0.5) * (lava) * 2 * (0.5 - x)
    x -= (x > 1) * (lava) * 2 * (x - 1)
    y += (y < 0) * 2 * (0 - y)
    y -= (y > 1) * 2 * (y - 1)
    
    # MIGRATION
    # Choose indices to migrate + create mask of mice to flip
    migration_mask = np.zeros(x.shape)
    migration_mask[np.random.choice(np.nonzero(lava)[0], settings['migration_count'], replace=False)] = 1
    migration_mask[np.random.choice(np.nonzero(~lava)[0], settings['migration_count'], replace=False)] = 1
    x += (migration_mask) * 2 * (0.5 - x)
    
    # REPORT GENOTYPES
    report_geno_before_counts(geno, lava)
    
    # MORTALITY
    # Choose indices to die + create mask of mice to progenate
    white = pheno == 'white'
    mortality_mask = np.zeros(x.shape).astype(bool)
    # Choosing mice to kill
    p = lava.astype(float) + (white & lava) * ((1.0 / (1.0 - settings['selection_intensity'])) - 1)
    mortality_mask[np.random.choice(range(settings['num_mice']), settings['mortality_count'], replace=False, p=p/np.sum(p))] = True
    p = (~lava).astype(float) + (~white & ~lava) * ((1.0 / (1.0 - settings['selection_intensity'])) - 1)
    mortality_mask[np.random.choice(range(settings['num_mice']), settings['mortality_count'], replace=False, p=p/np.sum(p))] = True
    
    # REPORT GENOTYPES
    geno_dist = report_geno_after_counts_and_get_geno_dist(geno, lava, mortality_mask, settings)
    
    # REPRODUCTION & MUTATION
    geno[(~lava & mortality_mask)] = np.random.choice([Geno.dd, Geno.Dd, Geno.DD], settings['mortality_count'], p=geno_dist[0])
    geno[(lava & mortality_mask)] = np.random.choice([Geno.dd, Geno.Dd, Geno.DD], settings['mortality_count'], p=geno_dist[1])
    
    return x, y, geno

settings_layout=widgets.Layout(width='50%')
speed_slider = widgets.FloatSlider(value=0.25, min=0.25, max=2, readout=False, layout=settings_layout)
num_mice_in = widgets.BoundedIntText(value=1000, min=0, max=10000, layout=settings_layout)
mutation_rate_in = widgets.BoundedFloatText(value=0.001, min=0, max=1, layout=settings_layout)
selection_intensity_in = widgets.BoundedFloatText(value=0.05, min=0, max=1, layout=settings_layout)
mortality_rate_in = widgets.BoundedFloatText(value=0.25, min=0, max=1, layout=settings_layout)
migration_rate_in = widgets.BoundedFloatText(value=0, min=0, max=1, layout=settings_layout)
labels = ['Simulation Speed', '# of Mice', 'Mutation Rate', 'Selection Intensity', 'Mortality Rate', 'Migration Rate']
settings_labels = widgets.VBox([widgets.Label(value=label) for label in labels])
settings = widgets.VBox([speed_slider, num_mice_in, mutation_rate_in, selection_intensity_in, mortality_rate_in, migration_rate_in])
simulate_button = widgets.Button(description='Simulate', layout=widgets.Layout(width='99%'))
reset_button = widgets.Button(description='Reset', layout=widgets.Layout(width='99%'))
clear_button = widgets.Button(description='Clear', layout=widgets.Layout(width='99%'))
debug = widgets.Textarea(layout=widgets.Layout(height='50%', width='99%'), value='') # TODO: Remove this when done with dev
control_bar = widgets.VBox([widgets.HBox([settings_labels, settings]), simulate_button, clear_button, reset_button, debug])

geno_layout=widgets.Layout(width='80%')
sand_before_DD = widgets.IntText(description='DD', value=0, layout=geno_layout)
sand_before_Dd = widgets.IntText(description='Dd', value=0, layout=geno_layout)
sand_before_dd = widgets.IntText(description='dd', value=0, layout=geno_layout)
sand_after_DD = widgets.IntText(description='DD', value=0, layout=geno_layout)
sand_after_Dd = widgets.IntText(description='Dd', value=0, layout=geno_layout)
sand_after_dd = widgets.IntText(description='dd', value=0, layout=geno_layout)
lava_before_DD = widgets.IntText(description='DD', value=0, layout=geno_layout)
lava_before_Dd = widgets.IntText(description='Dd', value=0, layout=geno_layout)
lava_before_dd = widgets.IntText(description='dd', value=0, layout=geno_layout)
lava_after_DD = widgets.IntText(description='DD', value=0, layout=geno_layout)
lava_after_Dd = widgets.IntText(description='Dd', value=0, layout=geno_layout)
lava_after_dd = widgets.IntText(description='dd', value=0, layout=geno_layout)
center_layout = widgets.Layout(display="flex", justify_content="center")
sand_before = widgets.VBox([widgets.Label(value='Before Selection', layout=center_layout), sand_before_DD, sand_before_Dd, sand_before_dd])
sand_after = widgets.VBox([widgets.Label(value='After Selection', layout=center_layout), sand_after_DD, sand_after_Dd, sand_after_dd])
lava_before = widgets.VBox([widgets.Label(value='Before Selection', layout=center_layout), lava_before_DD, lava_before_Dd, lava_before_dd])
lava_after = widgets.VBox([widgets.Label(value='After Selection', layout=center_layout), lava_after_DD, lava_after_Dd, lava_after_dd])
geno_counts = widgets.HBox([sand_before, sand_after, lava_before, lava_after])

def get_settings():
    return {
            "speed": speed_slider.value,
            "num_mice": num_mice_in.value,
            "mutation_rate": mutation_rate_in.value,
            "selection_intensity": selection_intensity_in.value,
            "mortality_rate": mortality_rate_in.value,
            "migration_rate": migration_rate_in.value,
            "migration_count": int((migration_rate_in.value * num_mice_in.value) / 2),
            "mortality_count": int((mortality_rate_in.value * num_mice_in.value) / 2)
        }