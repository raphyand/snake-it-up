#!/usr/bin/env python3
import pygame
import pdb
import event_manager
from utils import GameState
from rgbcolors import goldenrod, navyblue, cyan, purple1
from scene import Scene, TitleScene, LevelScene, LeaderBoardScene
from player import Player
from pickup import PickUp

#from scene import Scene
# Note: Everything in Pygame is a rect

def display_info():
	print('The display is using the "{}"driver.'.format(pygame.display.get_driver()))

	print('Video Info:')
	print(pygame.display.Info())

#def core_game_play_loop(self):
	"""Core Gameplay Loop method where states are determined and executed"""
#	while self.get_current_game_state() is not GameState.GAMEOVER:
#		if self.get_current_game_state() is GameState.MAIN_MENU:
#			self.main_menu()
#		elif self.get_current_game_state() is GameState.PLAYER_SELECTION_MENU:
#			self.player_selection_menu()
#		elif self.get_current_game_state() is GameState.WHO_GOES_FIRST:
#			self.who_goes_first_menu()
#		elif self.get_current_game_state() is GameState.TURN_MENU:
#			self.turn_menu()
#		elif self.get_current_game_state() is GameState.MATCH_END:
#			self.match_end_menu()

def create_level(game_state, screen, title, player):
	if game_state is GameState.MAIN_MENU:
		return TitleScene(GameState.MAIN_MENU, screen, goldenrod, title, navyblue, 72)
	if game_state is GameState.PLAY_LEVEL:
		return LevelScene(GameState.PLAY_LEVEL, screen, purple1, player)
	if game_state is GameState.LEADER_BOARD:
		return LeaderBoardScene(GameState.LEADER_BOARD, screen, navyblue, "LeaderBoard", goldenrod, 72)
		

def main():
	print('hello world')
	if not pygame.font:
		print("Warning, fonts disabled")
		exit(1)
	if not pygame.mixer:
		print("warning, sound disabled")
		exit(1)

	pygame.init()
	window_size = (800, 800)
	clock = pygame.time.Clock()

	#screen = pygame.display.set_mode(window_size)
	#background_color = purple1
	#background = pygame.Surface(screen.get_size())
	#background.fill(background_color)
	#player = Player(screen, background_color, True)
	#test_pickup = PickUp(screen, background_color)
	#title = 'Snake++'
	#pygame.display.set_caption(title)

	#scene_list = [TitleScene(GameState.MAIN_MENU, screen, goldenrod, title, navyblue, 72), LevelScene(GameState.PLAY_LEVEL, screen, purple1, player), LeaderBoardScene(GameState.LEADER_BOARD, screen, navyblue, "LeaderBoard", goldenrod, 72)]	
	current_game_state = GameState.MAIN_MENU

	while current_game_state is not GameState.END_MENU :
		title = 'Snake++'
		screen = pygame.display.set_mode(window_size)
		background_color = purple1
		background = pygame.Surface(screen.get_size())
		background.fill(background_color)
		pygame.display.set_caption(title)
		player = Player(screen, background_color, True)
		current_scene = create_level(current_game_state, screen, title, player)
		current_scene.start_scene()
		while current_scene.is_valid():
			clock.tick(current_scene.frame_rate())
			for event in pygame.event.get():
				current_scene.process_event(event)
			current_scene.update()
			current_scene.draw()
			pygame.display.update()
		current_game_state = current_scene.move_to_next_scene()



	#for scene in scene_list:
		# start the scene
	#	scene.start_scene()
	#	while scene.is_valid():
		#while the scene is valid
	#		clock.tick(scene.frame_rate())
			# measure the clock ticks
	#		for event in pygame.event.get():
	#			scene.process_event(event)
			#process all game events
	#		scene.update()
			#update the scene
	#		scene.draw()
	#		pygame.display.update()
			# draw the scene

		#end the scene
	#	scene.end_scene()
	pygame.quit()

if __name__ == '__main__':
    main()
