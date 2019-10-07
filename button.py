import pygame.font


class Button:
    def __init__(self, screen, msg, centerx, centery):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Button's properties
        self.msg = msg
        self.width, self.height = 200, 50
        self.button_color = (0, 0, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 40)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = centerx
        self.rect.centery = centery

    def draw(self):
        msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        msg_image_rect = msg_image.get_rect()
        msg_image_rect.center = self.rect.center

        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(msg_image, msg_image_rect)
