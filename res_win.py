# -*- coding: utf-8 -*-
import pygame
import localdefs
import os
import sys

f = open('resolution.txt', 'r')
pygame.init()
size = width, height = [int(a) for a in f.read().split('x')]
flag = False

pygame.init()
# Пока что игра будет автоматически запускаться в full-screen. Потом, возможно, стоит добавить настройку
# разрешения.
fps = 144
# Вообще было бы логично юзать 60, но у моего монитора 144 герц, гы.
fps_clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tower Defense Bullet Hell')
screen.fill((255, 255, 255))


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def main_window():
    global flag
    flag = False
    running = True
    imgs = {}
    rects = {}
    bg = pygame.Surface(size)
    while running:
        pygame.mouse.set_visible(True)
        f = open('resolution.txt', 'r')
        pygame.init()
        size1 = width1, height1 = [int(a) for a in f.read().split('x')]
        screen = pygame.display.set_mode(size)
        BackGround = Background('menuimages/pixil.png', [0, 0])
        bg.fill([255, 255, 255])
        bg.blit(pygame.transform.scale(BackGround.image, (width1, height1)), BackGround.rect)
        screen.blit(bg, (0, 0))
        for num, i in enumerate(["playmap", "edittowers", "options", "exit"]):
            imgs[i] = localdefs.imgLoad(os.path.join("menuimages", i + ".png"))
            rects[i] = imgs[i].get_rect(centerx=size1[0] / 2, centery=(num + 1) * size1[1] / 5)
        for key in imgs.keys():
            screen.blit(imgs[key], rects[key])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if rects["playmap"].collidepoint(event.dict['pos']):
                    flag = True
                    Game()
                    running = False
                elif rects["exit"].collidepoint(event.dict['pos']):
                    flag = False
                    sys.exit()
        pygame.display.flip()
        # Обновим экран.
        fps_clock.tick(fps)
        # Тик.


def Game():
    return flag