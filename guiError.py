import pygame
class GUIError:
    def __init__(self, error_message: str, font: pygame.font.Font, active:bool = False):
        error_message = error_message.strip()
        error_message = f" {error_message} "
        self.error: pygame.Surface = font.render(error_message, True, color= (0, 0, 0), bgcolor= (225, 45, 75))
        self.active: bool = active

    def get_error_surface(self) -> pygame.Surface:
        return self.error
    def get_active(self) -> bool:
        return self.active
    def set_active(self, status: bool) -> None:
        self.active = status
    
