import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surface = pygame.surface.Surface((64,64))):
        super().__init__()
        for group in groups:
            group.add(self)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos).inflate(0,-10)