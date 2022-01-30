import math
import os
import sys
import random
import pygame

BLACK = (0, 0, 0)

def load_image(name, colorkey=None):  # not sure if this method is needed
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)  # we can just use this one, cuz we know that pics are ok
    return image


enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = []
        self.cut_sheet(load_image("meteors1.png"), 5, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.count = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(width)
        self.rect.y = -1 * self.image.get_height()
        while pygame.sprite.spritecollideany(self, enemies, pygame.sprite.collide_mask) or\
                self.rect.x < 0 or self.rect.right > width:
            self.rect.x = random.randrange(width)
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

class bullet(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Loading the image for the character
        self.img = pygame.image.load("data/bullet.png")
        # creating a copy of the image
        self.img_orig = self.img.copy()
        # defining the starting angle of the character image
        self.angle = 0
        # obtaining rect details of original image position for collisions etc
        self.rect = self.img_orig.get_rect()
        self.x, self.y = self.rect.center

        is_not_destroyed= True

        pygame.draw.rect(self.img_orig, color, [0, 0, 25, 25])

        self.velocity = 5

        while (is_not_destroyed):
            self.moveForward()


    # def draw(screen):
    # screen.blit(self.img,(self.rect.x, self.rect.y))

    def rotate(self, change_angle):
        self.angle += change_angle
        self.img = pygame.transform.rotate(self.img_orig, self.angle)
        self.rect = self.img.get_rect(center=self.rect.center)

    def move(self, distance):
        self.x += distance * math.cos(math.radians(self.angle + 90))
        self.y -= distance * math.sin(math.radians(self.angle + 90))

        self.rect.center = round(self.x), round(self.y)

    def moveLeft(self):
        self.rotate(5)

    def moveRight(self):
        self.rotate(-5)

    def moveForward(self):
        self.move(self.velocity)

    def moveBackward(self):
        self.move(-self.velocity)



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 800 # other parameters may be set in the main game
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 3000)
    for _ in range(random.randrange(1, 4)):
        enemies.add(Enemy())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MYEVENTTYPE:  # every 3000 frames new enemies are created
                for _ in range(random.randrange(1, 4)):
                    enemies.add(Enemy())

        screen.fill(pygame.Color('blue'))  # in the main game, there will be a background(animated?)
        enemies.draw(screen)
        enemies.update()
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
    sys.excepthook = except_hook