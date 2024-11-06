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

    
