import pygame
import pygame.font


class StartScreen:
    def __init__(self, game_settings, screen):
        self.settings = game_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.font = pygame.font.Font(None, 60)
        self.font2 = pygame.font.Font(None, 36)
        self.text_color = (0, 255, 0)

        # title
        self.title = self.font.render('SPACE  INVADERS', True, self.text_color, self.settings.bg_color)
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.y = 50

        # alien score
        self.alien = pygame.image.load('images/alien1.bmp')
        self.alien_rect = self.alien.get_rect()
        self.alien_score = self.font2.render(': 50 points', True, self.text_color, self.settings.bg_color)
        self.alien_score_rect = self.alien_score.get_rect()
        self.alien_rect.y = self. alien_score_rect.y = 150
        self.alien_rect.x = 300
        self.alien_score_rect.x = 400

        self.squid = pygame.image.load('images/squid1.bmp')
        self.squid_rect = self.squid.get_rect()
        self.squid_score = self.font2.render(': 100 points', True, self.text_color, self.settings.bg_color)
        self.squid_score_rect = self.squid_score.get_rect()
        self.squid_rect.y = self.squid_score_rect.y = 200
        self.squid_rect.x = 300
        self.squid_score_rect.x = 400

        self.virus = pygame.image.load('images/virus1.bmp')
        self.virus_rect = self.virus.get_rect()
        self.virus_score = self.font2.render(': 150 points', True, self.text_color, self.settings.bg_color)
        self.virus_score_rect = self.virus_score.get_rect()
        self.virus_rect.y = self.virus_score_rect.y = 250
        self.virus_rect.x = 300
        self.virus_score_rect.x = 400

        self.boss = pygame.image.load('images/boss.bmp')
        self.boss_rect = self.boss.get_rect()
        self.boss_score = self.font2.render(': ??? points', True, self.text_color, self.settings.bg_color)
        self.boss_score_rect = self.virus_score.get_rect()
        self.boss_rect.y = self.boss_score_rect.y = 300
        self.boss_rect.x = 300
        self.boss_score_rect.x = 400

    def draw(self):
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.alien, self.alien_rect)
        self.screen.blit(self.alien_score, self.alien_score_rect)
        self.screen.blit(self.squid, self.squid_rect)
        self.screen.blit(self.squid_score, self.squid_score_rect)
        self.screen.blit(self.virus, self.virus_rect)
        self.screen.blit(self.virus_score, self.virus_score_rect)
        self.screen.blit(self.boss, self.boss_rect)
        self.screen.blit(self.boss_score, self.boss_score_rect)
