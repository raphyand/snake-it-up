"""Player Module to handle all things related to the Player"""
__author__ = 'Raphael S. Andaya'
__email__ = 'raphyand@csu.fullerton.edu'
__maintainer__ = 'raphyand'
import time
import pygame
#from pygame.locals import *

class Body:
    """Body Base Class for Player"""
    def __init__(self, screen, background_color):
        """Body Initialization"""
        self._screen_to_render = screen
        self._background_color = background_color
        self._current_direction = None
        self._next_direction = None
        self._is_tail = True

    def get_screen_to_render(self):
        """Body return screen that will be rendering"""
        return self._screen_to_render

    def get_background_color(self):
        """Body to get background color"""
        return self._background_color

    def get_current_direction(self):
        """Body to get current direction"""
        return self._current_direction

    def get_next_direction(self):
        """Body to return next direction"""
        return self._next_direction

    def get_tail(self):
        """Body to get tail"""
        return self._is_tail

    def set_current_direction(self, current_direction):
        """Body: set current direction"""
        self._current_direction = current_direction

    def set_next_direction(self, next_direction):
        """Body: set next direction"""
        self._next_direction = next_direction

    def set_tail(self, is_tail):
        """Body: set tail"""
        self._is_tail = is_tail

    #def update(self):
    #    """Body: update self """
    #    pygame.display.update()

