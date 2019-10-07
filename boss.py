import pygame
from pygame.sprite import Sprite
import random
import pygame.font


class Boss(Sprite):
    def __init__(self, game_settings, screen):
        super().__init__()
        self.settings = game_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # settings
        self.dead = False
        self.direction = 1
        self.sfx = pygame.mixer.Sound('audio/boss_sound.wav')
        self.sfx_playing = False

        # Load image
        self.image = pygame.image.load('images/boss.bmp')
        self.rect = self.image.get_rect()
        self.score = random.randint(2, 5) * 100 * game_settings.score_scale
        self.font = pygame.font.Font(None, 30)
        self.text_color = (0, 250, 0)
        self.score_image = self.font.render(str(int(self.score)), True, self.text_color, self.settings.bg_color)
        self.anim_time = 1000
        self.die_time = 0

        # starting pos (either from left or right edge of screen) and moving direction
        if random.randint(0, 1) == 0:
            self.rect.centerx = 0
            self.direction = 1
        else:
            self.rect.centerx = self.screen_rect.width
            self.direction = -1
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def draw(self):
        if not self.dead:
            self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(self.score_image, self.rect)

    def check_edges(self):
        return (self.rect.right < 0) or (self.rect.x > self.screen_rect.right)

    def update(self):
        if not self.sfx_playing and not self.dead:
            self.sfx.play(-1)
            self.sfx_playing = True

        if self.check_edges():
            self.sfx.stop()
            self.sfx_playing = False
            self.dead = True

        if not self.dead:
            self.x += (self.direction * self.settings.alien_speed_factor * 0.85)
            self.rect.x = int(self.x)
        else:
            if pygame.time.get_ticks() - self.die_time >= self.anim_time:
                self.settings.boss_number -= 1
                self.kill()

    def die(self):
        self.dead = True
        self.sfx.stop()
        self.sfx_playing = False
        self.die_time = pygame.time.get_ticks()
