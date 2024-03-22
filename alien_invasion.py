import sys     # py_1
from time import sleep  #67

import pygame

from settings import Settings #13
from game_stats import GameStats      #67
from ship import Ship                 #23
from bullet import Bullet             #43
from alien import Alien               #53
from button import Button
from scoreboard import Scoreboard      #89



class AlienInvasion:               # py_2
    """管理游戏资源的类"""
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('musics/music.ogg')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops = -1)
        
        self.clock = pygame.time.Clock()  # 10
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))  #py_3  #14
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)   #68
        self.ship = Ship(self)         #23
        self.bullets = pygame.sprite.Group()   #44
        self.aliens = pygame.sprite.Group() #54
        self.game_active = False      #71
        self.play_button = Button(self,"Play")   #77
        self.scoreboard1 = Scoreboard(self)    #89
        
        self._create_fleet()   #55
        
        #设置背景色
        #self.bg_color = (230,230,230)

    def run_game(self):   #4
        """游戏主循环"""
        print(1)
        while True:
            self._check_events()  #5
            if self.game_active:     #72
                self.ship.update() #29
                self._update_bullets()   #45  #48
                self._update_aliens()   #60
            self._update_screen() #7  #14
            self.clock.tick(60)  #11
            
    def _check_events(self):    #6
        """影响按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:   #25  #34
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:    #28   #34
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:  #78
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def _check_play_button(self,mouse_pos):  
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active: #79  #80
            self.settings.initialize_dynamic_settings()  #83
            self.stats.reset_stats()
            #self.stats.level = 1
            self.scoreboard1.prep_score()  #87
            self.scoreboard1.prep_level()
            self.scoreboard1.prep_ships()
            self.game_active = True
            
            self.bullets.empty()
            self.aliens.empty()
            
            self._create_fleet()
            self.ship.center_ship()
            
            pygame.mouse.set_visible(False) #81
            
                
                    
    def _check_keydown_events(self,event):   #34
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:    #35
            sys.exit()
        elif event.key == pygame.K_SPACE:  #46
            self._fire_bullet()
            
    def _check_keyup_events(self,event):  #34
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _fire_bullet(self):    #46
        if len(self.bullets)<self.settings.bullet_allowed: #50
            new_bullet = Bullet(self)   #47
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):  #45
        self.bullets.update()
        for bullet in self.bullets.copy():  #49
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()  #65
        
    def _check_bullet_alien_collisions(self):   #65
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        
        if collisions:  #89
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points*len(aliens)
            self.scoreboard1.prep_score()
            self.scoreboard1.check_high_score()
             
        if not self.aliens:     #66
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()  #85
            
            self.stats.level += 1
            self.scoreboard1.prep_level()
             
    def _update_aliens(self):    #61
        self.aliens.update()
        self._check_fleet_edges()   #64
        
        if pygame.sprite.spritecollideany(self.ship,self.aliens):  #70
            self._ship_hit()
            
        self._check_aliens_bottom()
        
    def _create_fleet(self):   #56
        alien = Alien(self)  
        alien_width ,alien_height = alien.rect.size  
        
        current_x,current_y = alien_width,alien_height
        while current_y <(self.settings.screen_height-3*alien_height):
            while current_x <(self.settings.screen_width - 2*alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2*alien_width   #57
            current_x = alien_width
            current_y += 2*alien_height
            
    def _create_alien(self,x_position,y_position): #58
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
       
    
    def _update_screen(self):       #8
        """更新屏幕上的图像，切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)    #14
        for bullet in self.bullets.sprites():  #48
            bullet.draw_bullet()
        self.ship.blitme()       #24
        self.aliens.draw(self.screen)#54
        self.scoreboard1.show_score()  #89
        if not self.game_active:   #77
            self.play_button.draw_button()
                    
        pygame.display.flip()     #让最近绘制的屏幕可见
        
        
    def _check_fleet_edges(self):   #64
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
            
    def _change_fleet_direction(self): #64
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
        
    def _ship_hit(self):   #69
        if self.stats.ships_left > 0:  #71
            self.stats.ships_left -= 1
            self.scoreboard1.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            
            self._create_fleet()
            self.ship.center_ship()
            
            sleep(1.5)
        else:   #71
            self.game_active = False
            pygame.mouse.set_visible(True) #82
        
    def _check_aliens_bottom(self):    #70
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
                    
if __name__ == '__main__':  #9
    ai = AlienInvasion()
    ai.run_game()



