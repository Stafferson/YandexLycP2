import pygame
import math

import bullets
from settings import SPACESHIP_LIVES

BLACK = (0, 0, 0)


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        self.lives = SPACESHIP_LIVES

        # Loading the image for the character
        self.img = pygame.transform.scale(pygame.image.load("data/starship.png").copy(), (50, 50))
        self.mask = pygame.mask.from_surface(self.img)
        #pygame.transform.scale(image, (200, 100))
        # creating a copy of the image
        self.img_orig = self.img.copy()
        # defining the starting angle of the character image
        self.angle = 0
        # obtaining rect details of original image position for collisions etc
        self.rect = self.img.get_rect()
        self.x, self.y = self.rect.center
        self.is_blown = False
        #print(self.rect.center)

        #pygame.draw.rect(self.img_orig, color, [0, 0, 200, 200])

        self.velocity = 5

    # def draw(screen):
    # screen.blit(self.img,(self.rect.x, self.rect.y))

    def rotate(self, change_angle):
        if (self.is_blown):
            change_angle = 0
        self.angle += change_angle
        self.img = pygame.transform.rotate(self.img_orig, self.angle)
        self.rect = self.img.get_rect(center=self.rect.center)

    def move(self, distance):
        self.x += distance * math.cos(math.radians(self.angle + 90))
        self.y -= distance * math.sin(math.radians(self.angle + 90))
        #print(self.x)
        #print(self.y)
        #print(self.rect.x)
        #print(self.rect.y)
        #print("?????////")
        self.rect.center = round(self.x), round(self.y)

    def moveLeft(self):
        self.rotate(5)

    def moveRight(self):
        self.rotate(-5)

    def moveForward(self):
        self.move(self.velocity)

    def moveBackward(self):
        self.move(-self.velocity)

    def shoot(self):
        return bullets.bullet(BLACK, self.rect.x, self.rect.y, self)

    def get_damage(self, attack):
        self.lives -= attack

    def get_number_of_hp(self):
        return self.lives

    def die(self):
        self.is_blown = True
        self.velocity = 0
        self.img = pygame.transform.scale(pygame.image.load("data/blown.png").copy(), (50, 50))
        self.img_orig = self.img
        self.img = self.img_orig
        #pygame.imag

    def restore(self):
        self.is_blown = False
        self.velocity = 5
        self.lives = 5
        self.img = pygame.transform.scale(pygame.image.load("data/starship.png").copy(), (50, 50))
        self.img_orig = self.img
        self.img = self.img_orig