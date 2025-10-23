import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Party:
	def __init__(self,game):
		self.game = game

		self.images = {}
		char_0_icon = self.game.data['Man'].getIcon()
		char_0_art = self.game.data['Man'].getArt()
		
		#char_0_icon = pygame.transform.scale_by(char_0_icon, (0.8, 0.8))
		char_0_art = pygame.transform.scale_by(char_0_art, (0.5, 0.5))

		self.images['image0'] = Image(char_0_icon,50,75)
		self.images['image1'] = Image(char_0_art,150,300)

		self.buttons = {}
		self.buttons['buttonname'] = Button(None,pygame.Rect(200, 450, 60, 40),[(0,255,0),'TEXT HERE',(247,13,26),24],[(0,190,0),None,None,None])

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

	def update(self):
		for name,button in self.buttons.items():
			button.checkHover(self.game.mousepos)

	def draw(self, screen):		
		screen.fill((30, 30, 160))
		screen.blit(EXITTXT, (20, 20))

		for id,image in self.images.items():
			if id=='togore0':
				image.draw(screen,grayscale=True)
			else:
				image.draw(screen)

		for name,button in self.buttons.items():
			button.draw(screen)
		
		pygame.draw.line(screen, (255,255,255), (650,80), (650,520), 1)