import pathlib
import typing as tp
import random
import typing import List

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    res = []
    for i in range(0, len(values), n):
        arr = []
        # j = 0
        for j in range(n):
            # while j != n:
            q = i
            arr.append(values[q + j])
            # j += 1
        res.append(arr)
    return res


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, col = pos
    return grid[row]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    row, col = pos
    res = [x[col] for x in grid]
    return res


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    res = []
    if col <= 2 and row <= 2:
        for i in range(3):
            for j in range(3):
                res.append(grid[i][j])
    elif col <= 2 and row <= 5 and row > 2:
        for i in range(3):
            for j in range(3):
                res.append(grid[i+3][j])
    elif col <= 2 and row <= 8 and row > 5:
        for i in range(3):
            for j in range(3):
                res.append(grid[i+6][j])
    elif col <= 5 and row <= 2 and row > 2:
        for i in range(3):
            for j in range(3):
                res.append(grid[i][j+3])
    elif col <= 5 and row <= 5 and row > 2:
        for i in range(3):
            for j in range(3):
                res.append(grid[i+3][j+3])
    elif col <= 5 and row <= 8 and col > 5 and row > 5:
        for i in range(3):
            for j in range(3):
                res.append(grid[i+6][j+3])
    elif col <= 8 and row <= 2 and col > 5:
        for i in range(3):
            for j in range(3):
                res.append(grid[i][j+6])
    elif col <= 8 and row <= 5 and col > 5 and row > 2:
        for i in range(3):
            for j in range(3):
                res.append(grid[i+3][j+6])
    elif col <= 8 and row <= 8 and row > 5 and col > 5:
        for i in range(3):
            for j in range(3):
                res.append(grid[i+6][j+6])
    return res


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    i = 0
    j = 0
    k = 10
    l = 10
    while grid[i][j] != ".":
        if j < len(grid[0]) - 1:
            j += 1
        elif j == len(grid[0]) - 1:
            j = 0
            i += 1
        if i == (len(grid)):
            return k, l
    return i, j


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    res = set()
    col = set(get_col(grid, pos))
    row = set(get_row(grid, pos))
    block = set(get_block(grid, pos))
    for i in range(1, 10):
        if str(i) not in col | row | block:
            ans.add(str(i))
    return ans


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if pos == (10, 10):
        return grid
    else:
        n, m = find_empty_positions(grid)
        res = find_possible_values(grid, pos)
        for i in res:
            grid[n][m] = str(i)
            if solve(grid) is not None:
                return grid
            grid[n][m] = '.'
        return None

def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    check = 0
    for i in range(0, 9):
        for j in range(0, 9):
            if solution[i][j] == ".":
                check = 0
                break
            if i % 3 == 0 or i == 0:
                col = get_col(solution, (i, j))
                row = get_row(solution, (i, j))
                block = get_block(solution, (i, j))
                b: List[str] = []
                for x in block:
                    b.extend(x)
                setcol = set(col)
                setrow = set(row)
                setb = set(b)
                if len(setcol) == len(col) and len(setrow) == len(row) and len(setb) == len(b):
                    check = 1
                if check == 1:
                    continue
                else:
                    break
    if check == 1:
        return True
    return False


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid: List[List[str]] = [[]]
    nums = []
    for i in range(1, 10):
        nums.append(str(i))
    for j in range(9):
        grid[0].append(random.choice(nums))
        nums.remove(grid[0][j])
    for q in range(1, 9):
        grid.append([])
        for w in range(9):
            grid[q].append(".")
    solve(grid)
    n = 81
    if N > 81:
        return grid
    else:
        while n != N:
            a, b = random.randint(0, 8), random.randint(0, 8)
            if grid[a][b] != ".":
                grid[a][b] = "."
                n -= 1
        return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)