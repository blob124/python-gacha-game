import pygame
from stuff import *

EXITTXT = pygame.font.SysFont(None, 24).render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Settings(Scene):
	def __init__(page,game):
		page.game = game

		page.bg = pygame.Surface(page.game.screen.get_size())
		page.bg.fill((100,100,100))
		page.bg.blit(EXITTXT,(20,20))

		page.images = {}
		page.textbox = {}
		page.buttons = {}
		page.groups = {	0:page.images,
				 		1:page.textbox,
				 		2:page.buttons}

		page.textbox['textboxABC'] = TextBox(pygame.Rect(250,250,400,40),bgcolor=(255,255,255),text='defaultText')
		page.textbox['textboxABC'].text['string'] = 'Hi pookie!!'
		page.textbox['textboxABC'].renderText(True)

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
		for _,obj in page.buttons.items():
			obj.state = 1 if obj.isHover(page.game.mousepos) else 0	

		if page.textbox['textboxABC'].rect.collidepoint(page.game.mousepos):
			if page.textbox['textboxABC'].box['boarderSize'] != 3:
				page.textbox['textboxABC'].box['boarderSize'] = 3
				page.textbox['textboxABC'].renderBox(True)
		else:
			if page.textbox['textboxABC'].box['boarderSize'] != 0:
				page.textbox['textboxABC'].box['boarderSize'] = 0
				page.textbox['textboxABC'].renderBox(True)

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			for _,obj in group.items():
				obj.draw(page.game.screen)
