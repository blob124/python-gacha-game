import pygame
from stuff import *

class Settings(Scene):
	def __init__(page,game):
		super().__init__(game)

		page.bg.fill((100,100,100))
		page.bg.blit(Scene.EXITTXT,(20,20))
		

		page.ui['music-text'] = TextBox(pygame.Rect(250,150,100,50),text='Music',textsize=48).fittotext(0)
		page.ui['redeem-text'] = TextBox(pygame.Rect(250,250,100,50),text='Redeem Code',textsize=48).fittotext(0)
		page.ui['reset-text'] = TextBox(pygame.Rect(250,350,100,50),text='Reset',textsize=48).fittotext(0)

		checkbox0 = pygame.image.load(f'data/images/checkbox_0.png').convert_alpha()
		checkbox1 = pygame.image.load(f'data/images/checkbox_1.png').convert_alpha()

		page.ui['music-input'] = Interactable((600,150), [pygame.Rect(4,4,32,32),Image(checkbox0)], [pygame.Rect(4,4,32,32),Image(checkbox0)], [pygame.Rect(4,4,32,32),Image(checkbox1)], [pygame.Rect(4,4,32,32),Image(checkbox1)],
			callback=lambda: (page.game.toggle_music(), setattr(page.inputbox['music'], 'state', 1 if page.game.musicplaying else 0)))
		page.ui['music-input'].state = 1

		page.ui['redeem-input'] = CoolTextBox(TextBox(pygame.Rect(600,250,400,40),bgcolor=(255,255,255),text='defaultText',align='left'),callback=lambda: page.updatewarningbox(page.game.enterCode(page.ui['redeem-input'].text.text)))

		page.ui['reset-input'] = SimpleButton(pygame.Rect(600,350,100,50), [TextBox(pygame.Rect(0,0,100,50),bgcolor=(128,128,160),text='Reset',textcolor=(247,13,26))], [TextBox(pygame.Rect(0,0,100,50),bgcolor=(78,78,97),text='Reset',textcolor=(247,13,26))], [TextBox(pygame.Rect(0,0,100,50),bgcolor=(255,0,0),text='ARE YOU\nSURE?',textcolor=(0,0,0),textsize=24)], [TextBox(pygame.Rect(0,0,100,50),bgcolor=(190,0,0),text='ARE YOU\nSURE?',textcolor=(0,0,0),textsize=24)],
			callback=lambda: page.proceed_reset())
		
		minigraycirc = pygame.Surface((26,26),flags=pygame.SRCALPHA)
		pygame.draw.circle(minigraycirc,(130,130,130),(minigraycirc.get_width()/2,minigraycirc.get_height()/2),minigraycirc.get_width()/2)
		page.ui['redeem-tooltip'] = ToolTip(Image(TextBox(Image(minigraycirc),text='i',textsize=24,textcolor=(255,255,255)).getSprite(),(484,253)),TextBox(pygame.Rect(0,0,120,50),(80,80,80,130),text='I am redeem-tooltip\n\"Click\" the thing and\ninsert redeemCode',textsize=16,textcolor=(255,255,255)))

	def enter(page):
		page.ui['redeem-input'].focus = False
		page.ui['redeem-input'].state = 0
		page.ui['redeem-input'].textcursorvisible = False
		page.ui['redeem-input'].text.text = 'ENTERCODEHERE'
		page.ui['redeem-input'].text.update()

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
		if not page.showwarning:
			page.ui['reset-input'].update(page.game.mousepos)
			page.ui['redeem-tooltip'].update(page.game.mousepos)
		else:
			page.ui['reset-input'].hovered = False
			page.ui['redeem-tooltip'].hovered = False

	def draw(page):
		super().draw()
	
	def proceed_reset(page):
		if page.ui['reset-input'].state==0:
			page.ui['reset-input'].state = 1
		else:
			page.game.reset_profile()
			page.updatewarningbox('your profile...\nprofile have been reset')
			page.ui['reset-input'].state = 0