import pygame, time

class Logbook:
  def __init__(self):
    super().__init__()
    self.image = pygame.image.load("graphics/gui/logbook.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.clicked = False
    self.action = False
  def click(self):
    mousepoint = pygame.mouse.get_pos()
    if self.rect.collidepoint(mousepoint):
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        self.action = True

    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False
      self.action = False
    return self.action
  def draw(self):
    pygame.display.get_surface().blit(self.image,self.rect)
  def update(self):
    self.click()
    self.draw()

class Logbook_Menu:
  def __init__(self):
    super().__init__()
    self.image = pygame.image.load("graphics/gui/logbook_menu.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.xvisible = False
    self.rvisible = False
  def draw(self):
    self.xvisible = Logbook().click()
    if self.xvisible == True:
      if self.rvisible == True:
        self.rvisible = False
      if self.rvisible == False:
        self.rvisible = True
    if self.rvisible == True:
      pygame.display.get_surface().blit(self.image,self.rect)
  def update(self):
    self.draw()