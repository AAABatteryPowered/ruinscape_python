import pygame, sys
from pygame.sprite import AbstractGroup
import pytweening as tween

class Item(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()

class Inventory(pygame.sprite.Sprite):
  def __init__(self,groups,controls):
    super().__init__()
    for group in groups:
      group.add(self)
    self.surface = pygame.display.get_surface()
    self.controls = controls
    self.image = pygame.image.load("graphics/gui/inventory/inventory_background.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.tween = tween.easeInCubic(1)
    self.visible = False
    self.sprite_type = ""
    self.items = []
    self.inputs = True
  def open_inventory(self):
    if self.visible == True:
      self.visible = False
    else:
      self.visible = True
  def draw(self):
    if self.visible == True:
      self.surface.blit(self.image,self.rect)
  def key_input(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        #if event.key == pygame.K_e:
        self.open_inventory()
  def update(self):
    self.draw()
    self.key_input()
  def gain_item(self,item):
    self.items.append(item)