import pygame          #37
from pygame.sprite import Sprite

class Bullet(Sprite):
    """飞船子弹"""
    
    def __init__(self,ai_game):
        """创建子弹对象"""
        super().__init__()
        self.screen = ai_game.screen    #38
        self.settings = ai_game.settings    #38
        self.color = self.settings.bullet_color  #38
        
        #在（0.0）创建子弹
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)  #39
        self.rect.midtop = ai_game.ship.rect.midtop   #40
        
        self.y = float(self.rect.y)               #41
        
    def update(self):                       #41
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y        
        
    def draw_bullet(self):                  #42
        pygame.draw.rect(self.screen,self.color,self.rect)
    