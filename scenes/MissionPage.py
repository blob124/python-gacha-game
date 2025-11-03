import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Mission(Scene):
	def __init__(page,game):
		page.game = game

		page.bg = pygame.Surface(page.game.screen.get_size())
		page.bg.fill((160,100,30))
		page.bg.blit(EXITTXT,(20,20))

		page.bg.blit(renderTextWithLines('Scene\nTemplate',size=67),(432,234))

		page.images = {}
		page.buttons = {}
		page.groups = {	0:page.images,
				 		1:page.buttons}
	
	def enter(page):
		pass

	def handle_events(page, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					page.game.change_scene(page.game.scenes['GachaPlace'])
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				pass

	def update(page):
		for _,obj in page.buttons.items():
			obj.state = 1 if obj.isHover(page.game.mousepos) else 0

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			for _,obj in group.items():
				obj.draw(page.game.screen)