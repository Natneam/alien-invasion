import json

class GameStats():
    ''' Track statics of Alien Invasion.'''
    
    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.reset_stats()

        # Start the alien Invasion in active state
        self.game_active = False

        # High score should never be reset.
        try:
            with open("high_score.json") as f_obj:
                self.high_score = int(json.load(f_obj))
        except FileNotFoundError:
            self.high_score = 0
    
    def reset_stats(self):
        ''' Initialize statistics that can change during the game.'''
        self.ships_left = self.game_settings.ship_limit
        self.score = 0
        self.level = 1