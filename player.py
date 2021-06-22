import pygame
from pygame.locals import *

class Player:
    def __init__(self, _screen, _rect ):
        self._screen_to_render = _screen
        self._player_bounds = _rect
        self._player = pygame.Rect(_rect)
        

    def get_screen_to_render(self):
        return self._screen_to_render

    def get_player_bounds(self):
        return self._player_bounds

    def get_player(self):
        return self._player
    
    def set_player(self, player):
        self._player = player

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            print("A key has been pressed.")
            if event.key == pygame.K_w:
                print("Move up")
                self.move_up()
            if event.key == pygame.K_a:
                print("Move left")
                #self.move()
            if event.key == pygame.K_s:
                print("Move down")
                #self.move()
            if event.key == pygame.K_d:
                print("Move right")
                #self.move()


    # Draw cyan for now
    def draw(self):
        pygame.draw.rect(self.get_screen_to_render(), (0, 255, 255), self.get_player())
        pygame.display.update()

    def move_up(self):
        player = self.get_player()
        #delete_player = pygame.Rect((self.get_screen_to_render, (0, 0, 0), player.get_player_bounds))
        self.set_player(player.move(0, -10))
        pygame.draw.rect(self.get_screen_to_render(), (0, 0, 0), player)
        self.print_info()
        pygame.display.update()

    def print_info(self):
        player = self.get_player()
        print("Center: ", player.center)
        print("Top: \t", player.left)
        print("Left: \t", player.bottom)
        print("Right: \t", player.right)
        print("Size: \t", player.size)
