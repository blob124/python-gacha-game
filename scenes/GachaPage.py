import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class GachaPlace:
	def __init__(page,game):
		page.game = game

		page.status = 0 # 0:normal, 1:pull animation
		page.justroll = []
		page.buttons = {}
		page.buttons['roll1'] = SimpleButton(pygame.Rect(200,450,100,50),
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(255,255,0,255),text='roll1',textcolor=(247,13,26),textsize=40,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(190,190,0,255),text='roll1',textcolor=(247,13,26),textsize=40,aligncenter=True)]
		)
		page.buttons['roll10'] = SimpleButton(pygame.Rect(769,450,100,50),
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(255,255,0,255),text='roll10',textcolor=(247,13,26),textsize=40,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(190,190,0,255),text='roll10',textcolor=(247,13,26),textsize=40,aligncenter=True)]
		)

		
		page.buttons['goMission'] = SimpleButton(pygame.Rect(790,25,50,50),
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(255,255,0,255),text='Quest',textcolor=(247,13,26),textsize=18,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(190,190,0,255),text='Quest',textcolor=(247,13,26),textsize=18,aligncenter=True)]
		)
		page.buttons['goParty'] = SimpleButton(pygame.Rect(855,25,50,50),
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(255,255,0,255),text='Party',textcolor=(247,13,26),textsize=18,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(190,190,0,255),text='Party',textcolor=(247,13,26),textsize=18,aligncenter=True)]
		)
		page.buttons['goArchive'] = SimpleButton(pygame.Rect(920,25,50,50),
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(255,255,0,255),text='Archive',textcolor=(247,13,26),textsize=18,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(190,190,0,255),text='Archive',textcolor=(247,13,26),textsize=18,aligncenter=True)]
		)
		page.buttons['goOption'] = SimpleButton(pygame.Rect(985,25,50,50),
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(255,255,0,255),text='Option',textcolor=(247,13,26),textsize=18,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(190,190,0,255),text='Option',textcolor=(247,13,26),textsize=18,aligncenter=True)]
		)

	def handle_events(page, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					pass
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				if page.status == 0:
					if page.buttons['roll1'].state == 1: # is Hover
						page.roll(1)
						page.status = 1
					elif page.buttons['roll10'].state == 1:
						page.roll(10)
						page.status = 1
					elif page.buttons['goMission'].state == 1:
						page.game.change_scene(page.game.scenes['Missions'])
					elif page.buttons['goParty'].state == 1:
						page.game.change_scene(page.game.scenes['TeamUp'])
					elif page.buttons['goArchive'].state == 1:
						page.game.change_scene(page.game.scenes['ArchivePage'])
					elif page.buttons['goOption'].state == 1:
						page.game.change_scene(page.game.scenes['OptionPage'])
				else:
					page.status = 0
					page.justroll = []

	def update(page):
		for name,button in page.buttons.items():
			button.checkHover(page.game.mousepos)

		screen.fill((30, 100, 130))
	def draw(page):

		for name,button in page.buttons.items():
			button.draw(page.game.screen)

		if page.status == 1:
			layer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
			layer.fill((0, 0, 0, 100))
			screen.blit(layer,(0,0))
			page.showroll()

	def roll(page,rolls=1):
		pass
