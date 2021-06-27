
import pygame
import rgbcolors
import random
import datetime
import pdb
import pickle
import os
from collections import namedtuple
from pickup import PickUp
from score import TimerScore
from utils import GameState
class Scene:
    def __init__(self, scene_id, screen, background_color=rgbcolors.springgreen1):
        self._id = scene_id
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._is_valid = True
        self._frame_rate = 60

    def draw(self):
        if self._screen:
            self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        if event.type == pygame.QUIT:
            print('Good bye!')
            self.set_not_valid()
            self._id = GameState.END_MENU
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_not_valid()
            self._id = GameState.END_MENU

    def is_valid(self):
        return self._is_valid

    def set_not_valid(self):
        self._is_valid = False

    def update(self):
        pass

    def start_scene(self):
        print('starting {}'.format(self))

    def end_scene(self):
        print('ending {}'.format(self))

    def frame_rate(self):
        return self._frame_rate

    def __str__(self):
        return 'Scene {}'.format(self._id)

    def get_game_state(self):
        return self._id

class TitleScene(Scene):
    def __init__(self, scene_id, screen, background_color, title, title_color, title_size):
        super().__init__(scene_id, screen, background_color)
        title_font = pygame.font.Font(pygame.font.get_default_font(), title_size)
        self._title = title_font.render(title, True, title_color)
        press_any_key_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self._press_any_key = press_any_key_font.render('Press any key to play. Press ESC to quit.', True, rgbcolors.black)
        (w, h) = self._screen.get_size()
        self._title_pos = self._title.get_rect(center=(w/2, h/3 - 100))
        self._press_any_key_pos = self._press_any_key.get_rect(center=(w/2, h * (3/4)))
      
    def draw_instructions(self):
        (w, h) = self._screen.get_size()
        self._instructions_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self._instructions = self._instructions_font.render("Instructions:", True, rgbcolors.black)
        self._instructions_pos = self._instructions.get_rect(center=(w/2, h/2 - 50))
        self._screen.blit(self._instructions, self._instructions_pos)

        self._instructions2_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self._instructions2 = self._instructions2_font.render("WASD to move up, left, down, right", True, rgbcolors.black)
        self._instructions2_pos = self._instructions2.get_rect(center=(w/2, h/2 - 20))
        self._screen.blit(self._instructions2, self._instructions2_pos)

        self._instructions3_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self._instructions3 = self._instructions3_font.render("Get the most points by surviving and gathering apples", True, rgbcolors.black)
        self._instructions3_pos = self._instructions3.get_rect(center=(w/2, h/2))
        self._screen.blit(self._instructions3, self._instructions3_pos) 

        self._instructions4_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self._instructions4 = self._instructions4_font.render("Eating an apple will make you grow", True, rgbcolors.black)
        self._instructions4_pos = self._instructions4.get_rect(center=(w/2, h/2 + 20))
        self._screen.blit(self._instructions4, self._instructions4_pos)               

        self._instructions5_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self._instructions5 = self._instructions5_font.render("Avoid the boundary, and your own body!", True, rgbcolors.black)
        self._instructions5_pos = self._instructions5.get_rect(center=(w/2, h/2 + 40))
        self._screen.blit(self._instructions5, self._instructions5_pos)  

    def draw(self):
        super().draw()
        self._screen.blit(self._title, self._title_pos)
        self._screen.blit(self._press_any_key, self._press_any_key_pos)
        self.draw_instructions()

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self.set_not_valid()

    def move_to_next_scene(self):
        if self._id is not GameState.END_MENU:
            return GameState.PLAY_LEVEL
        else:
            return GameState.END_MENU

