import time, sys, math, random, csv
import pygame
from variables import *
from simplePredator import SimplePredator
from probPredator import ProbPredator
from smartPredator import SmartPredator
from simpleFish import SimpleFish
from advancedFish import AdvancedFish
from circFish import CircFish
from propagationFish import PropagationFish

class Simulator():
    def __init__(self, fish_type, predator_type = 's', progress_file = ''):
        if fish_type == 's':
            self.Fish = SimpleFish
        elif fish_type == 'a':
            self.Fish = AdvancedFish
        elif fish_type == 'p':
            self.Fish = AdvancedFish
        else:
            self.Fish = CircFish

        if predator_type == 's':
            self.Predator = SimplePredator
        elif predator_type == 'r':
            self.Predator = ProbPredator
        elif predator_type == 'm':
            self.Predator = SmartPredator
        random.seed()
        self.score = 0
        self.ticks = 0
        self.fish = []
        self.predators = []
        self._init_fish()
        self._init_predators()
        if DRAW:
            self._init_pygame()
        if progress_file != '':
            self.out_file = open(progress_file, 'w+')
            self.wr = csv.writer(self.out_file)
            self.wr.writerow(['ticks', 'score'])
        else:
            self.wr = None

    def _init_pygame(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WORLD_SIZE[0]*SQUARE_SIZE, WORLD_SIZE[1]*SQUARE_SIZE))
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
        pygame.display.set_caption('289 fish flocking')

    def _init_fish(self):
        for _ in range(NUM_FISH):
            if START_CLUSTERED:
                self.fish.append(self.Fish(self, (WORLD_SIZE[0]/2 + (random.random()-0.5)*5, WORLD_SIZE[1]/2 + (random.random()-0.5)*5)))
            else:
                self.fish.append(self.Fish(self))

    def _init_predators(self):
        for _ in range(NUM_PREDATORS):
            if START_CLUSTERED:
                self.predators.append(self.Predator(self, (WORLD_SIZE[0]/2 + random.random()*10, WORLD_SIZE[1]/2)))
            else:
                self.predators.append(self.Predator(self))

    def _draw_fish(self, fish):
        x = int(fish.loc[0] * SQUARE_SIZE)
        y = int(fish.loc[1] * SQUARE_SIZE)
        pygame.draw.circle(self.surface, pygame.Color(*fish.color), (x, y), int(SQUARE_SIZE*FISH_SIZE))

    def _draw_pred(self, pred):
        x = int(pred.loc[0] * SQUARE_SIZE)
        y = int(pred.loc[1] * SQUARE_SIZE)
        pygame.draw.circle(self.surface, pygame.Color(*RED), (x, y), int(SQUARE_SIZE*PREDATOR_SIZE))

    def _draw_score(self):
        text_surf = self.font.render('Eaten = {}'.format(self.score), True, (255, 255, 255))
        self.surface.blit(text_surf, (0, 0))

    def _calc_dist(self, a, b):
        x = abs(a.loc[0] - b.loc[0])
        y = abs(a.loc[1] - b.loc[1])

        # Adjust for infinite world
        if x > WORLD_SIZE[0]/2:
            x = WORLD_SIZE[0] - x
        if y > WORLD_SIZE[0]/2:
            y = WORLD_SIZE[0] - y

        return math.sqrt(pow(x, 2) + pow(y, 2))

    def _update_agent_group_neighbors(self, group, sensing_dist):
        if len(group) > 0:
            group[0].neighbors = []
            for i1 in range(len(group)):
                for i2 in range(len(group[i1:])-1):
                    agent_a = group[i1]
                    agent_b = group[i1+i2+1]

                    # Clear old neighbors
                    if i1 == 0:
                        agent_b.neighbors = []

                    dist = self._calc_dist(agent_a, agent_b)
                    if dist <= sensing_dist:
                        agent_a.neighbors.append((agent_b, dist))
                        agent_b.neighbors.append((agent_a, dist))

    # Compute nearby marked fish within PROPAGATION_SENSING_DISTANCE.
    def _update_nearby_marked(self, sensing_dist):
        for fish1 in self.fish:
            fish1.nearby_marked = []
            for fish2 in self.fish:
                if fish1 != fish2:
                    dist = self._calc_dist(fish1, fish2)
                    if dist <= sensing_dist and fish2.marked:
                        fish1.nearby_marked.append((fish2, dist))


    # Compute nearby fish for each predator.
    def _update_predator_nearby_fish(self):
        for pred in self.predators:
            pred.nearby_fish = []
            for fish in self.fish:
                dist = self._calc_dist(pred, fish)
                if dist <= PREDATOR_EATING_DISTANCE and pred.cooldown == 0:
                    self.score += 1
                    if self.wr:
                        self.wr.writerow([self.ticks, self.score])
                    pred.cooldown = PREDATOR_EATING_COOLDOWN
                    self.fish.remove(fish)
                elif dist <= PREDATOR_SENSING_DISTANCE:
                    pred.nearby_fish.append((fish, dist))

    # Compute nearby predators for each fish.
    def _update_fish_nearby_predator(self):
        for fish in self.fish:
            fish.nearby_predators = []
            fish.marked = False
            for pred in self.predators:
                dist = self._calc_dist(pred, fish)
                if dist <= FISH_SENSING_DISTANCE:
                    fish.marked = True
                    fish.nearby_predators.append((pred, dist))

    def _update_neighbors(self):
        self._update_agent_group_neighbors(self.fish, FISH_SENSING_DISTANCE)
        self._update_agent_group_neighbors(self.predators, PREDATOR_SENSING_DISTANCE)
        self._update_predator_nearby_fish()
        self._update_fish_nearby_predator()
        self._update_nearby_marked(PROPAGATION_SENSING_DISTANCE)

    def _update(self):
        self.ticks += 1
        if DRAW:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit('quit')
        self._update_neighbors()
        for fish in self.fish:
            fish.update()
        for pred in self.predators:
            pred.update()
        if DRAW:
            self._flip_and_draw()
        else:
            self._flip()

    def _flip(self):
        for fish in self.fish:
            fish.flip()
        for pred in self.predators:
            pred.flip()

    def _flip_and_draw(self):
        self.surface.fill((0,0,0))
        for fish in self.fish:
            fish.flip()
            self._draw_fish(fish)
        for pred in self.predators:
            pred.flip()
            self._draw_pred(pred)
        self._draw_score()
        pygame.display.flip()

    def run(self):
        while True:
            self._update()
            if FREQUENCY > 0:
                time.sleep(1/FREQUENCY)
            if SCORE_THRESHOLD > 0 and self.score >= SCORE_THRESHOLD:
                self.out_file.close()
                return (self.ticks, self.score)
