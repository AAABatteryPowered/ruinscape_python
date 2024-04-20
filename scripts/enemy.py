import pygame

from scripts.entity import Entity
from data.enemies.enemylist import enemy_data
from scripts.support import *

enemy_data = {
  'mummy': {
    'health': 200,
    'damage': 100,
    'attack_type': 'slash',
    'attack_sound': 'none',
    'speed': 6,
    'resistance': 4,
    'attack_radius': 100,
    'range_radius': 400
  }
}

class Enemy(Entity):
  def __init__(self, groups, monster_name, pos, plr, damage_player, obs_sprites):

    #normal setup
    super().__init__(groups)
    self.sprite_type = 'enemy'
    self.status = 'move'

    self.found_player = False
    self.damage_player = damage_player

    self.obstacle_sprites = obs_sprites

    self.plr = plr
    self.name = monster_name
    print(monster_name)

    self.direction_x = ' '
    self.direction_y = ' '

    #graphics setup
    self.import_graphics()
    print(self.frame_index)
    print(self.animations)
    self.image = self.animations[self.status][self.frame_index]
    self.rect = self.image.get_rect(topleft = pos)
    self.hitbox = self.rect

    if monster_name in enemy_data:
      self.data = enemy_data[monster_name]
    else:
      print('no enemy found')
      self.data = enemy_data['skeleton']
    self.health = self.data['health']
    self.damage = self.data['damage']
    self.speed = self.data['speed']
    self.attack_range = self.data['attack_radius']
    self.activation_distance = self.data['range_radius']

    #player interaction
    self.can_attack = True
    self.attack_time = None
    self.attack_cooldown = 400

    #invincibility timer
    self.vulnerable = True
    self.hit_time = None
    self.invincibility_duration = 300
  def attack_cooldowns(self):
    if not self.can_attack:
      current_time = pygame.time.get_ticks()
      if current_time - self.attack_time >= self.attack_cooldown:
        self.can_attack = True
    
    if not self.vulnerable:
      current_time = pygame.time.get_ticks()
      if current_time - self.hit_time >= self.invincibility_duration:
        self.vulnerable = True
  def import_graphics(self):
    self.animations = {'move':[],'idle': [],'attack': []}
    character_path = f'graphics/entities/{self.name}/'
    for animation in self.animations.keys():
      full_path = character_path + animation
      print(full_path)
      print('yes')
      print(self.animations[animation])
      self.animations[animation] = import_folder(full_path)
      print(self.animations[animation])
    print(self.animations)
  def animate(self):
    animation = self.animations[self.status]

    self.frame_index += self.animation_speed
    if self.frame_index >= len(animation):
      if self.status == 'attack':
        self.can_attack = False
      self.frame_index = 0
    
    self.image = animation[int(self.frame_index)]
    self.rect = self.image.get_rect(center = self.rect.center)
  def get_player_distance_direction(self):
    enemy_vec = pygame.math.Vector2(self.rect.center)
    player_vec = pygame.math.Vector2(self.plr.rect.center)
    distance = (player_vec - enemy_vec).magnitude()

    if distance > 0:
      direction = (player_vec - enemy_vec).normalize()
    else:
      direction = pygame.math.Vector2()

    return (distance,direction)
  def get_damage(self,attack_type):
    #if attack_type == 'weapon':
    if self.vulnerable:
      self.health -= self.plr.get_full_weapon_damage()
      self.hit_time = pygame.time.get_ticks()
      self.vulnerable = False
  def check_death(self):
    if self.health <= 0:
      self.kill()
  def get_status(self):
    distance = self.get_player_distance_direction()[0]

    if distance <= self.attack_range and self.can_attack:
      if self.status != 'attack':
        self.frame_index = 0
      self.status = 'attack'
    elif distance <= self.activation_distance:
      self.status = 'move'
    else:
      self.status = 'idle'
  def actions(self):
    if self.status == 'attack':
      self.direction = pygame.math.Vector2()
      self.attack_time = pygame.time.get_ticks()
    elif self.status == 'move':
      self.direction = self.get_player_distance_direction()[1]
    else:
      self.direction = pygame.math.Vector2()
  def update(self):
    self.get_status()
    self.actions()
    self.move()
    self.animate()
    self.attack_cooldowns()
    self.check_death()
    print(self.health)