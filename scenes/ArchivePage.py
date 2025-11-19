import pygame
from stuff import *

class Archive(Scene):
	DISPLAY_LABEL_SURFACE = TextBox(pygame.Rect(0,0,240,80),(255,255,255),text=f'Name:\nRank:\nPower Level:\nNumbers:',align='left')
	def __init__(page,game):
		super().__init__(game)

		page.bg.fill((30,100,30))
		page.bg.blit(Scene.EXITTXT,(20,20))

		page.char_image_table = {}
		for id,char in page.game.data.items():
			page.char_image_table[id] = (Image(char.getIcon(bg=True)),Image(char.getArt()))

		page.char_icons = {}
		page.char_display = {}
		page.groups[-2] = page.char_icons
		page.groups[-1] = page.char_display

	def enter(page):
		ii = 0
		cmax = 5
		for id,char in page.game.data.items():
			if id==0:
				continue
			obtained = (page.game.char_obtained.get(id) or 0)>0
			r,c = ii%cmax,ii//cmax
			page.char_image_table[id][0].rect.topleft = (50+(80+10)*r,75+(80+10)*c)
			page.char_image_table[id][0].drawgrayscale = not obtained

			page.char_image_table[id][1].rect.topleft = (600,50)
			page.char_image_table[id][1].drawgrayscale = not obtained

			page.char_icons[id] = page.char_image_table[id][0]
			ii+=1

		page.hoverNewCharacter(None)

	def handle_events(page, events):
		super().handle_events(events)

	def update(page):
		super().update()

		for id,image in page.char_icons.items():
			image.update(page.game.mousepos)
			if image.rect.collidepoint(page.game.mousepos) and (page.currentcharacter is None or page.currentcharacter.id != id):
				page.hoverNewCharacter(page.game.data[id])

	def draw(page):
		super().draw()
		
		pygame.draw.line(page.game.screen, (255,255,255), (530,60), (530,540), 1)
	
	def hoverNewCharacter(page,char):
		page.currentcharacter = char
		if char != None:
			obtained = (page.game.char_obtained.get(char.id) or 0)>0
			if obtained:
				page.char_display['art'] = page.char_image_table[char.id][1]
				page.char_display['label'] = TextBox(Image(__class__.DISPLAY_LABEL_SURFACE.image, (680,500)), text=f'{char.name}\n{char.rarity}\n{char.power}\n{page.game.char_obtained.get(char.id) or 0}',align='right')
			else:
				page.char_display['art'] = page.char_image_table[char.id][1]
				page.char_display['label'] = TextBox(Image(__class__.DISPLAY_LABEL_SURFACE.image, (680,500)), text=f'???\n???\n???\n0',align='right')
		else:
			page.char_display['art'] = Image(BLANK_SURFACE,(600,50))
			page.char_display['label'] = TextBox(Image(__class__.DISPLAY_LABEL_SURFACE.image, (680,500)), text=f'-\n-\n0\n0',align='right')