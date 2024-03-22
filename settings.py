class Settings:
    """存储游戏所有的设置功能的类"""
    def __init__(self):
        """初始化游戏的设置"""
        self.screen_width = 1200       #12
        self.screen_height = 800
        self.bg_color = (230,230,230)
        #self.ship_speed = 3   #30
        #self.bullet_speed = 2.0   #36
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 15
        #self.alien_speed = 1.2
        self.fleet_drop_speed = 15  #62
        #self.fleet_direction = 1
        self.ship_limit = 3  #67
        
        self.speedup_scale = 1.1 #83
        self.speedup_scale3 = 1.2
        self.speedup_scale2 = 1.3
        self.alien_points = 50      #88
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings() #83
        
        
    def initialize_dynamic_settings(self): 
        self.ship_speed = 4.0
        self.bullet_speed = 2.5
        self.alien_speed = 2.0
        
        self.fleet_direction = 1
        
    def increase_speed(self):  #84
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale3
        self.alien_speed *= self.speedup_scale2
        self.alien_points = int(self.alien_points*self.score_scale)
        