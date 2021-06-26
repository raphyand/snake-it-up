import pygame
import random
from rgbcolors import green_yellow, purple1

class PickUp:
    def __init__(self, screen, background_color):
        self._screen_to_render = screen
        self._background_color = background_color
        self._dimension = (16, 16)
        self._x_locale = random.randrange(50, 750)
        self._y_locale = random.randrange(50, 750)
        self._location = (self._x_locale, self._y_locale)
        self._body = pygame.Rect(self._location, self._dimension)
        self._picked_up = False
        self._score_value = 5

    def get_screen_to_render(self):
        return self._screen_to_render

    def is_picked_up(self):
        return self._picked_up
    
    def draw(self):
        if self._picked_up is False:
            pygame.draw.rect(self.get_screen_to_render(), green_yellow, self._body)
        if self._picked_up is True:
            pygame.draw.rect(self.get_screen_to_render(), self._background_color, self._body)

    def add_to_score(self, score_counter):
        score_counter.add_bonus(self._score_value)

    def detect_collision(self, player):
        if self._body.colliderect(player.get_player()) and self._picked_up is False:
            self._picked_up = True
            player.spawn_tail()
            #pygame.draw.rect(self._screen_to_render(), self._background_color, self._body)
            print("Collision!")
        #if self._body.collidelist(player.get_body_list()) and self._picked_up is False:
        #    self._picked_up = True