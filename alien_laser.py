import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint, choice, random
from alien import Alien, AlienFleet
from pygame import mixer
from ship import Ship

class Alien_Lasers:
    def __init__(self, game):
        self.game = game
        self.stats = game.stats
        self.ship = self.game.ship
        self.alien_fleet = game.alien_fleet
        self.alien_lasers = Group()
        self.alien_laser_sound = mixer.Sound('sounds/enemy_laser.wav')

    def add(self, laser): self.lasers.add(laser)
    def empty(self): self.lasers.empty()
    # def fire(self): 
    #     new_laser = Alien_Laser(self.game)
    #     self.lasers.add(new_laser)
    #     self.alien_laser_sound.play()
    #     self.alien_laser_sound.set_volume(0.1)
            
    def update(self):
        time_now = pg.time.get_ticks()
        alien_cooldown = 1000 # in milliseconds
        last_alien_shot = pg.time.get_ticks()
        if time_now - last_alien_shot > alien_cooldown:
            attacking_alien = random.choice(self.alien_fleet)
            alien_laser = Alien_Laser(attacking_alien.rect.centerx, 
                                       attacking_alien.rect.bottom)
            # new_laser = Alien_Laser(self.game)
            self.alien_lasers.add(alien_laser)
            
        # for laser in self.alien_lasers.copy():
        #     if laser.rect.bottom <= 0: self.lasers.remove(laser)
            
        # for alien_laser in self.alien_lasers:
        #     alien_laser.update()

    def draw(self):
        for alien_laser in self.alien_lasers:
            alien_laser.draw()
            
            
class Alien_Laser(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.w, self.h = self.settings.laser_width, self.settings.laser_height
        self.ship = game.ship
        
        self.rect = pg.Rect(0, 0, self.w, self.h)
        self.center = copy(self.ship.center)
        # print(f'center is at {self.center}')
        # self.color = self.settings.laser_color
        self.color = (255, 255, 255)
        self.v = Vector(0, 1) * self.settings.laser_speed_factor    #shoots laser downward
        
    # def alien_fire(self):
    #     if self.alien_fleet:
    #         random_alien = choice(self.alien_fleet)
    #         new_laser = Alien_Lasers(self.game)
    #         self.lasers.add(new_laser)

    def update(self):
        self.center += self.v
        self.rect.x, self.rect.y = self.center.x, self.center.y

    def draw(self): pg.draw.rect(self.screen, color=self.color, rect=self.rect)
    
