import pygame
import math

import bullets

BLACK = (0, 0, 0)


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Loading the image for the character
        self.img = pygame.transform.scale(pygame.image.load("data/starship.png"), (50, 50))
        #pygame.transform.scale(image, (200, 100))
        # creating a copy of the image
        self.img_orig = self.img.copy()
        # defining the starting angle of the character image
        self.angle = 0
        # obtaining rect details of original image position for collisions etc
        self.rect = self.img.get_rect()
        self.x, self.y = self.rect.center
        print(self.rect.center)

        #pygame.draw.rect(self.img_orig, color, [0, 0, 200, 200])

        self.velocity = 5

    # def draw(screen):
    # screen.blit(self.img,(self.rect.x, self.rect.y))

    def rotate(self, change_angle):
        self.angle += change_angle
        self.img = pygame.transform.rotate(self.img_orig, self.angle)
        self.rect = self.img.get_rect(center=self.rect.center)

    def move(self, distance):
        self.x += distance * math.cos(math.radians(self.angle + 90))
        self.y -= distance * math.sin(math.radians(self.angle + 90))
        print(self.x)
        print(self.y)

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