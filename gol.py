import pygame
import numpy as np
from scipy.signal import convolve2d

# Colors
CYAN = (0, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

class GameOfLife:
    def __init__(self):
        self.running = True
        self.grid_size = None
        self.screen = None

    def draw_grid(self):
        if self.screen is not None:
            self.screen.fill(BLACK)
            cell_width = self.screen.get_width() // self.grid_size[0]
            cell_height = self.screen.get_height() // self.grid_size[1]

            changes = self.grid != self.prev_grid
            for i, j in np.argwhere(self.grid == 1):
                color = CYAN if changes[i, j] else GREY
                pygame.draw.rect(self.screen, color, (i * cell_width, j * cell_height, cell_width, cell_height))

            pygame.display.flip()

    def update_grid(self):
        self.prev_grid = self.grid.copy()

        kernel = np.array([[1,1,1], [1,0,1], [1,1,1]])
        neighbor_count = convolve2d(self.grid, kernel, mode='same', boundary='wrap')

        self.grid = np.where(
            (self.grid == 1) & ((neighbor_count == 2) | (neighbor_count == 3)) |
            (self.grid == 0) & (neighbor_count == 3),
            1, 0
        )

    def handle_mouse_click(self, pos):
        width, height = self.screen.get_size()
        cell_width = width // self.grid_size[0]
        cell_height = height // self.grid_size[1]
        grid_x = pos[0] // cell_width
        grid_y = pos[1] // cell_height

        if 0 <= grid_x < self.grid_size[0] and 0 <= grid_y < self.grid_size[1]:
            self.grid[grid_x, grid_y] = 1  # Set cell to alive

    def run(self):
        pygame.init()
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        grid_size = (int(WIDTH / 5), int(HEIGHT / 5))
        self.grid_size = grid_size
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.grid = np.random.choice([0, 1], size=grid_size, p=[0.5, 0.5])
        self.prev_grid = self.grid.copy()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event.pos)

            self.draw_grid()
            self.update_grid()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    GameOfLife().run()

