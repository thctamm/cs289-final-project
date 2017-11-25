import random, math
from agent import Agent
from variables import *

MAX_NEIGHBOR_FORCE = abs(math.log(FISH_SENSING_DISTANCE/FISH_DESIRED_DIST))

# Model attempt some sort of propagation wave.
# Affected by propagation wave that pushes it in circular form.
# If a marked fish is in a certain PROP_DIST (meaning getting
# attacked by Predator), then it experiences propagation wave force.
# Smaller force farther from the marked fish it is.
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
        self.nearby_predators = []
        self.nearby_marked = []
        self.marked = False
        self.color = (red, green, blue)

    def update(self):
        total_x_vec = 0.0
        total_y_vec = 0.0


        # Computing effect that nearby predators on fish.
        if len(self.nearby_predators) > 0:
            predators = self.nearby_predators
            for predator in predators:
                x_vec = 0.0
                y_vec = 0.0

                pred, dist = predator

                target = self.get_perceived_target_pos(pred.loc)
                x, y = self.get_vector_to_target(target)
                total_force = - PREDATOR_FISH_FORCE * pow((1.0)/dist, 4)
                total_x_vec += x * total_force
                total_y_vec += y * total_force

        # Compute effect of propagation wave and compute other effects normally.
        elif len(self.neighbors) > 0 or len(self.nearby_marked) > 0:
            marked = self.nearby_marked
            for fish in marked:
                x_vec = 0.0
                y_vec = 0.0

                a, dist = fish
                target = self.get_perceived_target_pos(a.loc)
                x, y = self.get_vector_to_target(target)

                updated_x, updated_y = self.get_perp_clockwise_vector(target)
                total_force = (1.0)*pow((1.0)/dist, 2)
                total_x_vec += updated_x * total_force
                total_y_vec += updated_y * total_force

            neighbors = self.neighbors
            if len(neighbors) > FISH_MAX_NEIGHBORS:
                neighbors = sorted(self.neighbors, key=lambda x: x[1])
                neighbors = neighbors[:FISH_MAX_NEIGHBORS]
            for neighbor in neighbors:
                x_vec = 0
                y_vec = 0
                fish, dist = neighbor
                target = self.get_perceived_target_pos(fish.loc)
                x, y = self.get_vector_to_target(target)
                # Made the force between fishes stronger. Maybe change neighbor
                # force constant in variables.py?
                if dist > FISH_DESIRED_DIST:
                    total_force = 10*FISH_NEIGHBOR_FORCE * math.log(dist/FISH_DESIRED_DIST)/MAX_NEIGHBOR_FORCE
                else:
                    total_force = -pow(FISH_DESIRED_DIST-dist, 1.5)
                total_x_vec += x * total_force
                total_y_vec += y * total_force

        elif len(self.nearby_predators) == 0 and len(self.neighbors) == 0:
            # randomly adjust speed
            total_x_vec = (random.random() - 0.5) * 2 * FISH_ACCEL
            total_y_vec = (random.random() - 0.5) * 2 * FISH_ACCEL


        # normalize acceleration
        accel = abs(total_x_vec) + abs(total_y_vec)
        if accel > FISH_ACCEL:
            adj = FISH_ACCEL/accel
            total_x_vec *= adj
            total_y_vec *= adj

        self.x_speed += total_x_vec
        self.y_speed += total_y_vec

        # normalize speed
        speed = abs(self.x_speed) + abs(self.y_speed)
        if speed > FISH_SPEED:
            adj = FISH_SPEED/speed
            self.x_speed *= adj
            self.y_speed *= adj

        self.move()
