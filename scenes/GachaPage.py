import pygame
import random
import math
from stuff import *

class GachaPlace(Scene):
	def __init__(page,game):
		page.game = game

		page.bg = pygame.Surface(page.game.screen.get_size())

		page.images = {}
		page.buttons = {}
		page.ui = {}
		page.groups = {	0:page.images,
				 		1:page.buttons,
						2:page.ui}
		
		page.vig = pygame.Surface(page.game.screen.get_size(), pygame.SRCALPHA)
		page.vig.fill((0,0,0,100))
		page.justroll = []
		page.displayroll = False

		page.banners = []
		page.currentbanner = 0

		tarvRC_bg = pygame.Surface((page.game.screen.get_size()))
		tarvRC_bg.fill((30,100,130))
		page.banners.append(page.Banner(page.game.data,'tarvRC','Tarvern Recruit', ('Man','Woman','Unnamed01','Unnamed02'), [0,0,90,9.4,0.6],bg=tarvRC_bg))
		pp0_bg = pygame.Surface((page.game.screen.get_size()))
		pp0_bg.fill((30,190,130))
		page.banners.append(page.Banner(page.game.data,'pp0','Pally Pal', ('Scribble','Redrill','Pebble'), [73,21,6,0,0],bg=pp0_bg))

		page.buttons['left-arrow'] = SimpleButton(pygame.Rect(40,(page.game.screen.get_height()-80)//2,50,80),
				[TextBox(pygame.Rect(0,0,50,80),bgcolor=(255,255,255,190),text='<',textsize=96,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,50,80),bgcolor=(190,190,190,255),text='<',textsize=96,aligncenter=True)]
		)
		page.buttons['right-arrow'] = SimpleButton(pygame.Rect(page.game.screen.get_width()-50-40,(page.game.screen.get_height()-80)//2,50,80),
				[TextBox(pygame.Rect(0,0,50,80),bgcolor=(255,255,255,190),text='>',textsize=96,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,50,80),bgcolor=(190,190,190,255),text='>',textsize=96,aligncenter=True)]
		)
		
		page.buttons['roll1'] = SimpleButton(pygame.Rect(200,500,100,50),
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(255,255,0,255),text='roll1\nx160',textcolor=(247,13,26),textsize=30,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(190,190,0,255),text='roll1\nx160',textcolor=(247,13,26),textsize=30,aligncenter=True)]
		)
		page.buttons['roll10'] = SimpleButton(pygame.Rect(769,500,100,50),
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(255,255,0,255),text='roll10\nx1600',textcolor=(247,13,26),textsize=30,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(190,190,0,255),text='roll10\nx1600',textcolor=(247,13,26),textsize=30,aligncenter=True)]
		)
		
		page.buttons['goMission'] = SimpleButton(pygame.Rect(790,25,50,50),
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(255,255,0,255),text='Quest',textcolor=(247,13,26),textsize=18,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(190,190,0,255),text='Quest',textcolor=(247,13,26),textsize=18,aligncenter=True)]
		)
		page.buttons['goParty'] = SimpleButton(pygame.Rect(855,25,50,50),
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(255,255,0,255),text='Party',textcolor=(247,13,26),textsize=18,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(190,190,0,255),text='Party',textcolor=(247,13,26),textsize=18,aligncenter=True)]
		)
		page.buttons['goArchive'] = SimpleButton(pygame.Rect(920,25,50,50),
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(255,255,0,255),text='Archive',textcolor=(247,13,26),textsize=18,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(190,190,0,255),text='Archive',textcolor=(247,13,26),textsize=18,aligncenter=True)]
		)
		page.buttons['goOption'] = SimpleButton(pygame.Rect(985,25,50,50),
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(255,255,0,255),text='Option',textcolor=(247,13,26),textsize=18,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,50,50),bgcolor=(190,190,0,255),text='Option',textcolor=(247,13,26),textsize=18,aligncenter=True)]
		)
		page.ui['kurenzy'] = TextBox(pygame.Rect(0,40,100,50),bgcolor=(255,255,255,255),text=f'kurenzy: {page.game.currency}',textsize=28).resize_fit(padding=5)

	def enter(page):
		page.bg = page.banners[page.currentbanner].bg

	def handle_events(page, events):
		for event in events:
			if not page.displayroll:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						pass
					elif event.key == pygame.K_LEFT:
						page.changeBanner(-1)
					elif event.key == pygame.K_RIGHT:
						page.changeBanner(+1)
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
					if page.buttons['roll1'].state == 1: # is Hover
						page.roll(1)
						page.displayroll = True
					elif page.buttons['roll10'].state == 1:
						page.roll(10)
						page.displayroll = True
					elif page.buttons['left-arrow'].state == 1:
						page.changeBanner(-1)
					elif page.buttons['right-arrow'].state == 1:
						page.changeBanner(+1)
					elif page.buttons['goMission'].state == 1:
						page.game.change_scene(page.game.scenes['Missions'])
					elif page.buttons['goParty'].state == 1:
						page.game.change_scene(page.game.scenes['TeamUp'])
					elif page.buttons['goArchive'].state == 1:
						page.game.change_scene(page.game.scenes['ArchivePage'])
					elif page.buttons['goOption'].state == 1:
						page.game.change_scene(page.game.scenes['OptionPage'])
			else:
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					page.displayroll = False
					page.justroll = []

	def update(page):
		for _,obj in page.buttons.items():
			obj.state = 1 if not page.displayroll and obj.isHover(page.game.mousepos) else 0

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			for _,obj in group.items():
				obj.draw(page.game.screen)

		if page.displayroll:
			page.game.screen.blit(page.vig,(0,0))

			cmax=5
			for i,char in enumerate(page.justroll):
				r,c = i//cmax,i%cmax
				page.game.screen.blit(char.getIcon(bg=True), (page.game.screen.get_width()/2-40+(c-2)*120,200+r*100))

	def roll(page,rolls=1):
		page.game.currency -= rolls*160
		page.ui['kurenzy'].text['string'] = f'kurenzy: {page.game.currency}'
		page.ui['kurenzy'].renderText(True)
		page.ui['kurenzy'].resize_fit(padding=5)
		for _ in range(rolls):
			daroll = page.banners[page.currentbanner].singleroll()
			page.game.increase_char_obtain(daroll.name)
			page.justroll.append(daroll)
	
	def changeBanner(page, step=1):
		page.currentbanner += step
		page.currentbanner %= len(page.banners)
		page.bg = page.banners[page.currentbanner].bg

	class Banner:
		def __init__(self,chardata,id,name,charlist,dropRateByRarity,bg):
			self.id = id
			self.name = name
			self.banner_rank = {1:[],2:[],3:[],4:[],5:[]}
			for charname in charlist:
				char = chardata[charname]
				self.banner_rank[char.rarity].append(char)
			self.droprate = [dr if len(self.banner_rank[i+1])>0 else 0 for i,dr in enumerate(dropRateByRarity)]

			self.bg = bg
			self.bg.blit(TextBox(pygame.Rect(0,0,100,50),text=id,antialias=False).sprite,(0,0))

		def singleroll(self):
				'''return a Character Class'''
				getrank = random.choices([1,2,3,4,5], weights=self.droprate,k=1)[0]
				same_rarity_char = self.banner_rank[getrank]
				return random.choices(same_rarity_char)[0]