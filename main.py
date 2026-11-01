import pygame
import pygame_gui
import pygbag
from gui import GameGUI
def main():
    gameGUI = GameGUI()
    clock = pygame.time.Clock()

    while gameGUI.running == True:
        pygame.event.get()
        gameGUI.draw_window()
        clock.tick(60)

if __name__ == "__main__":
    main()