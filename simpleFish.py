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
        total_x_vec = 0
        total_y_vec = 0
       
        if len(self.neighbors) > 0:
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
                if dist > FISH_DESIRED_DIST:
                    total_force = FISH_NEIGHBOR_FORCE * math.log(dist/FISH_DESIRED_DIST)/MAX_NEIGHBOR_FORCE
                else:
                    total_force = -pow(FISH_DESIRED_DIST-dist, 2)
                total_x_vec += x * total_force
                total_y_vec += y * total_force


        else:
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

