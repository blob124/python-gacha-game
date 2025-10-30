import pygame
import random
import math
from stuff import *

FONT24 = pygame.font.SysFont(None, 24)
FONT40 = pygame.font.SysFont(None, 40)
EXITTXT = FONT24.render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class GachaPlace:
	def __init__(page,game):
		page.game = game

		page.banners = []
		page.currentbanner = 0

		tarvRC_bg = pygame.Surface((page.game.screen.get_size()))
		tarvRC_bg.fill((30,100,130))
		page.banners.append(Banner('tarvRC','Tarvern Recruit', [page.game.data[char] for char in ('Man','Woman','Unnamed01','Unnamed02')], [0,0,90,9.4,0.6],bg=tarvRC_bg))
		pp0_bg = pygame.Surface((page.game.screen.get_size()))
		pp0_bg.fill((30,190,130))
		page.banners.append(Banner('pp0','Pally Pal', [page.game.data[char] for char in ('Scribble','Redrill','Pebble')], [73,21,6,0,0],bg=pp0_bg))
		
		page.status = 0 # 0:normal, 1:pull animation
		page.justroll = []

		page.buttons = {}
		page.buttons['roll1'] = SimpleButton(pygame.Rect(200,450,100,50),
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(255,255,0,255),text='roll1',textcolor=(247,13,26),textsize=40,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(190,190,0,255),text='roll1',textcolor=(247,13,26),textsize=40,aligncenter=True)]
		)
		page.buttons['roll10'] = SimpleButton(pygame.Rect(769,450,100,50),
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(255,255,0,255),text='roll10',textcolor=(247,13,26),textsize=40,aligncenter=True)],
				[TextBox(pygame.Rect(0,0,100,50),bgcolor=(190,190,0,255),text='roll10',textcolor=(247,13,26),textsize=40,aligncenter=True)]
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

	def handle_events(page, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					pass
				elif event.key == pygame.K_LEFT:
					page.changeBanner(-1)
				elif event.key == pygame.K_RIGHT:
					page.changeBanner(+1)
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				if page.status == 0:
					if page.buttons['roll1'].state == 1: # is Hover
						page.roll(1)
						page.status = 1
					elif page.buttons['roll10'].state == 1:
						page.roll(10)
						page.status = 1
					elif page.buttons['goMission'].state == 1:
						page.game.change_scene(page.game.scenes['Missions'])
					elif page.buttons['goParty'].state == 1:
						page.game.change_scene(page.game.scenes['TeamUp'])
					elif page.buttons['goArchive'].state == 1:
						page.game.change_scene(page.game.scenes['ArchivePage'])
					elif page.buttons['goOption'].state == 1:
						page.game.change_scene(page.game.scenes['OptionPage'])
				else:
					page.status = 0
					page.justroll = []

	def update(page):
		for name,button in page.buttons.items():
			button.checkHover(page.game.mousepos)

	def draw(page):
		page.game.screen.blit(page.getCurrentBanner().surface,(0,0))

		for name,button in page.buttons.items():
			button.draw(page.game.screen)

		if page.status == 1:
			page.showroll()

	def roll(page,rolls=1):
		for _ in range(rolls):
			daroll = page.banners[page.currentbanner].singleroll()
			page.game.increase_char_obtain(daroll.name)
			page.justroll.append(daroll)
	
	def showroll(page):
		screenwidth,screenheight = page.game.screen.get_size()
		alpha_surface = pygame.Surface((screenwidth, screenheight), pygame.SRCALPHA)
		alpha_surface.fill((0,0,0,100))
		page.game.screen.blit(alpha_surface,(0,0))

		cmax=5
		for i,char in enumerate(page.justroll):
			r,c = i//cmax,i%cmax
			page.game.screen.blit(char.getIcon(bg=True), (screenwidth/2-40+(c-2)*120,200+r*100))
	
	def changeBanner(page, step=1):
		page.currentbanner += step
		page.currentbanner %= len(page.banners)

	def getCurrentBanner(page):
		return page.banners[page.currentbanner]

class Banner:
	def __init__(self,id,name,charlist,dropRateByRarity,bg):
		self.id = id
		self.name = name
		self.charlist = {1:[],2:[],3:[],4:[],5:[]}
		for char in charlist:
			self.charlist[char.rarity].append(char)
		self.droprate = [dr if len(self.charlist[i+1])>0 else 0 for i,dr in enumerate(dropRateByRarity)]

		self.surface = bg
		self.surface.blit(TextBox(pygame.Rect(0,0,100,50),text=id,antialias=False).sprite,(0,0))
	
	def singleroll(self):
		'''return a Character Class'''
		getrank = random.choices([1,2,3,4,5], weights=self.droprate,k=1)[0]
		same_rarity_char = self.charlist[getrank]
		return random.choices(same_rarity_char)[0]