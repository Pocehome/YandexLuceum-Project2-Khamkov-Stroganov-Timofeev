import os
import sys
import pygame
import random

pygame.init()

FPS = 50
WIDTH = 320
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")


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
                return
        pygame.display.flip()
        clock.tick(FPS)

start_screen()

class Figure:

    colors = [
        (50, 57, 178),
        (219, 31, 31),
        (255, 116, 10),
        (226, 232, 50),
        (31, 162, 19),
        (13, 135, 167),
    ]

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, field_x, field_y):
        self.field_x = field_x
        self.field_y = field_y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.choice(self.colors)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    running_game = True
    cell_count_height = 0
    cell_count_width = 0
    field_x = 10
    field_y = 10
    cell_size = 30
    figure = None

    def __init__(self, cell_count_height, cell_count_width, difficulty=2):
        self.cell_count_height = cell_count_height
        self.cell_count_width = cell_count_width
        self.difficulty = difficulty
        self.field = []
        self.score = 0
        self.running_game = True
        for _ in range(cell_count_height):
            new_line = []
            for _ in range(cell_count_width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)

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

    def break_lines(self):
        lines = 0
        for i in range(1, self.cell_count_height):
            zeros = 0
            for j in range(self.cell_count_width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j1 in range(self.cell_count_width):
                        self.field[i1][j1] = self.field[i1 - 1][j1]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.field_y += 1
        self.figure.field_y -= 1
        self.freeze()

    def go_down(self):
        self.figure.field_y += 1
        if self.intersects():
            self.figure.field_y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.field_y][j + self.figure.field_x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.running_game = False

    def go_side(self, dx):
        old_x = self.figure.field_x
        self.figure.field_x += dx
        if self.intersects():
            self.figure.field_x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


pygame.init()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (320, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")


running = True
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10, difficulty=2)
counter = 0

pressing_down = False

while running:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
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
                    game.__init__(20, 10)
                    game.figure = None

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(BLACK)

    for i in range(game.cell_count_height):
        for j in range(game.cell_count_width):
            pygame.draw.rect(screen, GRAY, [game.field_x + game.cell_size * j, game.field_y + game.cell_size * i,
                                            game.cell_size, game.cell_size], 1)
            if game.field[i][j]  is not 0:
                pygame.draw.rect(screen, game.field[i][j],
                                 [game.field_x + game.cell_size * j + 1, game.field_y + game.cell_size * i + 1,
                                  game.cell_size - 2, game.cell_size - 1])

    if game.figure  is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, game.figure.color,
                                     [game.field_x + game.cell_size * (j + game.figure.field_x) + 1,
                                      game.field_y + game.cell_size * (i + game.figure.field_y) + 1,
                                      game.cell_size - 2, game.cell_size - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 50, True, False)
    text_score = font.render("Score:", True, WHITE)
    text_score_num = font.render(str(game.score), True, WHITE)
    text_game_over = font1.render("Game Over", True, WHITE)
    text_game_over1 = font1.render("Press ESC", True, WHITE)

    screen.blit(text_score, [25, 625])
    screen.blit(text_score_num, [50, 650])
    if game.running_game is False:
        screen.blit(text_game_over, [40, 200])
        screen.blit(text_game_over1, [60, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()