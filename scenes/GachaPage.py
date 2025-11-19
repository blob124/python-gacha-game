import pygame
import random
import math
from pathlib import Path
from stuff import *
import json

class GachaPlace(Scene):
	def __init__(page,game):
		super().__init__(game)

		page.showroll = False
		page.displayroll = {}
		page.groups[3] = page.displayroll

		page.banners = []
		page.currentbanner = 0
		with open(PATH_BANNERS_JSON,'r') as f:
			banners = json.load(f)
			for banner in banners:
				page.banners.append(page.Banner(page,**banner))

		page.ui['kurenzy'] = TextBox(pygame.Rect(0,40,1100,50),(255,255,255),text=f'kurenzy: 0',textsize=28).fittotext(padding=5)
		minigraycirc = pygame.Surface((26,26),flags=pygame.SRCALPHA)
		pygame.draw.circle(minigraycirc,(130,130,130),(minigraycirc.get_width()/2,minigraycirc.get_height()/2),minigraycirc.get_width()/2)
		tooltipIcon = TextBox(Image(minigraycirc),text='i',textsize=24,textcolor=(255,255,255))
		page.ui['tooltip'] = ToolTip(Image(tooltipIcon.image,(0,0)),TextBox(pygame.Rect(0,0,110,50),(80,80,80,130),text='tip for gambling: \ndon\'t',textsize=18,textcolor=(255,255,255)))

		page.buttons['left-arrow'] = SimpleButton(pygame.Rect(40,(page.game.screen.get_height()-80)//2,50,80), [TextBox(pygame.Rect(0,0,50,80),(255,255,255,190),text='<',textsize=96)], [TextBox(pygame.Rect(0,0,50,80),(190,190,190,255),text='<',textsize=96)],
			callback=lambda: page.changeBanner(-1))
		
		page.buttons['right-arrow'] = SimpleButton(pygame.Rect(page.game.screen.get_width()-50-40,(page.game.screen.get_height()-80)//2,50,80), [TextBox(pygame.Rect(0,0,50,80),(255,255,255,190),text='>',textsize=96)], [TextBox(pygame.Rect(0,0,50,80),(190,190,190,255),text='>',textsize=96)],
			callback=lambda: page.changeBanner(+1))
		
		page.buttons['roll1'] = SimpleButton(pygame.Rect(200,500,100,50), *[[TextBox(pygame.Rect(0,0,100,50),(255,255,0,255) if i==0 else (190,190,0,255),text=f'roll1\nx{banner.price}',textsize=30,textcolor=(247,13,26))] for banner in page.banners for i in range(2)],
			callback=lambda: page.roll(1))
		
		page.buttons['roll10'] = SimpleButton(pygame.Rect(769,500,100,50), *[[TextBox(pygame.Rect(0,0,100,50),(255,255,0,255) if i==0 else (190,190,0,255),text=f'roll10\nx{10*banner.price}',textsize=30,textcolor=(247,13,26))] for banner in page.banners for i in range(2)],
			callback=lambda: page.roll(10))
		'''
		page.buttons['goMission'] = SimpleButton(pygame.Rect(790,25,50,50), [TextBoxOldx(Box(pygame.Rect(0,0,50,50),(255,255,0,255)),Text('Quest',18,(247,13,26)))], [TextBoxOldx(Box(pygame.Rect(0,0,50,50),(190,190,0,255)),Text('Quest',18,(247,13,26)))],
			callback=lambda: page.game.change_scene('Missions'))
		
		page.buttons['goParty'] = SimpleButton(pygame.Rect(855,25,50,50), [TextBoxOldx(Box(pygame.Rect(0,0,50,50),(255,255,0,255)),Text('Party',18,(247,13,26)))], [TextBoxOldx(Box(pygame.Rect(0,0,50,50),(190,190,0,255)),Text('Party',18,(247,13,26)))],
			callback=lambda: page.game.change_scene('TeamUp'))
		'''
		page.buttons['goArchive'] = SimpleButton(pygame.Rect(920,25,50,50), [TextBox(pygame.Rect(0,0,50,50),(255,255,0,255),text='Archive',textsize=18,textcolor=(247,13,26))], [TextBox(pygame.Rect(0,0,50,50),(190,190,0,255),text='Archive',textsize=18,textcolor=(247,13,26))],
			callback=lambda: page.game.change_scene('ArchivePage'))
		
		page.buttons['goOption'] = SimpleButton(pygame.Rect(985,25,50,50), [TextBox(pygame.Rect(0,0,50,50),(255,255,0,255),text='Option',textsize=18,textcolor=(247,13,26))], [TextBox(pygame.Rect(0,0,50,50),(190,190,0,255),text='Option',textsize=18,textcolor=(247,13,26))],
			callback=lambda: page.game.change_scene('OptionPage'))
		

		page.displayroll['vig'] = VignetteLayer(page.game,(0,0,0,130))
		page.displayroll['reward'] = pygame.sprite.Group()
		page.displayroll['value'] = TextBox(pygame.Rect(__class__.DISPLAYROLL_TOPCENTER[0]-65,400,130,40),(225,225,225),text=f'worth: {0}',textsize=32,textcolor=(225,130,0))

	def enter(page):
		page.bg = page.currentBanner().bg
		page.reload_currency()
		
	def handle_events(page, events):
		for event in events:
			if page.showwarning:
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					page.showwarning = False
				continue

			if page.showroll:
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					page.showroll = False
					page.displayroll['reward'].empty()
				continue
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					pass
				elif event.key == pygame.K_LEFT:
					page.changeBanner(-1)
				elif event.key == pygame.K_RIGHT:
					page.changeBanner(+1)
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				pass

			for _,button in page.buttons.items():
				button.handle_event(event)

	def update(page):
		if not (page.showroll or page.showwarning):
			for _,button in page.buttons.items():
				button.update(page.game.mousepos)
			page.ui['tooltip'].update(page.game.mousepos)
		else:
			for _,button in page.buttons.items():
				button.hovered = False
			page.ui['tooltip'].hovered = False

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			if group is page.displaywarning and not page.showwarning:
				continue

			if group is page.displayroll and not page.showroll:
				continue
			
			for _,obj in group.items():
				obj.draw(page.game.screen)

	DISPLAYROLL_CMAX = 5
	DISPLAYROLL_TOPCENTER = (1067/2, 200)
	def roll(page,rolls=1):
		if page.game.currency < page.currentBanner().price * rolls:
			page.updatewarningbox('sowwy!\nnot enough kurenzy.')
			return

		page.reload_currency(-rolls*page.currentBanner().price)
		tcx, tcy = __class__.DISPLAYROLL_TOPCENTER
		sum_power = 0
		for i in range(rolls):
			chardrop = page.currentBanner().singleroll()
			page.game.increase_char_obtain(chardrop.id)

			r,c = i//__class__.DISPLAYROLL_CMAX,i%__class__.DISPLAYROLL_CMAX
			page.displayroll['reward'].add(Image(chardrop.getIcon(bg=True),(tcx-40+(c-2)*120,tcy+r*100)))
			sum_power += chardrop.power
		page.displayroll['value'].text = f'worth: {sum_power}'
		page.displayroll['value'].update()
		page.showroll = True
	
	def reload_currency(page,delta=0):
		page.game.currency += delta
		page.ui['kurenzy'].text = f'kurenzy: {page.game.currency}'
		page.ui['kurenzy'].updateText()
		page.ui['kurenzy'].fittotext(padding=5)

		page.ui['tooltip'].x = page.ui['kurenzy'].rect.right+10
		page.ui['tooltip'].y = page.ui['kurenzy'].rect.top+3
		page.ui['tooltip'].repostooltip()
		
	def currentBanner(page):
		return page.banners[page.currentbanner]
	
	def changeBanner(page, step=1):
		page.currentbanner += step
		page.currentbanner %= len(page.banners)
		page.bg = page.currentBanner().bg

		page.buttons['roll1'].state = page.buttons['roll10'].state = page.currentbanner

	class Banner:
		DIR_IMAGE = 'data/images/banners/'
		DAFAULT_BANNER_IMAGE = pygame.image.load(DIR_IMAGE+'banner_default.png')
		CHESTTHATGOTOTHECENTER = [pygame.transform.scale_by(pygame.image.load(path),0.1) if Path(path).is_file() else BLANK_SURFACE for path in [DIR_IMAGE+'ระดับเทพพพ.png',DIR_IMAGE+'ระดับกลางงงง.png',DIR_IMAGE+'อ่อนสุด.png']]
		def __init__(self,page,id,name,list,chance,price,img):
			self.id = id
			self.name = name
			self.banner_by_rank = {rank+1:(dr,[]) for rank,dr in enumerate(chance)}
			self.price = price
			for charid in list:
				char = page.game.data[charid]
				if char.rarity in self.banner_by_rank:
					self.banner_by_rank[char.rarity][1].append(char)

			if Path(__class__.DIR_IMAGE + img).is_file():
				self.bg = pygame.transform.scale(pygame.image.load(__class__.DIR_IMAGE + img).convert_alpha(), page.game.screen.get_size())
				self.bg.blit(__class__.DAFAULT_BANNER_IMAGE,(0,0))
				chest = 0
				if price < 120:
					chest = 2
				elif price < 160:
					chest = 1
				self.bg.blit(__class__.CHESTTHATGOTOTHECENTER[chest],(450,197))
				title = TextBox(text=self.name,textsize=67,textcolor=(255,255,255))
				title.rect.center = (1067/2,100)
				title.draw(self.bg)
			else:
				self.bg = pygame.surface(page.game.screen.get_size())
				TextBox(text=self.id,antialias=False).draw()

		def singleroll(self):
			'''return a Character Class'''
			getrank = random.choices([1,2,3,4,5], weights=[self.banner_by_rank[i][0] if self.banner_by_rank[i][1] else 0 for i in [1,2,3,4,5]],k=1)[0]
			same_rarity_char = self.banner_by_rank[getrank][1]
			return random.choices(same_rarity_char)[0]