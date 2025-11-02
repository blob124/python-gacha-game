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
		page.label = {}
		page.inputbox = {}
		page.buttons = {}
		page.groups = {-1:page.label,
						0:page.images,
				 		1:page.inputbox,
				 		2:page.buttons}
		
		page.label['music'] = TextBox(pygame.Rect(250,150,10,10),text='Music',textsize=48).resize_fit()
		page.label['redeem'] = TextBox(pygame.Rect(250,250,10,10),text='Redeem Code',textsize=48).resize_fit()
		page.label['reset'] = TextBox(pygame.Rect(250,350,10,10),text='Reset',textsize=48).resize_fit()

		page.inputbox['music'] = Interactable((600,150),
			[pygame.Rect(4,4,32,32),Image(pygame.image.load(f'data/images/checkbox_0.png').convert_alpha(),(0,0))],
			[pygame.Rect(4,4,32,32),Image(pygame.image.load(f'data/images/checkbox_1.png').convert_alpha(),(0,0))]
		)
		page.inputbox['music'].state = 1

		page.inputbox['redeem'] = TextBox(pygame.Rect(600,250,400,40),bgcolor=(255,255,255),text='defaultText')
		page.inputbox['redeem'].text['string'] = 'Hi pookie!!'
		page.inputbox['redeem'].renderText(True)

		page.inputbox['reset'] = SimpleButton(pygame.Rect(600,350,100,50),
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(128,128,160),text='Reset',textcolor=(247,13,26),aligncenter=True)],
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(78,78,97),text='Reset',textcolor=(247,13,26),aligncenter=True)],
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(255,0,0),text='ARE YOU\nSURE?',textcolor=(0,0,0),textsize=24,aligncenter=True)],
			[TextBox(pygame.Rect(0,0,100,50),bgcolor=(190,0,0),text='ARE YOU\nSURE?',textcolor=(0,0,0),textsize=24,aligncenter=True)]
		)
		page.inputbox['reset'].in_special_state = False

	def handle_events(page, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					pass
				elif event.key == pygame.K_ESCAPE:
						page.game.change_scene(page.game.scenes['GachaPlace'])
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				if page.inputbox['music'].isHover(page.game.mousepos):
					if page.inputbox['music'].state == 0:
						page.inputbox['music'].state = 1
						pygame.mixer.music.unpause()
					else:
						page.inputbox['music'].state = 0
						pygame.mixer.music.pause()
						pygame.mixer.music.set_pos(0)
				elif page.inputbox['reset'].isHover(page.game.mousepos):
					if page.inputbox['reset'].in_special_state:
						page.game.reset_profile()

					page.inputbox['reset'].in_special_state = not page.inputbox['reset'].in_special_state

	def update(page):
		for _,obj in page.buttons.items():
			obj.state = 1 if obj.isHover(page.game.mousepos) else 0
		
		reset_box = page.inputbox['reset']
		if not reset_box.in_special_state:
			if not reset_box.isHover(page.game.mousepos):
				reset_box.state = 0
			else:
				reset_box.state = 1
		else:
			if not reset_box.isHover(page.game.mousepos):
				reset_box.state = 2
			else:
				reset_box.state = 3

		if page.inputbox['redeem'].rect.collidepoint(page.game.mousepos):
			if page.inputbox['redeem'].box['boarderSize'] != 3:
				page.inputbox['redeem'].box['boarderSize'] = 3
				page.inputbox['redeem'].renderBox(True)
		else:
			if page.inputbox['redeem'].box['boarderSize'] != 0:
				page.inputbox['redeem'].box['boarderSize'] = 0
				page.inputbox['redeem'].renderBox(True)

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			for _,obj in group.items():
				obj.draw(page.game.screen)
