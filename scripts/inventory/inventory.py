import pygame, sys
from pygame.sprite import AbstractGroup
import pytweening as tween

from scripts.font import *
from data.items.items import *

class Inventory_Item(pygame.sprite.Sprite):
  def __init__(self, data):
    super().__init__()
    self.data = data
    self.name = self.data['name']
    self.image = pygame.image.load(f'graphics/items/{self.name}/full.png').convert_alpha()
    self.rect = self.image.get_rect()
    self.item_index = 8
    
    self.hover_info = Inventory_Hover_Widget(self.data)

class Inventory_Hover_Widget(pygame.sprite.Sprite):
  def __init__(self, data):
    super().__init__()
    self.data = data
    self.image = pygame.image.load('graphics/gui/inventory/inventory_item_hover.png').convert_alpha()
    self.rect = self.image.get_rect()
    self.rendered_rect_pos = (20,20)
    self.font = Font('graphics/fonts/2.png',None)

    #data variables
    self.name = data['name']
    self.damage = data['damage']
    self.rarity = data['rarity']
  def render_text(self):
    self.font.render(pygame.display.get_surface(),self.name, self.rendered_rect_pos)
    self.font.render(pygame.display.get_surface(),f'Rarity {self.rarity}', (self.rendered_rect_pos[0],self.rendered_rect_pos[1] + 20))
    self.font.render(pygame.display.get_surface(),f'Damage {self.damage}', (self.rendered_rect_pos[0],self.rendered_rect_pos[1] + 40))


class Inventory(pygame.sprite.Sprite):
  def __init__(self,player,groups,drop_item):
    super().__init__(groups)
    self.player = player
    self.surface = pygame.display.get_surface()
    self.vs_sprites = groups[0]
    self.image = pygame.image.load("graphics/gui/inventory/inventory_background.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.tween = tween.easeInCubic(1)
    self.visible = False
    self.sprite_type = "Unrendered"
    self.font = Font('graphics/fonts/2.png',None)
    self.items = list({
      item(swords['Egyptian Shorthand Dagger']),
      item(items["Mask of Tutankhamun"])
})
    self.item_slots = [
      0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0
    ]
    self.inputs = True

    #funcs
    self.drop_item = drop_item

    self.current_item = None
    self.about_to_remove_item = None
  def open_inventory(self):
    if self.visible == True:
      self.visible = False
      self.sprite_type = " "
    else:
      self.visible = True
      self.sprite_type = "Fixed"
  def add_item(self,item):
    self.items.append(item)
    print("added item")
  def remove_item(self,item):
    removing_item = False
    for eitem in self.items:
      if eitem == item:
        removing_item = eitem
    
    if removing_item != False:
      self.items.remove(removing_item)
      self.drop_item(removing_item,self.player.rect.midleft)
      self.about_to_remove_item = None
  def set_item_hover_info(self, item):
    item.item['inventory_data']['hover_info'] = Inventory_Hover_Widget(item.item)
  def draw(self):
    if self.visible == True:
      self.surface.blit(self.image,self.rect)
      self.font.render(pygame.display.get_surface(),'Inventory', (300,20))
      x_offset = 300
      y_offset = 100
      count = 0
      for item in self.items:
        r_item = item.item
        inv_data = r_item['inventory_data']
        inv_data['rect'].center = (x_offset,y_offset)
        self.surface.blit(inv_data['image'],inv_data['rect'].center)
        self.item_slots[count] = inv_data

        mousepoint = pygame.mouse.get_pos()
        if inv_data['rect'].collidepoint(mousepoint):
          if inv_data['hover_info'] != None:
            self.surface.blit(inv_data['hover_info'].image,mousepoint)
            inv_data['hover_info'].rendered_rect_pos = mousepoint
            inv_data['hover_info'].render_text()
            if pygame.mouse.get_pressed()[0] == 1:
              self.visible = False
              self.player.weapon_index = r_item['index']
              self.current_item = item
          else:
            self.set_item_hover_info(item)

        if count == 7 or count == 14 or count == 21:
          x_offset = 300
          y_offset += 100
        else:
          x_offset += 100
        count += 1
  def check_del_item(self):
    if self.current_item != None:
      self.about_to_remove_item = self.current_item
      self.current_item = None
  def find_current_item(self):
    mousepoint = pygame.mouse.get_pos()
    found_current_item = False
    if self.visible:
      for iteme in self.items:
        inv_data = iteme.item['inventory_data']
        if inv_data['rect'].collidepoint(mousepoint):
          self.current_item = iteme
          found_current_item = True
    
    if found_current_item != True:
      self.current_item = None
  def update(self):
    self.find_current_item()
    self.draw()
    if self.about_to_remove_item != None:
      self.remove_item(self.about_to_remove_item)
  def gain_item(self,item):
    if len(self.items) < len(self.item_slots):
      for eitem in self.items:
        if not eitem.id == item.id:
          self.items.append(item)