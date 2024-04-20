import pygame, sys
import pytweening as tween

from scripts.font import *
from data.items.items import item

class Location(pygame.sprite.Sprite):
  def __init__(self, data):
    super().__init__()
    self.data = data
    self.name = self.data['name']
    self.image = pygame.image.load(f'graphics/gui/travelmap/locations/{self.name}.png').convert_alpha()
    self.rect = self.image.get_rect()
    self.pos = self.data['pos']
    self.uptime = 5000
    
    self.hover_info = Hover_Widget(self.data)

class Hover_Widget(pygame.sprite.Sprite):
  def __init__(self, data):
    super().__init__()
    self.data = data
    self.image = pygame.image.load('graphics/gui/inventory/inventory_item_hover.png').convert_alpha()
    self.rect = self.image.get_rect()
    self.rendered_rect_pos = (20,20)
    self.font = Font('graphics/fonts/2.png',None)

    #data variables
    self.name = data['name']
  def render_text(self):
    self.font.render(pygame.display.get_surface(),self.name, self.rendered_rect_pos)


class Travelmap(pygame.sprite.Sprite):
  def __init__(self,player,groups, tp_player, transition):
    super().__init__(groups)
    self.player = player
    self.surface = pygame.display.get_surface()
    self.vs_sprites = groups[0]
    self.image = pygame.image.load("graphics/gui/travelmap/map_lowcont.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.center = (-600,pygame.display.get_surface().get_height()/2)
    #self.rect.size = (0,0)
    self.visible = False
    self.sprite_type = "Unrendered"
    self.font = Font('graphics/fonts/2.png',None)
    
    #funcs
    self.tp_player = tp_player
    self.transition = transition,None
    self.current_transition = None
    
    #map
    self.locations = list({
      Location({"name": "home", "pos": pygame.math.Vector2(0,0)}),
      Location({"name": "egypt", "pos": pygame.math.Vector2(1,200)})
    })

    self.tween = tween.easeOutCubic
    self.step = 0
    self.mode = 'off'

    self.inputs = True
  def open_menu(self):
    self.step = 0
    if self.mode == 'on':
      self.mode = 'out'
    elif self.mode == 'off':
      self.mode = 'in' 
      self.visible = True
  def set_item_hover_info(self, item):
    item.hover_info = Hover_Widget(item.item)
  def draw(self):
    if self.visible == True:

      if self.mode == "in":
        offset = 200 * (self.tween(self.step / 10))
        self.step += 0.05
        self.rect.x += offset
        if self.step >= 10:
          self.step = 0
        if self.rect.centerx >= pygame.display.get_surface().get_width()/2:
          self.step = 0
          self.rect.centerx = pygame.display.get_surface().get_width()/2
          self.mode = "on"
    
      if self.mode == "out":
        offset = 200 * (self.tween(self.step / 10))
        self.step += 0.05
        self.rect.x += offset * -1
        if self.step >= 10:
          self.step = 0
        if self.rect.centerx <= -pygame.display.get_surface().get_width()/2:
          self.step = 0
          self.rect.centerx = -pygame.display.get_surface().get_width()/2
          self.mode = "off"
          self.visible = False
      
      self.surface.blit(self.image,self.rect)
      self.font.render(pygame.display.get_surface(),'Travel Map', (300,20))
      x_offset = 300
      y_offset = 100
      count = 0
      for item in self.locations:
        item.rect.center = (x_offset,y_offset)
        self.surface.blit(item.image,item.rect.center)

        mousepoint = pygame.mouse.get_pos()
        if item.rect.collidepoint(mousepoint):
          if item.hover_info != None:
            self.surface.blit(item.hover_info.image,mousepoint)
            item.hover_info.rendered_rect_pos = mousepoint
            item.hover_info.render_text()
            if pygame.mouse.get_pressed()[0] == 1:
              self.visible = False
              self.mode = 'off'
              self.current_transition = self.transition(item.uptime)
              self.current_loc = item
          else:
            self.set_item_hover_info(item)

        if round(count/10,None) == count/10:
          x_offset += 200
        else:
          x_offset = 0
          y_offset += 100
        count += 1
  def find_current_item(self):
    mousepoint = pygame.mouse.get_pos()
    found_current_item = False
    for item in self.locations:
      if item.rect.collidepoint(mousepoint):
        self.current_item = item
        found_current_item = True
    
    if found_current_item != True:
      self.current_item = None
  def update(self):
    self.find_current_item()
    self.draw()
    if self.current_transition != None:
     if self.current_transition.mode == "done":
      self.tp_player(self.current_loc.pos)
  def gain_item(self,item):
    self.items.append(item)