class BlinkingTitle(TitleScene):
    def __init__(self, scene_id, screen, background_color, title, title_color, title_size):
        super().__init__(scene_id, screen, background_color, title, title_color, title_size)
        self._title_text = title
        self._title_size = title_size
        self._title_color = title_color
        self._title_color_complement = (255 - title_color[0], 255 - title_color[1], 255 - title_color[2])
        self._t = 0.0
        self._delta_t = 0.1

    def _interpolate(self):
        self._t += self._delta_t
        if self._t > 1.0 or self._t < 0.0:
            self._delta_t *= -1.0
        a = rgbcolors.mult_color((1.0 - self._t), self._title_color_complement)
        b = rgbcolors.mult_color((self._t), self._title_color)
        c = rgbcolors.sum_color(a, b)
        return c

    def draw(self):
        super().draw()
        title_font = pygame.font.Font(pygame.font.get_default_font(), self._title_size)
        title_color = self._interpolate()
        self._title = title_font.render(self._title_text, True, title_color)

        self._screen.blit(self._title, self._title_pos)


class LevelScene(Scene):
    def __init__(self, scene_id, screen, background_color, player):
        super().__init__(scene_id, screen, background_color)
        self._player = player
        self._score = TimerScore()
        self._background_color = background_color
        self._text = "Score: " + str(self._score.get_score())
        self._pickup_list = [PickUp(self._screen, background_color)]
        self._score_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        (w, h) = self._screen.get_size()
        self._score_display = self._score_font.render(self._text, True, rgbcolors.white)
        self._score_display_pos = self._score_display.get_rect(center=(w/2, h/16))
        self._boundaries = [    #Added 30 to original sizes; subtracted 30 from original positions
        pygame.Rect((0, -30), (800, 40) ), #Top Boundary (800, 10), (0, 0)
        pygame.Rect((-30, 0), (40, 800) ),  #Left Boundary
        pygame.Rect((0, 790),(800,40) ), #Bottom Boundary
        pygame.Rect((790, 0),(40, 800)) #Right Boundary 
        ]
        self._save_info = []

    def draw(self):
        super().draw()
        self._player.draw()
        self.draw_boundaries()
        self._screen.blit(self._score_display, self._score_display_pos)
        for pickup in self._pickup_list:
            pickup.draw()
        if self._player.dead is True:
            game_over_text = "Game Over!"
            (w, h) = self._screen.get_size()
            game_over_display = self._score_font.render(game_over_text, True, rgbcolors.white)
            game_over_pos = self._score_display.get_rect(center=(w/2, h/2))
            self._screen.blit(game_over_display, game_over_pos)

    def process_event(self, event):
        if event.type == pygame.QUIT:
            print('Good bye!')
            self.set_not_valid()
            self._id = GameState.END_MENU
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_not_valid()
            self._id = GameState.END_MENU
        if self._player.dead is False:
            self._player.process_events(event)
            for pickup in self._pickup_list:
                pickup.detect_collision(self._player)
            self.spawn_pickup()
        else:
            print("Game Over!")
            if event.type == pygame.KEYDOWN:
                self.set_not_valid()

    def spawn_pickup(self):
        for pickup in self._pickup_list:
            if pickup.is_picked_up():
                pickup.add_to_score(self._score)
                self._pickup_list.pop()
                self._pickup_list.append(PickUp(self._screen, self._background_color))
    
    def draw_boundaries(self):
        for boundary in self._boundaries:
            pygame.draw.rect(self._screen, rgbcolors.red, boundary)
        
    def collide_boundaries(self):
        for boundary in self._boundaries:
            if boundary.colliderect(self._player.get_player()):
                self._player.dead = True
        #print(self._player.get_player().top)
        #print(self._player.get_player().centery)
        if self._player.get_player().top < 15 or self._player.get_player().centery < 15:
            #pdb.set_trace()
            print("Boundary Top!")
            self._player.dead = True
        if self._player.get_player().left < 14 or self._player.get_player().centerx < 14:
            print("Boundary Left!")
            self._player.dead = True
        if self._player.get_player().right > 786 or self._player.get_player().centerx > 786:
            print("Boundary Right!")
            self._player.dead = True
        if self._player.get_player().bottom > 786 or self._player.get_player().centery > 786:
            print("Boundary Bottom!")
            self._player.dead = True

    def read_data(self):
        if not os.path.exists('record_data.pickle'):
            #open(filename, 'w').close()
            print("Record file does not exist")
        else:
            with open('record_data.pickle', 'rb') as fh:
                self._save_info = pickle.load(fh)
                #self._save_info.append(pickle.load(fh))
            print(self._save_info)

    def write_data(self):
        with open('record_data.pickle', 'wb') as fh:
            pickle.dump(self._save_info, fh, pickle.HIGHEST_PROTOCOL)

    def game_over_info(self):
        print("Game Over Info:")
        print("Score: " + str(self._score.get_score()))
        print(datetime.date.today())
        print(str(self._score.elapsed_time()) + " Seconds")
        score_data = self._score.get_score()
        date_data = datetime.date.today()
        time_data = self._score.elapsed_time()
        record = [score_data, date_data, time_data]
        self.read_data()
        self._save_info.append(record)
        self.write_data()
        
    def move_to_next_scene(self):
        if self._id is not GameState.END_MENU:
            return GameState.LEADER_BOARD
        else:
            return GameState.END_MENU

    
    def update(self):
        if self._player.dead is False:
            self.collide_boundaries()
            self._player.update()
            self._score.click()
            #elapsed_time = self._score.elapsed_time()
            self._text = "Score: " + str(self._score.get_score())
            self._score_display = self._score_font.render(self._text, True, rgbcolors.white)
            print(self._score.elapsed_time())
        else:
            game_over_text = "Game Over!"
            (w, h) = self._screen.get_size()
            game_over_display = self._score_font.render(game_over_text, True, rgbcolors.white)
            game_over_pos = self._score_display.get_rect(center=(w/2, h - 50))
            self._screen.blit(game_over_display, game_over_pos)
            if not self._save_info:
                self.game_over_info()
                

