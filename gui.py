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
    TOP_PANEL_HEIGHT = 140
    BOTTOM_PANEL_HEIGHT = 30
    WIDTH = BOARD_IMAGE_SIZE + (MARGIN * 2)
    HEIGHT = BOARD_IMAGE_SIZE + (TOP_PANEL_HEIGHT + BOTTOM_PANEL_HEIGHT) + (MARGIN * 2)
    LEFT_GRID_OFFSET = 78 + MARGIN
    TOP_GRID_OFFSET = TOP_PANEL_HEIGHT + LEFT_GRID_OFFSET

    def __init__(self):
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
        self.title_font = pygame.font.Font("graphicsArtifacts/fonts/celtica/Celtica-Bold.ttf", size=70)
        self.day_roman_20pt = pygame.font.Font("graphicsArtifacts/fonts/DayRoman/DAYROM__.ttf")

        # TITLE BANNER
        self.hnefatafl_banner = self.title_font.render("hnefatafl", True, (225, 45, 75))
        self.hnefatafl_banner_shadow = self.title_font.render("hnefatafl", True, (95, 5, 26))

        # Turn Text
        self.defense_turn_display = self.day_roman_20pt.render("DEFENSE TO MOVE", True, (232, 198, 112))
        self.offense_turn_display = self.day_roman_20pt.render("OFFENSE TO MOVE", True, (232, 198, 112))

        #gold line decoration surface
        self.decorative_line = pygame.Surface(((self.hnefatafl_banner.get_width() - 10), 2))
        self.decorative_line.fill((212, 168, 68))


        # RELEVANT BOARD ENGINE RELATED VARIABLES
        self.game_engine = Board()
        self.square_selected = None
        self.square_selected_valid_moves = []
        

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
        # Fill board Background colors and display board
        self.canvas.fill((28, 44, 62)) 
        self.canvas.blit(self.board_image, (self.MARGIN, self.TOP_PANEL_HEIGHT + self.MARGIN))

        # Draw title banner
        self.canvas.blit(self.hnefatafl_banner_shadow, 
            ((((self.WIDTH - self.hnefatafl_banner_shadow.get_width()) // 2) + 4),
            self.MARGIN + 4))
        self.canvas.blit(self.hnefatafl_banner, 
            (((self.WIDTH - self.hnefatafl_banner.get_width()) // 2),
            self.MARGIN))

        #Render turn text and gold decoration
        self._draw_turn_text()
        self.canvas.blit(self.decorative_line, ((self.WIDTH - self.decorative_line.get_width()) // 2,
            self.MARGIN + self.hnefatafl_banner_shadow.get_height() + self.defense_turn_display.get_height() + 4))

        # Render Pieces on Board
        self._draw_pieces_on_board()

    def _draw_turn_text(self):
        turn = self.game_engine.get_board_turn()
        match turn:
            case "defense":
                self.canvas.blit(self.defense_turn_display, (
                    (self.WIDTH - self.defense_turn_display.get_width()) // 2,
                    self.MARGIN + self.hnefatafl_banner_shadow.get_height()))
            case "offense":
                self.canvas.blit(self.offense_turn_display, (
                    (self.WIDTH - self.offense_turn_display.get_width()) // 2,
                    self.MARGIN + self.hnefatafl_banner_shadow.get_height()))
    def _draw_pieces_on_board(self):
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
        y, x = square
        x = int((x * self.SQUARE_SIZE) + self.LEFT_GRID_OFFSET + (((1 - self.PIECE_SQUARE_RATIO)/2) * self.SQUARE_SIZE))
        y = int((y * self.SQUARE_SIZE) + self.TOP_GRID_OFFSET + (((1 - self.PIECE_SQUARE_RATIO)/2) * self.SQUARE_SIZE))
        return (x, y)


    def process_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
                
    def _handle_click(self, click_position: tuple[int, int]) -> None:
        x, y = click_position
        x = int((x - self.canvas_offset[0]) // self.canvas_scale)
        y = int((y - self.canvas_offset[1]) // self.canvas_scale)
        relative_click_position = (x, y)
        x -= self.LEFT_GRID_OFFSET
        y -= self.TOP_GRID_OFFSET

        if 0 <= x < (self.SQUARE_SIZE * 11) and 0 <= y < (self.SQUARE_SIZE * 11):
            self._handle_board_grid_click((x, y))


    def _handle_board_grid_click(self, board_pixel_coordinate: tuple[int, int]) -> None:
        """Takes the grid position of a click inside the board area in pixels (x, y). 
            0px is considered to be the left edge of the leftmost square and the top edge of the top square.
            Uses those pixel coordinates to properly handles how it affects the game engine 
            and the class variable self.square_selected."""
        column, row = board_pixel_coordinate
        row = row // self.SQUARE_SIZE
        column = column // self.SQUARE_SIZE
        if (0 <= row <= 10) and (0 <= column <= 10):
            board_coordinate = (row, column)
            if self.square_selected == board_coordinate:
                self.square_selected = None
                self.square_selected_valid_moves = []
            elif self.square_selected == None:
                self._select_square(board_coordinate)
            elif self.square_selected != board_coordinate:
                self._make_move(board_coordinate)
        else:
            #Add error case: something happened so your passing a board coordinate out of range
            pass

    def _select_square(self, board_coordinate: tuple[int, int]) -> None:
        valid_moves = self.game_engine.select_board_square(board_coordinate)
        if valid_moves == None:
            #Add error case: Not your piece selected
            pass
        elif valid_moves == []:
            #Add error case: This piece has no valid moves
            pass
        elif len(valid_moves) >= 1:
            self.square_selected_valid_moves = valid_moves
            self.square_selected = board_coordinate


    def _make_move(self, board_coordinate: tuple[int, int]) -> None:
        if board_coordinate in self.square_selected_valid_moves:
            self.game_engine.move_piece(self.square_selected, board_coordinate)
            self.square_selected = None
            self.square_selected_valid_moves = []
        else:
            # Handle error case: this piece can't move here.
            pass

    def get_program_active(self) -> bool:
        return self.running



        
