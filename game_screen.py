from ui_objects import *
from camera import camera
from test_objects import Test_rect
from datetime import datetime
import math, noise

vec = pygame.math.Vector2

HEIGHT = 900
WIDTH = 1600
CAMERA_MIN, CAMERA_MAX = 0.01,10

non_camera_sprites = pygame.sprite.Group()

camera_pos_text = text("x: 0.0 y 0.0", (200,50), (0,0,0), get_font(30), non_camera_sprites)
camera_scale_text = text("scale: 0", (200,100), (0,0,0), get_font(30), non_camera_sprites)
objects_rendered_text = text("objects_rendered: 0", (200,150), (0,0,0), get_font(30), non_camera_sprites)

# button ui
next_screen_button_pressed = False
show_lines = False
render_all = False

def reset_button_click():
    game_screen_load()

def next_screen_button_click():
    global next_screen_button_pressed
    next_screen_button_pressed = True

def show_lines_click():
    global show_lines
    if show_lines:
        show_lines = False
        show_lines_button.update_text("show lines")
    else:
        show_lines = True
        show_lines_button.update_text("hide lines")


def render_all_click():
    global render_all
    if render_all:
        render_all = False
        render_all_button.update_text("render all")
    else:
        render_all = True
        render_all_button.update_text("render in camera")

reset_button = button("reset", rect=pygame.Rect((100,200), (200,50)), on_click=reset_button_click, group=non_camera_sprites)
next_screen_button = button("to title screen", rect=pygame.Rect((100,260), (200,50)), on_click=next_screen_button_click, group=non_camera_sprites)
show_lines_button = button("show lines", rect=pygame.Rect((100,320), (200,50)), on_click=show_lines_click, group=non_camera_sprites)
render_all_button = button("render all", rect=pygame.Rect((100,380), (200,50)), on_click=render_all_click, group=non_camera_sprites)

def game_screen_init():
    size = 100
    for rect_x in range(-size,size):
        for rect_y in range(-size,size):
            noise_color = (noise.pnoise2(rect_x/size,rect_y/size)+1)/2*255
            Test_rect(pygame.Rect((rect_x*100,rect_y*100), (100, 100)), (noise_color,noise_color,noise_color))

    Test_rect(pygame.Rect((0,0), (100, 100)), (255,0,0))
    Test_rect(pygame.Rect((-500,500), (100, 200)), (0,255,0))
    Test_rect(pygame.Rect((-250,200), (200, 100)), (0,0,255))
    Test_rect(pygame.Rect((-100,-50), (25, 25)), (0,0,0))
    Test_rect(pygame.Rect((400,-400), (300, 50)), (255,0,255))

def game_screen_load():
    global next_screen_button_pressed, camera_x, camera_y, camera_scale
    next_screen_button_pressed = False
    camera_x, camera_y, camera_scale = [0.0,0.0,1.000]

def game_screen_update():
    global next_screen_button_pressed, camera_x, camera_y, camera_scale

    keys_pressed = pygame.key.get_pressed()

    camera_move_speed = 10
    camera_scale_speed = 30

    if keys_pressed[pygame.K_LSHIFT]:
        camera_move_speed = 50
        camera_scale_speed = 10

    if keys_pressed[pygame.K_UP]:
        camera_y+=camera_move_speed
    if keys_pressed[pygame.K_DOWN]:
        camera_y-=camera_move_speed
    if keys_pressed[pygame.K_LEFT]:
        camera_x-=camera_move_speed
    if keys_pressed[pygame.K_RIGHT]:
        camera_x+=camera_move_speed

    if keys_pressed[pygame.K_z]:
        camera_scale = camera_scale*(1+1/camera_scale_speed)
    if keys_pressed[pygame.K_x]:
        camera_scale = camera_scale*(1-1/camera_scale_speed)
    
    if camera_scale < CAMERA_MIN:
        camera_scale = CAMERA_MIN
    if camera_scale > CAMERA_MAX:
        camera_scale = CAMERA_MAX

    reset_button.check_click()
    next_screen_button.check_click()
    show_lines_button.check_click()
    render_all_button.check_click()

    if next_screen_button_pressed == True:
        next_screen = get_screens()["title_screen"]
    else:
        next_screen = None
    
    all_sprites = pygame.sprite.Group()

    displayed_sprites = camera.get_displayed_sprites(vec(camera_x, camera_y),vec(WIDTH,HEIGHT), camera_scale, show_lines=show_lines, render_everything=render_all)
    for sprite in displayed_sprites:
        all_sprites.add(sprite)

    camera_pos_text.update_text(f"x: {round(camera_x,2)}, y {round(camera_y,2)}")
    camera_scale_text.update_text(f"scale: {round(camera_scale, 2)}")
    objects_rendered_text.update_text(f"objects_rendered: {len(all_sprites)}")

    for sprite in non_camera_sprites:
        all_sprites.add(sprite)

    return {"sprite_group":all_sprites, "next_screen":next_screen}

game_screen = screen("game_screen", game_screen_init, game_screen_load, game_screen_update)