import pygame
from pygame.locals import *
from ui import UI
from life import GameOfLife

class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        self.life = life
        self.speed = speed
        self.cell_size = cell_size
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)


    def draw_lines(self) -> None:
        # Отрисовка вертикальных линий
        for x in range(0, self.width + 1, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        # Отрисовка горизонтальных линий
        for y in range(0, self.height + 1, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                color = pygame.Color('green') if self.life.curr_generation[row][col] == 1 else pygame.Color('white')
                pygame.draw.rect(self.screen, color,
                                 (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused
                elif event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    col = x // self.cell_size
                    row = y // self.cell_size
                    self.life.curr_generation[row][col] = 1 if self.life.curr_generation[row][col] == 0 else 0
            self.screen.fill(pygame.Color('white'))
            self.draw_lines()
            self.draw_grid()
            if not paused:
                self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife((50, 50), max_generations=10)
    gui = GUI(game, cell_size=10, speed=10)
    gui.run()