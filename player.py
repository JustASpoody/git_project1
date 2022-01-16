import pygame
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = 5
        self.lasers = pygame.sprite.Group()
        self.shoot = True
        self.laser_time = 0
        self.laser_cooldown = 100

    def key_press(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE]:
            if self.shoot:
                self.laser_time = pygame.time.get_ticks()
                self.shoot_laser()
                self.shoot = False

    def update(self):
        self.key_press()
        self.lasers.update()
        self.reload()
        self.krai()

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -5, self.rect.bottom))

    def reload(self):
        if not self.shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.shoot = True

    def krai(self):
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 540:
            self.rect.x = 540
