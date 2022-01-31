import os
import random
import sys

import pygame
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