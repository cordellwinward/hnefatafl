from hnefatafl import Board
import pygame
import pygame_gui

class GameGUI:
    SQUARE = 50
    BOARD_IMAGE_SIZE = 705
    GRID_OFFSET = 78
    WIDTH = BOARD_IMAGE_SIZE
    PANEL_HEIGHT = 200
    HEIGHT = BOARD_IMAGE_SIZE + PANEL_HEIGHT
    def __init__(self):
        self.game_board = Board()
        pygame.init()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.canvas = pygame.Surface((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hnefatafl")
        self.running = True
        self.canvas_scale = 1
        self.canvas_offset = (0, 0)

    def draw_window(self):
        self.window.fill((74, 58, 60))
        self._draw_canvas()
        width, height = self.window.get_size()
        self.canvas_scale = min(width / self.WIDTH, height / self.HEIGHT)
        size = (int(self.WIDTH * self.canvas_scale), int(self.HEIGHT * self.canvas_scale))
        self.canvas_offset = ((width - size[0]) // 2, (height - size[1]) // 2)
        self.window.blit(pygame.transform.smoothscale(self.canvas, size), self.canvas_offset)
        pygame.display.flip()

    def _draw_canvas(self):
        self.canvas.fill((95, 181, 214))


        
