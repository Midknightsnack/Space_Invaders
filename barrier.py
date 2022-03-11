import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint
from timer import CommandTimer
# from alien import Alien
# from stats import Stats


class Barriers:
    def __init__(self, game):
        self.game = game
        # self.alien_fleet = game.alien_fleet
        # for n in range(5):
        #     create_barrier(n)
        barriers = BarrierElement(self.game, img_list=Barrier.img_list)
        self.barrier_h, self.barrier_w = barriers.rect.height, barriers.rect.width
        
        self.barrier_group = Group()

    def create_barrier_row(self): #pass
        n_rows = 1
        n_cols = 4
        for row in range(n_rows):
            for col in range(n_cols):
                self.create_barrier(row=row, col=col)
                
    def create_barrier(self, row, col):
        barrier_x = self.barrier_w * 1.5 * (col + 1)        
        barrier_y = self.barrier_h * (row + 1)
        barrier_images = Barrier.img_list

        # red_barrier = BarrierElement(game=self.game, ul=(barrier_x, barrier_y), img_list=img_list)
        # self.barrier_group.add(red_barrier)
            
        
    def update(self): 
        for barrier in self.barriers:
            barrier.update()

    def draw(self): 
        for barrier in self.barriers:
            barrier.draw()


class Barrier(Sprite):
    img_list = [pg.image.load(f'images/barrier{n}.png') for n in range(4)]
    
    def __init__(self, game, ul, wh): 
        self.game = game
        self.barrier_elements = Group()
        self.ul = ul
        self.wh = wh
        img_list = BarrierElement(self.game, image_list=img_list)
        
        for row in range(wh[0]):
            for col in range(wh[1]):
                be = BarrierElement(game=game, img_list=img_list,
                                    ul=(ul[0] + col, ul[1] + row), wh=(4, 4))
                self.barrier_elements.add(be)
        
    def update(self): 
        collisions = pg.sprite.groupcollide(self.barrier_elements, 
                                            self.lasers, False, True)
        for be in collisions: 
            be.hit()

    def draw(self): 
        for be in self.barrier_elements:
            be.draw()


class BarrierElement(Sprite):
    def __init__(self, game, img_list, ul, wh): 
        self.game = game
        self.ul = ul
        self.wh = wh
        self.img_list = img_list
        self.rect = pg.Rect(ul[0], ul[1], wh[0], wh[1])
        self.timer = CommandTimer(img_list=img_list, is_loop=False)

    def update(self): pass

    def hit(self):
        self.timer.next_frame()
        if self.timer.is_expired():
            self.kill()

    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)