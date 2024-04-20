import pygame
from scripts.font import Font

class Ui():
  def __init__(self):
    self.display_surface = pygame.display.get_surface()
    self.font = ('graphics/fonts/2.png',None)

    self.health_bar_image = pygame.image.load('graphics/ui/healthbar_bg.png').convert_alpha()
    self.health_bar_rect = self.health_bar_image.get_rect(topleft=pygame.Vector2(10,10))

    self.stamina_bar_image = pygame.image.load('graphics/ui/healthbar_bg.png').convert_alpha()
    self.stamina_bar_rect = self.stamina_bar_image.get_rect(topleft=pygame.Vector2(10,100))
  def show_bar(self,current,max_amount,bg_rect,color):
    pygame.draw.rect(self.display_surface,'black',bg_rect)

    ratio = current/max_amount
    current_width = bg_rect.width * ratio
    current_rect = bg_rect.copy()
    current_rect.width = current_width

    pygame.draw.rect(self.display_surface,color,current_rect)
  def display(self, player):
    self.display_surface.blit(self.health_bar_image,self.health_bar_rect)
    self.show_bar(player.health,player.max_health,pygame.rect.Rect(self.health_bar_rect.x + 10,self.health_bar_rect.centery - 15,self.health_bar_rect.width-20,self.health_bar_rect.height-50),'red')
    self.show_bar(player.health,player.max_stamina,pygame.rect.Rect(self.health_bar_rect.x + 10,self.health_bar_rect.centery - 15,self.health_bar_rect.width-20,self.health_bar_rect.height-50),'red')