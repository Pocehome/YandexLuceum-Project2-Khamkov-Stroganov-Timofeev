import pygame
import random
import os
import sys

pygame.init()

FPS = 50
WIDTH = 320
HEIGHT = 735
difficult = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")

colors = [
        (219, 31, 31),
        (255, 116, 10),
        (226, 232, 50),
        (31, 162, 19),
        (13, 135, 167),
        (50, 57, 178),
    ]
# Список возможных цветов фигур


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    title_sound.play(loops=-1)
    intro_text = [
                  " Матвей Хамков",
                  "Серафим Тимофеев",
                  "Строганов Роман"]

    fon = pygame.transform.scale(load_image('Начальный экран.jpeg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 20)
    text_coord = 600
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                level_hard()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()
                        elif event.type == pygame.KEYDOWN or \
                                event.type == pygame.MOUSEBUTTONDOWN:
                            return
        pygame.display.flip()
        clock.tick(FPS)


def level_hard():
    global difficult
    intro_text = ["Выберите сложность:"]

    fon = pygame.transform.scale(load_image('Начальный экран.jpeg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 250
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 65
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    image1 = load_image('button_1.jpg', -1)
    image1 = pygame.transform.scale(image1, (200, 70))
    screen.blit(image1, (60, 300))
    image2 = load_image('button_2.jpg', -1)
    image2 = pygame.transform.scale(image2, (200, 70))
    screen.blit(image2, (60, 370))
    image3 = load_image('button_3.jpg', -1)
    image3 = pygame.transform.scale(image3, (200, 70))
    screen.blit(image3, (60, 440))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 60 <= event.pos[0] <= 260 and 300 <= event.pos[1] <= 370:
                    difficult = 2
                    return
                if 60 <= event.pos[0] <= 260 and 370 <= event.pos[1] <= 440:
                    difficult = 3
                    return
                if 60 <= event.pos[0] <= 260 and 440 <= event.pos[1] <= 510:
                    difficult = 4
                    return
        pygame.display.flip()
        clock.tick(FPS)


title_sound = pygame.mixer.Sound("data/title_1.mp3")
in_game_sound = pygame.mixer.Sound("data/game.mp3")
fall_sound = pygame.mixer.Sound("data/fall.mp3")
break_sound = pygame.mixer.Sound("data/break.mp3")
game_over_sound = pygame.mixer.Sound("data/game_over.mp3")

start_screen()


class Figure:
    global colors

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]
    # Форма фигур и варианты их поворота, на поле 4 на 4. Например фигура Г выглядит так:
    #   0   *   *   3
    #   4   *   6   7
    #   8   *   10  11
    #   12  13  14  15
    # То есть [1, 2, 5, 9]

    def __init__(self, field_x, field_y):
        self.field_x = field_x
        self.field_y = field_y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.choice(colors)
        self.rotation = 0
        # В инициализации выбирается фигура и её цвет (так же можно добавить выбор градуса поворота,
        # но тогда надо уравнять кол-во елементов в списках)

    def image(self):
        return self.figures[self.type][self.rotation]
        # Возвращается елемент списка figures, заданного типа и поворота

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
        # Изменение значения rotate для поворота фигуры


class Tetris:
    global colors

    running_game = True
    cell_count_height = 0
    cell_count_width = 0
    field_x = 10
    field_y = 10
    cell_size = 30
    figure = None
    # данные для инициализации: состояние игры, кол-во ячеек в столбце, кол-во ячеек в линии,
    # положение поля по x и y, размер клетки (сторона квадрата), состояние падающей сейчас фигуры

    def __init__(self, cell_count_height, cell_count_width, count=0, difficulty=2):
        self.cell_count_height = cell_count_height
        self.cell_count_width = cell_count_width
        self.difficulty = difficulty
        self.field = []
        self.score = 0
        self.running_game = True
        self.count = count
        self.chase_figure = False
        for _ in range(cell_count_height):
            new_line = []
            for _ in range(cell_count_width):
                new_line.append(0)
            self.field.append(new_line)
            # создание матрицы поля

    def new_figure(self):
        if self.count == 0:
            self.figure = Figure(3, 0)
        elif self.count == 1:
            self.figure = Figure(6, 20)
        # добавление новой фигуры

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.field_y > self.cell_count_height - 1 or \
                            j + self.figure.field_x > self.cell_count_width - 1 or \
                            j + self.figure.field_x < 0 or \
                            self.field[i + self.figure.field_y][j + self.figure.field_x] is not 0:
                        intersection = True
        return intersection
        # поиск пересечений падающей фигуры с полем

    def break_lines(self):
        break_was = False
        lines = 0
        places = []

        for i in range(1, self.cell_count_height):
            zeros = 0
            for j in range(self.cell_count_width):
                if self.field[i][j] == 0:
                    zeros += 1
                    break
            if zeros == 0:
                places.append((i, self.field[i].copy()))
                break_was = True
                lines += 1
                for i1 in range(i, 1, -1):
                    for j1 in range(self.cell_count_width):
                        self.field[i1][j1] = self.field[i1 - 1][j1]

        if break_was:
            break_sound.play()
            for place in places:
                for pos_x in range(9):
                    create_particles((self.field_x + self.cell_size * pos_x,
                                      self.field_y + self.cell_size * place[0]),
                                     colors.index(place[1][pos_x]))
                break
        self.score += lines ** 2
        self.chase_figure = True
        # функция для уничтожения линий. Проверяет на наличие 0 в матрице, и если их нет, то убирает линию

    def go_space(self):
        while not self.intersects():
            self.figure.field_y += 1
        self.figure.field_y -= 1
        self.stop_game()
        # функция клавиши "пробел" (фигура моментально падает как можно ниже)

    def go_down(self):
        self.figure.field_y += 1
        if self.intersects():
            self.figure.field_y -= 1
            self.stop_game()
        # функция клавиши "вниз" (фигура ускоренно падает вниз)

    def stop_game(self):
        if self.count == 0:
            # проверка фигуры (статичная или динамичная она)
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.figure.image():
                        self.field[i + self.figure.field_y][j + self.figure.field_x] = self.figure.color
        self.break_lines()
        fall_sound.play()
        self.new_figure()
        if self.intersects():
            self.running_game = False
            game_over_sound.play()
            in_game_sound.stop()
        if self.count == 1:
            self.chase_figure = False
        # останавливает игру, вызывается другими функциями при наличии пересечений

    def go_side(self, dx):
        old_x = self.figure.field_x
        self.figure.field_x += dx
        if self.intersects():
            self.figure.field_x = old_x
        # функция клавиш "влево" и "вправо". Перемещает фигуру влево или вправо

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation
        # функция клавиши "вверх" поворачивает фигуру против часовой стрелки


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    white = load_image("particle_white.png")
    red = load_image("particle_red.png")
    orange = load_image("particle_orange.png")
    yellow = load_image("particle_yellow.png")
    green = load_image("particle_green.png")
    sky_blue = load_image("particle_sky_blue.png")
    blue = load_image("particle_blue.png")
    particles_colors = [red, orange, yellow, green, sky_blue, blue, white]
    particles = []

    def __init__(self, pos, dx, dy, color):
        super().__init__(all_sprites)
        self.image = self.particles_colors[color]
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

        for scale in (5, 10, 20):
            self.particles.append(pygame.transform.scale(self.particles_colors[color], (scale, scale)))

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(0, 0, WIDTH, HEIGHT):
            self.kill()


def create_particles(position, color):
    # количество создаваемых частиц
    particle_count = 5
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), color)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GRAVITY = 0.5

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
pygame.display.set_caption("Tetris")

running = True
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10, 0, difficulty=difficult)
title_sound.stop()
in_game_sound.play(loops=-1)

