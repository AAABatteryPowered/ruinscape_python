import pygame

from random import choice
from scripts.entity import Entity
from scripts.font import *
from data.items.items import *
from data.enemies.enemylist import enemy_data

npclines = {
  'sphinx': ['For one to enter the pyramids one must solve a riddle','Failing a riddle will lower your reward in the chambers!','Good luck!']
}

sphinxquestions = [['What is always coming but never arrives?',['Amazon Deliveries','Tomorrow','GTA 6'],1]]

class Npc(Entity):
  def __init__(self, groups, npc_name, pos, plr, open_dungeon):

    #normal setup
    super().__init__(groups)
    self.sprite_type = 'npc'
    self.lines = npclines[npc_name]
    self.line = 0
    self.currenttext = ' '
    self.line_duration = 2000
    self.text_speed = 1
    self.text_finished = False
    self.text_paused = False
    self.char_counter = 0
    self.decided = False
    self.activation_distance = 300
    self.read_time = pygame.time.get_ticks()
    self.reading = False
    self.chosen_question = None
    self.question_phase = False
    self.said_question = False
    self.plr = plr
    self.player_success = False
    self.done = False

    self.reward_scale = 7

    self.open_dungeon = open_dungeon

    #graphics setup
    self.image = pygame.image.load(f'graphics/npcs/{npc_name}.png').convert_alpha()
    self.rect = self.image.get_rect(topleft = pos)

    self.dialogue_image = pygame.image.load(f'graphics/npcs/{npc_name}_dialogue.png').convert_alpha()
    self.dialogue_rect = self.dialogue_image.get_rect(topleft=pygame.Vector2(50,400))
    self.font = Font('graphics/fonts/2.png',self.dialogue_rect.centerx + (self.dialogue_image.get_width() / 2))
  def collidey(self):
      x_distance = self.plr.rect.centerx - self.rect.centerx
      y_distance = self.plr.rect.centery - self.rect.centery
      outcome = False
      decided = False
      if y_distance > -self.activation_distance and y_distance < self.activation_distance:
        outcome = True
        decided = True
      elif y_distance < -self.activation_distance or y_distance < self.activation_distance:
        outcome = False
        decided = True
        self.text_finished = False
        self.question_phase = False
        self.chosen_question = None
        #self.response_line = False
      self.visible = outcome
      self.decided = decided
  def collidex(self):
      x_distance = self.plr.rect.centerx - self.rect.centerx
      y_distance = self.plr.rect.centery - self.rect.centery
      outcome = False
      decided = False
      if self.visible:
        if x_distance > -self.activation_distance and x_distance < self.activation_distance:
          if not decided:
            outcome = True
            decided = True
        elif x_distance < -self.activation_distance or x_distance < self.activation_distance:
          outcome = False
          decided = True
          self.text_finished = False
          self.question_phase = False
          self.chosen_question = None
        #self.response_line = False
        self.visible = outcome
        self.decided = decided
  def cooldown(self):
    current_time = pygame.time.get_ticks()

    if self.text_paused:
      if current_time - self.read_time >= self.line_duration:
        if self.line != None:
          self.text_paused = False
          self.line += 1
          self.char_counter = 0
  def choose_question(self):
    self.chosen_question = choice(sphinxquestions)
  def move_player(self):
    if self.player_success:
      self.open_dungeon(self.reward_scale)
      self.player_success = False
  def reply(self,success):
    if success:
      self.currenttext = 'Well done! You have chosen correctly and shall journey into the pyramids!'
      self.player_success = True
    else:
      self.currenttext = 'Rah! You have chosen incorrectly! You have been stripped of your anubis artifact and i banish you away for 5 minutes!'
      self.reward_scale -= 2
  def draw(self):
    if self.done:
      return
    if self.visible:
      pygame.display.get_surface().blit(self.dialogue_image,self.dialogue_rect)
      if not self.text_finished:
        if self.char_counter < self.text_speed * len(self.currenttext):
          self.char_counter += 1
        elif self.char_counter >= self.text_speed*len(self.currenttext):
          if self.text_paused == False:
            self.text_paused = True
            self.read_time = pygame.time.get_ticks()
          if self.line != None and not self.text_paused:
            self.line += 1
            self.char_counter = 0
          if self.currenttext == 'Well done! You have chosen correctly and shall journey into the pyramids!':
            self.visible = False
            self.done = True
          if self.currenttext == 'Rah! You have chosen incorrectly! You have been stripped of your anubis artifact and i banish you away for 5 minutes!':
            self.said_question = False
            self.choose_question()
        self.font.render(pygame.display.get_surface(),self.currenttext[0:self.char_counter//self.text_speed],self.dialogue_rect.topleft + pygame.Vector2(200,50))
      if self.question_phase:
        if self.chosen_question == None:
          self.choose_question()
          self.line = None
          self.currenttext = self.chosen_question[0]
          self.said_question = True
        else:
          if not self.said_question:
            self.currenttext = self.chosen_question[0]
            self.said_question = True
          offset = 0
          for answer in self.chosen_question[1]:
            btn_image = pygame.image.load('graphics/npcs/button.png').convert_alpha()
            btn_rect = btn_image.get_rect(topleft=pygame.Vector2(offset,200))
            pygame.display.get_surface().blit(btn_image,btn_rect)
            self.font.render(pygame.display.get_surface(),answer,btn_rect.topleft + pygame.Vector2(20,20))
            offset += 150
            mousepoint = pygame.mouse.get_pos()
            mousepress = pygame.mouse.get_pressed()
            if btn_rect.collidepoint(mousepoint):
              if mousepress[0] == 1:
                if answer == self.chosen_question[1][self.chosen_question[2]]:
                  self.reply(True)
                else:
                  self.reply(False)
    else:
      self.char_counter = 0
      self.line = 0
  def update(self):
    self.cooldown()
    self.collidey()
    self.collidex()
    self.move_player()
    self.draw()
    if self.line != None:
      if self.line < len(self.lines):
        self.currenttext = self.lines[self.line]
      else:
        self.question_phase = True
        self.char_counter = 0
        self.line = None

class Merchant(Entity):
  def __init__(self, groups, pos, plr):
    super().__init__(groups)

    self.sprite_type = 'npc'
    self.image = pygame.image.load('graphics/npcs/merchant.png').convert_alpha()
    self.rect = self.image.get_rect(topleft=pos)
    
    self.plr = plr

    self.bounding_range = 200
  def open(self):
    plr_value = 0
    for item in self.plr.inventory.items:
      plr_value += item.value
    for item in swords:
      pass

  def check_range(self):
    x_distance = self.plr.rect.centerx - self.rect.centerx
    y_distance = self.plr.rect.centery - self.rect.centery
    if x_distance > -self.bounding_range and x_distance < self.bounding_range:
      if not self in self.plr.bounding_npcs:
        self.plr.bounding_npcs.append(self)
    if y_distance > -self.bounding_range and y_distance < self.bounding_range:
      if not self in self.plr.bounding_npcs:
        self.plr.bounding_npcs.append(self)
  def update(self):
    self.check_range()