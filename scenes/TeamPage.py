import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Party:
	def __init__(page,game):
		page.game = game
		page.party = [None,None,None,None,None]

		char_0_icon = page.game.data['Man'].getIcon()

		page.images = {}
		page.images['image0'] = Image(char_0_icon,50,75)
		page.images['powerlevel'] = TextBox(pygame.Rect(80,520,300,50),(0,225,0),(0,0,0,0),0,'PowerLevel: 0',(255,190,190),32)


		page.buttons = {}
		page.buttons['buttonname'] = Button(None,pygame.Rect(950, 520, 80, 40),[(0,255,0),'TEXT HERE',(247,13,26),20],[(0,190,0),None,None,None])


		page.updateParty()

	def updateParty(page):
		for i in range(5):
			char = page.game.party[i]
			if char not in page.game.char_obtained:
				char = 'PHD'
			page.party[i] = char

			theart = page.game.data[char].getArt()
			theart = pygame.transform.scale_by(theart, (0.5, 0.5))
			page.images[f'slot{i}'] = Image(theart,433+(i-2)*160,300)
		
		page.images['powerlevel'].text['string'] = f'PowerLevel: {sum([page.game.data[char].power for char in page.party])}'

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

	def update(page):
		for name,button in page.buttons.items():
			button.checkHover(page.game.mousepos)

	def draw(page, screen):		
		screen.fill((30, 30, 160))
		screen.blit(EXITTXT, (20, 20))

		for id,image in page.images.items():
			image.draw(screen)

		for name,button in page.buttons.items():
			button.draw(screen)
		
		pygame.draw.line(screen, (255,255,255), (50,280), (1067-50,280), 1)