import pygame
from rgbcolors import green_yellow

class PickUp:
    def __init__(self, screen, background_color):
        self._screen_to_render = screen
        self._background_color = background_color
        self._dimension = (16, 16)
        self._location = (200, 200)
        self._body = pygame.Rect(self._location, self._dimension)
        self._picked_up = False
    
    def get_screen_to_render(self):
        return self._screen_to_render

    def draw(self):
        if self._picked_up is False:
            pygame.draw.rect(self.get_screen_to_render(), green_yellow, self._body)
        if self._picked_up is True:
            pygame.draw.rect(self.get_screen_to_render(), self._background_color, self._body)

    def detect_collision(self, player):
        if self._body.colliderect(player.get_player()) and self._picked_up is False:
            self._picked_up = True
            player.spawn_tail()
            #pygame.draw.rect(self._screen_to_render(), self._background_color, self._body)
            print("Collision!")