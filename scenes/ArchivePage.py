import pygame
from stuff import *

EXITTXT = pygame.font.SysFont(None, 24).render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Archive(Scene):
	def __init__(page,game):
		page.game = game

		page.bg = pygame.Surface(page.game.screen.get_size())
		page.bg.fill((30,100,30))
		page.bg.blit(EXITTXT,(20,20))

		page.images = {}
		page.char_icons = {}
		page.char_arts = {}
		page.buttons = {}
		page.groups = {	-2:page.char_icons,
				 		-1:page.char_arts,
						0:page.images,
				 		1:page.buttons}

		page.buttons['buttonname'] = SimpleButton(pygame.Rect(50,520,100,50),
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,255,0),text='TEXT HERE',textcolor=(247,13,26),aligncenter=True)],
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,190,0),text='HOVERING',textcolor=(247,13,26),aligncenter=True)]
		)

		page.buttons['alsobuttonname'] = SimpleButton(pygame.Rect(170,520,100,50),
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,190,255),text='TEXT HERE\n2',textcolor=(247,13,26),aligncenter=True)],
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(0,144,190),text='HOVERINGING',textcolor=(247,13,26),textsize=18,aligncenter=True)])

	def enter(page):
		char_0_icon = page.game.data['Man'].getIcon(bg=True)
		char_0_art = page.game.data['Man'].getArt()
		one_image = pygame.image.load('data/numba1.png').convert_alpha()
		one_image = pygame.transform.scale_by(one_image, (1.5, 0.15))

		page.char_icons['image0'] = Image(char_0_icon,(50,75))
		page.char_arts['image1'] = Image(char_0_art,(650,75))
		page.images['one'] = Image(one_image,(290,513))

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
		for _,obj in page.buttons.items():
			obj.state = 1 if obj.isHover(page.game.mousepos) else 0

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			for _,obj in group.items():
				obj.draw(page.game.screen)
		
		pygame.draw.line(page.game.screen, (255,255,255), (650,80), (650,520), 1)