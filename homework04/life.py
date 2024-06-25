import pathlib
import random
import typing as tp


Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[int] = None,
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """ Отрисовать сетку """
        return [
            [random.randint(0, 1) if randomize else 0 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

    def get_neighbours(self, cell: Cell) -> Cells:
        """ Запустить игру """
        neighbours = []
        row, col = cell

        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i, j) != cell and 0 <= i < self.rows and 0 <= j < self.cols:
                    neighbours.append(self.curr_generation[i][j])

        return neighbours


    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = self.create_grid(randomize=False)
        for row in range(self.rows):
            for col in range(self.cols):
                alive_neighbours = sum(self.get_neighbours((row, col)))
                if self.curr_generation[row][col] == 1:
                    new_grid[row][col] = 1 if alive_neighbours in [2, 3] else 0
                else:
                    new_grid[row][col] = 1 if alive_neighbours == 3 else 0

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation


    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open('glider.txt', 'r') as f:
            lines = f.readlines()
        grid = [[int(char) for char in line.strip()] for line in lines]
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0
        game = GameOfLife((rows, cols), randomize=False)
        game.curr_generation = grid
        return game


    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open('glider.txt', 'w') as f:
            for row in self.curr_generation:
                f.write("".join(map(str, row)) + "\n")
