from hnefatafl import Board
import pygame
import pygame_gui

class GameGUI:
    # GUI Dimensions
    SQUARE_SIZE = 50
    PIECE_SQUARE_RATIO = 0.9
    MARGIN = 10
    PIECE_IMAGE_SIZE = int(SQUARE_SIZE * PIECE_SQUARE_RATIO)
    BOARD_IMAGE_SIZE = 705
    TOP_PANEL_HEIGHT = 130
    BOTTOM_PANEL_HEIGHT = 40
    WIDTH = BOARD_IMAGE_SIZE + (MARGIN * 2)
    HEIGHT = BOARD_IMAGE_SIZE + (TOP_PANEL_HEIGHT + BOTTOM_PANEL_HEIGHT) + (MARGIN * 2)
    LEFT_GRID_OFFSET = 78 + MARGIN
    TOP_GRID_OFFSET = TOP_PANEL_HEIGHT + LEFT_GRID_OFFSET

    def __init__(self):
        self.game_board = Board()
        pygame.init()

        #SET DIMENSIONS AND SCALE OF MAJOR SURFACE OBJECTS
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.canvas = pygame.Surface((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hnefatafl")
        self.running = True
        self.canvas_scale = 1
        self.canvas_offset = (0, 0)

        # BOARD AND PIECE IMAGES
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
        # TEXT SURFACES
        # CREATE FONT OBJECTS
        self.title_font = pygame.font.Font("graphicsArtifacts/fonts/celtica/Celtica-Bold.ttf", size=75)
        self.day_roman_20pt = pygame.font.Font("graphicsArtifacts/fonts/DayRoman/DAYROM__.ttf")

        # TITLE BANNER
        self.hnefatafl_banner = self.title_font.render("hnefatafl", True, (225, 45, 75))
        self.hnefatafl_banner_shadow = self.title_font.render("hnefatafl", True, (95, 5, 26))
        # (70, 0, 13)


        # RELEVANT BOARD ENGINE RELATED VARIABLES
        self.game_engine = Board()
        self.square_selected = None
        

    def draw_window(self) -> None:
        self.window.fill((30, 18, 20))
        self._draw_canvas()
        width, height = self.window.get_size()
        self.canvas_scale = min(width / self.WIDTH, height / self.HEIGHT)
        size = (int(self.WIDTH * self.canvas_scale), int(self.HEIGHT * self.canvas_scale))
        self.canvas_offset = ((width - size[0]) // 2, (height - size[1]) // 2)
        self.window.blit(pygame.transform.smoothscale(self.canvas, size), self.canvas_offset)
        pygame.display.flip()

    def _draw_canvas(self) -> None:
        self.canvas.fill((28, 44, 62)) # original color (36, 86, 127)
        self.canvas.blit(self.board_image, (self.MARGIN, self.TOP_PANEL_HEIGHT + self.MARGIN))
        
        self.canvas.blit(self.hnefatafl_banner_shadow, 
        ((((self.WIDTH - self.hnefatafl_banner_shadow.get_width()) // 2) + 4),
        self.MARGIN + 4))
        self.canvas.blit(self.hnefatafl_banner, 
        (((self.WIDTH - self.hnefatafl_banner.get_width()) // 2),
        self.MARGIN))
        for row in range(0, 11):
            for column in range(0, 11):
                value = self.game_engine.get_board_square_value((row, column))
                match value:
                    case None:
                        continue
                    case ("defense", "standard"):
                        self.canvas.blit(self.defense_piece_image, (self._convert_piece_image_grid_to_pixels((row, column))))
                    case ("defense", "king"):
                        self.canvas.blit(self.king_piece_image, (self._convert_piece_image_grid_to_pixels((row, column))))
                    case ("offense", "standard"):
                        self.canvas.blit(self.offense_piece_image, (self._convert_piece_image_grid_to_pixels((row, column))))
    def _convert_piece_image_grid_to_pixels(self, square: tuple[int, int]) -> tuple[int, int]:
        row, column = square
        row = int((row * self.SQUARE_SIZE) + self.LEFT_GRID_OFFSET + (((1 - self.PIECE_SQUARE_RATIO)/2) * self.SQUARE_SIZE))
        column = int((column * self.SQUARE_SIZE) + self.TOP_GRID_OFFSET + (((1 - self.PIECE_SQUARE_RATIO)/2) * self.SQUARE_SIZE))
        return (row, column)


    def process_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
    def _handle_click(self, click_position: tuple[int, int]) -> None:
        pass

    def _convert_click_location_into_square_clicked(self) -> tuple[int, int]:
        pass

    def get_program_active(self) -> bool:
        return self.running



        
