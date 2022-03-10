from vector import Vector

class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = 41, 39, 105

        self.ship_speed_factor = 8
        self.ship_limit = 3

        self.alien_speed_factor = 4
        self.fleet_drop_speed = 20
        self.fleet_direction = Vector(1, 0)

        self.laser_speed_factor = 8
        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = 255, 0, 0
        
        self.speedup_scale = 1.1
        
    # def increase_speed(self):
    #     self.ship_speed_factor *= self.speedup_scale
    #     self.laser_speed_factor *= self.speedup_scale
    #     self.alien_speed_factor *= self.speedup_scale


