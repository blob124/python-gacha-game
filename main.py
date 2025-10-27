import pygame
import random
import sys

from scenes.GachaPage import GachaPlace
from scenes.MissionPage import Mission
from scenes.TeamPage import Party
from scenes.ArchivePage import Archive
from scenes.OptionPage import Settings

pygame.init()

class Game:
	def __init__(game):
		game.screen = pygame.display.set_mode((1067, 600))
		pygame.display.set_caption("Gacha Gambling")
		game.clock = pygame.time.Clock()

		game.loadData()
		game.scenes = {	'GachaPlace':GachaPlace(game),
						'Missions':Mission(game),
						'TeamUp':Party(game),
						'ArchivePage':Archive(game),
						'OptionPage':Settings(game)}

		pygame.mixer.init()
		pygame.mixer.music.load(f'data/sfx/music.mp3')
		pygame.mixer.music.set_volume(0.6)

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
				game.scene.draw(game.screen)

				pygame.display.flip()
				game.clock.tick(60)
		except Exception as e:
			game.saveData()
			print(e)
			
	
	def loadData(game):
		game.data = {}
		game.char_obtained = {}
		game.party = []

		try:
			with open('data/characterlist.txt','r') as charFile:
				for line in charFile:
					name,path_to_image,rarity,power = line.strip().split('_')
					game.data[name] = Character(name,int(rarity),int(power),path_to_image)
		except:
			print('character data file not found :sad:')
			pygame.quit()
			sys.exit()

		try:
			with open('data/profile.txt','r') as f:
				_,obtain,party,currency = f.read().strip().split('[--]')
				for char in obtain.strip().split():
					name,dup = char.split('=') 
					game.increase_char_obtain(name,int(dup))

				game.party = party.strip().split(',')
				game.currency = currency.strip()
				
		except Exception as e:
			print(e)
			pygame.quit()
			sys.exit()
	
	def saveData(game):
		with open('data/profile.txt','w') as f:
			obtain = '\n'.join([f'{char}={dup}' for char,dup in game.char_obtained.items()])
			party = ','.join(game.party)
			currency = game.currency
			f.writelines(f'[--]\n{obtain}\n[--]\n{party}\n[--]\n{currency}')
	
	def increase_char_obtain(game,name,amount=1):
		if name not in game.char_obtained:
			game.char_obtained[name] = amount
		else:
			game.char_obtained[name] += amount

	def change_scene(game, new_scene):
		game.scene = new_scene

class Character:
	def __init__(game, name, rarity, power, image_path):
		game.name = name
		game.rarity = rarity
		game.power = power

		game.imgpath = image_path
		game.imgIcon = None
		game.imgArt = None
	
	def getIcon(game):
		if game.imgIcon is None:
			try:
				icon = pygame.image.load(f'data/images/{game.imgpath}_icon.png').convert_alpha()
				icon = pygame.transform.scale(icon, (80, 80))
				game.imgIcon = icon
			except:
				icon = togoreIcon
			return icon
		else:
			return game.imgIcon
	
	def getArt(game):
		if game.imgArt is None:
			try:
				art = pygame.image.load(f'data/images/{game.imgpath}_art.png').convert_alpha()
				art = pygame.transform.scale(art, (400, 450))
				game.imgArt = art
			except:
				art = togoreArt
				
			return art
		else:
			return game.imgArt

game = Game()
togoreIcon = pygame.transform.scale(pygame.image.load('data/togore.bmp').convert_alpha(), (80, 80))
togoreArt = pygame.transform.scale(pygame.image.load('data/togorex464-T.png').convert_alpha(), (400, 450))


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