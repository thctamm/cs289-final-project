import random
from agent import Agent
from variables import *
from random import randint

class ProbPredator(Agent):
    def __init__(self, sim, start_loc = None):
        random.seed()
        super().__init__(sim, start_loc)
        self.nearby_fish = []
        self.nearby_predator = []
        self.cooldown = 0

    ## If really close to some fish, pick that fish.
    ## Otherwise, randomly select fish.
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        if len(self.nearby_fish) > 0:
            nearby_fish = sorted(self.nearby_fish, key=lambda x: x[1])

            fish, dist = nearby_fish[0]
            if dist < PREDATOR_PROB_DISTANCE:
                x_vec, y_vec = self.get_vector_to_target(dist)
                self.x_speed += x_vec * PREDATOR_ACCEL
                self.y_speed += y_vec * PREDATOR_ACCEL
            else:
                fishIndex = randint(0, len(nearby_fish) - 1)
                x_vec, y_vec = self.get_vector_to_target(nearby_fish[fishIndex][1])
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
