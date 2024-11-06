import pygame 
from pygame import mixer
pygame.init()
mixer.init()

running = True
screen_width = 600
screen_height = 780
black = (0,0,0,255)
fps = 60
timer = pygame.time.Clock()
game_font = pygame.font.Font(r'doodle_rs/doodlejump_v2.ttf', 60)
game_font_small = pygame.font.Font(r'doodle_rs/doodlejump_v2.ttf', 30)
gravity = 1
MAX_PLATFORMS = 15
SCROLL_THRESH = 350
scroll = 0
game_over_y = screen_height
bg_y = 0
player_y = - 5
score = 0
high_score = 0
sensitivity = 1
spawn_time = 2500
is_fail = True
is_hit = True

#VOLUME :
j_volume = 0.4
jump_fx = pygame.mixer.Sound(r'doodle_rs/jumpp.wav')
jump_fx.set_volume(j_volume)

monster_fx = pygame.mixer.Sound(r'doodle_rs/monster_sound.mp3')
monster_fx.set_volume(0.2)
crash_fx = pygame.mixer.Sound(r'doodle_rs/monster_crash.mp3')

shoot_fx = pygame.mixer.Sound(r'doodle_rs/shoot.mp3')
shoot_fx.set_volume(0.2)

fail_fx = pygame.mixer.Sound(r'doodle_rs/fail.mp3')
fail_fx.set_volume(0.2)
hit_fx = pygame.mixer.Sound(r'doodle_rs/hit.wav')
hit_fx.set_volume(0.2)

click_fx = pygame.mixer.Sound(r'doodle_rs/click.mp3')
click_fx.set_volume(0.1)

#STATUS :
main_status = True
gameplay_status = False
button_pressed_time = None
arrow_pressed_time = None
option_status = False
game_over = False

#SCREEN_DETAILS :
screen = pygame.display.set_mode((screen_width,screen_height))
icon = pygame.image.load(r'doodle_rs/doodler.png').convert_alpha() 
pygame.display.set_icon(icon)
pygame.display.set_caption('Doodle Jump')



#BACKGROUND :
main_background = pygame.image.load(r'doodle_rs/main_bg.jpg')
main_background = pygame.transform.scale(main_background,(600,800))

game_background = pygame.image.load(r'doodle_rs/background.png')
game_background = pygame.transform.scale(game_background, (600,800))


#Player :
doodler = pygame.image.load (r'doodle_rs/doodler.png').convert_alpha()
doolder_rect = doodler.get_rect(center=(200,player_y))
doodler_fail = pygame.transform.rotate(doodler, 90)
doodler_shoot = pygame.image.load(r'doodle_rs/doodler_shoot.png').convert_alpha()
doodler_shoot = pygame.transform.scale(doodler_shoot, (40, 68 ))


#PLATFORM :
platform_img = pygame.image.load(r'doodle_rs/platform.png').convert_alpha()
platform_img = pygame.transform.scale(platform_img,(64,12))

move_platform_img = pygame.image.load(r'doodle_rs/move_platform.jpg').convert_alpha()
move_platform_img = pygame.transform.scale(move_platform_img,(64,12))


spring_platform_img = pygame.image.load(r'doodle_rs/platform-spring.png').convert_alpha()
spring_platform_img = pygame.transform.scale(spring_platform_img,(64,12))

platform_group = pygame.sprite.Group()


#Bullet :
bullet_img = pygame.image.load(r'doodle_rs/bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, ( 15 , 15) )
bullet_group = pygame.sprite.Group()

#Monster :
monster1_img = pygame.image.load (r'doodle_rs/monster1.png').convert_alpha()
monster1_img = pygame.transform.scale(monster1_img, (90,75))

monster2_img = pygame.image.load (r'doodle_rs/monster2.png').convert_alpha()
monster2_img = pygame.transform.scale(monster2_img, (90,75))

monster3_img = pygame.image.load (r'doodle_rs/monster3.png').convert_alpha()
monster3_img = pygame.transform.scale(monster3_img, (90,75))

monster_group = pygame.sprite.Group()
monster_images = [monster1_img, monster2_img, monster3_img]