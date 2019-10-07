import pygame
from pygame.sprite import Sprite
from random import randint


class EnemyBullet(Sprite):
    def __init__(self, game_settings, screen, aliens):
        super().__init__()
        self.settings = game_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(0, self.screen_rect.height, game_settings.enemy_bullet_width,
                                game_settings.bullet_height)

        # Initiate starting pos (pick 1 random alien to fire)
        if len(aliens) > 0:
            i = randint(0, len(aliens)-1)
            self.rect.centerx = aliens.sprites()[i].rect.centerx
            self.rect.y = aliens.sprites()[i].rect.bottom
        self.y = float(self.rect.top)

        self.color = (0, 255, 0)
        self.speed = game_settings.bullet_speed_factor

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

        if self.rect.y > self.screen_rect.height:
            self.kill()

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
