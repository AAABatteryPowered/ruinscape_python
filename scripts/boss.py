import pygame

class Boss(pygame.sprite.Sprite):
    def __init__(self,groups,x,y):
        super().__init__()
        for group in groups:
            group.add(self)
        self.image = pygame.image.load("graphics/bosses/tangelo.png").convert_alpha()
        self.rect = self.image.get_rect()