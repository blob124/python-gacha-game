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
		page.displaywarning = {}
		page.showwarning = False
		page.groups = {-1:page.label,
						0:page.images,
				 		1:page.inputbox,
				 		2:page.buttons,
						9:page.displaywarning}

		page.label['music'] = Text(text='Music',textsize=48).update(xy=(250,150))
		page.label['redeem'] = Text(text='Redeem Code',textsize=48).update(xy=(250,250))
		page.label['reset'] = Text(text='Reset',textsize=48).update(xy=(250,350))

		checkbox0 = pygame.image.load(f'data/images/checkbox_0.png').convert_alpha()
		checkbox1 = pygame.image.load(f'data/images/checkbox_1.png').convert_alpha()

		page.inputbox['music'] = Interactable((600,150), [pygame.Rect(4,4,32,32),Image(checkbox0)], [pygame.Rect(4,4,32,32),Image(checkbox0)], [pygame.Rect(4,4,32,32),Image(checkbox1)], [pygame.Rect(4,4,32,32),Image(checkbox1)],
			callback=lambda: (page.game.toggle_music(), setattr(page.inputbox['music'], 'state', 1 if page.game.musicplaying else 0))
		)
		page.inputbox['music'].state = 1

		page.inputbox['redeem'] = CoolTextBox(Box(pygame.Rect(600,250,400,40),bgcolor=(255,255,255)),Text('defaultText'),callback=lambda: page.updatewarningbox(page.game.enterCode(page.inputbox['redeem'].text.text)))
		page.inputbox['redeem'].text.update('Hi pookie!!')

		page.inputbox['reset'] = SimpleButton(pygame.Rect(600,350,100,50), [TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(128,128,160)),Text('Reset',textcolor=(247,13,26)))], [TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(78,78,97)),Text('Reset',textcolor=(247,13,26)))], [TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(255,0,0)),Text('ARE YOU\nSURE?',textcolor=(0,0,0),textsize=24))], [TextBox(Box(pygame.Rect(0,0,100,50),bgcolor=(190,0,0)),Text('ARE YOU\nSURE?',textcolor=(0,0,0),textsize=24))],
			callback=lambda: page.proceed_reset()
		)

		page.displaywarning['vig'] = VignetteLayer(page.game)
		page.displaywarning['warnbox'] = TextBox(Box(pygame.Rect(page.game.screen.get_width()/2-175,page.game.screen.get_height()/2-30,350,60),(225,225,225)),Text(f'warningtext',32,(225,130,0)))

	def handle_events(page, events):
		for event in events:
			if page.showwarning:
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					page.showwarning = False
				continue

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
			if not page.showwarning:
				button.update(page.game.mousepos)
			else:
				button.hovered = False
		
		page.inputbox['music'].update(page.game.mousepos)
		page.inputbox['redeem'].update(page.game.mousepos)
		#page.inputbox['reset'].update(page.game.mousepos)
		
		if not page.showwarning:
			page.inputbox['reset'].update(page.game.mousepos)
		else:
			page.inputbox['reset'].hovered = False

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			if group is page.displaywarning and not page.showwarning:
				continue
			
			for _,obj in group.items():
				obj.draw(page.game.screen)

	def updatewarningbox(page,text):
		page.displaywarning['warnbox'].text.update(text)
		page.displaywarning['warnbox'].update()
		page.showwarning = True
	
	def proceed_reset(page):
		if page.inputbox['reset'].state==0:
			page.inputbox['reset'].state = 1
		else:
			page.game.reset_profile()
			page.updatewarningbox('your profile...\nprofile have been reset')
			page.inputbox['reset'].state = 0