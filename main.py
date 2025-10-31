import pygame
import sys
from pathlib import Path

from scenes.GachaPage import GachaPlace
from scenes.MissionPage import Mission
from scenes.TeamPage import Party
from scenes.ArchivePage import Archive
from scenes.OptionPage import Settings

from stuff import Scene

pygame.init()

class Game:
	def __init__(game):
		game.screen = pygame.display.set_mode((1067, 600))
		pygame.display.set_caption("Gacha Gambling")
		game.clock = pygame.time.Clock()

		game.loadData()
		game.scenes = {	'GachaPlace':GachaPlace(game),
						'Missions':Scene(game),
						'TeamUp':Scene(game),
						'ArchivePage':Archive(game),
						'OptionPage':Settings(game)
		}

		pygame.mixer.init()
		pygame.mixer.music.load(f'data/sfx/music.mp3')
		pygame.mixer.music.set_volume(0.4)

		game.change_scene(game.scenes['GachaPlace'])
		pygame.mixer.music.play(-1)

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

		if Path('data/characterlist.txt').is_file():
			with open('data/characterlist.txt','r') as charFile:
				for line in charFile:
					name,path_to_image,rarity,power = line.strip().split('_')
					game.data[name] = Character(name,int(rarity),int(power),path_to_image)
		else:
			print('character data file not found :sad:')
			pygame.quit()
			sys.exit()

		if Path('data/profile.txt').is_file():
			with open('data/profile.txt','r') as f:
				_,obtain,party,currency = f.read().strip().split('[--]')
				for char in obtain.strip().split():
					name,dup = char.split('=')
					game.char_obtained[name] = int(dup)

				game.party = party.strip().split(',')
				game.currency = currency.strip()
		else:
			print('something error')
			pygame.quit()
			sys.exit()
	
	def saveData(game):
		with open('data/profile.txt','w') as f:
			obtain = '\n'.join([f'{char}={dup}' for char,dup in game.char_obtained.items()])
			party = ','.join(game.party)
			currency = game.currency
			f.writelines(f'[--]\n{obtain}\n[--]\n{party}\n[--]\n{currency}')
	
	def increase_char_obtain(game,charname,amount=1):
		if charname not in game.char_obtained:
			game.char_obtained[charname] = amount
		else:
			game.char_obtained[charname] += amount

	def change_scene(game, new_scene):
		game.scene = new_scene
		game.scene.enter()

RANK_COLOR = [(124,142,161),(100,156,128),(91,150,186),(160,119,201),(204,152,88)]
class Character:
	def __init__(self, name, rarity, power, image_path):
		self.name = name
		self.rarity = rarity
		self.power = power

		self.imgpath = image_path
		self.imgIcon = None
		self.imgArt = None
	
	def getIcon(self,bg=False):
		icon = self.imgIcon
		if icon is None:
			if Path(f'data/images/characters/{self.imgpath}_icon.png').is_file():
				icon = pygame.transform.scale(pygame.image.load(f'data/images/characters/{self.imgpath}_icon.png').convert_alpha(), (80, 80))
				self.imgIcon = icon
			else:
				icon = pygame.transform.scale(pygame.image.load(f'data/images/characters/placeholder_icon.png').convert_alpha(), (80, 80))

		if not bg:
			return icon
		else:
			sf = pygame.Surface((80,80))
			sf.fill(RANK_COLOR[self.rarity-1])
			sf.blit(icon,(0,0))
			return sf

	def getArt(self):
		art = self.imgArt
		if art is None:
			if Path(f'data/images/characters/{self.imgpath}_art.png').is_file():
				art = pygame.transform.scale(pygame.image.load(f'data/images/characters/{self.imgpath}_art.png').convert_alpha(), (400, 450))
				self.imgArt = art
			else:
				art = pygame.transform.scale(pygame.image.load(f'data/images/characters/placeholder_art.png').convert_alpha(), (400, 450))
				
		return art

game = Game()
game.run()

pygame.quit()
sys.exit()