import random
from variables import *
from objects import Button, Platform, Bullets, Monster
from pygame import mixer

pygame.init()
mixer.init()


#DRAW TEXT :
def draw_text(text, font, color, x, y):
    img = font.render(text, True, black )
    screen.blit (img, (x,y) )

class Player():
    def __init__ (self, x , y):
        self.shoot = False
        self.image = doodler
        self.rect = pygame.Rect(0,0, 32 , 47)
        self.rect.center = (x,y)
        self.vel_y = 0
        self.flip = False
        self.last_shot = pygame.time.get_ticks()
    

    def draw(self) :
        if self.image == doodler_shoot :
            screen.blit(self.image, (self.rect.centerx - 20, self.rect.centery - 42) )

        else :

            if self.flip == False :
                screen.blit(self.image, self.rect )
            if self.flip == True :
                    screen.blit(pygame.transform.flip(self.image, True, False), (self.rect.centerx - 32 , self.rect.centery - 22 ))
        
        #pygame.draw.rect(screen, black, self.rect , 2)


    def move (self) :
        global sensitivity, game_over
        scroll = 0
        dy = 0
        dx = 0


        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] :
            dx -= 7 + sensitivity
            self.flip = True 
        if key[pygame.K_RIGHT] :
            dx += 7 + sensitivity
            self.flip = False

        #SHOOTING : 
        time_now = pygame.time.get_ticks()

        if key[pygame.K_SPACE] and time_now - self.last_shot > 250 :
            self.image = doodler_shoot
            shoot_fx.play()
            bullet = Bullets (self.rect.centerx, self.rect.top - 50 )
            bullet_group.add(bullet)
            self.last_shot = time_now

        if time_now - self.last_shot > 348 :
            self.image = doodler
    

        if self.rect.x > screen_width + 5 :
            self.rect.x = -5
        elif self.rect.x < -8 :
            self.rect.x = 600


        self.vel_y += gravity
        dy += self.vel_y 
    
        #PLATFORM COLLISION :
        for platform in platform_group :
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy , 40, 47 ) :
               if self.rect.bottom < platform.rect.centery :
                   if self.vel_y > 0 :    #falling 
                       self.rect.bottom = platform.rect.top
                       dy = 0
                       self.vel_y = -23
                       jump_fx.play()

        
        if self.rect.top <= SCROLL_THRESH :
            if self.vel_y < 0 :
                scroll = -dy
            
        #update player :
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll 

    


def main_menu():
    global main_status, gameplay_status, button_pressed_time, option_status
    screen.blit(main_background,(0,0))
    play_button_img = pygame.image.load (r'doodle_rs/play-button.png')
    play_button = Button( 'image', play_button_img, 90, 240, True, play_button_img.get_width(), play_button_img.get_height(), None)
    option_button = Button ('text', 'Options', 500, 750, True, None, None, 70 )
    if play_button.check_click():
        if button_pressed_time is None:  
            click_fx.play()
            button_pressed_time = pygame.time.get_ticks()  
        elif pygame.time.get_ticks() - button_pressed_time >= 50:  
            main_status = False
            gameplay_status = True
            button_pressed_time = None

    if option_button.check_click():
        if button_pressed_time is None:  
            click_fx.play()
            button_pressed_time = pygame.time.get_ticks()  
        elif pygame.time.get_ticks() - button_pressed_time >= 50:  
            main_status = False
            option_status = True
            button_pressed_time = None





#OPTIONS MENU : 
def options():

    global sensitivity, button_pressed_time, main_status, option_status, j_volume
    screen.blit (game_background, (0,0))
    draw_text('SENSITIVITY : ', game_font, black, 50, 250)
    draw_text (f'{int(sensitivity)}', game_font, black, 400, 250)

    arrow_img = pygame.image.load(r'doodle_rs/arrow.png')
    arrow_img = pygame.transform.scale(arrow_img, (50,50))
    arrow_down_img = pygame.transform.rotate(arrow_img, 180)
    
    up_arrow_button1 = Button('image', arrow_img, 500, 230, True, None, None, None )
    down_arrow_button1 = Button('image', arrow_down_img, 500, 300, True, None, None, None)
    back_button_1 = Button('text', 'Back', 60, 750, True, None, None, 60)

    draw_text('JUMP SOUND : ' ,game_font, black, 50, 430)
    On_button = Button('text', 'On', 400 , 460, True, None, None, 60 )
    Off_button = Button('text', 'Off', 500 , 460, True, None, None, 60 )

    #JUMP SOUND ON/OFF :
    if On_button.check_click() :
        if button_pressed_time is None:  
            click_fx.play()
            button_pressed_time = pygame.time.get_ticks()  
        elif pygame.time.get_ticks() - button_pressed_time >= 100:  
            jump_fx.set_volume(0.4)
            button_pressed_time = None

    if Off_button.check_click() :
        if button_pressed_time is None:  
            click_fx.play()
            button_pressed_time = pygame.time.get_ticks()  
        elif pygame.time.get_ticks() - button_pressed_time >= 100:  
            j_volume = 0
            jump_fx.set_volume(j_volume)
            button_pressed_time = None

    #INCREASE SENSITIVITY :
    if sensitivity < 10 :
        if up_arrow_button1.check_click():
            if button_pressed_time is None:  
                button_pressed_time = pygame.time.get_ticks()  
            elif pygame.time.get_ticks() - button_pressed_time >= 70:  
                sensitivity += 1
                button_pressed_time = None
    #DECREASE SENSITIVITY :
    if sensitivity > 1.5 :
        if down_arrow_button1.check_click():
            if button_pressed_time is None:  
                button_pressed_time = pygame.time.get_ticks()  
            elif pygame.time.get_ticks() - button_pressed_time >= 70:  
                sensitivity -= 1
                button_pressed_time = None

    

    #BACK CLICK :
    if back_button_1.check_click():
        if button_pressed_time is None:  
            click_fx.play()
            button_pressed_time = pygame.time.get_ticks()  
        elif pygame.time.get_ticks() - button_pressed_time >= 50:  
            option_status = False
            main_status = True
            button_pressed_time = None

    



