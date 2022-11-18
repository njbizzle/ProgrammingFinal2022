from worldmap import worldmap
import pygame, math

HEIGHT = 900
WIDTH = 1600
RENDER_BUFFER = 10

CAMERA_LINE_WIDTH = 1
CAMERA_LINE_COLOR = (0,0,0)

def convert_wm_surf(surf, wm_scale):
    surf_size = surf.get_size()
    return pygame.transform.scale(surf, (surf_size[0]* wm_scale, surf_size[1]* wm_scale))

def convert_wm_rect(rect, wm_scale, wall_l, wall_t):
    rect_pos = rect.topleft
    return pygame.Rect((wm_scale*(-wall_l + rect_pos[0]), wm_scale*(wall_t - rect_pos[1])), (rect.w*wm_scale, rect.h*wm_scale))

def convert_wm_sprite(sprite, wm_scale, wall_l, wall_t):
    new_surf = convert_wm_surf(sprite.surf, wm_scale)
    new_rect = convert_wm_rect(sprite.rect, wm_scale, wall_l, wall_t)
    return [new_surf, new_rect]
    
class Empty_sprite(pygame.sprite.Sprite):
    def __init__(self, surf, rect):
        super().__init__()
        self.surf = surf
        self.rect = rect

class Camera:
    def __init__(self):
        pass

    def get_displayed_sprites(self, pos_ws, size, wm_scale, use_rect_colliders = False, render_everything = False, show_lines = False):
        if wm_scale < 1:
            wm_scale = 1

        display_tile_h = size.x/wm_scale
        display_tile_w = size.y/wm_scale

        wall_l = (pos_ws.x - display_tile_h/2)
        wall_l_render = (pos_ws.x - display_tile_h/2) - RENDER_BUFFER

        wall_r = (pos_ws.x + display_tile_h/2)
        wall_r_render = (pos_ws.x + display_tile_h/2) + RENDER_BUFFER

        wall_b = (pos_ws.y - display_tile_w/2)
        wall_b_render = (pos_ws.y - display_tile_w/2) - RENDER_BUFFER
        
        wall_t = (pos_ws.y + display_tile_w/2)
        wall_t_render = (pos_ws.y + display_tile_w/2) + RENDER_BUFFER

        # gets [surface, position in wm]
        if render_everything:
            visable_sprites_wm = worldmap.get_all_sprites()
        elif use_rect_colliders:
            camera_rect = pygame.Rect(wall_l, wall_t, wall_r-wall_l, wall_t-wall_b) # uses rect collision
            visable_sprites_wm = worldmap.get_object_in_rect(camera_rect)
        else:
            visable_sprites_wm = worldmap.get_objects_in_tile_range((wall_l_render,wall_r_render),(wall_b_render,wall_t_render))

        visable_sprites_camera = []

        if show_lines:
            for hor_line_pos in range(math.floor(wall_b), math.ceil(wall_t)):
                line_surf = pygame.Surface((WIDTH, CAMERA_LINE_WIDTH))
                line_surf.fill(CAMERA_LINE_COLOR)

                line_rect = pygame.Rect(0, wm_scale*(wall_t - hor_line_pos), 0, 0)
                visable_sprites_camera.append(Empty_sprite(line_surf, line_rect))

                for vert_line_pos in range(math.floor(wall_l), math.ceil(wall_r)):
                    line_surf = pygame.Surface((CAMERA_LINE_WIDTH, HEIGHT))
                    line_surf.fill(CAMERA_LINE_COLOR)

                    line_rect = pygame.Rect(wm_scale*(-wall_l + vert_line_pos), 0, 0, 0)
                    visable_sprites_camera.append(Empty_sprite(line_surf, line_rect))

        # convert to position on camera
        for sprite in visable_sprites_wm:
            new_surf, new_rect = convert_wm_sprite(sprite, wm_scale, wall_l, wall_t)
            visable_sprites_camera.append(Empty_sprite(new_surf, new_rect))

        return visable_sprites_camera # sprite class containing all the surfaces and their postion the camera

camera = Camera()