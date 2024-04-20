import pygame
import math
from data.items.items import swords

class weapon(pygame.sprite.Sprite):
  def __init__(self,player,groups):
    super().__init__(groups)
    direction = player.status.split('_')[0]

    self.weapon_type = swords[player.weapon]['style']
    self.held = False

    self.shot = False
    self.shot_time = None

    self.direction = pygame.math.Vector2()
    self.decay = 3

    #graphics
    if 'melee' in swords[player.weapon]['style']:
      full_path = f'graphics/items/{player.weapon}/{direction}.png'
      self.image = pygame.image.load(full_path).convert_alpha()
      self.unrotated_image = pygame.image.load(full_path).convert_alpha()
    elif 'pullback' in swords[player.weapon]['style']:
      full_path = f'graphics/items/{player.weapon}/main.png'
      self.image = pygame.image.load(full_path).convert_alpha()
      self.unrotated_image = pygame.image.load(full_path).convert_alpha()
    self.sprite_type = 'weapon'

    #placement
    if 'melee' in swords[player.weapon]['style']:
      if direction == 'right':
        self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
      elif direction == 'down':
        self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
      else:
        self.rect = self.image.get_rect(center = player.rect.center)
    elif 'pullback' in swords[player.weapon]['style']:
      self.rect = self.image.get_rect(center = player.rect.center)
  def throw(self, dist):
    if self.held == True:
      self.direction = pygame.math.Vector2(dist.x/3.5,dist.y/3.5)
      self.image = pygame.transform.rotate(self.unrotated_image,dist.angle_to(pygame.Vector2(0,1)) + 45 + 180)
      self.shot_time = pygame.time.get_ticks()
      self.shot = True
      self.held = False
  def cooldown(self):
    if self.shot:
      if pygame.time.get_ticks() - self.shot_time >= 3000:
        self.kill()
  def rot_center(self, image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
  def point_mouse(self):
    direction = pygame.Vector2(pygame.mouse.get_pos()[0] - self.rect.centerx, pygame.mouse.get_pos()[1] - self.rect.centery)
        # .as_polar gives you the polar coordinates of the vector,
        # i.e. the radius (distance to the target) and the angle.
    radius, angle = direction.as_polar()
    angle -= 45
    if not self.shot:
      newimg = self.rot_center(self.unrotated_image,-angle)
      self.image = newimg
      self.rect = self.image.get_rect(center=self.rect.center)
  def move(self):
    self.rect.x += self.direction.x
    self.rect.y += self.direction.y
  def update(self):
    self.move()
    self.cooldown()
    self.point_mouse()