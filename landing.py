from decimal import HAVE_CONTEXTVAR
import imghdr
import pygame as pg
import sys
from alien import Alien
from vector import Vector
from button import Button
from pygame import mixer
from stats import Stats

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (57, 162, 64)
GREEN = (106, 233, 115)
BLUE = (61, 105, 171)
GREY = (130, 130, 130)
INDIGO = (88, 90, 139)


class LandingPage:
    green_alien = [pg.image.load(f'images/green_alien{n}.png') for n in range(2)] 
    blue_alien = [pg.image.load(f'images/blue_alien{n}.png') for n in range(2)]   
    purp_alien = [pg.image.load(f'images/purp_alien{n}.png') for n in range(2)]  
    ufo = [pg.image.load(f'images/ufo{n}.png') for n in range(2)]

    
    def __init__(self, game):
        self.screen = game.screen
        self.landing_page_finished = False
        self.highscore = game.stats.get_highscore()
        
        self.mixer = mixer.init()
        
        self.title_music = pg.mixer.Sound('sounds/title_screen.wav')
        self.title_music.play()
        self.title_music.set_volume(0.2)

        headingFont = pg.font.SysFont(None, 190)
        subheadingFont = pg.font.SysFont(None, 110)
        font = pg.font.SysFont(None, 48)

        strings = [('SPACE', WHITE, headingFont), ('INVADERS', GREEN, subheadingFont),
                   ('= 10 PTS', WHITE, font), ('= 20 PTS', WHITE, font),
                   ('= 30 PTS', WHITE, font), ('= ???', WHITE, font),
                   (f'HIGH SCORE = {self.highscore:}', WHITE, font)] 


        self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]

        self.posns = [150, 230]
        alien = [60 * x + 400 for x in range(4)]
        # play_high = [x for x in range(650, 760, 80)]
        self.posns.extend(alien)
        self.posns.append(730)
        # self.posns.extend(play_high)

        centerx = self.screen.get_rect().centerx
        
        self.play_button = Button(self.screen, "PLAY GAME", ul=(centerx - 110, 650))
        
        n = len(self.texts)
        self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]
        self.green_alien = Alien(game=game, image_list=LandingPage.green_alien, v=Vector(), ul=(centerx-130, 365))
        self.blue_alien = Alien(game=game, image_list=LandingPage.blue_alien, v=Vector(), ul=(centerx-130, 430))
        self.purp_alien = Alien(game=game, image_list=LandingPage.purp_alien, v=Vector(), ul=(centerx-130, 495))
        self.ufo = Alien(game=game, image_list=LandingPage.ufo, v=Vector(), ul=(centerx-130, 550))


    def get_text(self, font, msg, color): 
        return font.render(msg, True, color, INDIGO)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
            if e.type == pg.KEYUP and e.key == pg.K_p:   # pretend PLAY BUTTON pressed
                self.landing_page_finished = True        # TODO change to actual PLAY button
                # self.music.stop()
            elif e.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if self.play_button.rect.collidepoint(mouse_x, mouse_y):
                    self.landing_page_finished = True
                    self.title_music.stop()
                                                         # SEE ch. 14 of Crash Course for button
                                                         # you can also push P
    def update(self):       # TODO make aliens move
        pass 

    def show(self):
        while not self.landing_page_finished:
            self.update()
            self.draw()
            self.check_events()   # exits game if QUIT pressed

    def draw_text(self):
        n = len(self.texts)
        for i in range(n):
            self.screen.blit(self.texts[i], self.rects[i])
            
    def draw(self):
        space_bg = pg.image.load(f'images/space_bg.png').convert()
        self.screen.fill(BLACK)
        self.screen.blit(space_bg, (0, 0))
        self.green_alien.draw()
        self.blue_alien.draw()
        self.purp_alien.draw()
        self.ufo.draw()
        self.draw_text()
        self.play_button.draw()
        # self.score_button.draw()
        # self.alien_fleet.draw()   # TODO draw my aliens
        # self.lasers.draw()        # TODO dray my button and handle mouse events
        pg.display.flip()
