import pygame


class GUIError:
    """Store a rendered GUI error message and its active state."""

    # Error surface creation.

    def __init__(self, error_message: str, font: pygame.font.Font, active:bool = False):
        """Create an error surface from a message and font."""
        error_message = error_message.strip()
        error_message = f" {error_message} "
        self.error: pygame.Surface = font.render(error_message, True, color= (0, 0, 0), bgcolor= (225, 45, 75))
        self.active: bool = active

    # Error state accessors.

    def get_error_surface(self) -> pygame.Surface:
        """Return the rendered error message surface."""
        return self.error

    def get_active(self) -> bool:
        """Return whether this error is currently active."""
        return self.active

    def set_active(self, status: bool) -> None:
        """Set whether this error should be displayed."""
        self.active = status
    
