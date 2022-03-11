import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group, GroupSingle
from timer import Timer
from random import randint, randrange
from pygame import mixer


class AlienFleet:
    alien_exploding_images = [pg.image.load(f'images/rainbow_explode{n}.png') for n in range(8)]
    green_alien_images = [pg.image.load(f'images/green_alien{n}.png') for n in range(2)]
    blue_alien_images = [pg.image.load(f'images/blue_alien{n}.png') for n in range(2)]
    purp_alien_images = [pg.image.load(f'images/purp_alien{n}.png') for n in range(2)]
    ufo_images = [pg.image.load(f'images/ufo{n}.png') for n in range(2)]
    # ufo_exploding_images = [pg.image.load(f'images/bigscore{n}.png') for n in range(5)]

    def __init__(self, game, v=Vector(1, 0)):  
        self.game = game
        self.ship = self.game.ship
        self.settings = game.settings
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.v = v
        
        green_alien = Alien(self.game, image_list=AlienFleet.green_alien_images)
        self.g_alien_h, self.g_alien_w = green_alien.rect.height, green_alien.rect.width
        
        blue_alien = Alien(self.game, image_list=AlienFleet.blue_alien_images)
        self.b_alien_h, self.b_alien_w = blue_alien.rect.height, blue_alien.rect.width
        
        purp_alien = Alien(self.game, image_list=AlienFleet.purp_alien_images)
        self.p_alien_h, self.p_alien_w = purp_alien.rect.height, purp_alien.rect.width
        
        ufo = Extra_Alien(self.game, image_list=AlienFleet.ufo_images)
        self.ufo_h, self.ufo_w = ufo.rect.height, ufo.rect.width
        
        self.fleet = Group()
        self.create_fleet()
    
    
    def create_ufo_alien(self, row, col): 
        ufo_x = self.ufo_w * 5 * (col + 1)        
        ufo_y = self.ufo_h * (row)
        ufo_images = AlienFleet.ufo_images
        
        ufo_alien = Extra_Alien(game=self.game, ul=(ufo_x, ufo_y), v=self.v, image_list=ufo_images)
        self.fleet.add(ufo_alien)


    def create_fleet(self):
        n_rows = 1
        n_cols = 9
        for row in range(n_rows):
            for col in range(n_cols):
                self.create_alien(row=row, col=col)
                
        n_rows = 1
        n_cols = 1
        for row in range(n_rows):
            for col in range(n_cols):
                self.create_ufo_alien(row=row, col=col)
                
    
    def create_alien(self, row, col):
        g_x = self.g_alien_w * 1.5 * (col + 1)        # use x = self.alien_w * (col + 1) to make them close together, initially self.alien_w * (2*col + 1)
        g_y = self.g_alien_h * 4.5 * (row + 1)
        
        g_x1 = self.g_alien_w * 1.5 * (col + 1)       
        g_y1 = self.g_alien_h * 5.5 * (row + 1)
        green_images = AlienFleet.green_alien_images
        
        b_x = self.b_alien_w * 1.5 * (col + 1)        
        b_y = self.b_alien_h * 2.7 * (row + 1)
        
        b_x1 = self.b_alien_w * 1.5 * (col + 1)        
        b_y1 = self.b_alien_h * 3.6 * (row + 1)
        blue_images = AlienFleet.blue_alien_images
        
        p_x = self.p_alien_w * 1.5 * (col + 1)        
        p_y = self.p_alien_h * 1.9 * (row + 1)
        purp_images = AlienFleet.purp_alien_images

        g_alien = Alien(game=self.game, ul=(g_x, g_y), v=self.v, image_list=green_images, points=10)
        g1_alien = Alien(game=self.game, ul=(g_x1, g_y1), v=self.v, image_list=green_images, points=10)
        
        b_alien = Alien(game=self.game, ul=(b_x, b_y), v=self.v, image_list=blue_images, points=20)
        b1_alien = Alien(game=self.game, ul=(b_x1, b_y1), v=self.v, image_list=blue_images, points=20)
        
        p_alien = Alien(game=self.game, ul=(p_x, p_y), v=self.v, image_list=purp_images, points=30)
        
        self.fleet.add(g_alien)
        self.fleet.add(g1_alien) 
        self.fleet.add(b_alien)
        self.fleet.add(b1_alien)  
        self.fleet.add(p_alien)
        
        
    def set_ship(self, ship): self.ship = ship
    def empty(self): self.fleet.empty()
    def set_alien_lasers(self, alien_lasers): self.alien_lasers = alien_lasers

    def length(self): return len(self.fleet.sprites())

    def change_v(self, v):
        for alien in self.fleet.sprites():
            alien.change_v(v)

    def check_bottom(self): 
      for alien in self.fleet.sprites():
        if alien.check_bottom():
            self.ship.hit()
            break
      
    def check_edges(self): 
      for alien in self.fleet.sprites():
        if alien.check_edges(): return True
      return False

    def update(self):
        delta_s = Vector(0, 0)    # don't change y position in general
        if self.check_edges():
            self.v.x *= -1
            self.change_v(self.v)
            delta_s = Vector(0, self.settings.fleet_drop_speed)
        if pg.sprite.spritecollideany(self.ship, self.fleet) or self.check_bottom():
            if not self.ship.is_dying(): self.ship.hit() 
        for alien in self.fleet.sprites():
            alien.update(delta_s=delta_s)

    def draw(self):
        for alien in self.fleet.sprites():
            alien.draw()


