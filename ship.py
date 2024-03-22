import pygame       #15
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self, ai_game):  #16
        """初始化飞船"""
        super().__init__()
        self.screen = ai_game.screen  #17
        self.settings = ai_game.settings  #30
        self.screen_rect = ai_game.screen.get_rect()  #18
        
        #加载飞船图像，获取外界矩形
        self.image = pygame.image.load('images/ship.bmp')  #19
        self.rect = self.image.get_rect()   #20
        
        #每艘飞船放中间底部
        self.rect.midbottom = self.screen_rect.midbottom   #21
        
        self.x = float(self.rect.x)  #31
        
        #移动标志
        self.moving_right = False   #26
        self.moving_left = False
     
     
    def update(self):
        """根据移动标志调整飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:  #33
            self.x += self.settings.ship_speed  #27   #31
        if self.moving_left and self.rect.left > 0:   #33
            self.x -= self.settings.ship_speed  #27   #31
            
            
        #更新rect对象
        self.rect.x = self.x  #32
        
    def blitme(self):    #22
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)
        
    def center_ship(self):  #69
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        
    
    
    