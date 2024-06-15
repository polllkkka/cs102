import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        if max_generations and max_generations < 1:
            raise ValueError("Число поколений должно быть положительным!")
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """ Отрисовать сетку """
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """ Запустить игру """
        i, j = cell
        cells = []

        if i > 0:
            if j > 0:
                cells.append(self.curr_generation[i - 1][j - 1])
            cells.append(self.curr_generation[i - 1][j])
            if j < self.rows - 1:
                cells.append(self.curr_generation[i - 1][j + 1])

        if j > 0:
            cells.append(self.curr_generation[i][j - 1])
        if j < self.cols - 1:
            cells.append(self.curr_generation[i][j + 1])

        if i < self.rows - 1:
            if j > 0:
                cells.append(self.curr_generation[i + 1][j - 1])
            cells.append(self.curr_generation[i + 1][j])
            if j < self.cols - 1:
                cells.append(self.curr_generation[i + 1][j + 1])

        return cells

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                alive_neighbours_quantity = neighbours.count(1)
                if (alive_neighbours_quantity == 3 or
                        alive_neighbours_quantity == 2 and self.curr_generation[i][j]):
                    grid[i][j] = 1

        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.save_generation()
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.max_generations and self.max_generations < self.generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.curr_generation[i][j] != self.prev_generation[i][j]:
                    return True
        return False



    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open('glider.txt', 'r') as f:
            lines = [line.strip() for line in f.readline()]
        rows = len(lines)
        if rows == 0:
            raise ValueError("В файле должна быть хотя бы одна строка!")
        cols = len(lines[0])
        if cols == 0:
            raise ValueError("В строке должен быть хотя бы один символ!")

        grid = [[0 for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            if len(lines[i]) != cols:
                raise ValueError("В строках должно быть одинаковое количество символов!")
            for j in range(cols):
                char = lines[i][j]
                if char != '0' and char != '1':
                    raise ValueError("Допустимые значения - 0 и 1. Без пробелов.")
                grid[i][j] = int(char)

        game = GameOfLife(size=(rows, cols), randomize=False)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open('glider.txt', 'w') as f:
            for i in range(self.rows):
                row = self.curr_generation[i]
                f.write(''.join([str(v) for v in row]))
                f.write('\n')

    def save_generation(self):
        self.prev_generation = [row.copy() for row in self.curr_generation]

    def change_cell(self, cell):
        i, j = cell
        self.save_generation()
        self.generations = 1
        self.curr_generation[i][j] = 1 - self.curr_generation[i][j]
