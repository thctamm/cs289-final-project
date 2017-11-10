import random
from agent import Agent
from variables import *

class Predator(Agent):
    def __init__(self, sim, start_loc = None):
        random.seed()
        super().__init__(sim, start_loc)
        self.nearby_fish = []

    def _get_center_of_mass(self):
        avg_x = 0
        avg_y = 0
        for neighbor in self.nearby_fish:
            fish = neighbor[0]
            x, y = self.get_perceived_target_pos(fish.loc)
            avg_x += x
            avg_y += y

        return (avg_x/len(self.nearby_fish), avg_y/len(self.nearby_fish))

    def update(self):
        
        if len(self.nearby_fish) > 0:
            # Go for the center of mass
            target = self._get_center_of_mass()
            x_vec, y_vec = self.get_vector_to_target(target) 

            self.x_speed += x_vec * PREDATOR_ACCEL
            self.y_speed += y_vec * PREDATOR_ACCEL

        else:
            # swim randomly 
            self.x_speed += (random.random() - 0.5) * 2 * PREDATOR_ACCEL
            self.y_speed += (random.random() - 0.5) * 2 * PREDATOR_ACCEL

        # normalize
        speed = abs(self.x_speed) + abs(self.y_speed)
        if speed > PREDATOR_SPEED:
            adj = PREDATOR_SPEED/speed
            self.x_speed *= adj
            self.y_speed *= adj

        self.move()

        

