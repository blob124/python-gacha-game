import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Settings:
	def __init__(page,game):
		page.game = game

		page.textboxABC = TextBox(pygame.Rect(250,250,400,40),(255,255,255),(0,0,0),0,'defaultText',(0,0,0),24)
		page.textboxABC.text['string'] = 'Hi pookie!!'
		page.textboxABC.renderText(True)

		page.buttons = {}
		page.buttons['buttonname'] = Interactable((200,450),
			[pygame.Rect(0,0,100,50),
				TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,255,0),text='TEXT HERE',textcolor=(247,13,26),textsize=24,aligncenter=True)],
			[pygame.Rect(0,0,100,50),
				TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,255,0),text='HOVERING',textcolor=(247,13,26),textsize=24,aligncenter=True)])
		page.buttons['alsobuttonname'] = Interactable((400,450),
			[pygame.Rect(0,0,100,50),
				TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,190,255),text='TEXT HERE\n2',textcolor=(247,13,26),textsize=24,aligncenter=True)],
			[pygame.Rect(0,0,100,50),
				TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,144,190),text='HOVERINGING',textcolor=(247,13,26),textsize=18,aligncenter=True)])

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

		if page.textboxABC.rect.collidepoint(page.game.mousepos):
			if page.textboxABC.box['boarderSize'] != 3:
				page.textboxABC.box['boarderSize'] = 3
				page.textboxABC.renderBox(True)
		else:
			if page.textboxABC.box['boarderSize'] != 0:
				page.textboxABC.box['boarderSize'] = 0
				page.textboxABC.renderBox(True)

	def draw(page, screen):		
		screen.fill((100, 100, 100))
		screen.blit(EXITTXT, (20, 20))

		page.textboxABC.draw(screen)
		for name,button in page.buttons.items():
			button.draw(screen)