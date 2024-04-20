import pygame
import random

from data.items.items import enemies

class dungeon:
  def __init__(self, rewardscale):
    self.floor_image = None
    self.width = 24
    self.height = 24

    #dungeon data
    self.reward_scale = rewardscale
    self.level = self.generate_level()
  def get_level_row(self):
    return  ['#'] * self.width
  def generate_level(self):
    #floor image algorithm
    data = {
      'wallCountdown': 300,
      'padding': 2,
      'x': int(self.width/2),
      'y': int(self.height/2)
    }

    level = [self.get_level_row() for _ in range(self.height)]
    
    while data['wallCountdown'] >= 0:
      x = data['x']
      y = data['y']

      if level[y][x] == '#':
        level[y][x] = ' '
        data['wallCountdown'] -= 1

      rand = random.randint(1,4)
      if rand == 1 and x > data['padding']:
        data['x'] -= 1
      if rand == 2 and x < self.width - 1 - data['padding']:
        data['x'] += 1
      if rand == 3 and y > data['padding']:
        data['y'] -= 1
      if rand == 4 and y < self.height - 1 - data['padding']:
        data['y'] += 1

    dungeon_enemies = []
    for i in range(self.reward_scale * 3):
      rand = 1#random.randint(1,1)
      if rand == 1:
        enemy = enemies['mummy']
        dungeon_enemies.append(enemy)
    
    for nx in range(2,self.width-2):
      for ny in range(2,self.height-2):
        if level[ny-1][nx] == '#' and level[ny][nx] == '#' and level[ny+1][nx] == ' ':
          level[ny-1][nx] = '-'
          level[ny][nx] = '-'
        if level[ny+1][nx] == '#' and level[ny][nx] == '#' and level[ny-1][nx] == ' ':
          level[ny][nx] = '-'

    for row in level:
      for i in range(0,len(row)-1):
        if row[i-1] == '#' and row[i] == '#' and row[i+1] == ' ':
          row[i] = '|'
        if row[i+1] == '#' and row[i] == '#' and row[i-1] == ' ':
          row[i] = '|'

    return level
