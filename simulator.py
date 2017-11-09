import time, sys
import pygame
from variables import *
from fish import Fish

class Simulator():
    def __init__(self):
        self.fish = []
        self.predators = []
        self._init_fish()
        self._init_predators()
        self._init_pygame()

    def _init_pygame(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WORLD_SIZE[0]*SQUARE_SIZE, WORLD_SIZE[1]*SQUARE_SIZE))
        pygame.display.set_caption('289 fish flocking')

    def _init_fish(self):
        for _ in range(NUM_FISH):
            self.fish.append(Fish())

    def _init_predators(self):
        # TODO
        return

    def _draw_fish(self, fish):
        x = int(fish.loc[0] * SQUARE_SIZE)
        y = int(fish.loc[1] * SQUARE_SIZE)
        pygame.draw.circle(self.surface, pygame.Color(*fish.color), (x, y), int(SQUARE_SIZE/3))
        return

    def _draw_pred(self, pred):
        return

    def _update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit('quit')
        for fish in self.fish:
            fish.update()
        for pred in self.predators:
            pred.update()

        self._flip_and_draw()

    def _flip_and_draw(self):
        self.surface.fill((0,0,0))
        for fish in self.fish:
            fish.flip()
            self._draw_fish(fish)
        for pred in self.predators:
            pred.flip()
            self._draw_pred(pred)
        pygame.display.flip()


    def run(self):
        while True:
            self._update()
            time.sleep(1/FREQUENCY)
