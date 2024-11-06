import pygame
import random
from pygame import mixer
from variables import *

mixer.init()
#DRAW TEXT :
def draw_text(text, font, color, x, y):
    img = font.render(text, True, black )
    screen.blit (img, (x,y) )



#BUTTONS:
class Button :
    def __init__(self, type ,content, x_pos, y_pos, enabled, width = None, height = None, font_size = 40):
        self.type = type
        self.content = content
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        if self.type == 'image':

            self.width = self.content.get_width()
            self.height = self.content.get_height()

        elif self.type == 'text':
            self.font_size = font_size
            

        self.draw()

    def draw(self ) :
        
        if self.type == 'image' :
            image_2 = pygame.transform.scale(self.content,(self.width - 20, self.height - 20) )
            if self.check_click() :
                screen.blit( image_2, (self.x_pos + 10, self.y_pos + 10 ) )
            else :
                screen.blit (self.content, (self.x_pos, self.y_pos)) 
        
        elif self.type == 'text' :
            self.font = pygame.font.Font(r'doodle_rs/doodlejump_v2.ttf', self.font_size )
            text_surface = self.font.render(self.content, True, black )  
            text_rect = text_surface.get_rect( center= (self.x_pos, self.y_pos) )

            if self.check_click() :
                self.font = pygame.font.Font(r'doodle_rs/doodlejump_v2.ttf', 50)
                text_surface_2 = self.font.render (self.content, True, black )
                screen.blit(text_surface_2, (self.x_pos - 40 , self.y_pos - 30 ))

            else :
                screen.blit(text_surface, text_rect)



    
    def check_click (self) :
        if self.type == 'image' :
            button_rect = pygame.rect.Rect( (self.x_pos, self.y_pos) , (self.width , self.height) )
            
        elif self.type == 'text':
            text_surface = self.font.render(self.content, True, black)
            text_rect = text_surface.get_rect( center= (self.x_pos, self.y_pos) )
            button_rect = text_rect

        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        return False



#PLATFORM
class Platform (pygame.sprite.Sprite) :
    def __init__ (self, x, y, moving ) :
        pygame.sprite.Sprite.__init__(self)
        self.moving = moving
        if self.moving == False :
            self.image = platform_img
        if self.moving == True :
            self.image = move_platform_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = random.choice([-1,1])
        self.move_counter = random.randint(0,50)

    def update (self, scroll ) :
        
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        
        #moving platform :
        if self.moving == True :
            self.move_counter += 1
            self.rect.x += self.direction

        #change direction :
        if self.move_counter >= 100 or self.rect.left < 5 or self.rect.right > 595 :
            self.direction *= -1
            self.move_counter = 0

        self.rect.y += scroll #scroll platform

        #delete platform out of screen :
        if self.rect.top > screen_height :
            self.kill()

        if self.rect.right > screen_width :
            self.kill()

        if self.rect.left < 0 :
            self.kill()
    


class Bullets (pygame.sprite.Sprite) :
    def __init__ (self, x, y ) :
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.travel_distance = 0

    def update(self):
        self.dy = -10
        if self.travel_distance < 250:
            self.rect.y += self.dy
            self.travel_distance += abs(self.dy)
        else:
            self.kill()
         

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_index = 0
        self.image = monster_images[self.image_index] 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_speed = 0.4  # Tốc độ animation ban đầu
        self.animation_counter = 0  # Bộ đếm animation
        self.animation_threshold = 4  # Ngưỡng đếm để cập nhật hình ảnh
        self.health = 3
        
    def sound(self) :
        
            monster_fx.play()

    def stop(self) :
            monster_fx.stop()

    def update(self, scroll):
        
        # Tăng bộ đếm animation
        self.animation_counter += self.animation_speed

        # Nếu bộ đếm vượt qua ngưỡng, cập nhật hình ảnh và đặt lại bộ đếm
        if self.animation_counter >= self.animation_threshold:
            self.image_index = (self.image_index + 1) % len(monster_images)
            self.image = monster_images[self.image_index]
            self.animation_counter = 0

        self.rect.y += scroll/2

        if self.rect.top > screen_height :
            self.kill()

        for bullet in bullet_group :
            if bullet.rect.colliderect(self.rect) :
                hit_fx.play()
                bullet.kill()
                self.health -= 1
                if self.health <= 0:
                    monster_fx.stop()
                    self.kill()
                break
        
