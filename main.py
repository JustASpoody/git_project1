import pygame
from player import Player
from random import choice
from fire import Fire
from aliens import Aliens
import sys
import os


class Game:
    def __init__(self):
        self.player_sprite = Player((width / 2, height))
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_draw(rows=7, cols=8)
        self.alien_direction = 1
        self.font = pygame.font.Font(None, 50)
        self.lives = 3
        music = pygame.mixer.Sound('data_ost_bobby-prince-at-dooms-gate.mp3')
        music.set_volume(0.2)
        music.play(loops=-1)

    def run(self):
        self.player.draw(screen)
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.alien_lasers.update()
        self.aliens.update(self.alien_direction)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.alien_move()
        self.popadanie()
        self.final()
        self.livess()

    def livess(self):
        if self.lives > 0:
            text = self.font.render('Lives: ' + str(self.lives), True, (255, 255, 255))
            text_x = 10
            text_y = 10
        else:
            text = self.font.render('Lives: 0', True, (255, 255, 255))
            text_x = 10
            text_y = 10
        screen.blit(text, (text_x, text_y))

    def alien_draw(self, rows, cols, x_distance=60, y_distance=48, x_offset=80, y_offset=60):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index <= 1:
                    alien_sprite = Aliens('yellow', x, y)
                elif 2 <= row_index <= 4:
                    alien_sprite = Aliens('green', x, y)
                else:
                    alien_sprite = Aliens('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Fire(random_alien.rect.center, 5, height)
            self.alien_lasers.add(laser_sprite)

    def alien_move(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if pygame.sprite.spritecollide(alien, self.player, False):
                self.player_sprite.death()
                self.lives = 0
            if alien.rect.right >= width:
                self.alien_direction = -1
                for i in self.aliens.sprites():
                    i.rect.bottom += 3
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                for i in self.aliens.sprites():
                    i.rect.bottom += 3

    def popadanie(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.aliens, True):
                    laser.kill()
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
        if self.lives < 1:
            self.player_sprite.death()

    def final(self):
        if not self.aliens.sprites():
            text = self.font.render("YOU WON", True, (255, 255, 255))
            text_x = width // 2 - 70
            text_y = height // 2 - 50
            screen.blit(text, (text_x, text_y))
            self.player_sprite.win()
        else:
            for i in self.aliens.sprites():
                if i.rect.bottom >= 600 or self.lives <= 0:
                    text = self.font.render("YOU LOSE", True, (255, 255, 255))
                    text_x = width // 2 - 70
                    text_y = height // 2 - 50
                    screen.blit(text, (text_x, text_y))
                    break


if __name__ == '__main__':
    def terminate():
        pygame.quit()
        sys.exit()


    def start_screen():
        intro_text = ["ЗАСТАВКА! Нажми любую кнопку",
                      "Правила игры:",
                      "Используй A и D",
                      "     для движения",
                      "Стреляй, нажимая пробел",
                      "Не вздумай проиграть"]

        fon = pygame.transform.scale(load_image('fon2.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 0
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            clock.tick(FPS)


    def load_image(name):
        fullname = name
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image


    FPS = 50
    pygame.init()
    width = 600
    height = 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    start_screen()
    game = Game()
    ALIENLASER = pygame.USEREVENT
    pygame.time.set_timer(ALIENLASER, 500)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()
        screen.fill((0, 0, 0))
        game.run()
        pygame.display.flip()
        clock.tick(60)
