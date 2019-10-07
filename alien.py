import pygame
from pygame.sprite import Sprite
from Timer import Timer
import random


class Alien(Sprite):
    def __init__(self, game_settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = game_settings
        self.score = 50
        self.dead = False

        # moving animation
        self.frames = [pygame.image.load('images/alien1.bmp'), pygame.image.load('images/alien2.bmp')]
        self.rect = self.frames[0].get_rect()

        # explode animation
        self.die_frames = [pygame.image.load('images/alien_explode1.bmp'),
                           pygame.image.load('images/alien_explode2.bmp'),
                           pygame.image.load('images/alien_explode3.bmp')]

        # current animation
        self.animation = Timer(self.frames, wait=random.randint(2, 5)*100)

        # starting position near top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def draw(self):
        image = self.animation.imagerect()
        self.screen.blit(image, self.rect)

    def update(self):
        self.x += (self.settings.fleet_direction * self.settings.alien_speed_factor)
        self.rect.x = self.x
        if self.dead and self.animation.finished:
            self.kill()

    def die(self):
        self.animation = Timer(self.die_frames, wait=100, looponce=True)
        self.dead = True
