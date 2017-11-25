import random
import math
from variables import *

class Agent():
    def __init__(self, sim, start_loc = None):
        random.seed()
        if start_loc:
            self.loc = start_loc
        else:
            self.loc = (random.random() * WORLD_SIZE[0], random.random() * WORLD_SIZE[1])
        self.x_speed = 0
        self.y_speed = 0
        self.next_loc = self.loc
        self.neighbors = []
        self.sim = sim

    def _get_perceived_target_pos_dim(self, a, b, lim):
        dist = abs(a - b)
        if dist > lim:
            if a < lim/2:
                return a - lim
            else:
                return a + lim
        else:
            return a

    def get_perceived_target_pos(self, target):
        x = self._get_perceived_target_pos_dim(target[0], self.loc[0], WORLD_SIZE[0])
        y = self._get_perceived_target_pos_dim(target[1], self.loc[1], WORLD_SIZE[1])
        return (x, y)

    def get_vector_to_target(self, target):
        x_vec = target[0] - self.loc[0]
        y_vec = target[1] - self.loc[1]
        tot = abs(x_vec) + abs(y_vec)
        if tot != 0:
            x_vec = x_vec/tot
            y_vec = y_vec/tot
        return (x_vec, y_vec)

    def get_perp_clockwise_vector(self, target):
        x_vec = target[0]
        y_vec = target[1]
        return (-1.0 * y_vec, x_vec)

    def get_perp_counterclockwise_vector(self, target):
        x_vec = target[0]
        y_vec = target[1]
        return (y_vec, -1.0 * x_vec)

    def update(self):
        return

    def move(self):
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

    def flip(self):
        self.loc = self.next_loc
