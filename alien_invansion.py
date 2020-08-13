'''
Main file of Alien Invension game

In this game( Alien Invasion), the player controls a ship that appears at
the bottom center of the screen. The player can move the ship
right and left using the arrow keys and shoot bullets using the
spacebar. When the game begins, a fleet of aliens fills the sky
and moves across and down the screen. The player shoots and
destroys the aliens. If the player shoots all the aliens, a new fleet
appears that moves faster than the previous fleet. If any alien hits
the player’s ship or reaches the bottom of the screen, the player
loses a ship. If the player loses three ships, the game ends.

'''
import pygame
from pygame.sprite import Group

from settings import Setting
from ship import Ship
import game_functions as gf

def run_game():
    # Initialize pygame, settings and screen object. 
    pygame.init()
    game_settings = Setting()
    screen = pygame.display.set_mode((game_settings.screen_width,game_settings.screen_height))

    pygame.display.set_caption("Alien Invansion")

    # Make a ship, Group of aliens and Group of bullets
    ship =  Ship(game_settings, screen)
    aliens = Group()
    bullets = Group()

    # Create the fleet of aliens.
    gf.create_fleet(game_settings, screen, ship,aliens)

    # Start the main loop for the game.
    while True:
        gf.check_events(game_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(game_settings, screen, ship, aliens, bullets)

run_game()
