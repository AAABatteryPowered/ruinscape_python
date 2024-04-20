import pygame
import pytweening as tween

class Entity(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.frame_index = 0
    self.animation_speed = 0.1
    
    #movement
    self.speed = 10
    self.direction = pygame.Vector2()
  def move(self):
    if self.direction.magnitude() != 0:
        self.direction = self.direction.normalize()
    self.rect.x += self.direction.x * self.speed
    self.collision("horizontal")
    self.rect.y += self.direction.y * self.speed
    self.collision("vertical")
  def collision(self, direction):
    if direction == "horizontal":
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.x > 0 and self.direction.y > 0 or self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                if self.direction.x < 0 and self.direction.y < 0 or self.direction.x < 0:
                    self.rect.left = sprite.rect.right
    if direction == "vertical":
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom

class Item_Entity(pygame.sprite.Sprite):
    def __init__(self, groups, item, plr, inv, pos):
        super().__init__(groups)

        self.item = item
        self.image = self.item.image
        self.rect = self.item.rect
        self.rect.center = pos

        self.sprite_type = " "
        self.id = item.id
        self.picked_up = False

        self.plr = plr
        self.inv = inv

        self.tween = tween.easeInOutQuad
        self.step = 0
        self.dir = 1
        self.bob_range = 2
    def idle_tween(self):
        offset =  self.bob_range * (self.tween(self.step / self.bob_range) - 0.5)
        self.rect.y += offset * self.dir
        self.step += 0.1
        if self.step > self.bob_range:
            self.step = 0
            self.dir *= -1
    def collision(self):
        if self.plr.rect.colliderect(self.rect) and not self in self.plr.bounding_items:
            self.plr.bounding_items.append(self)
        else:
            if self in self.plr.bounding_items:
                self.plr.bounding_items.remove(self)
    def despawn(self):
        self.plr.bounding_items.remove(self)
        self.kill()
    def update(self):
        self.collision()
        self.idle_tween()