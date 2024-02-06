import pygame

class Card1(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__()
        for group in groups:
            group.add(self)
        self.sprite_type = "Fixed"
        self.card_value = "Jump Dodge"
        self.active = False
        self.image = pygame.image.load("graphics/cards/jump_dodge_card.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 468
    def use(self):
        return 9
        if self.card_value != False:
            if self.card_value == "Jump Dodge":
                self.image = pygame.image.load("graphics/cards/empty_card.png").convert_alpha()
                if self.active == False:
                    self.speed = 9
                if self.active == True:
                    self.speed = 3
                return "Dodge"
    def input(self):
        k_down = pygame.key.get_pressed()
        if k_down[pygame.K_1]:
            used = self.use()
    def update(self):
        self.input()
        self.card_value = "Jump Dodge"

class Card2(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__()
        for group in groups:
            group.add(self)
        self.sprite_type = "Fixed"
        self.card_value = "Jump Dodge"
        self.image = pygame.image.load("graphics/cards/empty_card.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 468
    def attack(self):
        if self.card_value != False:
            if self.card_value == "Jump Dodge":
                self.image = pygame.image.load("graphics/cards/jump_dodge_card.png").convert_alpha()
                return "Dodge"
    def input(self):
        k_down = pygame.key.get_pressed()
        if k_down[pygame.K_1]:
            self.attack()
    def _update(self,cardval):
        self.input()
        self.card_value = cardval

