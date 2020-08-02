'''
file to store a number of functions that make the logic
in alien_invasion.py easier to follow
'''
import pygame
import sys

#check events

def check_keydown_events(event, ship):
    '''Respond to key press'''
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the Left
        ship.moving_left = True

def check_keyup_events(event, ship):
    '''Respond to key release'''
    if event.key == pygame.K_RIGHT:
        # Stop moving the ship to the right
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # Stop moving the ship to the Left
        ship.moving_left = False

def check_event(ship):
    '''Respond to keypress and mouse events.'''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)            

#update screen function

def update_screen(game_settings, screen, ship):
    '''Update image on the screen and flip to the new screen'''

    # Redraw the screen during each pass through the loop.  
    screen.fill(game_settings.bg_color)
    ship.blit_me()

    # Make the most recently drawn screen visible.
    pygame.display.flip()