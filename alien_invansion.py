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
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # Initialize pygame, settings and screen object. 
    pygame.init()
    game_settings = Setting()
    screen = pygame.display.set_mode((game_settings.screen_width,game_settings.screen_height))

    pygame.display.set_caption("Alien Invansion")
    
    # Make the Play button
    
    play_button = Button(game_settings, screen, "Play")  

    # Create and instance to store game statstics and create a score board. 
    stats = GameStats(game_settings)
    sb = Scoreboard(game_settings, screen, stats)

    # Make a ship, Group of aliens and Group of bullets
    ship =  Ship(game_settings, screen)
    aliens = Group()
    bullets = Group()

    # Create the fleet of aliens.
    gf.create_fleet(game_settings, screen, ship,aliens)

    # Start the main loop for the game.
    while True:
        gf.check_events(game_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(game_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(game_settings, stats, screen, ship, aliens, bullets)
        gf.update_screen(game_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
