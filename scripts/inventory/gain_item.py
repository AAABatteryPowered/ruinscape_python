import pygame
import main

class gain_item(pygame.sprite.Sprite):
  def __init__(self, item):
    super().__init__()
    self.image = pygame.image.load('graphics/gui/logbook_menu.png')
    self.rect = self.image.get_rect()
    self.item = item
  def play_anim(self):
    main.Player.pick_up_item(self.item)
    #main.Player.pick_up_item(self.item)
  def update(self):
    pass