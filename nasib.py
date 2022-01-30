import os
import sys
import random
import pygame


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
    enemy_pic = load_image("meteor1.png")

    def __init__(self):
        super().__init__()
        self.image = Enemy.enemy_pic
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(width)
        self.rect.y = -1 * self.image.get_height()
        while pygame.sprite.spritecollideany(self, enemies, pygame.sprite.collide_mask) or\
                self.rect.x < 0 or self.rect.right > width:
            self.rect.x = random.randrange(width)
        self.life = 1

    def update(self):
        if pygame.sprite.spritecollideany(self, bullets, pygame.sprite.collide_mask):
            self.life -= 1
        if self.life > 0:
            self.rect = self.rect.move(0, 1)
        else:
            self.kill()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500 # other parameters may be set in the main game
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