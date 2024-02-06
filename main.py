from typing import Sequence, Union
import pygame, sys

from pygame.sprite import Sprite
from scripts.support import *
from scripts.fossils.fossil import *
from scripts.fossils.fossil import *
from scripts.inventory.inventory import *
from scripts.support import import_folder

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720),pygame.RESIZABLE)
        pygame.display.set_caption('Ruinscape')
        self.display_surface = pygame.display.get_surface()
        self.level = Level()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((245,245,245))
            self.level.update()
            pygame.display.update()
            pygame.time.delay(15)

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = YSortCameraGroup()
        self.updateable_sprites = SpriteGroup()
        self.fossil_sprites = YSortCameraGroup()
        self.player = Player([self.visible_sprites],256,256,self.obstacle_sprites)
        self.draw_map()
        self.controls = [
            pygame.K_e # open_inventory - 0
        ]
        self.inventory = Inventory([self.updateable_sprites],self.controls)
    def draw_map(self):
        layouts = {
            "fossilmap": import_csv_layout("map/map5.csv")
        } 
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * 64
                        y = row_index * 64
                        if style == "fossilmap":
                            #Tile((x,y),[self.visible_sprites],"invisible",)
                            fossil((x,y),[self.visible_sprites],'small',[])
    def update(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.updateable_sprites.update()

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surface = pygame.surface.Surface((64,64))):
        super().__init__()
        for group in groups:
            group.add(self)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos).inflate(0,-10)

class Player(pygame.sprite.Sprite):
    def __init__(self,groups,x,y,obs_sprites):
        super().__init__()
        for group in groups:
            group.add(self)
        self.image = pygame.image.load("graphics/player/down_idle/1.png").convert_alpha()
        self.hitbox = self.image.get_rect()
        self.rect = self.hitbox.inflate(0,-10)

        self.direction = pygame.math.Vector2()
        self.speed = 5#self.card1.speed
        self.health = 100
        self.stamina = 50

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        #graphics
        self.import_player_assets()
        self.status = 'up_idle'
        self.frame_index = 0
        self.animation_speed = 0.05

        self.sprite_type = "player"
        self.obstacle_sprites = obs_sprites
    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'up_idle': [],'down_idle': [],'left_idle': [],'right_idle': [], 'up_walk': [], 'down_walk': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            print(self.animations[animation])
    def get_status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                if 'walk' in self.status:
                    self.status = self.status.replace('_walk','_idle')
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    #override idle
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + "_attack"
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')
    def input(self):
        k_down = pygame.key.get_pressed()
        self.direction = pygame.math.Vector2()  
        if k_down[pygame.K_w]:
            self.direction.y = self.speed * -1
            self.status = 'up_walk'
        elif k_down[pygame.K_s]:
            self.direction.y = self.speed
            self.status = 'down_walk'
        if k_down[pygame.K_a]:
            self.direction.x = self.speed * -1
            self.status = 'left_idle'
        elif k_down[pygame.K_d]:
            self.direction.x = self.speed
            self.status = 'right_idle'
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * self.speed
        self.collision("horizontal")
        self.rect.y += self.direction.y * self.speed
        self.collision("vertical")

        if k_down[pygame.K_1] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("attack!")
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
    def animate(self):
        animation = self.animations[self.status]

        #loop over frames
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        #set the image
        self.image = animation[int(self.frame_index)]
        self.hitbox = self.image.get_rect(center = self.rect.center)
    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0 and self.direction.y > 0 or self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0 and self.direction.y < 0 or self.direction.x < 0:
                        self.rect.left = sprite.rect.right
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
    def health_bar(self):
        pass
        #self.display_surface = pygame.display.get_surface()
        #self.healthbarimage = pygame.image.load("graphics/gui/healthandstamina.png").convert_alpha()
        #self.healthbarimagerect = self.healthbarimage.get_rect()
        #self.healthoverlay = pygame.draw.rect(pygame.display.get_surface(),(255,0,0),(self.healthbarimage)) 

        #self.display_surface.blit(self.healthbarimage,self.healthbarimagerect)
    def pick_up_item(self, item):
        print(item)
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        #self.health_bar()

class Interact_Point(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__()
        for group in groups:
            group.add(self)
        self.image = pygame.image.load("graphics/buttons/interact.png")
        self.rect = self.image.get_rect()

class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        pass

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2 
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load('map/floor/spawn island.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            if sprite.sprite_type == "Fixed":
                self.display_surface.blit(sprite.image,sprite.rect)
            elif sprite.sprite_type == 'Unrendered':
                pass
            else:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image,offset_pos)
                sprite.renderedposition = offset_pos

if __name__ == "__main__":
    Game().run()