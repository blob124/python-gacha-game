import pygame
import sys
from pathlib import Path
import json

from scenes.GachaPage import GachaPlace
from scenes.MissionPage import Mission
from scenes.TeamPage import Party
from scenes.ArchivePage import Archive
from scenes.OptionPage import Settings

from stuff import *

pygame.init()

class Game:
	def __init__(game):
		game.screen = pygame.display.set_mode((1067, 600))
		pygame.display.set_caption("Gacha Gambling")
		game.clock = pygame.time.Clock()

		game.loadData()
		game.entercodehere_flag = 0

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
		game.usedcode = []

		needfile = [PATH_CHARDATA_JSON,PATH_PROFILE_JSON,PATH_BANNERS_JSON,PATH_MUSIC_FILE]
		missing = [file for file in needfile if not Path(file).is_file()]

		if missing:
			print(f'file(s) not found :sad:\n{missing}')
			pygame.quit()
			sys.exit()
		
		with open(PATH_CHARDATA_JSON,'r') as f:
			chardata = json.load(f)
			for char in chardata:
				game.data[char['id']] = Character(**char)

		with open(PATH_PROFILE_JSON,'r') as f:
			profile = json.load(f)
			for id,dup in profile['obtained'].items():
				game.char_obtained[int(id)] = dup

			game.party = profile['team']
			game.currency = profile['currency']
		
		try:
			with open('data/usedcode.json','r') as f:
				file = json.load(f)
				game.usedcode = file
		except:
			print(f'where is your history code O.o')
		
		pygame.mixer.init()
		pygame.mixer.music.load(PATH_MUSIC_FILE)
		pygame.mixer.music.set_volume(0.6)
		pygame.mixer.music.play(-1)
		game.musicplaying = True
	
	def saveData(game):
		with open(PATH_PROFILE_JSON,'w') as f:
			data = {
				"obtained": game.char_obtained,
				"team": game.party,
				"currency": game.currency
			}
			json.dump(data, f, indent='\t')
		
		with open('data/usedcode.json','w') as f:
			json.dump(game.usedcode, f)
	
	def increase_char_obtain(game,charid,amount=1):
		if charid not in game.char_obtained:
			game.char_obtained[charid] = amount
		else:
			game.char_obtained[charid] += amount
	
	def reset_profile(game):
		game.char_obtained = {'0':0}
		game.party = ['','','','','']
		game.currency = 6700
		game.usedcode = []
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
		if code in game.usedcode:
			return f'this code ({code})\nis used.'
		if code == 'NOTAGAME':
			game.currency += 2000
			game.usedcode.append(code)
			return 'you recieve 2000 kurenzy.'
		if code == 'GIVEME67000':
			game.currency += 67000
			game.usedcode.append(code)
			return 'you recieve 67000 kurenzy.'
		if code == 'ENTERCODEHERE':
			game.currency += 0
			text_return = ''
			if game.entercodehere_flag == 0:
				text_return = 'ENTERCODEHERE is not work bro\ntry again.'
			elif game.entercodehere_flag == 1:
				text_return = 'you think do it again make it work?\nit\'s not work like that bro.'
			elif game.entercodehere_flag == 2:
				text_return = 'why are you still doing it.'
			elif game.entercodehere_flag == 3:
				text_return = 'ok! i can do this all day.'
			elif game.entercodehere_flag == 4:
				text_return = 'i appreciate that you\ntyped each letter for this.'
			elif game.entercodehere_flag == 5:
				text_return = 'arent you here to do\nthe gacha thing?.'
			elif game.entercodehere_flag == 6:
				text_return = 'now you keep bugging me.'
			elif game.entercodehere_flag == 7:
				text_return = 'get out.'
			else:
				return 'ENTERCODEHERE\nis not a valid code.'
			game.entercodehere_flag += 1
			return text_return
		if code == 'again':
			game.currency += 0
			return 'if you want the code so bad,\n just find it in the code. bruh'
		if code == 'redeemCode':
			game.currency += 1
			return '* ok                                                     \n* (you recieve a single kurenzy.)'
		return 'Invalid Code'

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