import pygame
from fire import Fire


class Player(pygame.sprite.Sprite):
    image = pygame.image.load('player.png')
    image_boom = pygame.image.load('boom.png')

    def __init__(self, pos):
        super().__init__()
        self.image = Player.image
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = 5
        self.lasers = pygame.sprite.Group()
        self.shoot = True
        self.laser_time = 0
        self.laser_cooldown = 500
        self.is_already_dead = True

    def key_press(self):
        if self.is_already_dead:
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
        if self.is_already_dead:
            self.lasers.add(Fire(self.rect.center, -5, self.rect.bottom))

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

    def death(self):
        self.image = Player.image_boom
        if self.is_already_dead:
            self.rect.y -= 50
            self.is_already_dead = False
