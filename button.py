import pygame.font
import pygame as pg

DARK_GREEN = (57, 162, 64)
GREEN = (118, 182, 133) 
WHITE = (255, 255, 255)
BLUE = (61, 105, 171)
LIGHT_BLUE = (130, 182, 216)

class Button():
    def __init__(self, screen, msg, ul):
        self.screen = screen

        self.width, self.height = 220, 50
        self.color = BLUE
        self.text_color = WHITE
        self.font = pygame.font.SysFont(None, 48)
        self.ul = ul

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left, self.rect.top = ul[0], ul[1]

        self.image = self.font.render(msg, True, self.text_color, self.color)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center
        
        self.hovered_color = LIGHT_BLUE
        self.hover_image = self.font.render(msg, True, self.text_color, self.hovered_color)

    def draw(self):
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.image, self.image_rect)
        
        mouse_x, mouse_y = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            if self.color == BLUE:
                self.screen.fill(self.hovered_color, self.rect)
                self.screen.blit(self.hover_image, self.image_rect)

        
        
# class ScoreButton():
#     def __init__(self, screen, msg, ul):
#         self.screen = screen

#         self.width, self.height = 250, 50
#         self.color = BLUE
#         self.text_color = WHITE
#         self.font = pygame.font.SysFont(None, 48)
#         self.ul = ul

#         self.rect = pygame.Rect(0, 0, self.width, self.height)
#         self.rect.left, self.rect.top = ul[0], ul[1]

#         self.image = self.font.render(msg, True, self.text_color, self.color)
#         self.image_rect = self.image.get_rect()
#         self.image_rect.center = self.rect.center
        
#         self.hovered_color = LIGHT_BLUE
#         self.hover_image = self.font.render(msg, True, self.text_color, self.hovered_color)

#     def draw(self):
#         self.screen.fill(self.color, self.rect)
#         self.screen.blit(self.image, self.image_rect)
        
#         mouse_x, mouse_y = pg.mouse.get_pos()
#         if self.rect.collidepoint(mouse_x, mouse_y):
#             if self.color == BLUE:
#                 self.screen.fill(self.hovered_color, self.rect)
#                 self.screen.blit(self.hover_image, self.image_rect)
