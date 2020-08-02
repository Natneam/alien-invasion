'''
file to store a number of functions that make the logic
in alien_invasion.py easier to follow
'''
import pygame
import sys

#check event

def check_event():
    '''Respond to keypress and mouse events.'''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

#update screen function

def update_screen(game_setting, screen, ship):
    '''Update image on the screen and flip to the new screen'''

    # Redraw the screen during each pass through the loop.  
    screen.fill(game_setting.bg_color)
    ship.blit_me()

    # Make the most recently drawn screen visible.
    pygame.display.flip()