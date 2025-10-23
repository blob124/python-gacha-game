import pygame
import random
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Party:
	def __init__(self,game):
		self.game = game
		self.party = [None,None,None,None,None]

		char_0_icon = self.game.data['Man'].getIcon()

		self.images = {}
		self.images['image0'] = Image(char_0_icon,50,75)
		self.images['powerlevel'] = TextBox(pygame.Rect(80,520,300,50),(0,225,0),'PowerLevel: 0',(255,190,190),32)


		self.buttons = {}
		self.buttons['buttonname'] = Button(None,pygame.Rect(950, 520, 80, 40),[(0,255,0),'TEXT HERE',(247,13,26),20],[(0,190,0),None,None,None])


		self.updateParty()

	def updateParty(self):
		for i in range(5):
			char = self.game.party[i]
			print(char)
			if char not in self.game.char_obtained:
				char = 'PHD'
			self.party[i] = char

			theart = self.game.data[char].getArt()
			theart = pygame.transform.scale_by(theart, (0.5, 0.5))
			self.images[f'slot{i}'] = Image(theart,433+(i-2)*160,300)
		
		self.images['powerlevel'].setText(f'PowerLevel: {sum([self.game.data[char].power for char in self.party])}')

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
			image.draw(screen)

		for name,button in self.buttons.items():
			button.draw(screen)
		
		pygame.draw.line(screen, (255,255,255), (50,280), (1067-50,280), 1)