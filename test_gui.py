import os

# Prevent tests from opening a real window.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
import pytest

from gui import GameGUI


@pytest.fixture
def game_gui():
    """Create a GUI instance for a test and close pygame afterward."""
    pygame.init()
    gui = GameGUI()
    yield gui
    pygame.quit()


# Initialization and program-state tests.

def test_game_gui_init(game_gui):
    """Verify that the GUI creates its surfaces and initial state."""
    assert isinstance(game_gui.window, pygame.Surface)
    assert isinstance(game_gui.canvas, pygame.Surface)
    assert game_gui.running is True
    assert game_gui.square_selected is None
    assert game_gui.square_selected_valid_moves == []
    assert all(error.get_active() is False for error in game_gui.errors.values())


def test_get_program_active(game_gui):
    """Verify that the active-state method reports the running state."""
    assert game_gui.get_program_active() is True


# Event and coordinate-handling tests.

def test_process_events(game_gui):
    """Verify that quit and non-left-click events are handled correctly."""
    # A QUIT event should stop the game.
    quit_event = pygame.event.Event(pygame.QUIT)
    game_gui.process_events([quit_event])
    assert game_gui.running is False
    assert game_gui.get_program_active() is False

    # A non-QUIT event should not stop the game.
    game_gui.running = True
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    game_gui.process_events([event])
    assert game_gui.running is True
    assert game_gui.get_program_active() is True

    # Only a left-click should be handled as a board click.
    game_gui.process_events([
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (0, 0)})
    ])
    assert game_gui.square_selected is None


def test_convert_piece_image_grid_to_pixels(game_gui):
    """Verify that board coordinates convert to pixel positions."""
    assert game_gui._convert_piece_image_grid_to_pixels((0, 0)) == (90, 230)
    assert game_gui._convert_piece_image_grid_to_pixels((5, 5)) == (340, 480)
    assert game_gui._convert_piece_image_grid_to_pixels((10, 10)) == (590, 730)


# Rendering tests.

def test_draw_window(game_gui):
    """Verify that the window scales the canvas to a larger display."""
    pygame.display.set_mode((game_gui.WIDTH * 2, game_gui.HEIGHT * 2))

    game_gui.draw_window()

    assert game_gui.canvas_scale == 2
    assert game_gui.canvas_offset == (0, 0)


def test_draw_canvas(game_gui):
    """Verify that drawing the canvas fills its background and board."""
    game_gui._draw_canvas()

    assert game_gui.canvas.get_size() == (game_gui.WIDTH, game_gui.HEIGHT)
    assert game_gui.canvas.get_at((0, 0))[:3] == (28, 44, 62)


def test_draw_turn_text(game_gui):
    """Verify that the correct turn image is drawn for each team."""
    class RecordingCanvas:
        def __init__(self):
            self.last_image = None
        def blit(self, image, position):
            self.last_image = image

    recording_canvas = RecordingCanvas()
    game_gui.canvas = recording_canvas
    game_gui.game_engine.turn = "offense"
    game_gui._draw_turn_text()
    assert recording_canvas.last_image is game_gui.offense_turn_display

    game_gui.game_engine.turn = "defense"
    game_gui._draw_turn_text()
    assert recording_canvas.last_image is game_gui.defense_turn_display


# Selection and move tests.

def test_select_square(game_gui):
    """Verify that a piece can be selected with its valid moves."""
    game_gui._select_square((0, 3))

    assert game_gui.square_selected == (0, 3)
    assert game_gui.square_selected_valid_moves == [
        (0, 2), (0, 1), (1, 3), (2, 3), (3, 3), (4, 3)
    ]


def test_select_square_errors(game_gui):
    """Verify that empty and opposing squares set the selection error."""
    game_gui._select_square((0, 0))
    assert game_gui.errors["no_piece_on_square"].get_active() is True
    assert game_gui.square_selected is None

    game_gui._reset_errors()
    game_gui._select_square((5, 5))
    assert game_gui.errors["no_piece_on_square"].get_active() is True
    assert game_gui.square_selected is None