class Alien(Sprite):
    def __init__(self, game, image_list, start_index=0, ul=(0, 100), v=Vector(1, 0), points=0):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.points = points
        self.stats = game.stats
        
        self.image = pg.image.load('images/alien0.bmp')
        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = ul
        self.ul = Vector(ul[0], ul[1])   # position
        self.v = v                       # velocity
        self.image_list = image_list
        self.exploding_timer = Timer(image_list=AlienFleet.alien_exploding_images, delay=200, 
                                     start_index=start_index, is_loop=False)
        self.normal_timer = Timer(image_list=image_list, delay=1000, is_loop=True)
        self.timer = self.normal_timer
        self.dying = False
        
        self.lasers = None
        
        self.explosion_sound = mixer.Sound('sounds/Explosion+3.wav')
        self.fast_game_music = mixer.Sound('sounds/fast_game_music.wav')
    
    def change_v(self, v): self.v = v
    
    def check_bottom(self): return self.rect.bottom >= self.screen_rect.bottom
    
    def check_edges(self):
        r = self.rect
        return r.right >= self.screen_rect.right or r.left <= 0

    def hit(self): 
        self.stats.alien_hit(alien=self)
        self.timer = self.exploding_timer
        self.explosion_sound.play()
        self.explosion_sound.set_volume(0.05)
        self.dying = True

    def update(self, delta_s=Vector(0, 0)):
        if self.dying and self.timer.is_expired():
          self.kill()
        self.ul += delta_s
        self.ul += self.v * self.settings.alien_speed_factor
        self.rect.x, self.rect.y = self.ul.x, self.ul.y
        
        # if self.rect.y == 400:
        #     self.fast_game_music.play()
        #     self.fast_game_music.set_volume(0.2)

    def draw(self):  
      image = self.timer.image()
      rect = image.get_rect()
      rect.x, rect.y = self.rect.x, self.rect.y
      self.screen.blit(image, rect)
      
      
      
class Extra_Alien(Sprite):
    def __init__(self, game, image_list, start_index=0, ul=(0, 100), v=Vector(1, 0), points=randrange(100, 600, 100)):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.points = points
        self.stats = game.stats
        
        self.image = pg.image.load('images/alien0.bmp')
        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = ul
        self.ul = Vector(ul[0], ul[1])   # position
        self.v = v                       # velocity
        self.image_list = image_list
        
        if self.points == 100:
            exploding_score = [pg.image.load('images/bigscore0.png') for n in range(5)]
        elif self.points == 200: 
            exploding_score = [pg.image.load('images/bigscore1.png') for n in range(5)]
        elif self.points == 300: 
            exploding_score = [pg.image.load('images/bigscore2.png') for n in range(5)]
        elif self.points == 400: 
            exploding_score = [pg.image.load('images/bigscore3.png') for n in range(5)]
        elif self.points == 500: 
            exploding_score = [pg.image.load('images/bigscore4.png') for n in range(5)]
            
        # score is better seen if ufo is hit last, random big score each game
        self.exploding_timer = Timer(image_list=exploding_score, delay=200, 
                                     start_index=start_index, is_loop=False)
        self.normal_timer = Timer(image_list=image_list, delay=1000, is_loop=True)
        self.timer = self.normal_timer
        self.dying = False
        
        self.lasers = None
        
        self.explosion_sound = mixer.Sound('sounds/Explosion+3.wav')
        self.ufo_sound = mixer.Sound('sounds/ufo_hover.wav')
    
    def change_v(self, v): self.v = v
    
    def check_bottom(self): return self.rect.bottom >= self.screen_rect.bottom
    
    def check_edges(self):
        r = self.rect
        return r.right >= self.screen_rect.right or r.left <= 0

    def hit(self): 
        self.stats.alien_hit(alien=self)
        self.timer = self.exploding_timer
        self.explosion_sound.play()
        self.explosion_sound.set_volume(0.05)
        self.ufo_sound.stop()
        self.dying = True

    def update(self, delta_s=Vector(0, 0)):
        # self.ufo_sound.play()
        # self.ufo_sound.set_volume(0.1)
        if self.dying and self.timer.is_expired():
          self.kill()
        self.ul += delta_s
        self.ul += self.v * self.settings.ufo_speed_factor
        self.rect.x, self.rect.y = self.ul.x, self.ul.y

    def draw(self):  
        image = self.timer.image()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)

      