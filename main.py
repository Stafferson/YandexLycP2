import os
import sys
import random
import pygame
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
        while pygame.sprite.spritecollideany(self, enemies, pygame.sprite.collide_mask) or self.rect.x < 0 or self.rect.right > WINDOW_W:
            self.rect.x = random.randrange(WINDOW_W)
        while pygame.sprite.spritecollideany(self, bullets, pygame.sprite.collide_mask) or self.rect.x < 0 or self.rect.right > WINDOW_W:
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
        if pygame.sprite.spritecollideany(self, bullets, pygame.sprite.collide_mask):
            self.life -= 1
        if self.life > 0:
            self.rect = self.rect.move(0, 1)
            self.count += 1
            if self.count % 7 == 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
        else:
            self.kill()

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()


pygame.init()

# Opening a Window
size = (WINDOW_H, WINDOW_W)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PONG!")

# setting variables
lives = 5
score = 0

MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 3000)
for _ in range(random.randrange(1, 4)):
    enemies.add(Enemy())

# Setting up sprite lists
all_sprites = pygame.sprite.Group()

# Creating Player Objects
pSprite = Spaceship(RED, 25, 25)
pSprite.rect.x = 50
pSprite.rect.y = 50
pSprite.x, pSprite.y = pSprite.rect.center

MYEVENTTYPE1 = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE1, 1000)

# Creating an enemy

# Adding sprites to sprite lists
all_sprites.add(pSprite)

# Game Running Flag
run = True

# Clock Setup
clock = pygame.time.Clock()

### ----- THE GAME -----

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == MYEVENTTYPE:  # every 3000 frames new enemies are created
            for _ in range(random.randrange(1, 4)):
                enemies.add(Enemy())
        if event.type == MYEVENTTYPE1:
            bullets.add(pSprite.shoot())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        pSprite.moveForward()
    if keys[pygame.K_DOWN]:
        pSprite.moveBackward()
    if keys[pygame.K_LEFT]:
        pSprite.moveLeft()
    if keys[pygame.K_RIGHT]:
        pSprite.moveRight()
    #if keys[pygame.K_SPACE]:
        #bullets.add(pSprite.shoot())

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