from typing import Sequence, Union
import pygame, sys

from scripts.dungeon.dungeon import dungeon
from pygame.sprite import Sprite
from scripts.support import *
from scripts.fossils.fossil import *
from scripts.fossils.fossil import *
from scripts.enemy import Enemy
from scripts.inventory.inventory import *
from scripts.travelmap import *
from scripts.support import import_folder, spritesheet
from scripts.interaction.click_interact_point import *
from data.items.weapon import *
from scripts.entity import *
from scripts.transition import Transition
from scripts.map.tile import Tile
from scripts.npc import *
import data.items.items as items
from scripts.dungeon.dungeon import dungeon
from scripts.ui import Ui

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.level.player.check_javelin('DOWN')
                if event.type == pygame.MOUSEBUTTONUP:
                    self.level.player.check_javelin('UP')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.level.inventory.open_inventory()
                    if event.key == pygame.K_v:
                        self.level.inventory.check_del_item()
                    if event.key == pygame.K_m:
                        self.level.map.open_menu()
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
        self.enemy_sprites = YSortCameraGroup()
        self.player = Player([self.visible_sprites],256,256,self.obstacle_sprites,self.create_attack,self.destroy_attack,self.throw_javelin)
        self.inventory = Inventory(self.player,[self.updateable_sprites],self.spawn_item)
        self.map = Travelmap(self.player,[self.updateable_sprites],self.move_player, self.transition)
        self.player.inventory = self.inventory
        self.ui = Ui()

        self.region = "egypt"
        self.in_dungeon = False

        #attack sprites
        self.current_attack = None
        self.camera_shake = pygame.Vector2(0,0)
        self.attack_sprites = pygame.sprite.Group()

        #dungeon transitions
        self.c_transition = None

        self.draw_map()
    def throw_javelin(self,vec):
        if self.current_attack:
            self.current_attack.throw(vec)
    def damage_player(self,damage):
        self.player.health -= damage
        self.camera_shake = pygame.Vector2(damage*10,damage*10)
    def load_dungeon(self,reward_scale):
        self.in_dungeon = True
        ndungeon = dungeon(reward_scale)
        dungeon_tiles = []
        tile_images = spritesheet('graphics/dungeons/floor/sheet.png')
        self.dungeon_tiles = []
        self.unload_map()
        self.c_transition = self.transition(3000)
    def dungeon_map(self):
        self.in_dungeon = True
        layouts = {
            'wall': import_csv_layout('dungeons/dungeonmap_floor_walls.csv'),
            'enemy': import_csv_layout('dungeons/dungeonmap_floor_enemies2.csv')
        } 
        graphics = {
            'walls': import_folder('dungeons/tiles'),
            'enemies': ['monkey','mummy'] 
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * 64
                        y = row_index * 64
                        if style == "boundary":
                            n = Tile((x,y),[self.obstacle_sprites],'invisible')
                            self.dungeon_tiles.append(n)
                        if style == 'enemy':
                            enemy_name = graphics['enemies'][int(col)]
                            print('enemy spawned')
                            Enemy(
                                [self.visible_sprites,self.enemy_sprites],
                                enemy_name,(x,y),
                                self.player,
                                self.damage_player,
                                self.obstacle_sprites)
    def unload_map(self):
        for tile in self.tiles:
            tile.kill()
        for entity in self.entities:
            entity.kill()
    def draw_map(self):
        layouts = {
            "can_fossil_spawn": import_csv_layout("map/csv/fossilpoints.csv"),
            "interact": import_csv_layout("map/csv/interactpoints.csv"),
            'boundary': import_csv_layout('map/csv/boundaries.csv'),
            'object': import_csv_layout('map/csv/enemypoints.csv'),
            'npc': import_csv_layout('map/csv/npcs.csv'),
            'items': import_csv_layout('map/csv/items.csv')
        } 
        graphics = {
            'objects': spritesheet('map/objects/objects.png')
        }
        self.tiles = []
        self.entities = []
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * 64
                        y = row_index * 64
                        if style == "boundary":
                            n = Tile((x,y),[self.obstacle_sprites],'invisible')
                            self.tiles.append(n)
                        if style == 'object':
                            if int(col) <= len(graphics['objects']):
                                surf = graphics['objects'][int(col)]
                                Tile((x,y), [self.visible_sprites,self.obstacle_sprites],'object',surf)
                                self.tiles.append(n)
                        if style == 'npc':
                            if col == '25':
                                d = Npc([self.visible_sprites,self.obstacle_sprites],'sphinx',pygame.Vector2(-200,200),self.player,self.load_dungeon)
                                self.entities.append(d)
    def create_attack(self):
        self.current_attack = weapon(self.player,[self.visible_sprites,self.attack_sprites])
    def destroy_attack(self):
        print('attacketh destroyeth')
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    def move_player(self, pos):
        self.player.rect.center = pos
    def transition(self,ticks):
        plrtransition = Transition(self.updateable_sprites,ticks)
        return plrtransition
    def spawn_item(self,item,pos):
        entityitem = Item_Entity([self.visible_sprites],item, self.player, self.inventory,pos)
    def checks(self):
        if self.c_transition != None:
            if self.c_transition.mode == 'done':
                self.dungeon_map()
                self.c_transition = None
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.enemy_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'abcdefg':
                            pass
                        else:
                            if self.current_attack:
                                self.current_attack.held = self.player.weapon_holdable
                                if not self.current_attack.held:
                                    target_sprite.get_damage(self.player)#,attack_sprite.sprite_type)
                                else:
                                    attack_sprite.shot = self.player.weapon_shot
                                    attack_sprite.shot_time = pygame.time.get_ticks()
                                    if attack_sprite.shot:
                                        target_sprite.get_damage(self.player)
                                        attack_sprite.kill()
    def update_attackables(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                attack_sprite.held = self.player.weapon_holdable
                if attack_sprite.held == True and not attack_sprite.shot:
                    attack_sprite.rect.center = self.player.rect.center
    def update(self):
        self.visible_sprites.custom_draw(self.player,self.in_dungeon,self.camera_shake)
        self.visible_sprites.update()
        self.updateable_sprites.update()
        self.ui.display(self.player)
        self.checks()
        self.player_attack_logic()
        self.update_attackables()
        self.attack_sprites.update()

class Player(Entity):
    def __init__(self,groups,x,y,obs_sprites,create_attack,destroy_attack,throwjav):
        super().__init__(groups)
        for group in groups:
            group.add(self)
        self.image = pygame.image.load("graphics/player/down_idle/1.png").convert_alpha()
        self.hitbox = self.image.get_rect()
        self.rect = self.hitbox.inflate(0,-10)
        self.movement_trail = [0,0]

        #movement
        self.direction = pygame.math.Vector2()
        self.speed = 6#self.card1.speed

        #stats
        self.health = 50
        self.max_health = 100
        self.stamina = 50
        self.max_stamina = 50
        self.attack_damage = 5

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        #inventory
        self.inventory = None
        self.bounding_items = []
        self.bounding_npcs = []

        #weapon
        self.weapon_index = 2
        self.weapon = list(items.swords)[self.weapon_index]
        self.weapon_holdable = False
        self.weapon_shot = False
        
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        self.throw_jav = throwjav

        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        self.picked_up_item = False
        self.pickup_time = None
        self.pickup_cooldown = 0

        #javelin
        self.javelin_down_pos = None
        self.javelin_up_pos = None

        self.javelin_down_pos_set = False
        self.javelin_up_pos_set = False


        #graphics
        self.import_player_assets()
        self.status = 'down_idle'

        self.sprite_type = "player"
        self.obstacle_sprites = obs_sprites
    def throw_javelin(self):
        if self.javelin_down_pos != None and self.javelin_up_pos != None:
            x_diff = self.javelin_down_pos[0] - self.javelin_up_pos[0]
            y_diff = self.javelin_down_pos[1] - self.javelin_up_pos[1]
            vec_diff = pygame.math.Vector2(x_diff,y_diff)
            print(vec_diff)
            self.throw_jav(vec_diff)
            self.weapon_shot = True
            self.javelin_down_pos = None
            self.javelin_up_pos = None
            self.javelin_down_pos_set = False
            self.javelin_up_pos_set = False

    def check_javelin(self, etype):
        print('a')
        if self.weapon_index == 2:
            if etype == 'DOWN' and self.javelin_down_pos_set == False:
                self.javelin_down_pos = pygame.mouse.get_pos()
                self.javelin_down_pos_set = True
            elif etype == 'UP' and self.javelin_up_pos_set == False:
                self.javelin_up_pos = pygame.mouse.get_pos()
                self.javelin_up_pos_set = True
                self.throw_javelin()
    def get_full_weapon_damage(self):
        base_damage = self.attack_damage
        weapon_damage = items.swords[self.weapon]['damage']
        return base_damage + weapon_damage
    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
            'up_idle': {
                'animation': 0,
                'frames': 0
            },
            'down_idle': {
                'animation': 0,
                'frames': 0
            },
            'left_idle': {
                'animation': 0,
                'frames': 0
            },
            'right_idle': {
                'animation': 0,
                'frames': 0
            },
            'up_walk': {
                'animation': 0,
                'frames': 0.1
            },
            'down_walk': {
                'animation': 0,
                'frames': 0.1
            },
            'left_walk': {
                'animation': 0,
                'frames': 0.1
            },
            'right_walk': {
                'animation': 0,
                'frames': 0.1
            },
            'down_attack': {
                'animation': 0,
                'frames': 0.1
            },
            'right_attack': {
                'animation': 0,
                'frames': 0.1
            }
            }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation]['animation'] = import_folder(full_path)
            if self.animations[animation]['frames'] == 0:
                self.animations[animation]['frames'] = determine_anim_speed(full_path)
        #equip animation
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
                    self.status = self.status.replace('_idle','_attack')
                elif 'walk' in self.status:
                    self.status = self.status.replace('_walk','_attack')
                else:
                    self.status = self.status + "_attack"
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','_idle')
    def go_to(self, location):
        self.rect.center = location
    def input(self):
        self.movement_trail[0] - 0.02
        self.movement_trail[1] - 0.02
        k_down = pygame.key.get_pressed()
        mouse_down = pygame.mouse.get_pressed()
        self.direction = pygame.math.Vector2()  
        if mouse_down[0] == 1:
            if self.weapon_index == 2:
                self.javelin_down_pos = pygame.mouse.get_pos()
        if k_down[pygame.K_w]:
            self.direction.y = self.speed * -1
            self.movement_trail[1] = -10
            self.status = 'up_walk'
        elif k_down[pygame.K_s]:
            self.direction.y = self.speed
            self.movement_trail[1] = 10
            self.status = 'down_walk'
        if k_down[pygame.K_a]:
            self.direction.x = self.speed * -1
            self.status = 'left_walk'
        elif k_down[pygame.K_d]:
            self.direction.x = self.speed
            self.status = 'right_walk'
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * self.speed
        self.collision("horizontal")
        self.rect.y += self.direction.y * self.speed
        self.collision("vertical")

        if k_down[pygame.K_q] and not self.attacking:
            self.weapon_shot = False
            if not self.weapon_holdable:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
            self.create_attack()
            print(self.inventory)
        
        if k_down[pygame.K_f]:
            for item in self.bounding_items:
                if item.item.hasbeenpickedup == False:
                    self.inventory.add_item(item.item)
                    item.hasbeenpickedup = True
                    item.kill()
            npce = False
            for npc in self.bounding_npcs:
                if not npce:
                    npc.open()
                    npce = True
        
        if self.can_switch_weapon == True:
            if k_down[pygame.K_1]:
                self.can_switch_weapon = False
                self.weapon_holdable = False
                self.weapon_index = 0
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon = list(items.swords.keys())[self.weapon_index]
            if k_down[pygame.K_2]:
                self.can_switch_weapon = False
                self.weapon_holdable = False
                self.weapon_index = 1
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon = list(items.swords.keys())[self.weapon_index]
            if k_down[pygame.K_3]:
                self.weapon_holdable = True
                self.weapon_index = 2
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon = list(items.swords.keys())[self.weapon_index]
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking and not self.weapon_holdable:
            if current_time - self.attack_time >= self.attack_cooldown + items.swords[self.weapon]['cooldown']:
                self.attacking = False
                self.weapon_can_equip = False
                self.destroy_attack()
        
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        
        if self.weapon_holdable:
            if 'attack' in self.status:
                self.status.replace('_attack','_holding')
            else:
                if 'idle' in self.status:
                    self.status.replace('_idle','_holding')
    def animate(self):
        animation = self.animations[self.status]['animation']
        animation_speed = self.animations[self.status]['frames']

        #loop over frames
        self.frame_index += animation_speed
        #if animation complete
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if "attack" in self.status:
                self.attacking = False
                self.weapon_equipped = False

        #set the image
        self.image = animation[int(self.frame_index)]
        self.hitbox = self.image.get_rect(center = self.rect.center)
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

        self.floor_surf = pygame.image.load('map/floor/spawn island.png').convert_alpha()
        self.floor_surf = pygame.transform.scale(self.floor_surf, (8000,8000))
        self.floor_rect = self.floor_surf.get_rect(center = (0,0))

        self.dungeon_floor_surf = pygame.image.load('dungeons/dungeonmap.png').convert_alpha()
        self.dungeon_floor_surf = pygame.transform.scale(self.dungeon_floor_surf,(2000,2000))
        self.dungeon_floor_rect = self.dungeon_floor_surf.get_rect(center =(0,0))
    def custom_draw(self,player, in_dungeon,camera_shake):
        #set offsets
        self.offset.x = player.rect.centerx - self.half_width + camera_shake.x
        self.offset.y = player.rect.centery - self.half_height + camera_shake.y

        floor_offset_pos = self.floor_rect.topleft - self.offset
        dungeon_floor_offset_pos = self.dungeon_floor_rect.topleft - self.offset
        if not in_dungeon:
            self.display_surface.blit(self.floor_surf,floor_offset_pos)
        else:
            self.display_surface.blit(self.dungeon_floor_surf,dungeon_floor_offset_pos)

        for sprite in self.sprites():
            if "top" in sprite.sprite_type:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image,offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            if "Fixed" in sprite.sprite_type:
                self.display_surface.blit(sprite.image,sprite.rect)
            elif "Unrendered" in sprite.sprite_type:
                pass
            else:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image,offset_pos)
                sprite.renderedposition = offset_pos

if __name__ == "__main__":
    game = Game().run()
    #run!
    #test?
    #testing