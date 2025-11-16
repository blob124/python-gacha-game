import pygame
from stuff import *

class Settings(Scene):
	def __init__(page,game):
		super().__init__(game)

		page.bg.fill((100,100,100))
		page.bg.blit(Scene.EXITTXT,(20,20))
		

		page.ui['music-text'] = Text(text='Music',textsize=48).update(xy=(250,150))
		page.ui['redeem-text'] = Text(text='Redeem Code',textsize=48).update(xy=(250,250))
		page.ui['reset-text'] = Text(text='Reset',textsize=48).update(xy=(250,350))

		checkbox0 = pygame.image.load(f'data/images/checkbox_0.png').convert_alpha()
		checkbox1 = pygame.image.load(f'data/images/checkbox_1.png').convert_alpha()

		page.ui['music-input'] = Interactable((600,150), [pygame.Rect(4,4,32,32),Image(checkbox0)], [pygame.Rect(4,4,32,32),Image(checkbox0)], [pygame.Rect(4,4,32,32),Image(checkbox1)], [pygame.Rect(4,4,32,32),Image(checkbox1)],
			callback=lambda: (page.game.toggle_music(), setattr(page.inputbox['music'], 'state', 1 if page.game.musicplaying else 0)))
		page.ui['music-input'].state = 1

		page.ui['redeem-input'] = CoolTextBox(Box(pygame.Rect(600,250,400,40),bgcolor=(255,255,255)),Text('defaultText'),callback=lambda: page.updatewarningbox(page.game.enterCode(page.inputbox['redeem'].text.text)))

		page.ui['reset-input'] = SimpleButton(pygame.Rect(600,350,100,50), [TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(128,128,160)),Text('Reset',textcolor=(247,13,26)))], [TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(78,78,97)),Text('Reset',textcolor=(247,13,26)))], [TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(255,0,0)),Text('ARE YOU\nSURE?',textcolor=(0,0,0),textsize=24))], [TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(190,0,0)),Text('ARE YOU\nSURE?',textcolor=(0,0,0),textsize=24))],
			callback=lambda: page.proceed_reset())
	
	def enter(page):
		page.ui['redeem-input'].text.update('Hi pookie!!')

	def handle_events(page, events):
		for event in events:
			if page.showwarning:
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					page.showwarning = False
				continue
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					page.game.change_scene('GachaPlace')
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				pass
			
			for _,group in sorted(page.groups.items()):
				for _,obj in group.items():
					if hasattr(obj, 'handle_event') and callable(getattr(obj, 'handle_event')):
						obj.handle_event(event)

	def update(page):
		super().update()
		
		page.ui['music-input'].update(page.game.mousepos)
		page.ui['redeem-input'].update(page.game.mousepos)
		#page.inputbox['reset'].update(page.game.mousepos)
		
		if not page.showwarning:
			page.ui['reset-input'].update(page.game.mousepos)
		else:
			page.ui['reset-input'].hovered = False

	def draw(page):
		super().draw()
	
	def proceed_reset(page):
		if page.ui['reset-input'].state==0:
			page.ui['reset-input'].state = 1
		else:
			page.game.reset_profile()
			page.updatewarningbox('your profile...\nprofile have been reset')
			page.ui['reset-input'].state = 0