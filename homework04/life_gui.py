import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class Button:
    def __init__(self, x, y, width, height, text, handler):
        self.handler = handler
        self.position = (x, y, width, height)
        font = pygame.font.Font(None, 30)
        self.text = font.render(text, True, pygame.Color("black"))
        self.text_place = self.text.get_rect(center=(x + width/2, y + height/2))

    def draw(self, screen, color=pygame.Color("white")):
        pygame.draw.rect(screen, color, self.position)
        screen.blit(self.text, self.text_place)

    def click(self):
        self.handler()


class Menu:
    def __init__(self, width, height, screen, x=0, y=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.screen = screen


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.height = self.cell_size * self.life.rows
        self.width = self.cell_size * self.life.cols
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.menu = [Button(10, 0, 50, self.height, "save", self.save),
                     Button(70, 0, 50, self.height, "load", self.load)]
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.life.cols, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.life.rows))
        for y in range(0, self.life.rows, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.life.cols, y))


    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            y = self.menu_height + i * self.cell_size
            for j in range(self.life.cols):
                x = j * self.cell_size
                color = pygame.Color("green" if self.life.curr_generation[i][j] else "white")
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while self.life.is_changing and running:
            self.life.step()
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife((50, 50), max_generations=10000)
    gui = GUI(game)
    gui.run()