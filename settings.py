from pygame.mixer import Sound


class Settings:
    """A class to store all settings of the game"""
    def __init__(self):
        """Initialize game settings"""
        # Screen settings
        self.scr_width = 900
        self.scr_height = 600
        self.bg_color = (0, 0, 0)

        # Ship's settings
        self.ship_speed_factor = 3
        self.ship_limit = 3

        # Bullet's settings
        self.bullet_speed_factor = 6
        self.bullet_width = 1
        self.enemy_bullet_width = 1
        self.bullet_height = 15
        self.bullet_color = (200, 200, 200)
        self.bullets_allowed = 10
        self.enemy_timer_scale = 1

        # Alien's settings
        self.alien_speed_factor = 2
        self.fleet_drop_speed = 5
        self.fleet_direction = 1

        # Boss's settings
        self.boss_number = 0
        self.boss_number_limit = 1  # allow only 1 boss appears on the screen

        # Sound
        self.explode_sound = Sound('audio/invaderkilled.wav')

        # Speed up scale
        self.speedup_scale = 1.1
        self.drop_speed_scale = 1

        # Scoring
        self.score_scale = 1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 3
        self.bullet_speed_factor = 6
        self.alien_speed_factor = 2
        self.fleet_drop_speed = 5
        self.score_scale = 1
        self.enemy_timer_scale = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed += self.drop_speed_scale
        self.score_scale += 0.5
        self.enemy_timer_scale += 0.2
