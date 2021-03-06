import pygame 

class Ship(pygame.sprite.Sprite):
    ''' a class to manage most of the behavior of the ship'''
    def __init__(self ,game_settings ,screen):
        '''Initialize the ship and set its starting position.'''
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('image/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movment flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''update the position of the ship'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center 

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx

    def blit_me(self):
        '''draw the ship at its current location'''
        self.screen.blit(self.image,self.rect)