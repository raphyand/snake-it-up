import pygame
from rgbcolors import green_yellow

class PickUp:
    def __init__(self, screen, background_color):
        self._screen_to_render = screen
        self._background_color = background_color
        self._dimension = (16, 16)
        self._body = pygame.Rect((200,200), self._dimension)
    
    def get_screen_to_render(self):
        return self._screen_to_render

    def draw(self):
        pygame.draw.rect(self.get_screen_to_render(), green_yellow, self._body)