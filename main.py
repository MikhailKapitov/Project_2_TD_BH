# -*- coding: utf-8 -*-
import pygame
import os

# Неужели?

pygame.init()
size = width, height = 1920, 1080
# Пока что игра будет автоматически запускаться в full-screen. Потом, возможно, стоит добавить настройку
# разрешения.
fps = 144
# Вообще было бы логично юзать 60, но у моего монитора 144 герц, гы.


class Board:

    def __init__(self, cols, rows, siz, x_indent, y_indent):
        self.columns = cols
        self.rows = rows
        self.cells_data = [[0] * rows for _ in range(cols)]
        self.cell_size = siz
        self.indent = [x_indent, y_indent]
        return

    def render(self, surface):
        surface.fill((0, 0, 0))
        for i in range(self.columns):
            for j in range(self.rows):
                if self.cells_data[i][j] == 1:
                    pygame.draw.rect(surface, (0, 255, 0), (i * self.cell_size + self.indent[
                        0], j * self.cell_size + self.indent[1], self.cell_size, self.cell_size))
                pygame.draw.rect(surface, (255, 255, 255), (i * self.cell_size + self.indent[
                    0], j * self.cell_size + self.indent[1], self.cell_size, self.cell_size), 1)
        return

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
        return

    def get_cell(self, mouse_pos):
        cell = ((mouse_pos[0] - self.indent[0]) // self.cell_size, (mouse_pos[1] - self.indent[1]) // self.cell_size)
        if cell[0] >= self.columns or cell[0] < 0 or cell[1] >= self.rows or cell[1] < 0:
            return None
        return cell

    def on_click(self, cell):
        return


class Bullet:

    def __init__(self, current_position, speed, direction, radius):
        self.direction = direction
        self.speed = speed / fps
        self.current_position = current_position
        self.coefficient = 1 / ((self.direction[0] ** 2 + self.direction[1] ** 2) ** 0.5)
        self.radius = radius
        return

    def update(self, time):
        current_dist = time * self.speed * self.coefficient
        self.current_position[0] += self.direction[0] * current_dist
        self.current_position[1] += self.direction[1] * current_dist
        return (self.current_position[0] - self.radius > size[0] or self.current_position[
            0] + self.radius < 0 or self.current_position[1] - self.radius > size[1] or self.current_position[
                    1] + self.radius < 0)

    def display(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.current_position, self.radius)
        return


def load_image(name, color_key=None):
    fullname = os.path.join('Data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Tower Defense Bullet Hell')
    # Это временное название, честно. :)))
    bullets_list = []
    # Здесь хранятся все "пули"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        bullet_iter = 0
        while bullet_iter < len(bullets_list):
            current_bullet = bullets_list[bullet_iter]
            if current_bullet.update(fps):
                del bullets_list[bullet_iter]
            else:
                current_bullet.display(screen)
                bullet_iter += 1
        pygame.display.flip()
        fps_clock.tick(fps)
