import pygame
import pygame_gui
import pygbag
from gui import GameGUI
def main():
    gameGUI = GameGUI()
    clock = pygame.time.Clock()
    program_is_running = True
    while program_is_running == True:
        gameGUI.process_events(pygame.event.get())
        gameGUI.draw_window()
        clock.tick(60)
        program_is_running = gameGUI.get_program_active()

if __name__ == "__main__":
    main()