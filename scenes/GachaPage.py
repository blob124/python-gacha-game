import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class GachaPlace:
	def __init__(self,game):
		self.game = game

		self.status = 0 # 0:normal, 1:pull animation
		self.justroll = []
		self.buttons = {}
		self.buttons['roll1'] = Button(None,pygame.Rect(200, 450, 100, 50),[(255,255,0),'roll1',(247,13,26),40],[(190,190,0),None,None,None])
		self.buttons['goArchive'] = Button(None,pygame.Rect(880, 30, 50, 50),[(255,255,0),'Archive',(247,13,26),18],[(190,190,0),None,None,None])
		self.buttons['goOption'] = Button(None,pygame.Rect(970, 30, 50, 50),[(255,255,0),'Option',(247,13,26),18],[(190,190,0),None,None,None])
		
	def handle_events(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					pass
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				if self.status == 0:
					if self.buttons['roll1'].state == 1: # is Hover
						self.status = 1
					elif self.buttons['goArchive'].state == 1:
						self.game.change_scene(self.game.scenes['ArchivePage'])
					elif self.buttons['goOption'].state == 1:
						self.game.change_scene(self.game.scenes['OptionPage'])
				else:
					self.status = 0

	def update(self):
		for name,button in self.buttons.items():
			button.checkHover(self.game.mousepos)

	def draw(self, screen):
		screen.fill((130, 30, 30))

		for name,button in self.buttons.items():
			button.draw(screen)

		if self.status == 1:
			xt = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
			xt.fill((0, 0, 0, 100))
			screen.blit(xt,(0,0))

	def roll(self,rolls=1):
		pass
