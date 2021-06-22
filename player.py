import pygame
from pygame.locals import *

class Player:
    def __init__(self, screen, rect , background_color):
        self._screen_to_render = screen
        self._player_bounds = rect
        self._player = pygame.Rect(rect)
        self._background_color = background_color

    def get_screen_to_render(self):
        return self._screen_to_render

    def get_player_bounds(self):
        return self._player_bounds

    def get_player(self):
        return self._player
    
    def get_background_color(self):
        return self._background_color

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
                self.move_left()
            if event.key == pygame.K_s:
                print("Move down")
                self.move_down()
            if event.key == pygame.K_d:
                print("Move right")
                self.move_right()

    # Draw cyan for now
    def draw(self):
        pygame.draw.rect(self.get_screen_to_render(), (0, 255, 255), self.get_player())
        pygame.display.update()

    def move_up(self):
        player = self.get_player()
        #delete_player = pygame.Rect((self.get_screen_to_render, (0, 0, 0), player.get_player_bounds))
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.set_player(player.move(0, -10))
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.print_info()
        pygame.display.update()

    def move_left(self):
        player = self.get_player()
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.set_player(player.move(-10, 0))
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.print_info()
        pygame.display.update()    

    def move_down(self):
        player = self.get_player()
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.set_player(player.move(0, 10))
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.print_info()
        pygame.display.update()    

    def move_right(self):
        player = self.get_player()
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.set_player(player.move(10, 0))
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.print_info()
        pygame.display.update()           


    def print_info(self):
        player = self.get_player()
        print("Center: ", player.center)
        print("Top: \t", player.left)
        print("Left: \t", player.bottom)
        print("Right: \t", player.right)
        print("Size: \t", player.size)
