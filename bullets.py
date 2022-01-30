import pygame
import math

BLACK = (0, 0, 0)


class bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load("data/bullet.png"), (10, 30))

    def __init__(self, color, xc, yc, parent):
        super().__init__()

        self.img = parent.image
        self.img.fill(BLACK)
        self.img.set_colorkey(BLACK)

        self.rect = bullet.image.get_rect()
        self.rect.x, self.rect.y = self.rect.center
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(bullet.image)
        self.x, self.y = xc, yc
        self.image = pygame.Surface([25, 50])
        self.mask = pygame.mask.from_surface(bullet.image)
        #self.image.fill(BLACK)
        #self.image.set_colorkey(BLACK)

        # Loading the image for the character
        #self.img = pygame.image.load("data/bullet.png")
        # creating a copy of the image
        #self.img_orig = self.img.copy()
        # defining the starting angle of the character image
        self.angle = parent.angle
        # obtaining rect details of original image position for collisions etc
        #self.rect = self.img_orig.get_rect()
        #self.x, self.y = parent.rect.center

        self.is_not_destroyed = True

        #pygame.draw.rect(self.img_orig, color, [0, 0, 500, 500])

        self.velocity = 15

        self.rotate(self.angle)

    def rotate(self, change_angle):
        a = 0 + change_angle
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.transform.scale(pygame.image.load("data/bullet.png"), (10, 30)), (10, 30)), a)
        self.rect = self.image.get_rect(center=self.rect.center)

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

    def update(self):
        self.moveForward()