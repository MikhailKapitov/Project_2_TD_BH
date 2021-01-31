# -*- coding: utf-8 -*-
import pygame
import os
import sys
import res_win

pygame.init()
size = width, height = 1920, 1080
# Пока что игра будет автоматически запускаться в full-screen. А дальше это проблемы Ивана. :)))
fps = 144
# Вообще было бы логично юзать 60, но у моего монитора 144 герц, гы.
fps_clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tower Defense Bullet Hell')
# Это временное название, честно. :)))
enemy_bullets = pygame.sprite.Group()
# Группа спрайтов вражеских пуль.
cursor_group = pygame.sprite.Group()
# Группа для курсора.
enemy_group = pygame.sprite.Group()
# Группа врагов.
friendly_bullets = pygame.sprite.Group()
# Группа дружелюбных пуль.
towers_group = pygame.sprite.Group()
# Группа башен.
pygame.mouse.set_visible(False)
# Скрываем основной курсор ОС, у нас он круче.


def crop(image, color_key=None):
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_image(name, color_key=None):
    # Стандартная функция подгрузки картинок.
    fullname = os.path.join('Data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return crop(image, color_key)


class Board:
    # Стандартный класс-основа клеточного поля.

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


def search_for_road(pos, pr, board):
    # DFS, ищущий путь.
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    for direction in directions:
        new_pos = [pos[0] + direction[0], pos[1] + direction[1]]
        if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= 28 or new_pos[1] >= 12 or new_pos == pr:
            continue
        if board.cells_data[new_pos[0]][new_pos[1]] == 1:
            road.append([board.indent[0] + pos[0] * board.cell_size, board.indent[1] + pos[1] * board.cell_size])
            search_for_road(new_pos, pos, board)
            break
    return


class Field(Board):

    def __init__(self, level_name):
        super().__init__(28, 12, 64, 64, 64)
        level_map_file = open('levels\\' + level_name + '_map.txt')
        level_map_data = level_map_file.read().split('\n')
        level_map_file.close()
        for i in range(len(level_map_data)):
            for j in range(len(level_map_data[i])):
                if level_map_data[i][j] == '#':
                    self.cells_data[j][i] = 1
                elif level_map_data[i][j] == '%':
                    self.cells_data[j][i] = 3
        # Теперь найдем путь, по которому пройдут монстры.
        for j in range(28):
            if self.cells_data[0][j] == 1:
                search_for_road([0, j], [-1, -1], self)
                break
        return

    def render(self, surface):
        for i in range(self.columns):
            for j in range(self.rows):
                if self.cells_data[i][j] == 2 or self.cells_data[i][j] == 0:
                    pygame.draw.rect(surface, (255, 255, 255), (i * self.cell_size + self.indent[
                        0], j * self.cell_size + self.indent[1], self.cell_size, self.cell_size), 1)
                if self.cells_data[i][j] == 3:
                    pygame.draw.rect(surface, (32, 32, 32), (i * self.cell_size + self.indent[
                        0], j * self.cell_size + self.indent[1], self.cell_size, self.cell_size))
                    pygame.draw.rect(surface, (128, 128, 128), (i * self.cell_size + self.indent[
                        0], j * self.cell_size + self.indent[1], self.cell_size, self.cell_size), 1)
        return

    def on_click(self, cell):
        if self.cells_data[cell[0]][cell[1]] == 0 and cursor.selected_tower != 0 and cursor.coins >= shop.products[
                shop.selected][1]:
            towers_list.append(cursor.selected_tower([cell[0] * self.cell_size + 64, cell[
                1] * self.cell_size + 64], towers_group))
            self.cells_data[cell[0]][cell[1]] = 2
            cursor.coins -= shop.products[shop.selected][1]
        return


class Bullet(pygame.sprite.Sprite):
    # Основной класс простейшей пули.
    image = load_image('Simple_bullet.png', -1)

    def __init__(self, current_position, speed, direction, radius, damage, max_age, *group):
        super().__init__(*group)
        # Инициация спрайта.
        self.age = 0
        self.max_age = max_age
        # "Возраст" пули.
        self.image = pygame.transform.scale(Bullet.image, (radius + radius, radius + radius))
        # Изменение картинки для получения нужного радиуса.
        self.rect = self.image.get_rect()
        self.direction = direction
        # Направление движения пули.
        self.speed = speed / fps
        # Перевод скорости в секунду в скорость в тик.
        self.current_position = current_position
        # Позиция пули.
        self.rect.topleft = (int(self.current_position[0]), int(self.current_position[1]))
        self.coefficient = 1 / ((self.direction[0] ** 2 + self.direction[1] ** 2) ** 0.5)
        # Это нужно, чтобы от self.direction не зависила скорость.
        self.radius = radius
        # Размер пули.
        self.colour = (255, 255, 255)
        # Цвет пули.
        self.mask = pygame.mask.from_surface(self.image)
        # Маска пули для проверки столкновений.
        self.damage = damage
        # Урон, наносимый пулей.
        return

    def update(self):
        self.age += 1
        if self.age >= self.max_age:
            self.current_position = [-1000, -1000]
            self.rect.topleft = (int(self.current_position[0]), int(self.current_position[1]))
            return True
        current_dist = self.speed * self.coefficient
        self.current_position[0] += self.direction[0] * current_dist
        self.current_position[1] += self.direction[1] * current_dist
        self.rect.topleft = (int(self.current_position[0]), int(self.current_position[1]))
        # Обновляем положение пули.
        # Вернем True, если пуля вышла за экран, и нам она больше не интересна.
        return (self.current_position[0] > size[0] or self.current_position[
            0] + self.radius + self.radius < 0 or self.current_position[1] > size[1] or self.current_position[
            1] + self.radius + self.radius < 0)

    def set_pos(self, position=(-1000, -1000)):
        # Телепортируем пулю. Эта штука введена, чтобы убирать ее куда подальше, когда она нам уже не нужна, а то
        # у меня был какой-то там баг, где она не особо пропадала, ну короче пофиг, типо пофиксил, окда.
        self.current_position = position
        self.rect.topleft = (int(self.current_position[0]), int(self.current_position[1]))
        return


class PlusBullet(Bullet):
    image = load_image('PlusBullet.png', -1)

    def __init__(self, current_position, speed, direction, radius, damage, max_age, *group):
        super().__init__(current_position, speed, direction, radius, damage, max_age, group)
        self.image = crop(pygame.transform.scale(PlusBullet.image, (radius + radius, radius + radius)), -1)
        return


class Cursor(pygame.sprite.Sprite):
    # Стандартный класс курсора.
    standard_image = load_image('Standard_cursor.png', -1)
    invincible_standard_image = load_image('Standard_cursor_invincible.png', -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cursor.standard_image
        # Устанавливаем спрайт.
        self.rect = self.image.get_rect()
        self.curr_position = [0, 0]
        self.rect.topleft = (self.curr_position[0] - 16, self.curr_position[1] - 16)
        self.mask = pygame.mask.from_surface(self.image)
        # Настраиваем маску для столкновений.
        self.hp = 1000
        # ХП курсора.
        self.invincible = 0
        # Время неуязвимости курсора (в тиках).
        self.selected_tower = PlusTower
        # Башня, которую сейчас выбрал курсор.
        self.coins = 250
        # Деньги курсора.
        return

    def update(self, position):
        self.curr_position = position
        self.rect.topleft = (self.curr_position[0] - 16, self.curr_position[1] - 16)
        # Обновляем позицию курсора.
        return

    def attack(self, bullet):
        # Бьем курсор!
        if self.invincible:
            # А, нет, он неуязвим. Упс.
            return
        self.hp = max(self.hp - bullet.damage, 0)
        # Бьем курсор!
        if self.hp == 0:
            # Вызов экрана game-over.
            pass
        self.invincible = fps
        # Даем курсору временную неуязвимость.
        self.image = Cursor.invincible_standard_image
        # Отображаем курсор иначе, чтобы показать его неуязвимость. Обновлять маску нет нужды, его все равно нельзя
        # ударить.
        return

    def update_invincibility(self):
        # Обновляем время неуязвимости.
        self.invincible -= 1
        if self.invincible == 0:
            self.image = Cursor.standard_image
            # Все, он больше не неуязвим, вернем ему нормальный спрайт.
        return


class Enemy(pygame.sprite.Sprite):
    # Стандартный класс врага.
    useless_image = load_image('Blank_image.png', -1)  # Гыыыыы.

    def __init__(self, speed, hp, value, *group):
        super().__init__(*group)
        self.image = Enemy.useless_image
        self.rect = self.image.get_rect()
        # Установка спрайта.
        self.curr_position = road[0]
        # Начальная позиция врага.
        self.target = 1
        # Номер вершины дороги, к которому должен идти враг.
        self.rect.topleft = (int(self.curr_position[0]), int(self.curr_position[1]))
        self.mask = pygame.mask.from_surface(self.image)
        # Маска врага для столкновений.
        self.hp = hp
        self.max_hp = hp
        # ХП врага.
        self.speed = speed / fps
        # Перевод скорости из пикселей в секунду в пиксели в тик.
        self.value = value
        # Цена монстра (сколько денег игрок получит при его убийстве).
        return

    def update(self):
        distance = self.speed
        while distance >= 0.0000000000001 and self.target < len(road):
            # Оновляем врага, пока значеия не станут бессмысленными (спасибо погрешностям).
            dx = road[self.target][0] - self.curr_position[0]
            dy = road[self.target][1] - self.curr_position[1]
            distance_req = (dx * dx + dy * dy) ** 0.5
            coefficient = min(distance / distance_req, 1)
            distance -= coefficient * distance_req
            if coefficient == 1:
                self.target += 1
            self.curr_position[0] += dx * coefficient
            self.curr_position[1] += dy * coefficient
            # Умные переходы.
        self.rect.topleft = (int(self.curr_position[0]), int(self.curr_position[1]))
        # Все, обновили позицию.
        return

    def attack(self, bullet):
        # Бьем врага.
        self.hp = max(self.hp - bullet.damage, 0)
        if self.hp == 0:
            self.curr_position = [-1000, -1000]
            self.rect.topleft = (int(self.curr_position[0]), int(self.curr_position[1]))
            # Тут тот же прикол, как и с пулей.
            cursor.coins += self.value
            # Игрок получает прибыль!
        return

    def fire(self):
        # ВРАГ СТРЕЛЯЕТ!
        return

    def show_hp(self, surface):
        part = self.hp / self.max_hp
        pygame.draw.rect(surface, (255, 255, 255), (self.curr_position[0], self.curr_position[1] - 16, 64, 8))
        pygame.draw.rect(surface, (0, 0, 0), (
            self.curr_position[0] + int(64 * part), self.curr_position[1] - 14, int((1 - part) * 64), 5))
        return


class EnemyJack(Enemy):
    # Класс врага-Джека.
    jack_image = load_image('Jack.png', -1)

    def __init__(self, *group):
        super().__init__(50, 1000, 250, *group)
        self.image = EnemyJack.jack_image
        self.frequency = fps
        self.cooldown = fps
        # Он будет стрелять каждую секунду.

    def update(self):
        super().update()
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.fire()
            # Стреляем, если пора стрелять.
            self.cooldown = self.frequency
        return

    def fire(self):
        directions = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
        # Стреляем в восемь направлений.
        for direction in directions:
            enemy_bullets_list.append(Bullet([self.curr_position[0] + 24, self.curr_position[
                1] + 24], 100, direction, 8, 20, 2 * fps, enemy_bullets))
        return


class Tower(pygame.sprite.Sprite):
    # Стандартный класс башни.
    useless_image = load_image('Tower_sample.png', -1)

    def __init__(self, cooldown, position, *group):
        super().__init__(*group)
        self.image = Tower.useless_image
        self.rect = self.image.get_rect()
        # Установка спрайта.
        self.curr_position = position
        # Позиция башни.
        self.rect.topleft = (int(self.curr_position[0]), int(self.curr_position[1]))
        self.cooldown = int(cooldown * fps)
        self.frequency = int(cooldown * fps)
        # Перевод времени в тики.
        return

    def update(self):
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.cooldown = self.frequency
            self.fire()
        return

    def fire(self):
        # Башня стреляет!
        return


class PlusTower(Tower):
    # Башня, быстро стреляющая слабыми пулями "плюсиком".
    tower_image = pygame.transform.scale(load_image('Plus_tower.png', -1), (64, 64))

    def __init__(self, position, *group):
        super().__init__(0.333, position, *group)
        self.image = PlusTower.tower_image
        return

    def fire(self):
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        for direction in directions:
            friendly_bullets_list.append(PlusBullet([self.curr_position[
                0] + 22, self.curr_position[
                    1] + 22], 100, direction, 10, 10, fps, friendly_bullets))
        return


class Shop(Board):

    def __init__(self):
        super().__init__(10, 2, 64, 64, 896)
        self.products = [[PlusTower, 50], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        self.descriptions = ['+', '', '', '', '', '', '', '', '', '']
        self.selected = 0
        return

    def on_click(self, cell):
        self.selected = cell[0]
        cursor.selected_tower = self.products[self.selected][0]
        return

    def render(self, surface):
        for i in range(self.columns):
            for j in range(self.rows):
                if self.selected == i:
                    pygame.draw.rect(surface, (255, 255, 255), (i * self.cell_size + self.indent[
                        0], j * self.cell_size + self.indent[1], self.cell_size, self.cell_size), 1)
                else:
                    pygame.draw.rect(surface, (64, 64, 64), (i * self.cell_size + self.indent[
                        0], j * self.cell_size + self.indent[1], self.cell_size, self.cell_size), 1)
                if j == 1 and self.products[i][1] != 0:
                    cost = smaller_font.render('$' + str(self.products[i][1]), True, (255, 255, 255))
                    screen.blit(cost, (self.indent[0] + i * self.cell_size + 10, self.indent[
                        1] + j * self.cell_size + 10))
                elif j == 0:
                    cost = smaller_font.render(self.descriptions[i], True, (255, 255, 255))
                    screen.blit(cost, (self.indent[0] + i * self.cell_size + 10, self.indent[
                        1] + j * self.cell_size + 10))


def game():
    global road, enemy_bullets_list, enemies_list, towers_list, friendly_bullets_list
    global font, smaller_font, cursor, shop
    font = pygame.font.Font('Data/pixelated.ttf', 50)
    smaller_font = pygame.font.Font('Data/pixelated.ttf', 30)
    # Шрифт я стырил с https://www.dafont.com/pixelated.font, мне сказали, что можно.
    road = []
    # Путь врага.
    field = Field('level2')
    # А это поле.
    enemy_bullets_list = []
    # Здесь хранятся все "пули" врагов.
    cursor = Cursor(cursor_group)
    # Здесь - курсор.
    enemies_list = [EnemyJack(enemy_group)]
    # А здесь - враги.
    towers_list = []
    # Тут у нас башни.
    friendly_bullets_list = []
    # Тут - хорошие пули.
    shop = Shop()
    # Это магазин.
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                    running = False
            elif event.type == pygame.MOUSEMOTION:
                # Крусор двигается.
                cursor.update(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                field.get_click(event.pos)
                shop.get_click(event.pos)
        screen.fill((0, 0, 0))
        bullet_iter = 0
        while bullet_iter < len(enemy_bullets_list):
            # Цикл для вражеских пуль.
            current_bullet = enemy_bullets_list[bullet_iter]
            if current_bullet.update():
                del enemy_bullets_list[bullet_iter]
                # Удалим пулю, она не нужна.
            else:
                if pygame.sprite.collide_mask(current_bullet, cursor):
                    cursor.attack(current_bullet)
                    # Ударим курсор, если задели его.
                bullet_iter += 1
        enemy_iter = 0
        while enemy_iter < len(enemies_list):
            # Цикл для врагов.
            current_enemy = enemies_list[enemy_iter]
            if current_enemy.hp == 0:
                del enemies_list[enemy_iter]
                # Удалим врага, если он умер.
            else:
                current_enemy.update()
                enemy_iter += 1
        bullet_iter = 0
        while bullet_iter < len(friendly_bullets_list):
            # Цикл для хороших пуль.
            current_bullet = friendly_bullets_list[bullet_iter]
            if current_bullet.update():
                del friendly_bullets_list[bullet_iter]
                # Удалим пулю, она не нужна.
            else:
                attacked = False
                for enemy in enemies_list:
                    if pygame.sprite.collide_mask(current_bullet, enemy):
                        enemy.attack(current_bullet)
                        current_bullet.current_position = [-1000, -1000]
                        current_bullet.rect.topleft = (int(
                            current_bullet.current_position[0]), int(current_bullet.current_position[1]))
                        del friendly_bullets_list[bullet_iter]
                        attacked = True
                        break
                if not attacked:
                    bullet_iter += 1
        for current_tower in towers_list:
            current_tower.update()
        if cursor.invincible:
            cursor.update_invincibility()
            # Обновим неуязвимость курсора, если он неуязвим.
        hp_hud = font.render('<3   ' + str(cursor.hp), True, (255, 255, 255))
        screen.blit(hp_hud, (768, 896))
        coins_hud = font.render('   $      ' + str(cursor.coins), True, (255, 255, 255))
        screen.blit(coins_hud, (768, 960))
        shop.render(screen)
        towers_group.draw(screen)
        field.render(screen)
        cursor_group.draw(screen)
        enemy_group.draw(screen)
        friendly_bullets.draw(screen)
        for current_enemy in enemies_list:
            current_enemy.show_hp(screen)
        enemy_bullets.draw(screen)
        pygame.display.flip()
        # Обновим экран.
        fps_clock.tick(fps)
        # Тик.


def main_menu():
    res_win.main_window()
    if res_win.Game():
        game()


main_menu()