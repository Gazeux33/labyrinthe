import sys
import pygame
import random

COLORS = {"-1": "#000000",
          "0": "#FFFFFF",
          "1": "#4749FC",
          "2": "#BC47FC",
          "3": "#F747FC",
          "4": "#5CFC47",
          "5": "#F4FC47",
          "6": "#F4FC47",
          "7": "#FF0F01",
          "8": "#396E1F",
          "9": "#141075",
          }


class Game:
    def __init__(self):
        self.NB_CASE = 100
        self.TILE_SIZE = 20
        self.SIZE = self.NB_CASE * self.TILE_SIZE, self.NB_CASE * self.TILE_SIZE

        pygame.init()
        self.display_screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Labyrinth")

        self.clock = pygame.time.Clock()

        self.matrix = [[-1 for y in range(self.NB_CASE)] for i in range(self.NB_CASE)]
        self.add_colors()

        self.walls = self.get_walls()

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.transform_matrix()
            self.transform_matrix()
            
            self.draw_matrix()

            pygame.display.flip()

    def draw_matrix(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                rect = pygame.Rect(j * self.TILE_SIZE, i * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                color = self.matrix[i][j]
                pygame.draw.rect(self.display_screen, COLORS[str(color)], rect)

    def add_colors(self):
        for i in range(1, len(self.matrix) - 1, 2):
            for j in range(1, len(self.matrix) - 1, 2):
                self.matrix[i][j] = random.randint(1, len(COLORS) - 2)
        self.matrix[1][0] = 0
        self.matrix[len(self.matrix)-2][len(self.matrix)-1] = 0

    def print_matrix(self):
        for tab in self.matrix:
            print(tab)

    def get_walls(self):
        wall = []
        for i in range(1, len(self.matrix) - 1, 1):
            for j in range(1, len(self.matrix) - 1, 1):
                if self.matrix[i][j] == -1:
                    wall.append((j, i))  # add wall coordinates
        return wall

    def get_tiles(self):
        tiles = []
        for i in range(1, len(self.matrix) - 1, 1):
            for j in range(1, len(self.matrix) - 1, 1):
                if self.matrix[i][j] != -1:
                    tiles.append((j, i))  # add wall coordinates
        return tiles

    def transform_matrix(self):
        for wall in self.get_walls():
            axis = random.randint(1, 2)
            if axis == 1:
                if not self.transform_lines(wall):
                    self.transform_columns(wall)
            elif axis == 2:
                if not self.transform_columns(wall):
                    self.transform_lines(wall)

    def transform_lines(self, wall):
        y, x = wall
        if self.matrix[y][x - 1] != -1 and self.matrix[y][x + 1] != -1:
            if self.matrix[y][x - 1] != self.matrix[y][x + 1]:
                self.spread_color(wall, random.choice([self.matrix[y][x - 1], self.matrix[y][x + 1]]))
                return True
        return False


    def transform_columns(self, wall):
        y, x = wall
        if self.matrix[y - 1][x] != -1 and self.matrix[y + 1][x] != -1:
            if self.matrix[y - 1][x] != self.matrix[y + 1][x]:
                self.spread_color(wall, random.choice([self.matrix[y - 1][x], self.matrix[y + 1][x]]))
                return True
        return False


    def spread_color(self, wall, color):
        y, x = wall
        self.matrix[y][x] = color
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i)+abs(j) == 1 and self.is_wall_in_range(y + i, x + j) and self.matrix[y + i][x + j] != color and self.matrix[y + i][x + j] != -1:
                    self.spread_color((y + i, x + j), color)

    def is_wall_in_range(self, x, y):
        if x >= len(self.matrix) - 1 or y >= len(self.matrix) - 1 or x < 0 or y < 0:
            return False
        return True


game = Game()
game.play()
