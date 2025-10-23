import pygame
import random
import sys

from scenes.GachaPage import GachaPlace
from scenes.ArchivePage import Archive
from scenes.OptionPage import Settings

pygame.init()

class Game:
	def __init__(self):
		self.screen = pygame.display.set_mode((1067, 600))
		pygame.display.set_caption("Gacha Gambling")
		self.clock = pygame.time.Clock()

		self.loadData()
		self.scenes = {'GachaPlace':GachaPlace(self), 'ArchivePage':Archive(self), 'OptionPage':Settings(self)}

		pygame.mixer.init()
		pygame.mixer.music.load(f'data/sfx/music.mp3')
		pygame.mixer.music.set_volume(0.6)

		self.change_scene(self.scenes['GachaPlace'])
		pygame.mixer.music.play(-1)

	def run(self):
		self.running = True
		while self.running:
			self.mousepos = pygame.mouse.get_pos()
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					self.running = False

			self.scene.handle_events(events)
			self.scene.update()
			self.scene.draw(self.screen)

			pygame.display.flip()
			self.clock.tick(60)
	
	def loadData(self):
		self.data = {}
		self.char_obtained = {}

		try:
			with open('data/characterlist.txt','r') as charFile:
				for line in charFile:
					name,path_to_image,rarity,power = line.strip().split('_')
					try:
						image_art = pygame.image.load(f'data/art/{path_to_image}.png').convert_alpha()
					except:
						image_art = pygame.image.load('data/togorex464-T.png').convert_alpha()
					
					try:
						image_profile = pygame.image.load(f'data/icons/{path_to_image}.png').convert_alpha()
					except:
						image_profile = pygame.image.load('data/togore.bmp').convert_alpha()
					
					image_profile = pygame.transform.scale(image_profile, (80, 80))
					self.data[name] = Character(name,rarity,power,image_profile,image_art)
		except:
			print('character data file not found :sad:')
			pygame.quit()
			sys.exit()

		try:
			with open('data/profile.txt','r') as f:
				for line in f:
					name,dup = line.strip().split('=')
					self.char_obtained[name] = int(dup)
		except Exception as e:
			print('no profile, but that\'s fine')
			print(e)

		try:
			with open('data/currency.txt','r') as f:
				self.currency = f.readlines()[0].strip()
		except:
			self.currency = 0
	
	def saveData(self):
		with open('data/profile.txt','w') as f:
			towrite = []
			for char,dup in self.char_obtained.items():
				towrite.append(f'{char}={dup}')
			f.writelines('\n'.join(towrite))
		
		with open('data/currency.txt','w') as f:
			f.writelines(f'{self.currency}')

	def change_scene(self, new_scene):
		self.scene = new_scene

class Character:
	def __init__(self, name, rarity, power, icon_image, art_image):
		self.name = name
		self.rarity = rarity
		self.power = power
		self.imgIcon = icon_image
		self.imgArt = art_image

DEBUGGING = False
if not DEBUGGING:
	game = Game()
	game.run()
else:
	import cProfile

	if __name__ == "__main__":
		profiler = cProfile.Profile()
		profiler.enable()
		
		Game().run()
		
		profiler.disable()
		profiler.print_stats(sort="cumtime")

pygame.quit()
sys.exit()