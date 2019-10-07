from high_score import HighScore


class GameStats:
    """Track statistics for the game"""
    def __init__(self, game_settings, screen):
        self.settings = game_settings
        self.ships_left = self.settings.ship_limit
        # self.game_active = False
        self.game_status = 0  # 0: main menu, 1: high score, 2: play game
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.score_data = HighScore('save.txt', game_settings, self, screen)

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
