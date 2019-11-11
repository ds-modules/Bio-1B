import random
import math
from IPython.display import clear_output, display
from IPython.display import HTML as html
import time
import io
import matplotlib.pyplot as plt
import matplotlib.patches
from calysto.graphics import *
import threading

class World:
    def __init__(self, pwidth=50, pheight=50, grass=True, 
                sheep=100, wolves=50, grass_regrowth_time=30):
        # Width and Height (in patches):
        self.pwidth = pwidth
        self.pheight = pheight
        # -----------------------------------
        # Parameters:
        # -----------------------------------
        # grass:
        self.use_grass = grass
        self.grass_regrowth_time = grass_regrowth_time # 0 to 100
        # sheep:
        self.initial_number_sheep = sheep # 0 to 250
        # wolves:
        self.initial_number_wolves = wolves # 0 to 250
        self.state = "stopped"
        self.setup()
        
    def setup(self):
        self.history = []
        self.ticks = 0
        if self.use_grass:
            self.patches = [[Patch(self, random.choice([-1, 1])) 
                             for w in range(self.pheight)] for h in range(self.pwidth)]
        else:
            self.patches = [[Patch(self, math.inf) 
                             for w in range(self.pheight)] for h in range(self.pwidth)]
        self.animals = []
        for i in range(self.initial_number_sheep):
            self.animals.append(Sheep(self))
        for i in range(self.initial_number_wolves):
            self.animals.append(Wolf(self))
        
    def draw(self, pixels=10):
        canvas = Canvas(size=(self.pwidth * pixels, self.pheight * pixels))
        if self.use_grass:
            grass = 0
            non_grass = 0
            if self.use_grass:
                for h in range(self.pheight):
                    for w in range(self.pwidth):
                        if self.patches[w][h].level > 0:
                            grass += 1
                        else:
                            non_grass += 1
            if non_grass > grass:
                rectangle = Rectangle((0,0), (self.pwidth * pixels - 1, self.pheight * pixels - 1))
                rectangle.draw(canvas)
                rectangle.fill("brown")
                for h in range(self.pheight):
                    for w in range(self.pwidth):
                        if self.patches[w][h].level > 0:
                            rect = Rectangle((w * pixels, h * pixels), 
                                             (pixels, pixels))
                            rect.fill("green")
                            rect.stroke("green")
                            rect.draw(canvas)
            else:
                rectangle = Rectangle((0,0), (self.pwidth * pixels - 1, self.pheight * pixels - 1))
                rectangle.draw(canvas)
                rectangle.fill("green")
                for h in range(self.pheight):
                    for w in range(self.pwidth):
                        if self.patches[w][h].level <= 0:
                            rect = Rectangle((w * pixels, h * pixels), 
                                             (pixels, pixels))
                            rect.fill("brown")
                            rect.stroke("brown")
                            rect.draw(canvas)
        else:
            rectangle = Rectangle((0,0), (self.pwidth * pixels - 1, self.pheight * pixels - 1))
            rectangle.draw(canvas)
            rectangle.fill("green")
        for animal in self.animals:
            animal.draw(canvas, pixels)
        rectangle = Rectangle((0,0), (self.pwidth * pixels - 1, self.pheight * pixels - 1))
        rectangle.draw(canvas)
        rectangle.fill(None)
        return canvas
        
    def get_stats(self):
        sheep = 0;
        wolves = 0
        for animal in self.animals:
            if isinstance(animal, Sheep):
                sheep += 1
            elif isinstance(animal, Wolf):
                wolves += 1
        grass = 0
        if self.use_grass:
            for h in range(self.pheight):
                for w in range(self.pwidth):
                    if self.patches[w][h].level > 0:
                        grass += 1
        return (sheep, wolves, grass/4)
        
    def update(self):
        for animal in list(self.animals): ## copy of list in case changes
            animal.update()
        for h in range(self.pheight):
            for w in range(self.pwidth):
                self.patches[w][h].update()
                
    def stop(self):
        self.state = "stopped"
                
    def run(self, widgets, width=4.0, height=3.0, pixels=10):
        self.state = "running"
        while 0 < len(world.animals) and self.state == "running":
            self.ticks += 1
            self.update()
            stats = self.get_stats()
            self.history.append(stats)
            widgets["plot"].value = self.plot(width, height)
            widgets["canvas"].value = str(world.draw(pixels))
            widgets["sheep"].value = str(stats[0])
            widgets["wolves"].value = str(stats[1])
            widgets["grass"].value = str(stats[2])
            widgets["ticks"].value = str(self.ticks)
        self.state = "stopped"
            
    def plot(self, width=4.0, height=3.0):
        plt.rcParams['figure.figsize'] = (width, height)
        fig = plt.figure()
        plt.plot([h[0] for h in self.history], "y", label="Sheep")
        plt.plot([h[1] for h in self.history], "k", label="Wolves")
        plt.plot([h[2] for h in self.history], "g", label="Grass")
        plt.legend()
        plt.xlabel('time')
        plt.ylabel('count')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        png_bytes = buf.getvalue()
        plt.close(fig)
        return png_bytes
            
    def __repr__(self):
        matrix = [[" " for w in range(self.pheight)] for h in range(self.pwidth)]
        for h in range(self.pheight):
            for w in range(self.pwidth):
                matrix[w][h] = repr(self.patches[w][h])
        for animal in self.animals:
            matrix[int(animal.x)][int(animal.y)] = animal.SYMBOL
        string = ""
        for h in range(self.pheight):
            for w in range(self.pwidth):
                string += matrix[w][h]
            string += "\n"
        return string

