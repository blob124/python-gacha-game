import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Archive:
	def __init__(self,game):
		self.game = game

		self.images = {}
		togore_image_0 = pygame.image.load('data/togore.bmp').convert_alpha()
		togore_image_0 = pygame.transform.scale(togore_image_0, (72, 72))
		
		togore_image_1 = pygame.image.load('data/togorex464-T.png').convert_alpha()
		togore_image_1 = pygame.transform.scale_by(togore_image_1, (0.8, 0.8))
		
		one_image = pygame.image.load('data/images/numba1.png').convert_alpha()

		self.images['togore0'] = Image(togore_image_0,50,75)
		self.images['togore1'] = Image(togore_image_1,250,75)
		self.images['one'] = Image(one_image,750,110)

		self.buttons = {}
		self.buttons['buttonname'] = Button(None,pygame.Rect(200, 450, 100, 50),[(0,255,0),'TEXT HERE',(247,13,26),24],[(0,190,0),None,None,None])
		self.buttons['alsobuttonname'] = Button(None,pygame.Rect(400, 450, 100, 50),[(0,190,255),'TEXT HERE\n2',(247,13,26),24],[(0,144,190),'HOVERINGING',None,18])
		
	def handle_events(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					pass
				elif event.key == pygame.K_ESCAPE:
						self.game.change_scene(self.game.scenes['GachaPlace'])
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				if self.buttons['buttonname'].state == 1: # is Hover
					pass
				elif self.buttons['alsobuttonname'].state == 1:
					pass

	def update(self):
		for name,button in self.buttons.items():
			button.checkHover(self.game.mousepos)

	def draw(self, screen):		
		screen.fill((30, 100, 30))
		screen.blit(EXITTXT, (20, 20))

		for id,image in self.images.items():
			if id=='togore0':
				image.draw(screen,grayscale=True)
			else:
				image.draw(screen)

		for name,button in self.buttons.items():
			button.draw(screen)
		
		pygame.draw.line(screen, (255,255,255), (650,80), (650,520), 1)