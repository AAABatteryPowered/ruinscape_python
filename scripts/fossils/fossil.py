import pygame, random
import sys
from scripts.inventory.gain_item import *
import main

class fossil(pygame.sprite.Sprite):
  def __init__(self, location, groups, fossil_size, details):
    super().__init__()
    for group in groups:
      group.add(self)
    self.fossil_size = fossil_size
    self.fossil = 0
    self.details = details
    self.maxstrength = 5
    self.strength = 5
    self.image = pygame.image.load('graphics/fossils/small_fossil.png')#(f'graphics/fossils/{fossil_size}.png')
    self.rect = self.image.get_rect()
    self.renderedposition = 1
    self.sprite_type = 'Fixaed'
    self.clicked = False
    self.action = False
  def choose_fossil(self):
    main.Player.pick_up_item(1,"ammont")
    gain_item("Ammonite")
    rand = random.randint(1,30)
    if rand <= 30:
      self.fossil = 'ammonite'
      gain_item("Ammonite")
  def uncover(self):
    self.strength -= 1
    print(self.strength)
    if self.strength <= 0:
      self.sprite_type = 'Unrendered'
      self.choose_fossil()
    self.action = False
  def check_click(self):
    mousepoint = pygame.mouse.get_pos()
    #print(self.rect)
    #print(self.renderedposition)
    if self.renderedrect.collidepoint(mousepoint):
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        self.action = True

    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False
    return self.action
  def show_health(self):
    print(f"im at {self.strength} health pls dont hurt me")
  def update(self):
    self.renderedrect = pygame.Rect(self.renderedposition.x,self.renderedposition.y,100,200)
    #pygame.display.get_surface().blit(self.image,self.renderedrect)
    clicked = self.check_click()
    if clicked == True:
      self.uncover()
    if self.strength < self.maxstrength and self.strength > 0:
      self.show_health()