class Patch:
    def __init__(self, world, level):
        self.world = world
        self.level = level
        if level == -1:
            self.time = random.randint(0, self.world.grass_regrowth_time)
        else:
            self.time = 0            
        
    def update(self):
        if self.level == math.inf:
            pass
        elif self.level == 0:
            self.time = 0
            self.level = -1
        elif self.time == self.world.grass_regrowth_time:
            self.level = 1
        else:
            self.time += 1
            
    def __repr__(self):
        if self.level > 0:
            return "."
        return " "
    
class Animal:
    GAIN_FROM_FOOD = 1
    REPRODUCE = 0 ## percentage
    SYMBOL = "a"
    
    def __init__(self, world):
        self.world = world
        self.x = random.random() * self.world.pwidth
        self.y = random.random() * self.world.pheight
        self.direction = random.random() * 360
        
    def turnLeft(self, degrees):
        self.direction -= degrees
        self.direction = self.direction % 360
    
    def turnRight(self, degrees):
        self.direction += degrees
        self.direction = self.direction % 360

    def forward(self, distance):
        radians = self.direction * (math.pi/180.0)
        x = math.cos(radians) * distance
        y = math.sin(radians) * distance
        self.x = (self.x + x) % self.world.pwidth
        self.y = (self.y + y) % self.world.pheight
    
    def update(self):
        self.move()
        self.eat()
        if self.energy > 0:
            if random.random() < self.REPRODUCE:
                self.hatch()
        else: # die
            self.world.animals.remove(self)
    
    def move(self):
        self.turnRight(random.random() * 50)
        self.turnLeft(random.random() * 50)
        self.forward(1)
        if isinstance(self, Wolf) or (isinstance(self, Sheep) and self.world.use_grass):
            self.energy -= 1.0
        
    def hatch(self):
        child = self.__class__(self.world) ## hatch an offspring 
        child.x = self.x
        child.y = self.y
        self.energy /= 2                   ## divide energy between parent and offspring
        child.energy = self.energy
        child.forward(1)                   ## move offspring forward 1 step
        self.world.animals.append(child)   ## add offspring to list of animals

    def eats(self, other):
        return False
    
    def eat(self):
        pass
        
    def distance(self, a, b):
        # minimal distance on torus
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        return math.sqrt(min(dx, self.world.pwidth - dx) ** 2 + 
                         min(dy, self.world.pheight - dy) ** 2)
            
    def __repr__(self):
        return self.SYMBOL
        
class Wolf(Animal):
    GAIN_FROM_FOOD = 20 # 0 to 50
    REPRODUCE = 0.05 ## percentage
    SYMBOL = "w"
    
    def eats(self, other):
        return isinstance(other, (Sheep))

    def eat(self):
        if self.energy >= 0: # if I am alive:
            for animal in list(self.world.animals):
                if (self.eats(animal) and 
                    self.distance(self, animal) < 1.0 and
                    animal.energy >= 0):
                    self.energy += self.GAIN_FROM_FOOD
                    animal.energy = -1 ## mark dead
                    break # don't eat any more!
    
    
    def __init__(self, world):
        super().__init__(world)
        self.energy = random.randint(5, 40)

    def draw(self, canvas, pixels):
        wolf = Ellipse((self.x * pixels, self.y * pixels), (pixels/2, pixels/3))
        wolf.fill("black")
        wolf.stroke("black")
        wolf.draw(canvas)
        
class Sheep(Animal):
    GAIN_FROM_FOOD = 4 # 0 to 50
    REPRODUCE = 0.04 ## percentage
    SYMBOL = "s"
    
    def __init__(self, world):
        super().__init__(world)
        self.energy = random.randint(1, 7)

    def eat(self):
        patch = self.world.patches[int(self.x)][int(self.y)]
        if patch.level >= 0 and patch.level < math.inf:
            self.energy += self.GAIN_FROM_FOOD
            patch.level -= 1

    def draw(self, canvas, pixels):
        sheep = Ellipse((self.x * pixels, self.y * pixels), (pixels/2, pixels/2))
        sheep.fill("white")
        sheep.stroke("white")
        sheep.draw(canvas)        