figure_in = Tetris(20, 10, 1, difficulty=difficult)
# создание статичной фигуры в нижнем правом углу

counter = 0
# создание игры. counter - счетчик отвечающий за отсчет время падения

pressing_down = False

while running:
    if game.figure is None:
        game.new_figure()
    if figure_in.figure is None:
        figure_in.new_figure()
    counter += 1
    if counter > 6000:
        counter = 0

    if counter % (fps // game.difficulty // 2) == 0 or pressing_down:
        if game.running_game is True:
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game.running_game is True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
        if game.running_game is False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    title_sound.play(loops=-1)
                    level_hard()
                    title_sound.stop()
                    in_game_sound.play(loops=-1)
                    game.__init__(20, 10, difficulty=difficult)
                    game.figure = None

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
        # обработка событий

    screen.fill(BLACK)

    for i in range(game.cell_count_height):
        for j in range(game.cell_count_width):
            pygame.draw.rect(screen, GRAY, [game.field_x + game.cell_size * j, game.field_y + game.cell_size * i,
                                            game.cell_size, game.cell_size], 1)
            if game.field[i][j] is not 0:
                pygame.draw.rect(screen, game.field[i][j],
                                 [game.field_x + game.cell_size * j + 1, game.field_y + game.cell_size * i + 1,
                                  game.cell_size - 2, game.cell_size - 1])
                # отрисовка поля и сетки

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, game.figure.color,
                                     [game.field_x + game.cell_size * (j + game.figure.field_x) + 1,
                                      game.field_y + game.cell_size * (i + game.figure.field_y) + 1,
                                      game.cell_size - 2, game.cell_size - 2])
                if p in figure_in.figure.image():
                    pygame.draw.rect(screen, figure_in.figure.color,
                                     [figure_in.field_x + figure_in.cell_size * (j + figure_in.figure.field_x) + 1,
                                      figure_in.field_y + figure_in.cell_size * (i + figure_in.figure.field_y) + 1,
                                      figure_in.cell_size - 2, figure_in.cell_size - 2])
        # отрисовка падающей и статичной фигуры

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 50, True, False)
    text_score = font.render("Score:", True, WHITE)
    text_score_num = font.render(str(game.score), True, WHITE)
    text_game_over = font1.render("Game Over", True, WHITE)
    text_game_over1 = font1.render("Press ESC", True, WHITE)
    text_figure_1 = font.render("Next", True, WHITE)
    text_figure_2 = font.render("figure:", True, WHITE)

    screen.blit(text_score, [25, 625])
    screen.blit(text_score_num, [50, 650])
    screen.blit(text_figure_1, [120, 625])
    screen.blit(text_figure_2, [120, 650])

    if game.running_game is False:
        screen.blit(text_game_over, [40, 200])
        screen.blit(text_game_over1, [60, 265])

    if game.chase_figure:
        game.chase_figure = False
        game.figure.color = figure_in.figure.color
        game.figure.type = figure_in.figure.type
        figure_in = Tetris(20, 10, 1, difficulty=difficult)
        # замена фигуры падуюший на статичную

    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
