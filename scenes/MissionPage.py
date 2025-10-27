import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Mission:
	def __init__(page,game):
		page.game = game
	
	def handle_events(page, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					pass
				elif event.key == pygame.K_ESCAPE:
						page.game.change_scene(page.game.scenes['GachaPlace'])

	def update(page):
		pass

	def draw(page, screen):		
		screen.fill((160, 100, 30))
		screen.blit(EXITTXT, (20, 20))