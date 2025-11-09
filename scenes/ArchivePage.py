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
		page.char_display = {}
		page.buttons = {}
		page.groups = {	-2:page.char_icons,
				 		-1:page.char_display,
						0:page.images,
				 		1:page.buttons}

		page.buttons['buttonname'] = SimpleButton(pygame.Rect(50,520,100,50),
			[TextBox(Box(pygame.Rect(0,0,100,50),(0,255,0)),Text('TEXT HERE',textcolor=(247,13,26)))],
			[TextBox(Box(pygame.Rect(0,0,100,50),(0,190,0)),Text('HOVERING',textcolor=(247,13,26),textsize=18))]
		)

		page.buttons['alsobuttonname'] = SimpleButton(pygame.Rect(170,520,100,50),
			[TextBox(Box(pygame.Rect(0,0,100,50),(0,190,255)),Text('TEXT HERE\n2',textcolor=(247,13,26)))],
			[TextBox(Box(pygame.Rect(0,0,100,50),(0,144,190)),Text('HOVERINGING',textcolor=(247,13,26),textsize=18))]
		)
		
		page.images['charlist'] = TextBox(Box(pygame.Rect(50,75,100,50),bgcolor=(255,255,255,255)),Text('',28),align='left')

	def enter(page):
		page.currentcharacter = page.game.data[1]
		char_0_icon = page.currentcharacter.getIcon(bg=True)

		for i in range(5):
			page.char_icons[f'image{i}'] = Image(char_0_icon,(50+90*i,75))

		page.char_display['art'] = Image(page.currentcharacter.getArt(),(650,50))
		page.char_display['label-left'] = TextBox(
			Box(pygame.Rect(725,500,250,80),(255,255,255)),
			Text(f'Name:\nRank:\nPower Level:\nNumbers:',align='left'),align='left'
		)
		page.char_display['label-right'] = TextBox(
			Box(pygame.Rect(725,500,250,80),(0,0,0,0)),
			Text(f'{page.currentcharacter.name}\n{page.currentcharacter.rarity}\n{page.currentcharacter.power}\n{page.game.char_obtained.get(page.currentcharacter.id) or 0}',align='right'),align='right'
		)
		#page.char_display['name'] = Image(Text(page.currentcharacter.name).sprite,(650,500))
		#page.char_display['rarity'] = Image(Text(page.currentcharacter.rarity).sprite,(800,500))
		#page.char_display['power'] = Image(Text(page.currentcharacter.power).sprite,(650,550))
		#page.char_display['dup'] = Image(Text(page.game.char_obtained.get(page.currentcharacter.id) or 0).sprite,(800,550))

		
		
		#for demo
		page.images['charlist'].text.sprite = renderTextWithLines(f'{'\n'.join([f'{page.game.data[charid].name}:{' '*max(0,round(2.5*(12-len(str(page.game.data[charid].name)+':'+str(dup)))))}{dup}' for charid,dup in page.game.char_obtained.items()])}',size=28,horizontal_align='left')
		page.images['charlist'].text.rect = page.images['charlist'].text.sprite.get_rect()
		page.images['charlist'].resize_fit(padding=5)

	def handle_events(page, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					pass
				elif event.key == pygame.K_ESCAPE:
						page.game.change_scene('GachaPlace')
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				pass

	def update(page):
		for _,button in page.buttons.items():
			button.update(page.game.mousepos)

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			for _,obj in group.items():
				obj.draw(page.game.screen)
		
		pygame.draw.line(page.game.screen, (255,255,255), (630,80), (630,520), 1)