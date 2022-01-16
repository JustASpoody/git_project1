import pygame
from player import Player
from random import choice, randint
from laser import Laser
from alien import Alien


class Game:
    def __init__(self):
        player_sprite = Player((width / 2, height))
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=5, cols=8)
        self.alien_direction = 1
        self.font = pygame.font.Font(None, 50)

    def run(self):
        self.player.draw(screen)
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.alien_lasers.update()
        self.aliens.update(self.alien_direction)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.alien_move()
        self.collision_checks()
        self.victory_message()

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=80, y_offset=220):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, height)
            self.alien_lasers.add(laser_sprite)

    def alien_move(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= width:
                self.alien_direction = -1
                for i in self.aliens.sprites():
                    i.rect.bottom += 2
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                for i in self.aliens.sprites():
                    i.rect.bottom += 2

    def collision_checks(self):

        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # alien collisions
                if pygame.sprite.spritecollide(laser, self.aliens, True):
                    laser.kill()

    def victory_message(self):
        if not self.aliens.sprites():
            text = self.font.render("YOU WON", True, (255, 255, 255))
            text_x = width // 2 - 70
            text_y = height // 2 - 50
            screen.blit(text, (text_x, text_y))
        else:
            for i in self.aliens.sprites():
                if i.rect.bottom >= 600:
                    text = self.font.render("YOU LOSE", True, (255, 255, 255))
                    text_x = width // 2 - 70
                    text_y = height // 2 - 50
                    screen.blit(text, (text_x, text_y))
                    break


if __name__ == '__main__':
    pygame.init()
    width = 600
    height = 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((0, 0, 0))
        game.run()
        pygame.display.flip()
        clock.tick(60)
