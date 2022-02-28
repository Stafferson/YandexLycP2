import os
import sys
import random
import pygame

import ufos
from player import Spaceship
from settings import *


def load_image(name, colorkey=None):  # not sure if this method is needed
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)  # we can just use this one, cuz we know that pics are ok
    return image


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = []
        self.cut_sheet(load_image("meteors1.png"), 5, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.count = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(WINDOW_W)
        self.rect.y = -1 * self.image.get_height()
        while pygame.sprite.spritecollideany(self, enemies,
                                             pygame.sprite.collide_mask) or self.rect.x < 0 or self.rect.right > WINDOW_W:
            self.rect.x = random.randrange(WINDOW_W)
        # while pygame.sprite.spritecollideany(self, bullets,
        #                                      pygame.sprite.collide_mask) or self.rect.x < 0 or self.rect.right > WINDOW_W:
        #     self.rect.x = random.randrange(WINDOW_W)
        self.life = 1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if pygame.sprite.spritecollideany(self, bullets, pygame.sprite.collide_mask):
            self.life -= 1
        if self.life > 0 and self.rect.y <= WINDOW_H:
            self.rect = self.rect.move(0, 1)
            self.count += 1
            if self.count % 7 == 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
        else:
            self.kill()

        if pygame.sprite.collide_mask(self, pSprite):
            if (pSprite.lives >= 2):
                pSprite.get_damage(1)
                self.kill()
            else:
                pSprite.get_damage(1)
                #self.kill();



enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

ufos = pygame.sprite.Group()
players = pygame.sprite.Group()

fps = 60

pygame.init()

# Opening a Window
size = (WINDOW_H, WINDOW_W)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PONG!")

# setting variables
lives = 5
score = 0

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 3000)

MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 3000)

# Setting up sprite lists
all_sprites = pygame.sprite.Group()

enemies1 = pygame.sprite.Group()
bullets1 = pygame.sprite.Group()
ufos1 = pygame.sprite.Group()
players1 = pygame.sprite.Group()

# Creating Player Objects
pSprite = Spaceship(RED, 25, 25)
pSprite.rect.x = 50
pSprite.rect.y = 50
pSprite.x, pSprite.y = pSprite.rect.center

PLAYER_BULLET_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(PLAYER_BULLET_EVENT, 1000)

def end_screen():
    intro_text = ["DIED, NOOB"]

    fon = pygame.transform.scale(load_image('background.jpg'), (WINDOW_W, WINDOW_H))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
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
                game1()
        pygame.display.flip()
        clock.tick(60)

# Creating an enemy

# Adding sprites to sprite lists
all_sprites.add(pSprite)

# Game Running Flag
run = True

# Clock Setup
clock = pygame.time.Clock()