class LeaderBoardScene(Scene):
    def __init__(self, scene_id, screen, background_color, title, title_color, title_size):
        super().__init__(scene_id, screen, background_color)
        title_font = pygame.font.Font(pygame.font.get_default_font(), title_size)
        self._title = title_font.render(title, True, title_color)
        press_any_key_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self._press_any_key = press_any_key_font.render('Press ESC to quit. Press any key to play again.', True, rgbcolors.black)
        (w, h) = self._screen.get_size()
        self._title_pos = self._title.get_rect(center=(w/2, h/10))
        self._press_any_key_pos = self._press_any_key.get_rect(center=(w/2, h - 50))
        self.record_font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.record_display = self.record_font.render("_____________________________________", True, rgbcolors.black)
        self.record_pos = self.record_display.get_rect(center=(w/2, h/6))
        self._save_info = []
        self.has_drawn = False
        self._display_list = []
        self._padding_value = 30

    def draw(self):
        super().draw()
        self._screen.blit(self._title, self._title_pos)
        self._screen.blit(self._press_any_key, self._press_any_key_pos)
        self._screen.blit(self.record_display, self.record_pos)
        #self.leaderboard()
        #self.draw_records("Fuck")
        if self.has_drawn is False:
            #self.draw_records("FuckToo")
            self.leaderboard()
            self.has_drawn = True
        else:
            self.draw_records()

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self.set_not_valid()

    def leaderboard(self):
        self.read_data() 
        for record in self._save_info:
            for index in record:
                #print(index)
                self.load_records(str(index))
                #for attr in index:
                    #print(attr)
                    #self.load_records(str(attr))

    def move_to_next_scene(self):
        if self._id is not GameState.END_MENU:
            return GameState.PLAY_LEVEL
        else:
            return GameState.END_MENU  

    def load_records(self, record):
        (w, h) = self._screen.get_size()
        record_font = pygame.font.Font(pygame.font.get_default_font(), 24)
        record_display = record_font.render(record, True, rgbcolors.black)
        record_pos = record_display.get_rect(center=(w/2, h/6 + self._padding_value))
        instance = [record_font, record_display, record_pos, self._padding_value]
        self._display_list.append(instance)
        self._padding_value = self._padding_value + 30
        #self._screen.blit(record_display, record_pos)
        
    def draw_records(self):
        for record in self._display_list:
            self._screen.blit(record[1], record[2])

    def read_data(self):
        if not os.path.exists('record_data.pickle'):
        #open(filename, 'w').close()
            print("Record file does not exist")
        else:
            with open('record_data.pickle', 'rb') as fh:
                #self._save_info = pickle.load(fh)
                self._save_info.append(pickle.load(fh))
            print(self._save_info)

