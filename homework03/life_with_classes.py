import pygame
import random
import copy
from pygame.locals import *


class Cell:
    def __init__(self, row: int, col: int, state=False) -> None:
        self.state = state
        self.row = row
        self.col = col

    def is_alive(self) -> bool:
        return self.state


class CellList:
    def __init__(self, nrows: int, ncols: int, randomize=False) -> None:
        self.nrows = nrows
        self.ncols = ncols
        if randomize:
            self.grid = [[Cell(i, j, random.randint(0, 1)) for j in range(ncols)]
                         for i in range(nrows)]
        else:
            self.grid = [[Cell(i, j, 0) for j in range(ncols)] for i in range(nrows)]

    def update(self) -> object:
        deepcopy = copy.deepcopy(self.grid)
        for cell in self:
            list = self.get_neighbours(cell)
            neighbours = sum(unit.is_alive() for unit in list)
            if cell.is_alive():
                if not 1 < neighbours < 4:
                    deepcopy[cell.row][cell.col].state = 0
            else:
                if neighbours == 3:
                    deepcopy[cell.row][cell.col].state = 1
        self.grid = deepcopy
        return self

    def get_neighbours(self, cell: Cell) -> list:
        x, y = cell.row, cell.col
        n = self.nrows - 1
        m = self.ncols - 1
        neighbours = [self.grid[i][j] for i in range(x - 1, x + 2) for j in range(y - 1, y + 2)
                      if 0 <= i <= n and 0 <= j <= m and (i != x or j != y)]
        return neighbours

    @classmethod
    def from_file(cls, filename: str) -> "CellList":
        grid = []
        with open(filename) as file:
            for i, line in enumerate(file):
                grid.append([Cell(i, j, int(c))
                             for j, c in enumerate(line) if c in "01"])
        clist = cls(len(grid), len(grid[0]), False)
        clist.grid = grid
        return clist

    def __iter__(self):
        self.i, self.j = 0, 0
        return self

    def __next__(self) -> Cell:
        if self.i == self.nrows:
            raise StopIteration

        cell = self.grid[self.i][self.j]
        self.j += 1
        if self.j == self.ncols:
            self.i += 1
            self.j = 0
        return cell

    def __str__(self) ->str:
        str = ''
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.grid[i][j].state:
                    str += '1 '
                else:
                    str += '0 '
            str += '\n'
        return str


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.grid = self.cell_list()

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        cell_list = CellList(self.cell_height, self.cell_width, randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            x = 0
            y = 0
            for cell in cell_list:
                if cell.is_alive():
                    pygame.draw.rect(self.screen, pygame.Color('green'), [
                        x+1, y+1, self.cell_size-1, self.cell_size-1])
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), [
                        x+1, y+1, self.cell_size-1, self.cell_size-1])
                x += self.cell_size
                if x >= self.width:
                    y += self.cell_size
                    x = 0
            cell_list.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True)->tuple:
        self.clist = CellList(self.cell_width, self.cell_height, randomize)
        self.grid = self.clist.grid
        return self.grid

    '''def draw_cell_list(self, cell_list: "CellList") -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                x = j * self.cell_size + 1
                y = i * self.cell_size + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if self.grid[j][i].is_alive():
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, a, b))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, a, b))'''


if __name__ == '__main__':
    game = GameOfLife(1000, 1000, 20,100)
    game.run()
