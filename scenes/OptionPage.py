import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Settings:
		self.buttons['buttonname'] = Button(None,pygame.Rect(200, 450, 100, 50),[(0,255,0),'TEXT HERE',(247,13,26),24],[(0,190,0),'HOVERING',None,None])
		self.buttons['alsobuttonname'] = Button(None,pygame.Rect(400, 450, 100, 50),[(0,190,255),'TEXT HERE\n2',(247,13,26),24],[(0,144,190),'HOVERINGING',None,18])
	def __init__(page,game):
		page.game = game

		page.textboxABC = TextBox(pygame.Rect(250,250,400,40),(255,255,255),(0,0,0),0,'defaultText',(0,0,0),24)

		page.buttons = {}
		
	def handle_events(page, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					pass
				elif event.key == pygame.K_ESCAPE:
						page.game.change_scene(page.game.scenes['GachaPlace'])
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				if page.buttons['buttonname'].state == 1: # is Hover
					pass
				elif page.buttons['alsobuttonname'].state == 1:
					pass


	def update(page):
		for name,button in page.buttons.items():
			button.checkHover(page.game.mousepos)		

		if self.textboxABC.rect.collidepoint(self.game.mousepos):
			self.textboxABC.haveBoarder = True
		else:
			self.textboxABC.haveBoarder = False

		self.textboxABC.update()

	def draw(page, screen):		
		screen.fill((30, 100, 160))
		screen.blit(EXITTXT, (20, 20))

		page.textboxABC.draw(screen)
		for name,button in page.buttons.items():
			button.draw(screen)