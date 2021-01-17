# -*- coding: utf-8 -*-
import pygame
import os

pygame.init()
size = width, height = 1920, 1080
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
pygame.mouse.set_visible(False)
INVINCIBILITY_TIME = pygame.USEREVENT + 1
pygame.time.set_timer(INVINCIBILITY_TIME, 0)


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


class Bullet(pygame.sprite.Sprite):
    image = load_image('Simple_bullet.png', -1)

    def __init__(self, current_position, speed, direction, radius, damage, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Bullet.image, (radius + radius, radius + radius))
        self.rect = self.image.get_rect()
        self.direction = direction
        self.speed = speed / fps
        self.current_position = current_position
        self.rect.topleft = (int(self.current_position[0]), int(self.current_position[1]))
        self.coefficient = 1 / ((self.direction[0] ** 2 + self.direction[1] ** 2) ** 0.5)
        self.radius = radius
        self.colour = (255, 255, 255)
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = damage
        return

    def update(self, time):
        current_dist = time * self.speed * self.coefficient
        self.current_position[0] += self.direction[0] * current_dist
        self.current_position[1] += self.direction[1] * current_dist
        self.rect.topleft = (int(self.current_position[0]), int(self.current_position[1]))
        if pygame.sprite.collide_mask(self, cursor):
            cursor.attack(self)
        return (self.current_position[0] > size[0] or self.current_position[
            0] + self.radius + self.radius < 0 or self.current_position[1] > size[1] or self.current_position[
            1] + self.radius + self.radius < 0)

    def set_pos(self, position=(-1000, -1000)):
        self.current_position = position
        self.rect.topleft = (int(self.current_position[0]), int(self.current_position[1]))
        return


class Cursor(pygame.sprite.Sprite):
    standard_image = load_image('Standard_cursor.png', -1)
    invincible_standard_image = load_image('Standard_cursor_invincible.png', -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cursor.standard_image
        self.rect = self.image.get_rect()
        self.curr_position = [0, 0]
        self.rect.topleft = (self.curr_position[0] - 16, self.curr_position[1] - 16)
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = 1000
        self.invincible = False
        return

    def update(self, position):
        self.curr_position = position
        self.rect.topleft = (self.curr_position[0] - 16, self.curr_position[1] - 16)
        return

    def attack(self, bullet):
        if self.invincible:
            return
        self.hp = max(self.hp - bullet.damage, 0)
        if self.hp == 0:
            # Вызов экрана game-over.
            pass
        self.invincible = True
        self.image = Cursor.invincible_standard_image
        pygame.time.set_timer(INVINCIBILITY_TIME, 1000)
        return

    def stop_invincibility(self):
        self.invincible = False
        self.image = Cursor.standard_image
        pygame.time.set_timer(INVINCIBILITY_TIME, 0)
        return


if __name__ == '__main__':
    bullets_list = []
    # Здесь хранятся все "пули"
    cursor = Cursor(cursor_group)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                cursor.update(event.pos)
            elif event.type == INVINCIBILITY_TIME:
                cursor.stop_invincibility()
        screen.fill((0, 0, 0))
        bullet_iter = 0
        while bullet_iter < len(bullets_list):
            current_bullet = bullets_list[bullet_iter]
            if current_bullet.update(fps):
                del bullets_list[bullet_iter]
            else:
                bullet_iter += 1
        enemy_bullets.draw(screen)
        cursor_group.draw(screen)
        pygame.display.flip()
        fps_clock.tick(fps)
