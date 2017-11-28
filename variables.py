# Visualization
RED = (255, 0 , 0)

# Simulator
START_CLUSTERED = False
DRAW = False
SCORE_THRESHOLD = 40
NUM_FISH = 70
NUM_PREDATORS = 2
WORLD_SIZE = (100, 70)
FREQUENCY = 0

# Pygame
SQUARE_SIZE = 10

# Predator
PREDATOR_SPEED = 0.5
PREDATOR_ACCEL = 0.015
PREDATOR_SIZE = 1;
PREDATOR_SENSING_DISTANCE = 15
PREDATOR_EATING_DISTANCE = 1.5
PREDATOR_EATING_COOLDOWN = 30
PREDATOR_FISH_FORCE = 50*PREDATOR_ACCEL

# Fish
PROPAGATION_SENSING_DISTANCE = 20
FISH_SPEED = 0.25
FISH_ACCEL = 0.05
FISH_SIZE = 0.5;
FISH_SENSING_DISTANCE = 10
FISH_MAX_NEIGHBORS = 10

# Flock
FISH_DESIRED_DIST = 5
FISH_NEIGHBOR_FORCE = FISH_ACCEL/2
