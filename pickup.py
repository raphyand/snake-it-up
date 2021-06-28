"""Pickup module to handle growth and score bonuses for player"""
__author__ = 'Raphael S. Andaya'
__email__ = 'raphyand@csu.fullerton.edu'
__maintainer__ = 'raphyand'
import random
import pygame
from rgbcolors import green_yellow

class PickUp:
    """Pickup Class for points and growing"""
    def __init__(self, screen, background_color):
        """Pickup Initialization"""
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
        """Pickup: Get screen to render"""
        return self._screen_to_render

    def is_picked_up(self):
        """Pickup: return if it is picked up"""
        return self._picked_up

    def draw(self):
        """Pickup: Draw itself, and if picked up, disappear"""
        if self._picked_up is False:
            pygame.draw.rect(self.get_screen_to_render(), green_yellow, self._body)
        if self._picked_up is True:
            pygame.draw.rect(self.get_screen_to_render(), self._background_color, self._body)

    def add_to_score(self, score_counter):
        """Pickup: Add score to score counter"""
        score_counter.add_bonus(self._score_value)

    def detect_collision(self, player):
        """Pickup: Detect if player picks up pickup"""
        if self._body.colliderect(player.get_player()) and self._picked_up is False:
            self._picked_up = True
            player.spawn_tail()
