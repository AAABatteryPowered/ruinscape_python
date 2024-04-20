import pygame, random
import sys
import main
import scripts.player.go_to as goto

class click_interact_point(pygame.sprite.Sprite):
  def __init__(self, groups, location):
    super().__init__()
    for group in groups:
      group.add(self)
    self.image = pygame.image.load('map_art_template/template.png')
    self.rect = self.image.get_rect()
    self.rect.center = location
    self.renderedposition = 1
    self.sprite_type = ' '
    self.script = 1
    self.call = False

    self.action_time = 1

    self.clicked = False
    self.action = False
  def use(self):
    pass
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
  def update(self):
    self.call = False
    self.renderedrect = pygame.Rect(self.renderedposition.x,self.renderedposition.y,100,200)
    #pygame.display.get_surface().blit(self.image,self.renderedrect)
    clicked = self.check_click()
    if clicked == True:
      self.call = ["move_player",(1,20)]
      #self.use()