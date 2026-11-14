import os

# Prevent tests from opening a real window.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
import pytest

from gui import GameGUI


@pytest.fixture
def game_gui():
    pygame.init()
    gui = GameGUI()
    yield gui
    pygame.quit()


def test_game_gui_init(game_gui):
    assert isinstance(game_gui.window, pygame.Surface)
    assert isinstance(game_gui.canvas, pygame.Surface)
    assert game_gui.running is True


def test_get_program_active(game_gui):
    assert game_gui.get_program_active() is True


def test_process_events(game_gui):
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


def test_convert_piece_image_grid_to_pixels(game_gui):
    assert game_gui._convert_piece_image_grid_to_pixels((0, 0)) == (90, 230)
    assert game_gui._convert_piece_image_grid_to_pixels((5, 5)) == (340, 480)
    assert game_gui._convert_piece_image_grid_to_pixels((10, 10)) == (590, 730)


def test_draw_window(game_gui):
    pygame.display.set_mode((game_gui.WIDTH * 2, game_gui.HEIGHT * 2))

    game_gui.draw_window()

    assert game_gui.canvas_scale == 2
    assert game_gui.canvas_offset == (0, 0)


def test_draw_canvas(game_gui):
    game_gui._draw_canvas()

    assert game_gui.canvas.get_size() == (game_gui.WIDTH, game_gui.HEIGHT)
    assert game_gui.canvas.get_at((0, 0))[:3] == (28, 44, 62)


def test_draw_turn_text(game_gui):
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


def test_draw_pieces_on_board(game_gui):
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

