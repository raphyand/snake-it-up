"""Score module to handle score system for game."""
__author__ = 'Raphael S. Andaya'
__email__ = 'raphyand@csu.fullerton.edu'
__maintainer__ = 'raphyand'
import pygame

class Score:
    """Score base class to tally points"""
    def __init__(self):
        self._score = 0

    def add_bonus(self, bonus_points):
        """Score base class: to add points"""
        self._score += bonus_points

    def get_score(self):
        """Score base class: get score"""
        return self._score

# Every 3 seconds
class TimerScore(Score):
    """Timer Score Class to add score based on time"""
    def __init__(self, points_per_click=1, click_time_ms = 3000):
        """Timer Score Class: Initialization"""
        super().__init__()
        self._points_per_click = points_per_click
        self._click_time = click_time_ms
        self._last_time = pygame.time.get_ticks()
    def click(self):
        """Timer Score Class: Add every 3 seconds, one point"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self._last_time
        if elapsed > self._click_time:
            self._last_time = current_time
            self._score += self._points_per_click

    def elapsed_time(self):
        """Timer Score Class: Return time elapsed since
        playing"""
        counting = pygame.time.get_ticks()
        return counting / 1000
