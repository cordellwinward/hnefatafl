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

if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])

