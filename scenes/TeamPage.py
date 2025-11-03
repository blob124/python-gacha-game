import pygame
from stuff import *

EXITTXT = pygame.font.SysFont(None, 24).render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Party(Scene):
	def __init__(page,game):
		page.game = game

		page.bg = pygame.Surface(page.game.screen.get_size())
		page.bg.fill((0,43,128))
		page.bg.blit(EXITTXT,(20,20))

		page.images = {}
		page.char_icons = {}
		page.char_arts = {}
		page.buttons = {}
		page.groups = {	-2:page.char_icons,
				 		-1:page.char_arts,
						0:page.images,
				 		1:page.buttons}

		page.party = [None,None,None,None,None]

		char_0_icon = page.game.data['Man'].getIcon(True)

		page.char_icons[0] = Image(char_0_icon,(50,75))

		page.images['powerlevel'] = TextBox(pygame.Rect(80,520,300,50),bgcolor=(0,225,0),text='PowerLevel: 0',textcolor=(255,190,190),textsize=32)

		page.buttons['buttonname'] = SimpleButton(pygame.Rect(950,520,80,40),
			[TextBox(pygame.Rect(0,0,80,40),(0,255,0),text='TEXT HERE',textcolor=(247,13,26),textsize=20)],
			[TextBox(pygame.Rect(0,0,80,40),(0,190,0),text='TEXT HERE',textcolor=(247,13,26),textsize=20)]
		)

		page.updateParty()
	
	def enter(page):
		pass

	def updateParty(page):
		for i in range(5):
			char = page.game.party[i]
			if char not in page.game.char_obtained:
				char = 'PHD'
			page.party[i] = char

			theart = page.game.data[char].getArt()
			theart = pygame.transform.scale_by(theart, (0.5, 0.5))
			page.char_arts[i] = Image(theart,(433+(i-2)*160,300))
		
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
		for _,obj in page.buttons.items():
			obj.state = 1 if obj.isHover(page.game.mousepos) else 0

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			for _,obj in group.items():
				obj.draw(page.game.screen)

		pygame.draw.line(page.game.screen, (255,255,255), (50,280), (1067-50,280), 1)

	class PartyIcon(Interactable):
		def __init__(self):
			pass
	
	class PartyArt(Interactable):
		def __init__(self,xy):
			super().__init__(xy,[])