import pygame, random
import sys
from scripts.inventory.gain_item import *
import main

class fossil(pygame.sprite.Sprite):
  def __init__(self, location, groups, fossil_size, details, player):
    super().__init__()
    for group in groups:
      group.add(self)
    self.fossil_size = fossil_size
    self.fossil = 0
    self.details = details
    self.maxstrength = 5
    self.plr = player
    self.strength = 5
    self.action_cooldown = 200
    self.image = pygame.image.load('graphics/artefacts/small_fossil.png')#(f'graphics/fossils/{fossil_size}.png')
    self.rect = self.image.get_rect()
    self.rect.center = location
    self.sprite_type = 'Fixaed'
    self.clicked = False
    self.action = False
  def choose_fossil(self):
    self.plr.inventory.add_item({'name': 'ching'})
    rand = random.randint(1,30)
    if rand <= 30:
      self.fossil = 'ammonite'
      gain_item("Ammonite")
  def cooldowns(self):
    current_time = pygame.time.get_ticks()

    if self.action:
        if current_time - self.action_time >= self.action_cooldown:
            self.action = False

  def uncover(self):
    self.strength -= 1
    print(self.strength)
    if self.strength <= 0:
      self.sprite_type = 'Unrendered'
      self.choose_fossil()
    self.action = False
  def check_click(self):
    mousepoint = pygame.mouse.get_pos()
    mouseclick = pygame.mouse.get_pressed()
    #print(self.rect)
    #print(self.renderedposition)
    if self.rect.collidepoint(mousepoint):
      if pygame.mouse.get_pressed()[0] and self.clicked == False:
        self.clicked = True
        self.action = True

    return self.action
  def show_health(self):
    print(f"im at {self.strength} health pls dont hurt me")
  def update(self):
    pygame.display.get_surface().blit(self.image,(self.rect.centerx - self.plr.rect.centerx, self.rect.centery - self.plr.rect.centery))
    #pygame.display.get_surface().blit(self.image,self.renderedrect)
    clicked = self.check_click()
    if clicked == True:
      self.uncover()
    if self.strength < self.maxstrength and self.strength > 0:
      self.show_health()