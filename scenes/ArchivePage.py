import pygame
from stuff import *

class Archive(Scene):
	DISPLAY_LABEL_SURFACE = TextBox(Box(pygame.Rect(0,0,240,80),(255,255,255)),Text(f'Name:\nRank:\nPower Level:\nNumbers:',align='left'),align='left')
	def __init__(page,game):
		page.game = game

		page.bg = pygame.Surface(page.game.screen.get_size())
		page.bg.fill((30,100,30))
		page.bg.blit(Scene.EXITTXT,(20,20))

		page.char_image_table = {}
		for id,char in page.game.data.items():
			page.char_image_table[id] = (Image(char.getIcon(bg=True),(0,0)),Image(char.getArt(),(600,50)))

		page.images = {}
		page.char_icons = {}
		page.char_display = {}
		page.buttons = {}
		page.groups = {	-2:page.char_icons,
				 		-1:page.char_display,
						0:page.images,
				 		1:page.buttons}

	def enter(page):
		ii = 0
		cmax = 5
		for id,char in page.game.data.items():
			if id==0:
				continue
			obtained = (page.game.char_obtained.get(id) or 0)>0
			r,c = ii//cmax,ii%cmax
			page.char_image_table[id][0].rect.topleft = (50+(80+10)*ii,75)
			page.char_image_table[id][0].drawgrayscale = not obtained

			page.char_image_table[id][1].rect.topleft = (600,50)
			page.char_image_table[id][1].drawgrayscale = not obtained

			page.char_icons[id] = page.char_image_table[id][0]
			ii+=1

		page.updateDisplay(page.game.data[1])

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
		for id,image in page.char_icons.items():
			if image.rect.collidepoint(page.game.mousepos):
				if page.currentcharacter.id != id:
					page.updateDisplay(page.game.data[id])
					break

		for _,button in page.buttons.items():
			button.update(page.game.mousepos)
	
	def updateDisplay(page,char):
		page.currentcharacter = char
		if char != None:
			obtained = (page.game.char_obtained.get(char.id) or 0)>0
			if obtained:
				page.char_display['art'] = page.char_image_table[char.id][1]
				page.char_display['label'] = TextBox(
					Image(__class__.DISPLAY_LABEL_SURFACE.image, (680,500)),
					Text(f'{char.name}\n{char.rarity}\n{char.power}\n{page.game.char_obtained.get(char.id) or 0}',align='right'),align='right'
				)
			else:
				page.char_display['art'] = page.char_image_table[char.id][1]
				page.char_display['label'] = TextBox(
					Image(__class__.DISPLAY_LABEL_SURFACE.image, (680,500)),
					Text(f'???\n???\n???\n0',align='right'),align='right'
				)
		else:
			page.char_display['art'] = Image(BLANK_SURFACE,(600,50))
			page.char_display['label'] = TextBox(
				Image(__class__.DISPLAY_LABEL_SURFACE.image, (680,500)),
				Text(f'-\n-\n0\n0',align='right'),align='right'
			)

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			for _,obj in group.items():
				obj.draw(page.game.screen)
		
		pygame.draw.line(page.game.screen, (255,255,255), (530,60), (530,540), 1)