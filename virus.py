import pygame
from alien import Alien
from Timer import Timer
import random


class Virus(Alien):
    def __init__(self, game_settings, screen):
        super().__init__(game_settings, screen)
        self.score = 150

        # moving animation
        self.frames = [pygame.image.load('images/virus1.bmp'), pygame.image.load('images/virus2.bmp')]
        self.rect = self.frames[0].get_rect()

        # current animation
        self.animation = Timer(self.frames, wait=random.randint(2, 5)*100)
