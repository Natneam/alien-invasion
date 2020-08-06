'''
file to store a number of functions that make the logic
in alien_invasion.py easier to follow
'''
import pygame
import sys
from bullet import Bullet

#check events

def check_keydown_events(event, game_settings, screen, ship, bullets):
    '''Respond to key press'''
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the Left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # fire bullet
        fire_bullet(game_settings, screen, ship, bullets)

def check_keyup_events(event, ship):
    '''Respond to key release'''
    if event.key == pygame.K_RIGHT:
        # Stop moving the ship to the right
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # Stop moving the ship to the Left
        ship.moving_left = False

def check_events(game_settings, screen, ship, bullets):
    '''Respond to keypress and mouse events.'''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)            

# Fire bullet

def fire_bullet(game_settings,screen, ship, bullets):
    ''' Fire a bullet if the limit number is not reached'''
    
    # Create a new bullet and add it to the bullets group
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add((new_bullet))

# Update bullets position

def update_bullets(bullets):
    '''update the position of the bullet and get rid of old bullets'''
    # Update bullets positions.
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


#update screen function

def update_screen(game_settings, screen, ship, bullets):
    '''Update image on the screen and flip to the new screen'''

    # Redraw the screen during each pass through the loop.  
    screen.fill(game_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    ship.blit_me()

    # Make the most recently drawn screen visible.
    pygame.display.flip()