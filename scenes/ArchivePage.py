import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Archive:
	def __init__(page,game):
		page.game = game

		page.images = {}
		char_0_icon = page.game.data['Man'].getIcon(bg=True)
		char_0_art = page.game.data['Man'].getArt()
		
		one_image = pygame.image.load('data/numba1.png').convert_alpha()
		one_image = pygame.transform.scale_by(one_image, (2, 0.2))

		page.images['image0'] = Image(char_0_icon,(50,75))
		page.images['image1'] = Image(char_0_art,(650,75))
		page.images['one'] = Image(one_image,(150,200))

		page.buttons = {}
		page.buttons['buttonname'] = SimpleButton(pygame.Rect(200,450,100,50),
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,255,0),text='TEXT HERE',textcolor=(247,13,26),aligncenter=True)],
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,255,0),text='HOVERING',textcolor=(247,13,26),aligncenter=True)]
		)

		page.buttons['alsobuttonname'] = SimpleButton(pygame.Rect(400,450,100,50),
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,190,255),text='TEXT HERE\n2',textcolor=(247,13,26),aligncenter=True)],
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,144,190),text='HOVERINGING',textcolor=(247,13,26),textsize=18,aligncenter=True)])

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

	def draw(page):
		page.game.screen.fill((30, 100, 30))
		page.game.screen.blit(EXITTXT, (20, 20))

		for id,image in page.images.items():
			image.draw(page.game.screen,grayscale=False)

		for name,button in page.buttons.items():
			button.draw(page.game.screen)
		
		pygame.draw.line(page.game.screen, (255,255,255), (650,80), (650,520), 1)