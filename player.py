import pygame
import time
import pdb
import rgbcolors
from pygame.locals import *

class Body: 
    def __init__(self, screen, background_color):
        self._screen_to_render = screen
        self._background_color = background_color
        self._current_direction = None
        self._next_direction = None
        self._is_tail = True

    def get_screen_to_render(self):
        return self._screen_to_render

    def get_background_color(self):
        return self._background_color

    def get_current_direction(self):
        return self._current_direction
    
    def get_next_direction(self):
        return self._next_direction

    def get_tail(self):
        return self._is_tail

    def set_current_direction(self, current_direction):
        self._current_direction = current_direction

    def set_next_direction(self, next_direction):
        self._next_direction = next_direction

    def set_tail(self, is_tail):
        self._is_tail = is_tail

    #def draw(self):
    #   pygame.draw.rect(self.get_screen_to_render(), (0, 255, 255), pygame.Rect(self.get_rect_bounds()))

    def update(self):
        pygame.display.update()

# Optimize 10 percent of the code that takes 90% of the time
class Player(Body):
    def __init__(self, screen, background_color, is_head): 
        super().__init__(screen, background_color)
        #self._player = pygame.Rect(rect)
        self._dimension = (32, 32)
        self._direction = (0,0)
        self._previous_event = None
        self._previous_key = None
        self._body_list = [pygame.Rect((400, 400), self._dimension)]
        self._speed = 35#17 #33
        self._click_time = 1
        self._last_time = pygame.time.get_ticks()
        self._time_btw_moves = 500
        self._is_head = is_head
        self._player = self._body_list[0]
        self._repeat_move = 0
        self._direction = None
        self.dead = False
       # self._avatar = [pygame.Rect(400,400) self._dimension)]

    def get_player(self):
        return self._player

    def get_previous_key(self):
        return self._previous_key

    def get_previous_event(self):
        return self._previous_event

    def get_speed(self):
        return self._speed

    def get_is_head(self):
        return self._is_head

    def get_body_list(self):
        return self._body_list

    def is_dead(self):
        return self.dead

    def set_player(self, player):
        self._player = player

    def set_previous_key(self, key):
        self._previous_key = key

    def set_previous_event(self, event):
        self._previous_event = event

    def set_speed(self, speed):
        self._speed = speed

    def set_is_head(self, is_head):
        self._is_head = is_head

    def process_events(self, event):
        pygame.event.clear()
        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.KEYUP, pygame.TEXTINPUT])

        #print(event)
        if event == None:
            print("None")
        if event.type == pygame.KEYDOWN and event.type != self.get_previous_key():
            pygame.event.clear()
            if event.key == pygame.K_w and self.get_previous_key() != pygame.K_s and self.get_previous_key() != pygame.K_w:
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                self._repeat_move = 0
                self._direction = "Up"
                self.move_up()
            elif event.key == pygame.K_a and self.get_previous_key() != pygame.K_d and self.get_previous_key() != pygame.K_a:
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                self._repeat_move = 0
                self._direction = "Left"
                self.move_left()
            elif event.key == pygame.K_s and self.get_previous_key() != pygame.K_w and self.get_previous_key() != pygame.K_s:
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                self._repeat_move = 0
                self._direction = "Down"
                self.move_down()
            elif event.key == pygame.K_d and self.get_previous_key() != pygame.K_a and self.get_previous_key() != pygame.K_d:
                self.set_previous_key(event.key)
                self.set_previous_event(event)
                self._repeat_move = 0
                self._direction = "Right"
                self.move_right()
            #elif event.key == pygame.K_q:
            #    self.spawn_tail()
                #print("Spawn tail")
            time.sleep(.001)
            # Block to continue moving in one direction after
            # pressing the move button once.
            if self.get_previous_key() == pygame.K_w and self.get_previous_key() != pygame.K_s: #and self._repeat_move < 2:
                pygame.event.clear()
                pygame.time.set_timer(self.get_previous_event(), self._time_btw_moves, True)
                #self._repeat_move = self._repeat_move + 1
                self.move_up()
            elif self.get_previous_key() == pygame.K_a and self.get_previous_key() != pygame.K_d:# and self._repeat_move < 2:
                pygame.event.clear()
                pygame.time.set_timer(self.get_previous_event(), self._time_btw_moves, True)
                #self._repeat_move = self._repeat_move + 1
                self.move_left()           
            elif self.get_previous_key() == pygame.K_s and self.get_previous_key() != pygame.K_w:# and self._repeat_move < 2:
                pygame.event.clear()
                pygame.time.set_timer(self.get_previous_event(), self._time_btw_moves, True)
                #self._repeat_move = self._repeat_move + 1
                self.move_down()
            elif self.get_previous_key() == pygame.K_d and self.get_previous_key() != pygame.K_a:# and self._repeat_move < 2:
                pygame.event.clear()
                pygame.time.set_timer(self.get_previous_event(), self._time_btw_moves, True)
                #self._repeat_move = self._repeat_move + 1
                self.move_right()
            pygame.event.clear()

    def self_collision(self):
        head = self._body_list[0]
        tail_list = self._body_list[3:]
        for part in tail_list:
            if part.colliderect(head):
                #print("Hit self!")
                self.dead = True


    def update(self):
        self.self_collision()

    # Draw cyan for now
    # You update THEN draw
    # don't draw, THEN update
    def draw(self):
        for part in self._body_list:
            pygame.draw.rect(self.get_screen_to_render(), (0, 255, 255), part)
            #pygame.display.update()

    def spawn_tail(self):
        print("Spawn Tail")
        new_body_part = None
        if self._direction == "Up":
            new_body_part = (self.get_player().move(0, -1 * self.get_speed())) #64
            #self.set_player(self._body_list[0])
            #self.move_up()
        elif self._direction == "Left":
            new_body_part = (self.get_player().move(-1 * self.get_speed(), 0))
            #self.set_player(self._body_list[0])
            #self.move_left()
        elif self._direction == "Down":
            new_body_part = (self.get_player().move(0, self.get_speed()))
            #self.set_player(self._body_list[0])
            #self.move_down()
        elif self._direction == "Right":
            new_body_part = (self.get_player().move(self.get_speed(), 0))
            #self.set_player(self._body_list[0])
            #self.move_right()

        self._body_list.insert(0, new_body_part)
        self.set_player(self._body_list[0])

    def move_up(self):
        player = self._body_list[0]
        pygame.display.update(player)
        new_position = (player.move(0, -1 * self.get_speed()))
        self._body_list.insert(0, new_position)
        pygame.draw.rect(self.get_screen_to_render(), super().get_background_color(), self._body_list[-1]) #Draw the ground after the last bodypart
        self._body_list.pop()
        self.set_player(player)

    def move_left(self):
        player = self._body_list[0]
        pygame.display.update(player)
        new_position = (player.move(-1 * self.get_speed(), 0))
        self._body_list.insert(0, new_position)
        pygame.draw.rect(self.get_screen_to_render(), super().get_background_color(), self._body_list[-1]) #Draw the ground after the last bodypart
        self._body_list.pop()
        self.set_player(player)

    def move_down(self):
        player = self._body_list[0]
        pygame.display.update(player)
        new_position = (player.move(0, 1 * self.get_speed()))
        self._body_list.insert(0, new_position)
        pygame.draw.rect(self.get_screen_to_render(), super().get_background_color(), self._body_list[-1]) #Draw the ground after the last bodypart
        self._body_list.pop()
        self.set_player(player)       

    def move_right(self):
        player = self._body_list[0]
        pygame.display.update(player)
        new_position = (player.move(self.get_speed(), 0))
        self._body_list.insert(0, new_position)
        pygame.draw.rect(self.get_screen_to_render(), super().get_background_color(), self._body_list[-1]) #Draw the ground after the last bodypart
        self._body_list.pop()
        self.set_player(player)        

    def print_info(self):
        player = self.get_player()
        print("Center: ", player.center)
        print("Top: \t", player.left)
        print("Left: \t", player.bottom)
        print("Right: \t", player.right)
        print("Size: \t", player.size)