class Ufo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = []
        self.cut_sheet(load_image("ufos4.png"), 6, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.count = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(WINDOW_W)
        self.rect.y = -1 * self.image.get_height()
        while pygame.sprite.spritecollideany(self, enemies, pygame.sprite.collide_mask) or\
                self.rect.x < 0 or self.rect.right > WINDOW_W:
            self.rect.x = random.randrange(WINDOW_W)
        self.life = 1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if pygame.sprite.spritecollideany(self, bullets, pygame.sprite.collide_mask) or \
                pygame.sprite.spritecollideany(self, players, pygame.sprite.collide_mask):
            self.life -= 1
        if pygame.sprite.spritecollideany(self, players, pygame.sprite.collide_mask):
            self.life -= 1
        if self.life > 0 and self.rect.y <= WINDOW_H:
            self.rect = self.rect.move(0, 1)
            self.count += 1
            if self.count % 7 == 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
        else:
            self.kill()

        if pygame.sprite.collide_mask(self, pSprite):
            if (pSprite.lives >= 2):
                pSprite.get_damage(1)
                self.kill()
            else:
                pSprite.get_damage(1)
                #self.kill();

    def for_bullet(self):
        return self.rect.x + (self.rect.w // 2), self.rect.y + (self.rect.h // 2)


class Ufobullet(pygame.sprite.Sprite):
    def __init__(self, a, b):
        super().__init__()
        self.image = pygame.transform.scale(load_image("ufobullet.png", -1), (20, 60))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = a
        self.rect.y = b

    def update(self):
        if not pygame.sprite.spritecollideany(self, players, pygame.sprite.collide_mask) and self.rect.y <= WINDOW_H:
            self.rect = self.rect.move(0, 5)
        else:
            self.kill()
        if pygame.sprite.collide_mask(self, pSprite):
            if (pSprite.lives >= 2):
                pSprite.get_damage(1)
                self.kill()
            else:
                pSprite.get_damage(1)
                #self.kill();


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

# ----- THE GAME -----
def game():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == CREATE_ENEMY:  # every 3000 frames new enemies are created
                for _ in range(random.randrange(1, 4)):
                    enemies.add(Enemy())
            if event.type == PLAYER_BULLET_EVENT:
                bullets.add(pSprite.shoot())

        if pygame.sprite.spritecollideany(pSprite, enemies, pygame.sprite.collide_mask):
            #pSprite.get_damage(1)
            print(pSprite.get_number_of_hp())
            if (pSprite.get_number_of_hp() <= 0):
                pSprite.die();
                end_screen()
                #break;
        #print(pSprite.get_number_of_hp())

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pSprite.moveForward()
        if keys[pygame.K_DOWN]:
            pSprite.moveBackward()
        if keys[pygame.K_LEFT]:
            pSprite.moveLeft()
        if keys[pygame.K_RIGHT]:
            pSprite.moveRight()
        # if keys[pygame.K_SPACE]:
        #    bullets.add(pSprite.shoot())

        # ---- Game Logic Here
        if pSprite.rect.x < 0:
            pSprite.rect.x = 0
            pSprite.rect = pSprite.img.get_rect(center=pSprite.rect.center)
        if pSprite.rect.x > 750:
            pSprite.rect.x = 750
            pSprite.rect = pSprite.img.get_rect(center=pSprite.rect.center)

        if pSprite.rect.y < 0:
            pSprite.rect.y = 0
            pSprite.rect = pSprite.img.get_rect(center=pSprite.rect.center)
        if pSprite.rect.y > 750:
            pSprite.rect.y = 750
            pSprite.rect = pSprite.img.get_rect(center=pSprite.rect.center)
        pSprite.x, pSprite.y = pSprite.rect.center

        # --- Drawing Code Here
        # Reset the screen to blank
        screen.fill(BLUE)
        # Draw Play Area

        # Draw Sprites
        all_sprites.draw(screen)
        enemies.draw(screen)
        bullets.draw(screen)
        all_sprites.update()
        enemies.update()
        bullets.update()
        screen.blit(pSprite.img, (pSprite.rect.x, pSprite.rect.y))
        # Text on Screen

        # update the screen and show drawings
        pygame.display.flip()

        # Control the Clock
        clock.tick(60)

def game1():

    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    ufos = pygame.sprite.Group()
    players = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()


    if __name__ == '__main__':
        for _ in range(random.randrange(1, 4)):
            k = Ufo()
            enemies.add(k)
            ufos.add(k)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == MYEVENTTYPE:  # every 3000 frames new enemies are created
                    for _ in range(random.randrange(1, 4)):
                        k = Ufo()
                        enemies.add(k)
                        ufos.add(k)
                        for i in ufos:
                            enemies.add(Ufobullet(*i.for_bullet()))
                if event.type == PLAYER_BULLET_EVENT:
                    bullets.add(pSprite.shoot())

            if pygame.sprite.spritecollideany(pSprite, ufos, pygame.sprite.collide_mask):
                pSprite.get_damage(1)
                print(pSprite.get_number_of_hp())
                if (pSprite.get_number_of_hp() <= 0):
                    pSprite.die()
                    end_screen()

            if pygame.sprite.spritecollideany(pSprite, bullets, pygame.sprite.collide_mask):
                # pSprite.get_damage(1)
                print(pSprite.get_number_of_hp())
                if (pSprite.get_number_of_hp() <= 0):
                    pSprite.die();
                    end_screen()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                pSprite.moveForward()
            if keys[pygame.K_DOWN]:
                pSprite.moveBackward()
            if keys[pygame.K_LEFT]:
                pSprite.moveLeft()
            if keys[pygame.K_RIGHT]:
                pSprite.moveRight()
            # if keys[pygame.K_SPACE]:
            #    bullets.add(pSprite.shoot())

            # ---- Game Logic Here
            if pSprite.rect.x < 0:
                pSprite.rect.x = 0
                pSprite.rect = pSprite.img.get_rect(center=pSprite.rect.center)
            if pSprite.rect.x > 750:
                pSprite.rect.x = 750
                pSprite.rect = pSprite.img.get_rect(center=pSprite.rect.center)

            if pSprite.rect.y < 0:
                pSprite.rect.y = 0
                pSprite.rect = pSprite.img.get_rect(center=pSprite.rect.center)
            if pSprite.rect.y > 750:
                pSprite.rect.y = 750
                pSprite.rect = pSprite.img.get_rect(center=pSprite.rect.center)
            pSprite.x, pSprite.y = pSprite.rect.center

            screen.fill(pygame.Color('blue'))  # in the main game, there will be a background(animated?)
            enemies.draw(screen)
            all_sprites.draw(screen)
            all_sprites.update()
            enemies.update()
            screen.blit(pSprite.img, (pSprite.rect.x, pSprite.rect.y))
            clock.tick(fps)
            pygame.display.flip()

        pygame.quit()
        sys.excepthook = except_hook


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["SPACESHIP SHOOTER", "",
                  "Правила игры:", "передвигайтесь по полю с помощью стрелок",
                  "пуля выпускается каждую секунду: попадайте в астероиды, чтобы получать", "очки",
                  "но будьте осторожны: важно не задеть  их самим кораблем!",
                  "(или потеряете жизнь)", "",
                  "НАЖМИТЕ 1, ЧТОБЫ НАЧАТЬ ИГРУ С ЛЕГКИМ УРОВНЕМ СЛОЖНОСТИ", "",
                  "НАЖМИТЕ 2, ЧТОБЫ НАЧАТЬ ИГРУ С ВЫСОКИМ УРОВНЕМ СЛОЖНОСТИ"]

    fon = pygame.transform.scale(load_image('background.jpg'), (WINDOW_W, WINDOW_H))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
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
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                terminate()
            elif keys[pygame.K_1]:
                game()
                #ufos.game()
            elif keys[pygame.K_2]:
                game1()
        pygame.display.flip()
        clock.tick(60)

start_screen()