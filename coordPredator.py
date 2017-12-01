import random, math
from agent import Agent
from variables import *

MAX_NEIGHBOR_FORCE = abs(math.log(PREDATOR_SENSING_DISTANCE/PREDATOR_DESIRED_DIST))

## Built on predator that zig-zags.
## Coordinate with other predators.
class CoordPredator(Agent):
    def __init__(self, sim, start_loc = None):
        random.seed()
        super().__init__(sim, start_loc)
        self.nearby_fish = []
        self.nearby_predator = []
        self.cooldown = 0

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
        if self.cooldown > 0:
            self.cooldown -= 1

        ## Check for predators and apply force
        if len(self.neighbors) > 0:
            neighbors = self.neighbors
            for neighbor in neighbors:
                x_vec = 0
                y_vec = 0
                predator, dist = neighbor
                target = self.get_perceived_target_pos(predator.loc)
                x, y = self.get_vector_to_target(target)
                if dist > PREDATOR_DESIRED_DIST:
                    total_force = PREDATOR_NEIGHBOR_FORCE * math.log(dist/PREDATOR_DESIRED_DIST)/MAX_NEIGHBOR_FORCE
                else:
                    total_force = -pow(PREDATOR_DESIRED_DIST-dist, 1)
                self.x_speed += x * total_force
                self.y_speed += y * total_force

        ## Go after the flock of fish.
        if len(self.nearby_fish) > 0:
            # Go for the center of mass
            target = self._get_center_of_mass()
            x_vec, y_vec = self.get_vector_to_target(target)
            new_vec = self.get_rotated_vector((x_vec,y_vec), math.pi/6)

            self.x_speed += new_vec[0] * PREDATOR_ACCEL
            self.y_speed += new_vec[1] * PREDATOR_ACCEL

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
