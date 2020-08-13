import pygame

class Alien(pygame.sprite.Sprite):
    ''' A class to represent alien in the fleet.'''

    def __init__(self, game_settings, screen) :
        '''Initialize alien and set its start position'''
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('image/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position 
        self.x = float(self.rect.x)

    def blit_me(self):
        ''' Draw the alien at its current position'''
        self.screen.blit(self.image, self.rect)