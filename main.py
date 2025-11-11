import pygame
import sys
from pathlib import Path
import json

from scenes.GachaPage import GachaPlace
from scenes.MissionPage import Mission
from scenes.TeamPage import Party
from scenes.ArchivePage import Archive
from scenes.OptionPage import Settings

from stuff import Scene

PATH_CHAR_DATA = 'data/characterlist.json'
PATH_PROFILE = 'data/profile.json'
PATH_BANNERS = 'data/banners.json'
PATH_MUSIC = 'data/sfx/music.mp3'

pygame.init()

class Game:
	def __init__(game):
		game.screen = pygame.display.set_mode((1067, 600))
		pygame.display.set_caption("Gacha Gambling")
		game.clock = pygame.time.Clock()

		pygame.mixer.init()
		pygame.mixer.music.load(PATH_MUSIC)
		pygame.mixer.music.set_volume(0.6)
		pygame.mixer.music.play(-1)
		game.musicplaying = True

		game.loadData()
		game.scenes = {	'GachaPlace':GachaPlace(game),
						'Missions':Scene(game),
						'TeamUp':Scene(game),
						'ArchivePage':Archive(game),
						'OptionPage':Settings(game)
		}

		game.change_scene('GachaPlace')

	def run(game):
		game.running = True
		try:
			while game.running:
				game.mousepos = pygame.mouse.get_pos()
				events = pygame.event.get()
				for event in events:
					if event.type == pygame.QUIT:
						game.saveData()
						game.running = False

				game.scene.handle_events(events)
				game.scene.update()
				game.scene.draw()

				pygame.display.flip()
				game.clock.tick(60)
		except Exception as e:
			game.saveData()
			print(e)

	def loadData(game):
		game.data = {}
		game.char_obtained = {}
		game.party = []

		if Path(PATH_CHAR_DATA).is_file():
			with open(PATH_CHAR_DATA,'r') as f:
				chardata = json.load(f)
				for char in chardata:
					game.data[char['id']] = Character(char)
		else:
			print(f'{PATH_CHAR_DATA} not found :sad:')
			pygame.quit()
			sys.exit()

		if Path(PATH_PROFILE).is_file():
			with open(PATH_PROFILE,'r') as f:
				profile = json.load(f)
				for id,dup in profile['obtained'].items():
					game.char_obtained[int(id)] = dup

				game.party = profile['team']
				game.currency = profile['currency']
		else:
			print(f'{PATH_PROFILE} err something error')
			pygame.quit()
			sys.exit()
	
	def saveData(game):
		with open(PATH_PROFILE,'w') as f:
			data = {
				"obtained": game.char_obtained,
				"team": game.party,
				"currency": game.currency
			}
			json.dump(data, f, indent='\t')
	
	def increase_char_obtain(game,charid,amount=1):
		if charid not in game.char_obtained:
			game.char_obtained[charid] = amount
		else:
			game.char_obtained[charid] += amount
	
	def reset_profile(game):
		game.char_obtained = {'0':0}
		game.party = ['','','','','']
		game.currency = 6700
		game.saveData()
	
	def toggle_music(game):
		if game.musicplaying:
			game.musicplaying = False
			pygame.mixer.music.pause()
			pygame.mixer.music.set_pos(0)
		else:
			game.musicplaying = True
			pygame.mixer.music.unpause()

	def change_scene(game, new_scene):
		game.scene = game.scenes[new_scene]
		game.scene.enter()

	def enterCode(game, code):
		if code == 'NOTAGAME':
			game.currency += 2000
			return 'you recieve 2000 kurenzy.'
		return 'Invalid Code'

class Character:
	DIR = 'data/images/characters/'
	RANK_COLOR = [(124,142,161),(100,156,128),(91,150,186),(160,119,201),(204,152,88)]
	def __init__(self, char):
		self.id = char['id']
		self.name = char['name']
		self.rarity = char['rarity']
		self.power = char['power']
		self.imgpath = char['path']

		self.imgIcon = None
		self.imgArt = None
	
	def getIcon(self,bg=False):
		icon = self.imgIcon
		if icon is None:
			if Path(Character.DIR + self.imgpath + '_icon.png').is_file():
				icon = pygame.transform.scale(pygame.image.load(Character.DIR + self.imgpath + '_icon.png').convert_alpha(), (80, 80))
				self.imgIcon = icon
			else:
				icon = pygame.transform.scale(pygame.image.load(Character.DIR + 'placeholder_icon.png').convert_alpha(), (80, 80))

		if not bg:
			return icon
		else:
			sf = pygame.Surface((80,80))
			sf.fill(Character.RANK_COLOR[self.rarity-1])
			sf.blit(icon,(0,0))
			return sf

	def getArt(self):
		art = self.imgArt
		if art is None:
			artX, artY = 400,450
			if Path(Character.DIR + self.imgpath + '_art.png').is_file():
				art = pygame.transform.scale(pygame.image.load(Character.DIR + self.imgpath + '_art.png').convert_alpha(), (artX, artY))
				self.imgArt = art
			else:
				art = pygame.transform.scale(pygame.image.load(Character.DIR + 'placeholder_art.png').convert_alpha(), (artX, artY))
				
		return art

game = Game()
DEBUGGING = False
if not DEBUGGING:
	game.run()
else:
	import cProfile

	if __name__ == "__main__":
		profiler = cProfile.Profile()
		profiler.enable()
		
		game.run()
		
		profiler.disable()
		profiler.print_stats(sort="cumtime")

pygame.quit()
sys.exit()