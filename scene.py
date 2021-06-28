"""Utilties module for enumerations of AI behavior and game states"""
__author__ = 'Raphael S. Andaya'
__email__ = 'raphyand@csu.fullerton.edu'
__maintainer__ = 'raphyand'

import datetime
import pickle
import os
import pygame
import rgbcolors
from pickup import PickUp
from score import TimerScore
from utils import GameState
class Scene:
    """Base Scene Class"""
    def __init__(self, scene_id, screen, background_color=rgbcolors.springgreen1):
        """Base Scene Class Init"""
        self._id = scene_id
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._is_valid = True
        self._frame_rate = 60

    def draw(self):
        """Base Scene Class Draw"""
        if self._screen:
            self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Base Scene Class Event Processing: press ESC
            to end current scene. """
        if event.type == pygame.QUIT:
            print('Good bye!')
            self.set_not_valid()
            self._id = GameState.END_MENU
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_not_valid()
            self._id = GameState.END_MENU

    def is_valid(self):
        """Base Scene Class return validity of scene"""
        return self._is_valid

    def set_not_valid(self):
        """Base Scene Class to set invalidity"""
        self._is_valid = False

    def update(self):
        """Base Scene Class Update to establish update function"""
        pass

    def start_scene(self):
        """Base Scene Class print string for starting scene"""
        print('starting {}'.format(self))

    def end_scene(self):
        """Base Scene Class print string for ending scene"""
        print('ending {}'.format(self))

    def frame_rate(self):
        """Base Scene Class frame rate"""
        return self._frame_rate

    def __str__(self):
        """Base Scene Class string"""
        return 'Scene {}'.format(self._id)

    def get_game_state(self):
        """Base Scene Class Game State handler"""
        return self._id

class TitleScene(Scene):
    """Title Scene Subclass"""
    def __init__(self, scene_id, screen, background_color, title, title_color, title_size):
        """Title Scene Subclass Initiation"""
        super().__init__(scene_id, screen, background_color)
        title_font = pygame.font.Font(pygame.font.get_default_font(), title_size)
        self._title = title_font.render(title, True, title_color)
        press_any_key_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self._press_any_key = press_any_key_font.render(
            'Press any key to play. Press ESC to quit.', True, rgbcolors.black)
        (_w, _h) = self._screen.get_size()
        self._title_pos = self._title.get_rect(center=(_w/2, _h/3 - 100))
        self._press_any_key_pos = self._press_any_key.get_rect(center=(_w/2, _h * (3/4)))

    def draw_instructions(self):
        """Title Scene Subclass: Draw instructions of the game"""
        (_w, _h) = self._screen.get_size()
        instructions_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        instructions = instructions_font.render("Instructions:", True, rgbcolors.black)
        instructions_pos = instructions.get_rect(center=(_w/2, _h/2 - 50))
        self._screen.blit(instructions, instructions_pos)

        instructions2_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        instructions2 = instructions2_font.render(
            "WASD to move up, left, down, right", True, rgbcolors.black)
        instructions2_pos = instructions2.get_rect(center=(_w/2, _h/2 - 20))
        self._screen.blit(instructions2, instructions2_pos)

        instructions3_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        instructions3 = instructions3_font.render(
            "Get the most points by surviving and gathering apples", True, rgbcolors.black)
        instructions3_pos = instructions3.get_rect(center=(_w/2, _h/2))
        self._screen.blit(instructions3, instructions3_pos)

        instructions4_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        instructions4 = instructions4_font.render(
            "Eating an apple will make you grow", True, rgbcolors.black)
        instructions4_pos = instructions4.get_rect(center=(_w/2, _h/2 + 20))
        self._screen.blit(instructions4, instructions4_pos)

        instructions5_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        instructions5 = instructions5_font.render(
            "Avoid the boundary, and your own body!", True, rgbcolors.black)
        instructions5_pos = instructions5.get_rect(center=(_w/2, _h/2 + 40))
        self._screen.blit(instructions5, instructions5_pos)

    def draw(self):
        """Title Scene Subclass Draw all parts of scene"""
        super().draw()
        self._screen.blit(self._title, self._title_pos)
        self._screen.blit(self._press_any_key, self._press_any_key_pos)
        self.draw_instructions()

    def process_event(self, event):
        """Title Scene Subclass process all events."""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self.set_not_valid()

    def move_to_next_scene(self):
        """Title Scene Subclass move to next scene upon id change"""
        if self._id is not GameState.END_MENU:
            return GameState.PLAY_LEVEL
        else:
            return GameState.END_MENU

class LevelScene(Scene):
    """Level Scene Subclass"""
    def __init__(self, scene_id, screen, background_color, player):
        """Level Scene Subclass Initialization"""
        super().__init__(scene_id, screen, background_color)
        self._player = player
        self._score = TimerScore()
        self._background_color = background_color
        self._text = "Score: " + str(self._score.get_score())
        self._pickup_list = [PickUp(self._screen, background_color)]
        self._score_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        (_w, _h) = self._screen.get_size()
        self._score_display = self._score_font.render(self._text, True, rgbcolors.white)
        self._score_display_pos = self._score_display.get_rect(center=(_w/2, _h/16))
        self._boundaries = [    #Added 30 to original sizes; subtracted 30 from original positions
        pygame.Rect((0, -30), (800, 40) ), #Top Boundary (800, 10), (0, 0)
        pygame.Rect((-30, 0), (40, 800) ),  #Left Boundary
        pygame.Rect((0, 790),(800,40) ), #Bottom Boundary
        pygame.Rect((790, 0),(40, 800)) #Right Boundary
        ]
        self._save_info = []

    def draw(self):
        """Level Scene Subclass Draw all parts of scene, including
        player and pickups"""
        super().draw()
        self._player.draw()
        self.draw_boundaries()
        self._screen.blit(self._score_display, self._score_display_pos)
        for pickup in self._pickup_list:
            pickup.draw()
        if self._player.dead is True:
            game_over_text = "Game Over!"
            (_w, _h) = self._screen.get_size()
            game_over_display = self._score_font.render(game_over_text, True, rgbcolors.white)
            game_over_pos = self._score_display.get_rect(center=(_w/2, _h/2))
            self._screen.blit(game_over_display, game_over_pos)

    def process_event(self, event):
        """Level Scene Subclass Event Processing, including
        controls for the player, and what occurs upon player death"""
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
        """Level Scene Subclass spawn pickups (apples)"""
        for pickup in self._pickup_list:
            if pickup.is_picked_up():
                pickup.add_to_score(self._score)
                self._pickup_list.pop()
                self._pickup_list.append(PickUp(self._screen, self._background_color))

    def draw_boundaries(self):
        """Level Scene Subclass draw danger boundaries"""
        for boundary in self._boundaries:
            pygame.draw.rect(self._screen, rgbcolors.red, boundary)

    def collide_boundaries(self):
        """Level Scene Subclass detect collision of boundaries
        and stop player."""
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
        """Level Scene Subclass to read data found
        in record_data.pickle if it exists yet."""
        if not os.path.exists('record_data.pickle'):
            #open(filename, 'w').close()
            print("Record file does not exist")
        else:
            with open('record_data.pickle', 'rb') as _f_h:
                self._save_info = pickle.load(_f_h)
                #self._save_info.append(pickle.load(_f_h))
            #print(self._save_info)

    def write_data(self):
        """Level Scene Subclass write record of score, date,
        and time elapsed"""
        with open('record_data.pickle', 'wb') as _f_h:
            pickle.dump(self._save_info, _f_h, pickle.HIGHEST_PROTOCOL)

    def game_over_info(self):
        """Level Scene Subclass execution of game over
        and save and uploading of info via pickle"""
        #print("Game Over Info:")
        #print("Score: " + str(self._score.get_score()))
        #print(datetime.date.today())
        #print(str(self._score.elapsed_time()) + " Seconds")
        score_data = self._score.get_score()
        date_data = datetime.date.today()
        time_data = self._score.elapsed_time()
        record = [score_data, date_data, time_data]
        self.read_data()
        self._save_info.append(record)
        self.write_data()

    def move_to_next_scene(self):
        """Level Scene Subclass move to next scene
        which is Leaderboard"""
        if self._id is not GameState.END_MENU:
            return GameState.LEADER_BOARD
        return GameState.END_MENU


    def update(self):
        """Level Scene Subclass update everything in scene"""
        if self._player.dead is False:
            self.collide_boundaries()
            self._player.update()
            self._score.click()
            #elapsed_time = self._score.elapsed_time()
            self._text = "Score: " + str(self._score.get_score())
            self._score_display = self._score_font.render(self._text, True, rgbcolors.white)
            #print(self._score.elapsed_time())
        else:
            game_over_text = "Game Over!"
            (_w, _h) = self._screen.get_size()
            game_over_display = self._score_font.render(game_over_text, True, rgbcolors.white)
            game_over_pos = self._score_display.get_rect(center=(_w/2, _h - 50))
            self._screen.blit(game_over_display, game_over_pos)
            if not self._save_info:
                self.game_over_info()


class LeaderBoardScene(Scene):
    """LeaderBoard Scene Subclass"""
    def __init__(self, scene_id, screen, background_color, title, title_color, title_size):
        """LeaderBoard Scene Subclass Initialization"""
        super().__init__(scene_id, screen, background_color)
        title_font = pygame.font.Font(pygame.font.get_default_font(), title_size)
        self._title = title_font.render(title, True, title_color)
        press_any_key_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self._press_any_key = press_any_key_font.render(
            'Press ESC to quit. Press any key to play again.', True, rgbcolors.black)
        (_w, _h) = self._screen.get_size()
        self._title_pos = self._title.get_rect(center=(_w/2, _h/10))
        self._press_any_key_pos = self._press_any_key.get_rect(center=(_w/2, _h - 50))
        self.record_font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.record_display = self.record_font.render(
            "_____________________________________", True, rgbcolors.black)
        self.record_pos = self.record_display.get_rect(center=(_w/2, _h/6))
        self._save_info = []
        self.has_drawn = False
        self._display_list = []
        self._padding_value = 30

    def draw(self):
        """LeaderBoard Scene Subclass draw for all in scene"""
        super().draw()
        self._screen.blit(self._title, self._title_pos)
        self._screen.blit(self._press_any_key, self._press_any_key_pos)
        self._screen.blit(self.record_display, self.record_pos)
        if self.has_drawn is False:
            self.leaderboard()
            self.has_drawn = True
        else:
            self.draw_records()

    def process_event(self, event):
        """LeaderBoard Scene Subclass to process events"""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self.set_not_valid()

    def leaderboard(self):
        """LeaderBoard Scene Subclass to read and load
        data from pickle file"""
        self.read_data()
        for record in self._save_info:
            for index in record:
                self.load_records(str(index))

    def move_to_next_scene(self):
        """LeaderBoard Scene Subclass to move to
        play level again or exit"""
        if self._id is not GameState.END_MENU:
            return GameState.PLAY_LEVEL
        return GameState.END_MENU

    def load_records(self, record):
        """LeaderBoard Scene Subclass to load records
        and process them into displayable text"""
        (_w, _h) = self._screen.get_size()
        record_font = pygame.font.Font(pygame.font.get_default_font(), 24)
        record_display = record_font.render(record, True, rgbcolors.black)
        record_pos = record_display.get_rect(center=(_w/2, _h/6 + self._padding_value))
        instance = [record_font, record_display, record_pos, self._padding_value]
        self._display_list.append(instance)
        self._padding_value = self._padding_value + 30
        #self._screen.blit(record_display, record_pos)

    def draw_records(self):
        """LeaderBoard Scene Subclass to draw records"""
        for record in self._display_list:
            self._screen.blit(record[1], record[2])

    def read_data(self):
        """LeaderBoard Scene Subclass to read in data
        from pickle file"""
        if not os.path.exists('record_data.pickle'):
        #open(filename, 'w').close()
            print("Record file does not exist")
        else:
            with open('record_data.pickle', 'rb') as _f_h:
                #self._save_info = pickle.load(_f_h)
                self._save_info.append(pickle.load(_f_h))
            #print(self._save_info)
