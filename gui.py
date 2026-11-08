from hnefatafl import Board
import pygame
import pygame_gui

class GameGUI:
    SQUARE = 50
    PIECE_SQUARE_RATIO = 0.8
    PIECE_IMAGE_SIZE = int(SQUARE * PIECE_SQUARE_RATIO)
    BOARD_IMAGE_SIZE = 705
    WIDTH = BOARD_IMAGE_SIZE
    PANEL_HEIGHT = 100
    HEIGHT = BOARD_IMAGE_SIZE + (PANEL_HEIGHT * 2)
    LEFT_GRID_OFFSET = 78
    TOP_GRID_OFFSET = PANEL_HEIGHT + LEFT_GRID_OFFSET
    def __init__(self):
        self.game_board = Board()
        pygame.init()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.canvas = pygame.Surface((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hnefatafl")
        self.running = True
        self.canvas_scale = 1
        self.canvas_offset = (0, 0)
        self.square_selected = None
        self.board_image = pygame.transform.smoothscale(
            pygame.image.load("graphicsArtifacts/board-full.png").convert(), 
            (self.BOARD_IMAGE_SIZE, self.BOARD_IMAGE_SIZE)
            )
        self.offense_piece_image = pygame.transform.smoothscale(
            pygame.image.load("graphicsArtifacts/offense-full.png").convert_alpha(),
            (self.PIECE_IMAGE_SIZE, self.PIECE_IMAGE_SIZE)
        )
        self.defense_piece_image = pygame.transform.smoothscale(
            pygame.image.load("graphicsArtifacts/defense-full.png").convert_alpha(),
            (self.PIECE_IMAGE_SIZE, self.PIECE_IMAGE_SIZE)
        )
        self.king_piece_image = pygame.transform.smoothscale(
            pygame.image.load("graphicsArtifacts/king-full.png").convert_alpha(),
            (self.PIECE_IMAGE_SIZE, self.PIECE_IMAGE_SIZE)
        )
        self.game_engine = Board()
        

    def draw_window(self) -> None:
        self.window.fill((74, 58, 60))
        self._draw_canvas()
        width, height = self.window.get_size()
        self.canvas_scale = min(width / self.WIDTH, height / self.HEIGHT)
        size = (int(self.WIDTH * self.canvas_scale), int(self.HEIGHT * self.canvas_scale))
        self.canvas_offset = ((width - size[0]) // 2, (height - size[1]) // 2)
        self.window.blit(pygame.transform.smoothscale(self.canvas, size), self.canvas_offset)
        pygame.display.flip()

    def _draw_canvas(self) -> None:
        self.canvas.fill((95, 181, 214))
        self.canvas.blit(self.board_image, (0, self.PANEL_HEIGHT))

    def process_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
    def _handle_click(self, click_position: tuple[int, int]) -> None:
        pass

    def _convert_click_location_into_square_clicked(self) -> tuple(int, int):
        pass


        
