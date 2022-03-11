import pygame as pg
from sys import exit
import game_functions as gf
from time import sleep
from stats import Stats
from laser import Lasers
from alien_laser import Alien_Lasers
from ship import Ship
from alien import AlienFleet
from settings import Settings
from landing import LandingPage
from score import Scoreboard
from pygame import mixer


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.stats = Stats(game=self)
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        self.scoreboard = Scoreboard(game=self)
        
        pg.display.set_caption("Space Invaders")
        self.ship = Ship(game=self)
        self.alien_fleet = AlienFleet(game=self)
        self.lasers = Lasers(game=self)
        self.ship.set_alien_fleet(self.alien_fleet)
        self.ship.set_lasers(self.lasers)
        
        self.alien_lasers = Alien_Lasers(game=self)
        self.alien_fleet.set_alien_lasers(self.alien_lasers)
        
        self.mixer = mixer.init()
         
    def restart(self):
        # self.music.stop()
        if self.stats.ships_left == 0: 
          self.game_over()
        print("restarting game")
        self.lasers.empty()
        self.alien_fleet.empty()
        self.alien_fleet.create_fleet()
        self.settings.increase_speed()
        self.ship.center_bottom()
        self.ship.reset_timer()
        self.update()
        self.draw()
        sleep(0.5)

    def update(self):
        self.ship.update()
        self.alien_fleet.update()
        self.lasers.update()
        # self.alien_lasers.update()
        self.scoreboard.update()

    def draw(self):
        #self.screen.fill(self.bg_color)
        space_bg = pg.image.load(f'images/space_bg.png').convert()
        self.screen.blit(space_bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.lasers.draw()
        # self.alien_lasers.draw()
        for n in range(6):
            barrier0 = pg.image.load('images/barrier0.png')
            self.screen.blit(barrier0, (50+(200*n), 550))
        self.scoreboard.draw()
        pg.display.flip()
        
    def play(self):
        self.finished = False
        self.music = pg.mixer.Sound('sounds/game_music.wav')
        self.fast_game_music = mixer.Sound('sounds/fast_game_music.wav')
        self.music.play(loops=-1)
        self.music.set_volume(0.2)
        # if len(self.alien_fleet.green_alien_images) == 0:
        #     self.music.stop()
        #     self.fast_game_music.play()
        #     self.fast_game_music.set_volume(0.2)
        while not self.finished:
            self.update()
            self.draw()
            gf.check_events(game=self)   # exits game if QUIT pressed
        self.game_over()

    def game_over(self): 
        print('\nGAME OVER!\n\n') 
        self.music.stop()
        exit()    # can ask to replay here instead of exiting the game

def main():
    g = Game()
    lp = LandingPage(game=g)
    lp.show()
    g.play()


if __name__ == '__main__':
    main()
