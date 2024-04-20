import pygame, random

items = {
  #item structure

  "moon pickle": {
    'name': 'moon pickle',
    'damage': 'legendary',
    'cooldown': '1',
    'rarity': 'legendary',
    'weight': '1',
    'index': 1000234,
    'price': 500,
    'inventory_data': {
      'image': pygame.image.load('graphics/items/Moon Sickle/full.png'),
      'rect': pygame.image.load('graphics/items/Moon Sickle/full.png').get_rect(),
      'hover_info': None
    }
  },
  "Mask of Tutankhamun": {
    'name': 'Mask of Tutankhamun',
    'damage': '5',
    'cooldown': '2',
    'rarity': 'legendary',
    'weight': '1',
    'index': 1356,
    'price': 3000,
    'inventory_data': {
      'image': pygame.image.load('graphics/artefacts/tutenkhamun.png'),
      'rect': pygame.image.load('graphics/artefacts/tutenkhamun.png').get_rect(),
      'hover_info': None
    }
  },
  'Egyptian Shorthand Dagger': {'name': 'Egyptian Shorthand Dagger','damage': 10,'cooldown': 0.6,'rarity': 'uncommon','weight': '1','index': 10002234,'price': 50,'inventory_data': {'image': pygame.image.load('graphics/items/Egyptian Shorthand Dagger/full.png'),'rect': pygame.image.load('graphics/items/Egyptian Shorthand Dagger/full.png').get_rect(),'hover_info': None}}
}

ids = []

class item:
  def __init__(self, item):
    super().__init__()
    self.item = item
    self.inv_data = self.item['inventory_data']
    self.image = items[item['name']]['inventory_data']['image'].convert_alpha()
    self.rect = self.image.get_rect()
    self.value = items[item['name']]['price']
    self.id = 0
    
    self.hasbeenpickedup = False

    self.locate_id()
  def locate_id(self):
    rand  = random.randint(1,10)
    if len(ids) > 0:
      for itemid in ids:
        if not itemid == rand:
          self.id = rand
          ids.append(rand)
        else:
          self.locate_id()
    else:
      self.id = rand

enemies = {
  'mummy': {'name': 'Mummy', 'health': 100, 'damage': 10, 'range': 100, 'cooldown': 0.75}
}

swords = {
  'moon pickle': {'style': 'melee', 'name': 'moon pickle','damage': 40,'cooldown': 1,'rarity': 'legendary','weight': '1','index': 1000234,'price': 500,'inventory_data': {'image': pygame.image.load('graphics/items/Moon Sickle/full.png'),'rect': pygame.image.load('graphics/items/Moon Sickle/full.png').get_rect(),'hover_info': None}},
  'Egyptian Shorthand Dagger': {'style': 'melee', 'name': 'Egyptian Shorthand Dagger','damage': 50,'cooldown': 0.6,'rarity': 'uncommon','weight': '1','index': 10002234,'price': 50,'inventory_data': {'image': pygame.image.load('graphics/items/Egyptian Shorthand Dagger/full.png'),'rect': pygame.image.load('graphics/items/Egyptian Shorthand Dagger/full.png').get_rect(),'hover_info': None}},
  'Javelin': {'style': 'pullback', 'name': 'Javelin','damage': 50,'cooldown': 1.5,'rarity':'rate','weight':'1','index':87123564,'price':300,'inventory_data': {'image': pygame.image.load('graphics/items/Javelin/main.png'),'rect': pygame.image.load('graphics/items/Javelin/main.png').get_rect(), 'hover_info': None}}
}
  #{ "name":"Backhand Longsword", "rarity":3, "lore":"Good luck concealing this behind your back!", "damage": 30, "cooldown":1, "range": 80 },
#  { "name":"Shattered Slabsword", "rarity": 2, "lore":"This sword hits like a brick!", "damage": 45, "cooldown": 2, "range": 70 },
 # { "name":"Moon Sickle", "rarity": 5, "lore": "Slice through your opponents with the smoothness of a moon crescent", "damage": 90, "cooldown":0.4, "range": 60 },
  #{ "name":"BONK™", "rarity": 4, "lore":"BONK™ is a certified masterpiece - CEO of BONK™ LLC", "damage": 200, "cooldown": 3.5, "range": 50}