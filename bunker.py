import pygame
from PIL import Image
from pygame.sprite import Sprite
from random import randint


class Bunker(Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/bunker.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image2 = Image.open('images/bunker.bmp').convert("RGBA")
        self.image_data = self.image2.convert("RGBA").load()

    def draw(self):
        image = pygame.image.fromstring(self.image2.tobytes(), self.image2.size, self.image2.mode)
        self.screen.blit(image, self.rect)

    def update(self, bullets, enemy_bullets):
        # player's bullets collide with bunker
        hit_bullet = pygame.sprite.spritecollideany(self, bullets)
        if hit_bullet is not None:
            hit_position_x = int(hit_bullet.rect.centerx - self.rect.x)
            hit_position_y = int(hit_bullet.rect.top - self.rect.y)
            hit_position_x, hit_position_y = self.adjust_hit_position(hit_position_x, hit_position_y)

            if self.image_data[hit_position_x, hit_position_y][3] != 0:
                self.destroy_area(hit_position_x, hit_position_y, 4)
                hit_bullet.kill()

        # enemy's bullets collide with bunker
        hit_bullet = pygame.sprite.spritecollideany(self, enemy_bullets)
        if hit_bullet is not None:
            hit_position_x = int(hit_bullet.rect.centerx - self.rect.x)
            hit_position_y = int(hit_bullet.rect.bottom - self.rect.y)
            hit_position_x, hit_position_y = self.adjust_hit_position(hit_position_x, hit_position_y)

            if self.image_data[hit_position_x, hit_position_y][3] != 0:
                self.destroy_area(hit_position_x, hit_position_y, 4)
                hit_bullet.kill()

    def destroy_area(self, x, y, radius):
        min_x = x-radius if (x-radius > 0) else 0
        max_x = x+radius if (x+3 < self.rect.width - 1) else self.rect.width - 1
        min_y = y-radius if (y-radius > 0) else 0
        max_y = y+radius if (y+radius < self.rect.height - 1) else self.rect.height - 1

        for destroy_y in range(min_y, max_y+1):
            for destroy_x in range(min_x, max_x+1):
                if randint(0, 4) > 0 and (destroy_x - x)**2 + (destroy_y - y)**2 <= radius**2:
                    self.image_data[destroy_x, destroy_y] = (0, 0, 0, 0)
                    self.image2.putpixel((destroy_x, destroy_y), (0, 0, 0, 0))
        self.image2.putpixel((x, y), (0, 0, 0, 0))
        self.image2.putpixel((x, min_y), (0, 0, 0, 0))
        self.image2.putpixel((x, max_y), (0, 0, 0, 0))

    def adjust_hit_position(self, hit_position_x, hit_position_y):  # avoid image's out of range index
        if hit_position_x < 0:
            hit_position_x = 0
        if hit_position_x > self.rect.width - 1:
            hit_position_x = self.rect.width - 1
        if hit_position_y < 0:
            hit_position_y = 0
        if hit_position_y > self.rect.height - 1:
            hit_position_y = self.rect.height - 1
        return hit_position_x, hit_position_y
