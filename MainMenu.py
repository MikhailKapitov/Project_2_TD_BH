import pygame
from past.builtins import execfile
from pygame.locals import *
import localdefs
import os
import sys
import GameWindow


f = open('resolution.txt', 'r')
pygame.init()
size = width, height = [int(a) for a in f.read().split('x')]

# Пока что игра будет автоматически запускаться в full-screen. Потом, возможно, стоит добавить настройку
# разрешения.
fps = 144
# Вообще было бы логично юзать 60, но у моего монитора 144 герц, гы.
fps_clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tower Defense Bullet Hell')
# Это временное название, честно. :)))
enemy_bullets = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
INVINCIBILITY_TIME = pygame.USEREVENT + 1
pygame.time.set_timer(INVINCIBILITY_TIME, 0)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def main(size):
    pygame.mouse.set_visible(True)
    bg = pygame.Surface(size)
    run = 1
    imgs = dict()
    rects = dict()
    while run:
        pygame.mouse.set_visible(True)
        f = open('resolution.txt', 'r')
        pygame.init()
        size = width, height = [int(a) for a in f.read().split('x')]
        screen = pygame.display.set_mode(size)
        for num, i in enumerate(["playmap", "edittowers", "options", "exit"]):
            imgs[i] = localdefs.imgLoad(os.path.join("menuimages", i + ".png"))
            rects[i] = imgs[i].get_rect(centerx=size[0] / 2, centery=(num + 1) * size[1] / 5)
        BackGround = Background('menuimages/background_image_2.jpg', [0, 0])
        bg.fill([255, 255, 255])
        bg.blit(pygame.transform.scale(BackGround.image, (width, height)), BackGround.rect)
        screen.blit(bg, (0, 0))
        for key in imgs.keys():
            screen.blit(imgs[key], rects[key])
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                if rects["playmap"].collidepoint(event.dict['pos']):
                    GameWindow.mainGame()
                elif rects["options"].collidepoint(event.dict['pos']):
                    execfile('OptionsWindow.py')
                elif rects["edittowers"].collidepoint(event.dict['pos']):
                    print("Not Yet Implemented")
                elif rects["exit"].collidepoint(event.dict['pos']):
                    sys.exit()

        pygame.display.flip()


main(size)
