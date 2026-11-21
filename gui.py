from typing import ClassVar
from hnefatafl import Board
from guiError import GUIError
import pygame
import pygame_gui


class GameGUI:
    """Manage the pygame window, board rendering, and player interactions."""

    # GUI Dimensions

    SQUARE_SIZE: ClassVar[int] = 50
    PIECE_SQUARE_RATIO: ClassVar[float] = 0.9
    MOVEMENT_DOT_RATIO: ClassVar[float] = 0.3
    MARGIN: ClassVar[int] = 10
    BOARD_GRID_SIZE: ClassVar[int] = 11
    PIECE_IMAGE_SIZE: ClassVar[int] = int(SQUARE_SIZE * PIECE_SQUARE_RATIO)
    MOVEMENT_DOT_IMAGE_SIZE: ClassVar[int] = int(SQUARE_SIZE * MOVEMENT_DOT_RATIO)
    BOARD_IMAGE_SIZE: ClassVar[int] = 705
    TOP_PANEL_HEIGHT: ClassVar[int] = 140
    BOTTOM_PANEL_HEIGHT: ClassVar[int] = 30
    WIDTH: ClassVar[int] = BOARD_IMAGE_SIZE + (MARGIN * 2)
    HEIGHT: ClassVar[int] = (
        BOARD_IMAGE_SIZE + (TOP_PANEL_HEIGHT + BOTTOM_PANEL_HEIGHT) + (MARGIN * 2)
    )
    LEFT_GRID_OFFSET: ClassVar[int] = 78 + MARGIN
    TOP_GRID_OFFSET: ClassVar[int] = TOP_PANEL_HEIGHT + LEFT_GRID_OFFSET

    def __init__(self) -> None:
        """Initialize pygame resources, game state, and display surfaces."""
        pygame.init()

        # Set dimensions and scale of major surface objects.

        self.window: pygame.Surface = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT), pygame.RESIZABLE
        )
        self.canvas: pygame.Surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hnefatafl")
        self.running: bool = True
        self.canvas_scale: float = 1.0
        self.canvas_offset: tuple[int, int] = (0, 0)

        # Board and piece images.

        self.board_image: pygame.Surface = pygame.transform.smoothscale(
            pygame.image.load("graphicsArtifacts/board-full.png").convert(), 
            (self.BOARD_IMAGE_SIZE, self.BOARD_IMAGE_SIZE)
            )
        self.offense_piece_image: pygame.Surface = pygame.transform.smoothscale(
            pygame.image.load("graphicsArtifacts/offense-full.png").convert_alpha(),
            (self.PIECE_IMAGE_SIZE, self.PIECE_IMAGE_SIZE)
        )
        self.defense_piece_image: pygame.Surface = pygame.transform.smoothscale(
            pygame.image.load("graphicsArtifacts/defense-full.png").convert_alpha(),
            (self.PIECE_IMAGE_SIZE, self.PIECE_IMAGE_SIZE)
        )
        self.king_piece_image: pygame.Surface = pygame.transform.smoothscale(
            pygame.image.load("graphicsArtifacts/king-full.png").convert_alpha(),
            (self.PIECE_IMAGE_SIZE, self.PIECE_IMAGE_SIZE)
        )

        # Text surfaces and font objects.

        self.title_font: pygame.font.Font = pygame.font.Font(
            "graphicsArtifacts/fonts/celtica/Celtica-Bold.ttf", size=70
        )
        self.day_roman_20pt: pygame.font.Font = pygame.font.Font(
            "graphicsArtifacts/fonts/DayRoman/DAYROM__.ttf"
        )
        self.day_roman_16pt: pygame.font.Font = pygame.font.Font(
            "graphicsArtifacts/fonts/DayRoman/DAYROM__.ttf", size=16
        )

        # Title banner.

        self.hnefatafl_banner: pygame.Surface = self.title_font.render(
            "hnefatafl", True, (225, 45, 75)
        )
        self.hnefatafl_banner_shadow: pygame.Surface = self.title_font.render(
            "hnefatafl", True, (95, 5, 26)
        )

        # Turn text.

        self.defense_turn_display: pygame.Surface = self.day_roman_20pt.render(
            "DEFENSE TO MOVE", True, (232, 198, 112)
        )
        self.offense_turn_display: pygame.Surface = self.day_roman_20pt.render(
            "OFFENSE TO MOVE", True, (232, 198, 112)
        )

        # Gold line decoration surface.

        self.decorative_line: pygame.Surface = pygame.Surface(
            (self.hnefatafl_banner.get_width() - 10, 2)
        )
        self.decorative_line.fill((212, 168, 68))

        # Selected square highlight and possible move dots.

        self.select_square_highlight: pygame.Surface = pygame.Surface(
            (self.SQUARE_SIZE, self.SQUARE_SIZE)
        )
        self.select_square_highlight.fill((107, 131, 196))
        self.possible_move_dot: pygame.Surface = pygame.transform.smoothscale(
            pygame.image.load(
                "graphicsArtifacts/blue-movement-dot.png"
            ).convert_alpha(),
            (self.MOVEMENT_DOT_IMAGE_SIZE, self.MOVEMENT_DOT_IMAGE_SIZE)
        )

        # Move error surfaces and flags.

        self.errors: dict[str, GUIError] = {
            "unexpected": GUIError(
                "An unexpected error occurred. Please Move Again.",
                self.day_roman_16pt,
            ),
            "no_piece_on_square": GUIError(
                "You do not have a piece on that square. "
                "Please select a square with your piece.",
                self.day_roman_16pt,
            ),
            "piece_no_valid_moves": GUIError(
                "That piece has no valid moves. "
                "Please select a different piece.",
                self.day_roman_16pt,
            ),
            "invalid_move": GUIError(
                "That piece cannot move to that square. "
                "Please make a different move.",
                self.day_roman_16pt,
            ),
        }

        #GAME OVER TEXT SURFACES


        #GAME INSTRUCTION SURFACE


        # RELEVANT BOARD ENGINE RELATED VARIABLES
        self.game_engine: Board = Board()
        self.square_selected: tuple[int, int] | None = None
        self.square_selected_valid_moves: list[tuple[int, int]] = []

    # Window and canvas rendering.

    def draw_window(self) -> None:
        """Draw the canvas to the resizable window and update the display."""
        self.window.fill((30, 18, 20))
        self._draw_canvas()
        width, height = self.window.get_size()
        self.canvas_scale = min(width / self.WIDTH, height / self.HEIGHT)
        size = (
            int(self.WIDTH * self.canvas_scale),
            int(self.HEIGHT * self.canvas_scale),
        )
        self.canvas_offset = ((width - size[0]) // 2, (height - size[1]) // 2)
        self.window.blit(
            pygame.transform.smoothscale(self.canvas, size), self.canvas_offset
        )
        pygame.display.flip()

    def _draw_canvas(self) -> None:
        """Draw the board, interface text, pieces, selections, and errors."""

        # Fill board background colors and display board.
        self.canvas.fill((28, 44, 62))
        self.canvas.blit(
            self.board_image, (self.MARGIN, self.TOP_PANEL_HEIGHT + self.MARGIN)
        )

        # Draw title banner
        self.canvas.blit(self.hnefatafl_banner_shadow, 
            ((((self.WIDTH - self.hnefatafl_banner_shadow.get_width()) // 2) + 4),
            self.MARGIN + 4))
        self.canvas.blit(self.hnefatafl_banner, 
            (((self.WIDTH - self.hnefatafl_banner.get_width()) // 2),
            self.MARGIN))

        # Render turn text and gold decoration.
        self._draw_turn_text()
        self.canvas.blit(
            self.decorative_line,
            (
                (self.WIDTH - self.decorative_line.get_width()) // 2,
                self.MARGIN
                + self.hnefatafl_banner_shadow.get_height()
                + self.defense_turn_display.get_height()
                + 4,
            ),
        )

        # Draw selected square highlight and its possible moves.
        self._draw_highlight_selected_square()
        self._draw_possible_move_dots()

        # Render pieces on board.
        self._draw_pieces_on_board()

        # Render errors.
        self._draw_errors()

    def _draw_turn_text(self) -> None:
        """Draw the message identifying which team moves next."""
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
                
    def _draw_pieces_on_board(self) -> None:
        """Draw each board piece using its team and piece type."""
        for row in range(self.BOARD_GRID_SIZE):
            for column in range(self.BOARD_GRID_SIZE):
                value = self.game_engine.get_board_square_value((row, column))
                match value:
                    case None:
                        continue
                    case ("defense", "standard"):
                        position = self._convert_piece_image_grid_to_pixels(
                            (row, column)
                        )
                        self.canvas.blit(self.defense_piece_image, position)
                    case ("defense", "king"):
                        position = self._convert_piece_image_grid_to_pixels(
                            (row, column)
                        )
                        self.canvas.blit(self.king_piece_image, position)
                    case ("offense", "standard"):
                        position = self._convert_piece_image_grid_to_pixels(
                            (row, column)
                        )
                        self.canvas.blit(self.offense_piece_image, position)

    def _draw_highlight_selected_square(self) -> None:
        """Draw the highlight behind the currently selected square."""
        if self.square_selected is not None:
            self.canvas.blit(self.select_square_highlight, 
                             (
                                 self.LEFT_GRID_OFFSET
                                 + (self.square_selected[1] * self.SQUARE_SIZE - 1),
                                 self.TOP_GRID_OFFSET
                                 + (self.square_selected[0] * self.SQUARE_SIZE - 1),
                             ))

    def _draw_possible_move_dots(self) -> None:
        """Draw a movement dot on every valid destination square."""
        if self.square_selected is not None:
            for square in self.square_selected_valid_moves:
                self.canvas.blit(self.possible_move_dot,
                                 self._convert_piece_image_grid_to_pixels(
                                     square, ratio=self.MOVEMENT_DOT_RATIO
                                 ))

    def _draw_errors(self) -> None:
        """Draw each active move error below the board."""
        for error in self.errors.values():
            if error.get_active():
                self.canvas.blit(error.get_error_surface(), 
                                (
                                    self.MARGIN
                                    + (
                                        (
                                            self.WIDTH
                                            - error.get_error_surface().get_width()
                                        )
                                        // 2
                                    ),
                                    self.MARGIN
                                    + self.TOP_PANEL_HEIGHT
                                    + self.BOARD_IMAGE_SIZE
                                    + self.MARGIN,
                                ))

    def _reset_errors(self) -> None:
        """Deactivate all currently displayed move errors."""
        for error in self.errors.values():
            error.set_active(False)

    def _draw_game_over_pop_up(self) -> None:
        """Draw the game-over popup when that interface is implemented."""
        pass

    def _reset_game(self) -> None:
        """Reset the game and interface state when that feature is implemented."""
        pass

    # Coordinate conversion.

    def _convert_piece_image_grid_to_pixels(
        self,
        square: tuple[int, int],
        ratio: float = PIECE_SQUARE_RATIO,
    ) -> tuple[int, int]:
        """Convert a board square and image ratio into canvas pixel coordinates."""
        y, x = square
        x = int(
            (x * self.SQUARE_SIZE)
            + self.LEFT_GRID_OFFSET
            + (((1 - ratio) / 2) * self.SQUARE_SIZE)
        )
        y = int(
            (y * self.SQUARE_SIZE)
            + self.TOP_GRID_OFFSET
            + (((1 - ratio) / 2) * self.SQUARE_SIZE)
        )
        return (x, y)

    # Event handling and board interaction.

    def process_events(self, events: list[pygame.event.Event]) -> None:
        """Process pygame events and handle quit or left-click actions."""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)

    def _handle_click(self, click_position: tuple[int, int]) -> None:
        """Convert a window click to canvas coordinates and process board clicks."""
        x, y = click_position
        x = int((x - self.canvas_offset[0]) // self.canvas_scale)
        y = int((y - self.canvas_offset[1]) // self.canvas_scale)
        x -= self.LEFT_GRID_OFFSET
        y -= self.TOP_GRID_OFFSET

        if (0 <= x < (self.SQUARE_SIZE * self.BOARD_GRID_SIZE)
            and 0 <= y < (self.SQUARE_SIZE * self.BOARD_GRID_SIZE)
            and not self.game_engine.get_game_over()[0]):
            self._handle_board_grid_click((x, y))

    def _handle_board_grid_click(self, board_pixel_coordinate: tuple[int, int]) -> None:
        """Takes the grid position of a click inside the board area in pixels (x, y). 
            0px is considered to be the left edge of the leftmost square and the top
            edge of the top square. Uses those pixel coordinates to properly handle
            how it affects the game engine and self.square_selected."""
        column, row = board_pixel_coordinate
        row = row // self.SQUARE_SIZE
        column = column // self.SQUARE_SIZE
        self._reset_errors()
        if (0 <= row < self.BOARD_GRID_SIZE) and (0 <= column < self.BOARD_GRID_SIZE):
            board_coordinate = (row, column)
            if self.square_selected == board_coordinate:
                self.square_selected = None
                self.square_selected_valid_moves = []
            elif self.square_selected is None:
                self._select_square(board_coordinate)
            elif self.square_selected != board_coordinate:
                self._make_move(board_coordinate)
        else:
            # Display an error for an invalid board coordinate.
            self.errors["unexpected"].set_active(True)

    def _select_square(self, board_coordinate: tuple[int, int]) -> None:
        """Select a piece or activate the appropriate selection error."""
        valid_moves = self.game_engine.select_board_square(board_coordinate)
        if valid_moves is None:
            # Display an error when the square has no current player's piece.
            self.errors["no_piece_on_square"].set_active(True)
        elif not valid_moves:
            # Display an error when the piece has no legal moves.
            self.errors["piece_no_valid_moves"].set_active(True)
        elif len(valid_moves) >= 1:
            self.square_selected_valid_moves = valid_moves
            self.square_selected = board_coordinate

    def _make_move(self, board_coordinate: tuple[int, int]) -> None:
        """Move the selected piece or activate the invalid-move error."""
        if board_coordinate in self.square_selected_valid_moves:
            self.game_engine.move_piece(self.square_selected, board_coordinate)
            self.square_selected = None
            self.square_selected_valid_moves = []
        else:
            # Display an error for an invalid destination.
            self.errors["invalid_move"].set_active(True)

    # Program state.

    def get_program_active(self) -> bool:
        """Return whether the GUI event loop should continue running."""
        return self.running