def test_make_move(game_gui):
    """Verify that a valid move updates the board and clears selection."""
    game_gui._select_square((0, 3))
    game_gui._make_move((0, 2))

    assert game_gui.square_selected is None
    assert game_gui.square_selected_valid_moves == []
    assert game_gui.game_engine.get_board_square_value((0, 3)) is None
    assert game_gui.game_engine.get_board_square_value((0, 2)) == (
        "offense", "standard"
    )
    assert game_gui.game_engine.get_board_turn() == "defense"


def test_make_invalid_move(game_gui):
    """Verify that an invalid move sets an error without moving a piece."""
    game_gui._select_square((0, 3))
    game_gui._make_move((5, 5))

    assert game_gui.errors["invalid_move"].get_active() is True
    assert game_gui.square_selected == (0, 3)
    assert game_gui.game_engine.get_board_square_value((0, 3)) == (
        "offense", "standard"
    )


def test_handle_click(game_gui):
    """Verify that scaled window coordinates select the expected square."""
    game_gui.canvas_scale = 2
    game_gui.canvas_offset = (10, 20)
    board_x = game_gui.LEFT_GRID_OFFSET + (3 * game_gui.SQUARE_SIZE) + 1
    board_y = game_gui.TOP_GRID_OFFSET + 1

    game_gui._handle_click((10 + (board_x * 2), 20 + (board_y * 2)))

    assert game_gui.square_selected == (0, 3)


def test_handle_click_rejects_outside_board_and_game_over(game_gui):
    """Verify that outside-board and game-over clicks are ignored."""
    game_gui._handle_click((0, 0))
    assert game_gui.square_selected is None

    game_gui.game_engine.game_over = True
    board_x = game_gui.LEFT_GRID_OFFSET + (3 * game_gui.SQUARE_SIZE) + 1
    board_y = game_gui.TOP_GRID_OFFSET + 1
    game_gui._handle_click((board_x, board_y))
    assert game_gui.square_selected is None


def test_draw_selection(game_gui):
    """Verify that the selected square and possible moves are drawn."""
    blit_calls = []

    class RecordingCanvas:
        def blit(self, image, position):
            blit_calls.append((image, position))

    game_gui.canvas = RecordingCanvas()
    game_gui.square_selected = (0, 3)
    game_gui.square_selected_valid_moves = [(0, 2), (0, 1)]

    game_gui._draw_highlight_selected_square()
    game_gui._draw_possible_move_dots()

    assert blit_calls[0][0] is game_gui.select_square_highlight
    assert blit_calls[1][0] is game_gui.possible_move_dot
    assert blit_calls[2][0] is game_gui.possible_move_dot


def test_draw_errors(game_gui):
    """Verify that only active GUI errors are rendered and reset."""
    blit_calls = []

    class RecordingCanvas:
        def blit(self, image, position):
            blit_calls.append((image, position))

    game_gui.canvas = RecordingCanvas()
    game_gui.errors["invalid_move"].set_active(True)
    game_gui._draw_errors()

    assert len(blit_calls) == 1
    assert blit_calls[0][0] is game_gui.errors["invalid_move"].get_error_surface()

    game_gui._reset_errors()
    assert all(error.get_active() is False for error in game_gui.errors.values())


def test_draw_pieces_on_board(game_gui):
    """Verify that offense, defense, and king pieces are rendered."""
    blit_calls = []

    class RecordingCanvas:
        def blit(self, image, position):
            blit_calls.append((image, position))

    game_gui.canvas = RecordingCanvas()

    game_gui._draw_pieces_on_board()
    drawn_images = [image for image, _ in blit_calls]
    assert game_gui.offense_piece_image in drawn_images
    assert game_gui.defense_piece_image in drawn_images
    assert game_gui.king_piece_image in drawn_images

if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])

