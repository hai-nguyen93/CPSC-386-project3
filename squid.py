import random
import pygame
from Timer import Timer
from alien import Alien


class Squid(Alien):
    def __init__(self, game_settings, screen):
        super().__init__(game_settings, screen)
        self.score = 100

        # moving animation
        self.frames = [pygame.image.load('images/squid1.bmp'), pygame.image.load('images/squid2.bmp')]
        self.rect = self.frames[0].get_rect()

        # current animation
        self.animation = Timer(self.frames, wait=random.randint(2, 5)*100)
