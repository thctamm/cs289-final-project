import random
from variables import *

class Agent():
    def __init__(self, start_loc = None):
        random.seed()
        if start_loc:
            self.loc = start_loc
        else:
            self.loc = (random.random() * WORLD_SIZE[0], random.random() * WORLD_SIZE[1])
        self.x_speed = 0
        self.y_speed = 0
        self.next_loc = self.loc 

    def update(self):
        return 

    def flip(self):
        self.loc = self.next_loc
