#!/usr/bin/env python3
import pygame
import pdb
import event_manager
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

def main():
	print('hello world')
	if not pygame.font:
		print("Warning, fonts disabled")
		exit(1)
	if not pygame.mixer:
		print("warning, sound disabled")
		exit(1)

	pygame.init()
	#display_info()
	window_size = (800, 800)
	# 768, 768 for the playable perimiter
	clock = pygame.time.Clock()

	#clock = pygame.time.clock(60)
	screen = pygame.display.set_mode(window_size)
	#background_color = (120, 120, 150)
	background_color = purple1#rgbcolors.purple1
	background = pygame.Surface(screen.get_size())
	#background = pygame.Surface((768, 768))
	background.fill(background_color)
	#player = pygame.Rect(400, 400, 25, 25)
	player = Player(screen, background_color, True)
	#player2 = Player(screen, pygame.Rect(400, 434, 32, 32), background_color, True)
	test_pickup = PickUp(screen, background_color)

	#Professor's code____________
	title = 'Snake++'
	pygame.display.set_caption(title)

	scene_list = [TitleScene(1, screen, goldenrod, title, navyblue, 72), LevelScene(2, screen, purple1, player), LeaderBoardScene(3, screen, navyblue, "LeaderBoard", goldenrod, 72)]	

	for scene in scene_list:
		# start the scene
		scene.start_scene()
		while scene.is_valid():
		#while the scene is valid
			clock.tick(scene.frame_rate())
			# measure the clock ticks
			for event in pygame.event.get():
				scene.process_event(event)
			#process all game events
			scene.update()
			#update the scene
			scene.draw()
			pygame.display.update()
			# draw the scene

		#end the scene
		scene.end_scene()
	pygame.quit()

if __name__ == '__main__':
    main()