jumpy = Player(300,700)

#create starting platform :
platform = Platform(265, 720, False)
platform_group.add(platform)



def game_reset():
    global score, scroll, jumpy, platform, player_y, game_over,spawn_time, is_fail, is_hit
    #reset game_variables :
    score = 0
    scroll = 0
    jumpy.rect.center = (300,700)
    platform_group.empty()
    platform = Platform(265, 720, False )
    platform_group.add(platform)
    player_y = -5
    bullet_group.empty()
    monster_group.empty()
    spawn_time = 2500
    is_fail = True
    is_hit = True
    game_over = False



#GAME LOOPS :
while running :
    timer.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
        
    

    if main_status == True:
        main_menu()

    if option_status == True :
        options()

    if gameplay_status == True :

        screen.blit(game_background, (0,bg_y))

        if game_over == False :

            #GENERATE PLATFORMS :
            if len(platform_group) < MAX_PLATFORMS :
                p_x = random.randint(0, screen_width - 60)
                p_y = platform.rect.y - random.choice([95, 110])
                p_y_2 = platform.rect.y - random.randint(90, 100)

                # Tạo ra nền tảng thứ hai
                if score < 1000:
                    platform_2 = Platform(p_x + 300, p_y_2, False)
                else:
                    random_X = random.choice([-300, -200, 200, 300])
                    p_moving = random.choice([True, False])
                    platform_2 = Platform(p_x + random_X, p_y_2, p_moving)

                platform_group.add(platform_2)

                # Tạo ra nền tảng đầu tiên
                platform = Platform(p_x, p_y, False)
                platform_group.add(platform)

        
            #SCROLL LINE :
            #pygame.draw.line(screen,black,(0, SCROLL_THRESH), (screen_width, SCROLL_THRESH))

            draw_text(f'{int(score)}'  ,game_font_small, black, 20, 5 )

            platform_group.update(scroll)
            bullet_group.update()

            #update score : 
            if scroll > 0 :

                score += scroll 
                if score > high_score :
                    high_score = score
            #draw platform :
            platform_group.draw(screen)

            jumpy.draw()
            scroll = jumpy.move()
            bullet_group.draw(screen)

            if score > spawn_time :
                x_monster = random.randint(70,screen_width - 70)
                monster = Monster( x_monster, -200 )
                monster_group.add(monster)
                monster.sound()
            
                spawn_time += random.randint(6000,8000)

            monster_group.update(scroll)
            monster_group.draw(screen)
            


            if jumpy.rect.top > screen_height :
                
                game_over = True

            for monster in monster_group :
                if jumpy.rect.colliderect(monster.rect):
                    crash_fx.play()
                    game_over = True
                    break 
        

        else :
            if is_fail :
                fail_fx.play()
                is_fail = False

            for monster in monster_group :
                monster.stop()

            if player_y < 750 :
                screen.blit(doodler, (jumpy.rect.centerx, player_y ))
                player_y += 15
            
            else :
                screen.blit(doodler_fail, (jumpy.rect.x, 747) )
                if is_hit  :
                    hit_fx.play()
                    is_hit = False
                #GAME INFO :
                draw_text('GAME OVER', game_font, black, 200 , 60 )
                draw_text('score : ', game_font, black, 170 , 180 )
                draw_text(f'{int(score)}' , game_font, black, 340 , 180 )
                draw_text('high score : ', game_font, black, 120, 270  )
                draw_text(f'{int(high_score)}', game_font, black, 380, 270 )



                #BUTTONS :
                play_again_img = pygame.image.load(r'doodle_rs/play-again-button.png').convert_alpha()
                play_again_button = Button('image',play_again_img, 330,500, True, 70, 70, None)
                Menu_button = Button('text', "MENU", 170 , 540, True, None, None, 70)


                if play_again_button.check_click() :
                    click_fx.play()
                    game_reset()

                if Menu_button.check_click() :
                    if button_pressed_time is None:  
                        click_fx.play()
                        button_pressed_time = pygame.time.get_ticks()  
                    elif pygame.time.get_ticks() - button_pressed_time >= 30:  
                        #status :
                        gameplay_status = False
                        main_status = True
                        button_pressed_time = None
                        #reset game_variables :
                        game_reset()
                        


        
            
            

    pygame.display.update()