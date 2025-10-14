import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Settings:
	def __init__(self,game):
		self.game = game

		self.textboxABC = TextBox(pygame.Rect(250,250,400,40),bgcolor=(255,255,255),text=None,textcolor=(0,0,0),textsize=24)
		self.textboxABC.setText('Hi!')
		self.textboxABC.haveBoarder = True
		self.buttons = {}
		self.buttons['buttonname'] = Button(None,pygame.Rect(200, 450, 100, 50),[(0,255,0),'TEXT HERE',(247,13,26),24],[(0,190,0),'HOVERING',None,None])
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

		if self.textboxABC.rect.collidepoint(self.game.mousepos):
			self.textboxABC.haveBoarder = True
		else:
			self.textboxABC.haveBoarder = False

		self.textboxABC.update()

	def draw(self, screen):		
		screen.fill((30, 100, 160))
		screen.blit(EXITTXT, (20, 20))

		self.textboxABC.draw(screen)
		for name,button in self.buttons.items():
			button.draw(screen)