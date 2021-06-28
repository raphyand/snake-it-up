"""Utilities module for enumerations of game states"""
__author__ = 'Raphael S. Andaya'
__email__ = 'raphyand@csu.fullerton.edu'
__maintainer__ = 'raphyand'

from enum import Enum
class GameState(Enum):
    """Game State Enumerations"""
    END_MENU = -1
    MAIN_MENU = 0
    PLAY_LEVEL = 1
    LEADER_BOARD = 2
