import random
from agent import Agent
from variables import *

class Fish(Agent):
    def __init__(self, start_loc = None):
        random.seed()
        super().__init__(start_loc)
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

        # randomly adjust speed
        self.x_speed += (random.random() - 0.5) * 0.1
        self.y_speed += (random.random() - 0.5) * 0.1

        # normalize
        speed = self.x_speed + self.y_speed
        if speed > FISH_SPEED:
            adj = FISH_SPEED/speed
            self.x_speed *= adj
            self.y_speed *= adj

        new_x = self.loc[0] + self.x_speed
        new_y = self.loc[1] + self.y_speed

        # wrap around
        if new_x > WORLD_SIZE[0]:
            new_x -= WORLD_SIZE[0]
        elif new_x < 0:
            new_x += WORLD_SIZE[0]
        
        if new_y > WORLD_SIZE[1]:
            new_y -= WORLD_SIZE[1]
        elif new_y < 0:
            new_y += WORLD_SIZE[1]

        self.next_loc = (new_x, new_y)

