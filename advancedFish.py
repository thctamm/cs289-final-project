import random, math
from agent import Agent
from variables import *

MAX_NEIGHBOR_FORCE = abs(math.log(FISH_SENSING_DISTANCE/FISH_DESIRED_DIST))

class Fish(Agent):
    def __init__(self, sim, start_loc = None):
        random.seed()
        super().__init__(sim, start_loc)
        blue = random.randint(150, 255)
        green = random.randint(0, 100)
        red = random.randint(0, 100)
        missing = 400-blue-green-red
        red += missing//2
        if red > 255:
            red = 255
        green += missing//2
        if green > 255:
            green = 255
        self.color = (red, green, blue)

    def update(self): 
        #TODO
        self.move() 

