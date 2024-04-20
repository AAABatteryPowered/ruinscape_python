import pygame
import pytweening as tween

class Transition(pygame.sprite.Sprite):
  def __init__(self, groups, time):
    super().__init__(groups)

    self.image = pygame.image.load("graphics/gui/transition_screen.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.center = (-640,360)
    self.dtime = pygame.time.get_ticks()

    self.delay = time
    self.tween = tween.easeInOutCubic
    self.mode = "in"

    self.step = 0
    self.dir = 1
  def draw(self):
    display_surf = pygame.display.get_surface()
    display_surf.blit(self.image, self.rect)
    if self.mode == "in":
      offset = 50 * (self.tween(self.step / 10))
      self.step += 0.05
      self.rect.x += offset
      if self.step >= 10:
        self.step = 0
      
      if self.rect.x >= 0:
        self.rect.x = 0
        self.mode = "done"
    
    if self.mode == "out":
      offset = 50 * (self.tween(self.step / 10))
      self.step += 0.05
      self.rect.x += offset
      if self.step >= 10:
        self.step = 0
      
      if self.rect.x >= 1280:
        self.rect.x = 1280
        self.mode = "done"
        self.kill()
      
  def duration(self):
    time = pygame.time.get_ticks()

    if time - self.dtime >= self.delay:
      self.mode = "out"
  def update(self):
    self.draw()
    self.duration()