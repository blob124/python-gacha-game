import pygame
from stuff import *

class Settings(Scene):
	def __init__(page,game):
		page.game = game

		page.bg = pygame.Surface(page.game.screen.get_size())
		page.bg.fill((100,100,100))
		page.bg.blit(Scene.EXITTXT,(20,20))

		page.images = {}
		page.label = {}
		page.inputbox = {}
		page.buttons = {}
		page.groups = {-1:page.label,
						0:page.images,
				 		1:page.inputbox,
				 		2:page.buttons}
		
		page.label['music'] = Text(text='Music',textsize=48).update((250,150))
		page.label['redeem'] = Text(text='Redeem Code',textsize=48).update((250,250))
		page.label['reset'] = Text(text='Reset',textsize=48).update((250,350))

		page.inputbox['music'] = Interactable((600,150),
			[pygame.Rect(4,4,32,32),Image(pygame.image.load(f'data/images/checkbox_0.png').convert_alpha(),(0,0))],
			[pygame.Rect(4,4,32,32),Image(pygame.image.load(f'data/images/checkbox_0.png').convert_alpha(),(0,0))],
			[pygame.Rect(4,4,32,32),Image(pygame.image.load(f'data/images/checkbox_1.png').convert_alpha(),(0,0))],
			[pygame.Rect(4,4,32,32),Image(pygame.image.load(f'data/images/checkbox_1.png').convert_alpha(),(0,0))],
			callback=lambda: (page.game.toggle_music(), setattr(page.inputbox['music'], 'state', 1 if page.game.musicplaying else 0))
		)
		page.inputbox['music'].state = 1

		page.inputbox['redeem'] = CoolTextBox(Box(pygame.Rect(600,250,400,40),bgcolor=(255,255,255)),Text('defaultText'),callback=lambda: page.game.enterCode(page.inputbox['redeem'].text.text))
		page.inputbox['redeem'].text.text = 'Hi pookie!!'
		page.inputbox['redeem'].text.update()

		page.inputbox['reset'] = SimpleButton(pygame.Rect(600,350,100,50),
			[TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(128,128,160)),Text('Reset',textcolor=(247,13,26)))],
			[TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(78,78,97)),Text('Reset',textcolor=(247,13,26)))],
			[TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(255,0,0)),Text('ARE YOU\nSURE?',textcolor=(0,0,0),textsize=24))],
			[TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(190,0,0)),Text('ARE YOU\nSURE?',textcolor=(0,0,0),textsize=24))],
			callback=lambda: (page.game.reset_profile() if page.inputbox['reset'].state==1 else None, setattr(page.inputbox['reset'], 'state', 0 if page.inputbox['reset'].state==1 else 1))
		)

	def handle_events(page, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					pass
				elif event.key == pygame.K_ESCAPE:
					page.game.change_scene('GachaPlace')
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				pass
			
			for _,group in sorted(page.groups.items()):
				for _,obj in group.items():
					if hasattr(obj, 'handle_event') and callable(getattr(obj, 'handle_event')):
						obj.handle_event(event)

	def update(page):
		for _,button in page.buttons.items():
			button.update(page.game.mousepos)
		
		page.inputbox['music'].update(page.game.mousepos)
		page.inputbox['redeem'].update(page.game.mousepos)
		page.inputbox['reset'].update(page.game.mousepos)

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			for _,obj in group.items():
				obj.draw(page.game.screen)