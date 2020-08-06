class Setting():
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        '''Initializing the game setting.'''

        # Screen settings
        self.screen_width = 800
        self.screen_height = 500
        self.bg_color = (230,230,230)

        # Ship setting

        self.ship_speed_factor = 1.5

        # Bullet Settings
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3