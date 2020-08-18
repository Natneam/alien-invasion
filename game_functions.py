'''
file to store a number of functions that make the logic
in alien_invasion.py easier to follow
'''
import pygame
import sys
from bullet import Bullet
from alien import Alien

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

def update_bullets(game_settings, screen, ship, aliens, bullets):
    '''update the position of the bullet and get rid of old bullets'''
    # Update bullets positions.
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collision(game_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collision(game_settings, screen, ship, aliens, bullets):
    '''Respond to bullet-alien collisions'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Destroy existing bullet and create new fleet.
        bullets.empty()
        create_fleet(game_settings, screen, ship, aliens)

#update screen function

def update_screen(game_settings, screen, ship, aliens, bullets):
    '''Update image on the screen and flip to the new screen'''

    # Redraw the screen during each pass through the loop.  
    screen.fill(game_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    ship.blit_me()
    aliens.draw(screen)

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def get_number_aliens(game_settings, alien_width):
    '''Determine number of aliens that fit in a row'''
    available_space_x = game_settings.screen_width - (2*alien_width)
    number_aliens_x = int(available_space_x / (2*alien_width))

    return number_aliens_x

def get_number_rows(game_settings, ship_height, alien_height):
    '''Determine the number of rows of aliens that fit on the screen.'''
    available_space_y = game_settings.screen_height - (3*alien_height) - ship_height
    number_rows = int(available_space_y / (2*alien_height))

    return number_rows

def create_alien(game_settings, screen, aliens, alien_number, row_number):
    # Create and alien and place it in the row
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)

def create_fleet(game_settings, screen, ship, aliens):
    '''create a full fleet of aliens'''
    #Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.

    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    #Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number, row_number)


def update_aliens(game_settings, aliens):
    ''' Check if the fleet is at an edge,
    and then update the postions of all aliens in the fleet. '''
    check_fleet_edge(game_settings,aliens)
    aliens.update()

def check_fleet_edge(game_settings, aliens):
    ''' Respond appropriately if any alien reached an edge '''
    for alien in aliens:
        if alien.check_edge():
            change_fleet_direction(game_settings, aliens)
            break

def change_fleet_direction(game_settings, aliens):
    '''Drop the entire fleet and change fleet's direction'''
    for alien in aliens:
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1