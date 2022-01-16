import pygame


class Fire(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill('green')
        self.speed = speed
        self.screen_height = screen_height
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.y += self.speed
