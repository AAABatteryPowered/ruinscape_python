from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter=",")
        for row in layout:
           terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    
    return surface_list

def import_dungeon_fold(path):
    surface_list = []
    count = 0

    order_count = 0
    #sort by name
    ordered_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            ggg = image.replace('.png','')
            intname = int(ggg)
            ordered_list.append(intname)

    for _,__,img_files in walk(path):
        for image in ordered_list:
            full_path = path + '/' + image +'.png'
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
#
 #   for _,__,img_files in walk(path):
  #      for image in img_files:
   #         full_path = path + '/' + image
    #        ggg = image.replace('.png','')
     #       image_surf = pygame.image.load(full_path).convert_alpha()
      #      surface_list[ggg] = image_surf
       #     count += 1
    
    print(f'here is thhhhhhhhhhhhhhhhhhhhhhhhhhe rendered surfaces{surface_list}')
    return surface_list

def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip()).convert_alpha()
    return image

def spritesheet(image_path):
    surfaces = {}

    character_count = 0
    count = 0

    x_offset = 0
    y_offset = 16

    tile_size = 64
    sheet_tile_size = 16

    image = pygame.image.load(image_path).convert_alpha()

    x = 0
    for ax in range(image.get_width()):
        if x/sheet_tile_size == round(x/sheet_tile_size):
            char_img = clip(image, x - tile_size, y_offset, tile_size, tile_size)
            surfaces[count] = char_img
            character_count += 1
            count += 1
        if x >= image.get_width():
            x = 0
            y_offset += tile_size
        x += 1
    
    print(surfaces)
    return surfaces

def determine_anim_speed(path):
    frames = 1
    speed = 0.6

    for _,__,img_files in walk(path):
        for image in img_files:
            frames += 1
    
    speed = (speed/frames) - 0.025
    
    return speed