import pygame
from pygame.sprite import Sprite
from Timer import Timer


class Ship(Sprite):
    def __init__(self, game_settings, screen):
        """Initialize a ship and set its starting position"""
        super().__init__()
        self.screen = screen
        self.settings = game_settings
        self.dead = False

        # Load ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Ship's starting position
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.centerx = float(self.rect.centerx)

        # Ship's explosion animation
        frames = [pygame.image.load('images/ship_explode1.bmp'),
                  pygame.image.load('images/ship_explode2.bmp'),
                  pygame.image.load('images/ship_explode3.bmp'),
                  pygame.image.load('images/ship_explode4.bmp'),
                  pygame.image.load('images/ship_explode5.bmp'),
                  pygame.image.load('images/ship_explode6.bmp'),
                  pygame.image.load('images/ship_explode7.bmp'),
                  pygame.image.load('images/ship_explode8.bmp')]
        self.die_anim = Timer(frames, wait=100, looponce=True)

        # Moving flags
        self.move_right = self.move_left = False

    def update(self):
        """Update ship's position"""
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.settings.ship_speed_factor
        if self.move_left and self.rect.left > 0:
            self.centerx -= self.settings.ship_speed_factor

        # Update the rect object
        self.rect.centerx = self.centerx

    def draw(self):
        """Draw the ship"""
        if not self.dead:
            self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(self.die_anim.imagerect(), self.rect)

    def center_ship(self):
        self.centerx = self.screen_rect.centerx

    def reset(self):
        self.center_ship()
        self.dead = False
        self.die_anim.reset()