class Player(Body):
    """Player subclass of Body"""
    def __init__(self, screen, background_color, is_head):
        """Player subclass: Initialization"""
        super().__init__(screen, background_color)
        self._dimension = (32, 32)
        self._direction = (0,0)
        self._previous_event = None
        self._previous_key = None
        self._body_list = [pygame.Rect((400, 400), self._dimension)]
        self._speed = 35
        self._click_time = 1
        self._last_time = pygame.time.get_ticks()
        self._time_btw_moves = 500
        self._is_head = is_head
        self._player = self._body_list[0]
        self._repeat_move = 0
        self._direction = None
        self.dead = False

    def get_player(self):
        """Player subclass: get current player head"""
        return self._player

    def get_previous_key(self):
        """Player subclass: get previous key pushed"""
        return self._previous_key

    def get_previous_event(self):
        """Player subclass: get previous event
        that occurred"""
        return self._previous_event

    def get_speed(self):
        """Player subclass: get speed"""
        return self._speed

    def get_is_head(self):
        """Player subclass: check if
        current player is head"""
        return self._is_head

    def get_body_list(self):
        """Player subclass: get body list"""
        return self._body_list

    def is_dead(self):
        """Player subclass: check if dead"""
        return self.dead

    def set_player(self, player):
        """Player subclass: set current player"""
        self._player = player

    def set_previous_key(self, key):
        """Player subclass: set previous key"""
        self._previous_key = key

    def set_previous_event(self, event):
        """Player subclass: set previous event"""
        self._previous_event = event

    def set_speed(self, speed):
        """Player subclass: set speed"""
        self._speed = speed

    def set_is_head(self, is_head):
        """Player subclass: set current head"""
        self._is_head = is_head

    def process_events(self, event):
        """Player subclass: process events of player"""
        pygame.event.clear()
        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.KEYUP, pygame.TEXTINPUT])

        if event is None:
            print("None")
        if event.type == pygame.KEYDOWN and event.type != self.get_previous_key():
            pygame.event.clear()
            if (event.key == pygame.K_w and self.get_previous_key() != pygame.K_s
            and self.get_previous_key() != pygame.K_w):
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                self._repeat_move = 0
                self._direction = "Up"
                self.move_up()
            elif (event.key == pygame.K_a and self.get_previous_key() != pygame.K_d
            and self.get_previous_key() != pygame.K_a):
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                self._repeat_move = 0
                self._direction = "Left"
                self.move_left()
            elif (event.key == pygame.K_s and self.get_previous_key() != pygame.K_w
            and self.get_previous_key() != pygame.K_s):
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                self._repeat_move = 0
                self._direction = "Down"
                self.move_down()
            elif (event.key == pygame.K_d and self.get_previous_key() != pygame.K_a
            and self.get_previous_key() != pygame.K_d):
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                self._repeat_move = 0
                self._direction = "Right"
                self.move_right()
            time.sleep(.001)
            if self.get_previous_key() == pygame.K_w and self.get_previous_key() != pygame.K_s:
                pygame.event.clear()
                pygame.time.set_timer(self.get_previous_event(), self._time_btw_moves, True)
                self.move_up()
            elif self.get_previous_key() == pygame.K_a and self.get_previous_key() != pygame.K_d:
                pygame.event.clear()
                pygame.time.set_timer(self.get_previous_event(), self._time_btw_moves, True)
                self.move_left()
            elif self.get_previous_key() == pygame.K_s and self.get_previous_key() != pygame.K_w:
                pygame.event.clear()
                pygame.time.set_timer(self.get_previous_event(), self._time_btw_moves, True)
                self.move_down()
            elif self.get_previous_key() == pygame.K_d and self.get_previous_key() != pygame.K_a:
                pygame.event.clear()
                pygame.time.set_timer(self.get_previous_event(), self._time_btw_moves, True)
                self.move_right()
            pygame.event.clear()

    def _self_collision(self):
        """Player subclass: check if collision
        occurs in long body"""
        head = self._body_list[0]
        tail_list = self._body_list[3:]
        for part in tail_list:
            if part.colliderect(head):
                #print("Hit self!")
                self.dead = True


    def update(self):
        """Player subclass: update to
        check for collision with self"""
        self._self_collision()

    # Draw cyan for now
    # You update THEN draw
    # don't draw, THEN update
    def draw(self):
        """Player subclass: draw each part of the body"""
        for part in self._body_list:
            pygame.draw.rect(self.get_screen_to_render(), (0, 255, 255), part)

    def spawn_tail(self):
        """Player subclass: spawn a tail"""
        new_body_part = None
        if self._direction == "Up":
            new_body_part = (self.get_player().move(0, -1 * self.get_speed())) #64
        elif self._direction == "Left":
            new_body_part = (self.get_player().move(-1 * self.get_speed(), 0))
        elif self._direction == "Down":
            new_body_part = (self.get_player().move(0, self.get_speed()))
        elif self._direction == "Right":
            new_body_part = (self.get_player().move(self.get_speed(), 0))
        self._body_list.insert(0, new_body_part)
        self.set_player(self._body_list[0])

    def move_up(self):
        """Player subclass: pop from tail and add to front
        in order to move up"""
        player = self._body_list[0]
        pygame.display.update(player)
        new_position = (player.move(0, -1 * self.get_speed()))
        self._body_list.insert(0, new_position)
        pygame.draw.rect(self.get_screen_to_render(),
        super().get_background_color(), self._body_list[-1])
        self._body_list.pop()
        self.set_player(player)

    def move_left(self):
        """Player subclass: pop from tail and add to front
        in order to move up"""
        player = self._body_list[0]
        pygame.display.update(player)
        new_position = (player.move(-1 * self.get_speed(), 0))
        self._body_list.insert(0, new_position)
        pygame.draw.rect(self.get_screen_to_render(),
        super().get_background_color(), self._body_list[-1])
        self._body_list.pop()
        self.set_player(player)

    def move_down(self):
        """Player subclass: pop from tail and add to front
        in order to move down"""
        player = self._body_list[0]
        pygame.display.update(player)
        new_position = (player.move(0, 1 * self.get_speed()))
        self._body_list.insert(0, new_position)
        pygame.draw.rect(self.get_screen_to_render(),
        super().get_background_color(), self._body_list[-1])
        self._body_list.pop()
        self.set_player(player)

    def move_right(self):
        """Player subclass: pop from tail and add to front
        in order to move right"""
        player = self._body_list[0]
        pygame.display.update(player)
        new_position = (player.move(self.get_speed(), 0))
        self._body_list.insert(0, new_position)
        pygame.draw.rect(self.get_screen_to_render(),
        super().get_background_color(), self._body_list[-1])
        self._body_list.pop()
        self.set_player(player)

    def _print_info(self):
        """Player subclass: print information
        about player locale and size"""
        player = self.get_player()
        print("Center: ", player.center)
        print("Top: \t", player.left)
        print("Left: \t", player.bottom)
        print("Right: \t", player.right)
        print("Size: \t", player.size)
