import pygame
import time
import pdb
import rgbcolors
from pygame.locals import *

# Optimize 10 percent of the code that takes 90% of the time
class Player:
    def __init__(self, screen, rect , background_color):    
        self._screen_to_render = screen
        self._player_bounds = rect
        self._player = pygame.Rect(rect)
        self._background_color = background_color
        self._previous_event = None
        self._previous_key = None
        self._body_list = [self._player]
        self._speed = 2


    def get_screen_to_render(self):
        return self._screen_to_render

    def get_player_bounds(self):
        return self._player_bounds

    def get_player(self):
        return self._player
    
    def get_background_color(self):
        return self._background_color

    def get_previous_key(self):
        return self._previous_key

    def get_previous_event(self):
        return self._previous_event

    def get_speed(self):
        return self._speed

    def set_player(self, player):
        self._player = player

    def set_previous_key(self, key):
        self._previous_key = key

    def set_previous_event(self, event):
        self._previous_event = event

    def set_speed(self, speed):
        self._speed = speed

    def add_tail(self, event):
        pass

    def process_events(self, event):
        pygame.event.clear()
        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.KEYUP])
        if event == None:
            print("None")
        if event.type == pygame.KEYDOWN:
            #print("A key has been pressed.")
            #self.set_previous_key(event.key)
            #self.set_previous_event(event)
            if event.key == pygame.K_w:
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                #print("Move up")
                self.move_up()
            if event.key == pygame.K_a:
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                #print("Move left")
                self.move_left()
            if event.key == pygame.K_s:
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                #print("Move down")
                self.move_down()
            if event.key == pygame.K_d:
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                #print("Move right")
                self.move_right()
            if event.key == pygame.K_q:
                self.spawn_tail()
                #print("Spawn tail")
            time.sleep(.001)

        # Block to continue moving in one direction after
        # pressing the move button once.
        if self.get_previous_key() == pygame.K_w:
            pygame.event.post(self.get_previous_event())
            self.move_up()
        
        if self.get_previous_key() == pygame.K_a:
            pygame.event.post(self.get_previous_event())
            self.move_left()

        if self.get_previous_key() == pygame.K_s:
            pygame.event.post(self.get_previous_event())
            self.move_down()

        if self.get_previous_key() == pygame.K_d:
            pygame.event.post(self.get_previous_event())
            self.move_right()

    # Draw cyan for now
    # You update THEN draw
    # don't draw, THEN update
    def draw(self):
        pygame.draw.rect(self.get_screen_to_render(), (0, 255, 255), self.get_player())
        pygame.display.update()

    def spawn_tail(self):
        print("Spawn Tail")
        pygame.draw.rect(self.get_screen_to_render(), (255, 0, 255), self.get_screen_to_render())

    
    def move_up(self):
        player = self.get_player()
        #delete_player = pygame.Rect((self.get_screen_to_render, (0, 0, 0), player.get_player_bounds))
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.set_player(player.move(0, -1 * self.get_speed()))
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        #self.print_info()
        pygame.display.update(player)

    def move_left(self):
        player = self.get_player()
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.set_player(player.move(-1 * self.get_speed(), 0))
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        #self.print_info()
        pygame.display.update(player)    

    def move_down(self):
        player = self.get_player()
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.set_player(player.move(0, self.get_speed()))
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        #self.print_info()
        pygame.display.update(player)    

    def move_right(self):
        player = self.get_player()
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        self.set_player(player.move(self.get_speed(), 0))
        pygame.draw.rect(self.get_screen_to_render(), self.get_background_color(), player)
        #self.print_info()
        pygame.display.update(player)           

    def print_info(self):
        player = self.get_player()
        print("Center: ", player.center)
        print("Top: \t", player.left)
        print("Left: \t", player.bottom)
        print("Right: \t", player.right)
        print("Size: \t", player.size)
