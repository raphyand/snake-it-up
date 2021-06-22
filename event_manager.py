"""Event Manager for snake.py"""
import pygame
import pdb

def handle_events():
    #pdb.set_trace()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
        else:
            return False
    return False
    print("This should be done executing")

def process_events_exit(event):
    if event.type == pygame.QUIT:
        return True
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return True
    else: 
        return False
    return False

		#for event in pygame.event.get():
		#	if pygame.event.EventType == pygame.QUIT:
		#		return
		#	elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
		#		turn_off = True
		#		return
