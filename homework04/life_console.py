import curses

from life import GameOfLife
from ui import UI
import time

QUIT_KEYS = [81, 113, 201, 233]
SAVE_KEYS = [83, 115, 251, 219]
LOAD_KEYS = [76, 228, 196, 108]
PAUSE_KEYS = [32]


class Console(UI):
    def __init__(self, life: GameOfLife, speed: int = 20) -> None:
        super().__init__(life)
        self.width = life.cols + 2
        self.height = life.rows + 2
        self.speed = 1 / speed

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        for i in range(1, self.width - 1):
            screen.addch(0, i, '-')
            screen.addch(self.height - 1, i, '-')

        for j in range(1, self.height-1):
            screen.addch(j, 0, '|')
            screen.addch(j, self.width-1, '|')

        screen.addch(0, 0, '+')
        screen.addch(self.height - 1, 0, '+')
        screen.addch(0, self.width - 1, '+')
        screen.addch(self.height - 1, self.width - 1, '+')

        screen.refresh()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            y = 1 + i
        for j in range(self.life.cols):
            x = 1 + j
            screen.addch(y, x, '●' if self.life.curr_generation[i][j] else ' ')
        screen.refresh()

    def run(self) -> None:
        screen = curses.initscr()
        screen.resize(self.height + 1, self.width + 1)
        screen.nodelay(True)
        curses.noecho()
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        print('\033[?1003h')

        self.draw_borders(screen)

        running = True
        while running:
            key = screen.getch()
            if key in PAUSE_KEYS:
                self.pause(screen)
            elif key in QUIT_KEYS:
                running = False
            elif key in SAVE_KEYS:
                self.save()
            elif key in LOAD_KEYS:
                self.load()

            self.draw_grid(screen)
            self.life.step()
            time.sleep(self.speed)
            if not self.life.is_changing or self.life.is_max_generations_exceeded:
                self.life.generations = 1
                running = False

        curses.endwin()

    def pause(self, screen):
        edit_mode = True
        while edit_mode:
            key = screen.getch()
            if key in PAUSE_KEYS:
                edit_mode = False
            elif key in SAVE_KEYS:
                self.save()
            elif key in QUIT_KEYS:
                edit_mode = False
            elif key in LOAD_KEYS:
                self.load()
            elif key == curses.KEY_MOUSE:
                _, x, y, _, _ = curses.getmouse()
                if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                    i = y - 1
                    j = x - 1
                    self.life.change_cell((i, j))
                    self.draw_grid(screen)


if __name__ == '__main__':
    life = GameOfLife((24, 80), max_generations=1000)
    ui = Console(life)
    ui.run()