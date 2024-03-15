import numpy as np
import pandas as pd
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
from IPython.display import display
from IPython.display import clear_output
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def mean_difference(stat, data):
    
    def difference_in_means(pd_series):
        return abs(pd_series['North'].mean(numeric_only=True) - pd_series['South'].mean(numeric_only=True))

    n_repeats = 1000
    permutation_differences = np.array([])
    for i in range(n_repeats):
        permutation = pd.Series(
            np.array(data[stat].sample(len(data[stat]))),
            index=np.array(data['Fork'])
        )
        new_difference = np.array(difference_in_means(permutation))
        permutation_differences = np.append(permutation_differences, new_difference)
        
    observed_difference = abs(data[data['Fork']=='North'].mean(numeric_only=True) - data[data['Fork']=='South'].mean(numeric_only=True))
    p_val_count = sum(i > observed_difference[stat] for i in permutation_differences)/len(permutation_differences)
    
    plt.figure(figsize=(12,4))
    
    plt.subplot(121)
    dataNorth = data[data['Fork'] == 'North']
    dataSouth = data[data['Fork'] == 'South']
    plt.hist(dataNorth[stat], color='blue', alpha=0.5, label='North')
    plt.hist(dataSouth[stat], color='gold', alpha=0.5, label='South')
    plt.axvline(dataNorth[stat].mean(numeric_only=True), color='blue', linestyle='--', label='North Mean')
    plt.axvline(dataSouth[stat].mean(numeric_only=True), color='gold', linestyle='--', label='South Mean')
    plt.xlabel(str(stat))
    plt.ylabel('Frequency')
    plt.title(str(stat) + " for North and South Fork")
    plt.legend()
    
    plt.subplot(122)
    plt.hist(permutation_differences)
    plt.axvline(observed_difference[stat], color='red', linestyle='--', label='Observed Difference')
    plt.xlabel('Mean Difference')
    plt.ylabel('Frequency')
    plt.title(str(stat) + " Mean Differences " + "(P-Value: " + str(round(p_val_count, 3)) + ")")
    plt.legend()
    
def load_data(room_numer):
    df = pd.read_csv("sp24.csv")
    df = df[df['Room'] == room_numer]
    return df