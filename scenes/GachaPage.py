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
		page.buttons['roll1'] = Button(None,pygame.Rect(200, 450, 100, 50),[(255,255,0),'roll1',(247,13,26),40],[(190,190,0),None,None,None])
		page.buttons['goMission'] = Button(None,pygame.Rect(790, 25, 50, 50),[(255,255,0),'Quest',(247,13,26),18],[(190,190,0),None,None,None])
		page.buttons['goParty'] = Button(None,pygame.Rect(855, 25, 50, 50),[(255,255,0),'Party',(247,13,26),18],[(190,190,0),None,None,None])
		page.buttons['goArchive'] = Button(None,pygame.Rect(920, 25, 50, 50),[(255,255,0),'Archive',(247,13,26),18],[(190,190,0),None,None,None])
		page.buttons['goOption'] = Button(None,pygame.Rect(985, 25, 50, 50),[(255,255,0),'Option',(247,13,26),18],[(190,190,0),None,None,None])
		
	def handle_events(page, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					pass
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				if page.status == 0:
					if page.buttons['roll1'].state == 1: # is Hover
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

	def update(page):
		for name,button in page.buttons.items():
			button.checkHover(page.game.mousepos)

	def draw(page, screen):
		screen.fill((130, 30, 30))

		for name,button in page.buttons.items():
			button.draw(screen)

		if page.status == 1:
			xt = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
			xt.fill((0, 0, 0, 100))
			screen.blit(xt,(0,0))

	def roll(page,rolls=1):
		pass
