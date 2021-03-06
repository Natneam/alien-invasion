'''
file to store a number of functions that make the logic
in alien_invasion.py easier to follow
'''
import pygame, sys, json
from time import sleep
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

def check_events(game_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '''Respond to keypress and mouse events.'''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            try:
                with open("high_score.json", 'w') as f_obj:
                    json.dump(stats.high_score, f_obj)
            except:
                pass
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(game_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    ''' Start a new game when the player clicks play.'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(game_settings, screen, stats, sb, aliens, bullets, ship)


def start_game(game_settings, screen, stats, sb, aliens, bullets, ship):
    # Reset the game settings.
    game_settings.initialize_dynamic_settings()
    
    # Hide the mouse curser
    pygame.mouse.set_visible(False)

    # Reset the game statics 
    stats.reset_stats()
    stats.game_active = True

    # Empty the list of alien and bullets
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship
    create_fleet(game_settings, screen, ship, aliens)
    ship.center_ship()

    # reseting the scoreboard display
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()



# Fire bullet

def fire_bullet(game_settings,screen, ship, bullets):
    ''' Fire a bullet if the limit number is not reached'''
    
    # Create a new bullet and add it to the bullets group
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add((new_bullet))

# Update bullets position

def update_bullets(game_settings, screen, stats, sb, ship, aliens, bullets):
    '''update the position of the bullet and get rid of old bullets'''
    # Update bullets positions.
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collision(game_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collision(game_settings, screen, stats, sb, ship, aliens, bullets):
    '''Respond to bullet-alien collisions'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        # If the entire fleet is destroy start new level.

        bullets.empty()
        game_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(game_settings, screen, ship, aliens)

#update screen function

def update_screen(game_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    '''Update image on the screen and flip to the new screen'''

    # Redraw the screen during each pass through the loop.  
    screen.fill(game_settings.bg_color)
    
    # Draw the play button if the game is in active.
    if not stats.game_active:
        play_button.draw_button()
    else:
        # Redraw all bullets behind ship and aliens
        for bullet in bullets.sprites():
            bullet.draw_bullet()
            
        ship.blit_me()
        aliens.draw(screen)

        # Draw the score information.
        sb.show_score()
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

def ship_hit(game_settings ,stats, screen, sb, ship, aliens, bullets):
    ''' Respond to ship hit by alien.'''
    if stats.ships_left > 1:
        # Decremet ship's left
        stats.ships_left -= 1

        # Update Scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)



def update_aliens(game_settings ,stats, screen, sb, ship, aliens, bullets):
    ''' Check if the fleet is at an edge,
    and then update the postions of all aliens in the fleet. '''
    check_fleet_edge(game_settings,aliens)
    aliens.update()

    # Look for alien-ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings ,stats, screen, sb, ship, aliens, bullets)
    
    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(game_settings ,stats, screen,sb, ship, aliens, bullets)

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


def check_aliens_bottom(game_settings ,stats, screen, sb, ship, aliens, bullets):
    ''' Check if any alien reached the bottom of the bottom of the screen'''
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this as if the ship got hit
            ship_hit(game_settings ,stats, screen, sb, ship, aliens, bullets)
            break
              

def check_high_score(stats, sb):
    ''' Check to see if there's new high score.'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()