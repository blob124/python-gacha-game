import pygame
import numpy as np
from pathlib import Path

import typing

PATH_CHARDATA_JSON = 'data/characterlist.json'
PATH_PROFILE_JSON = 'data/profile.json'
PATH_BANNERS_JSON = 'data/banners.json'
PATH_MUSIC_FILE = 'data/sfx/music.ogg'

pygame.init()

BLANK_SURFACE = pygame.Surface((0,0))
FONT_ABLE = {(None,24):pygame.font.SysFont(None,24)}

def getFont(font,size):
	if FONT_ABLE.get((font,size)) is None:
		FONT_ABLE[(font,size)] = pygame.font.SysFont(font,size)
	return FONT_ABLE.get((font,size))

class Character:
	DIR = 'data/images/characters/'
	RANK_COLOR = [(124,142,161),(100,156,128),(91,150,186),(160,119,201),(204,152,88)]
	def __init__(self, id, name, rarity, power, path):
		self.id = id
		self.name = name
		self.rarity = rarity
		self.power = power
		self.imgpath = path

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

class Scene:
	EXITTXT = getFont(None,24).render('Press Esc, it stands for Escape!', True, (255, 255, 255))
	def __init__(page, game):
		page.game = game

		page.bg = pygame.Surface(page.game.screen.get_size())
		page.bg.fill((100,100,100))
		page.bg.blit(Scene.EXITTXT,(20,20))
		page.bg.blit(renderTextWithLines('Scene\nTemplate',size=67),(432,234))

		page.images = {}
		page.buttons = {}
		page.ui = {}
		page.displaywarning = {}
		page.groups = {	0:page.images,
				 		1:page.buttons,
						2:page.ui,
						9:page.displaywarning}
		
		page.showwarning = False
		page.displaywarning['vig'] = VignetteLayer(page.game)
		page.displaywarning['warnbox'] = TextBox(Box(pygame.Rect(page.game.screen.get_width()/2-175,page.game.screen.get_height()/2-30,350,60),(225,225,225)),Text(f'warningtext',32,(225,130,0)))
	
	def enter(page):
		pass

	def handle_events(page, events):
		for event in events:
			if page.showwarning:
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					page.showwarning = False
				continue
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					page.game.change_scene('GachaPlace')
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				pass

			for _,button in page.buttons.items():
				button.handle_event(event)

	def update(page):
		for _,button in page.buttons.items():
			if not page.showwarning:
				button.update(page.game.mousepos)
			else:
				button.hovered = False

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			if group is page.displaywarning and not page.showwarning:
				continue
			for _,obj in group.items():
				obj.draw(page.game.screen)

	def updatewarningbox(page,text):
		page.displaywarning['warnbox'].text.update(text)
		page.displaywarning['warnbox'].update()
		page.showwarning = True

class Image(pygame.sprite.Sprite):
	tweenDuration = 100
	def __init__(self, image:pygame.Surface, topleft:tuple[float,float] = (0,0)):
		super().__init__()
		self.image = self.ogimage = image
		self.rect = self.image.get_rect(topleft=topleft)

		self.drawgrayscale = False
		self.imageButGray = None

		self.animating = False
		self.start_time = 0
		self.scale = self.target_scale = self.start_scale = 1

	def get_grayscale(self):
		if self.imageButGray is None:
			self.imageButGray = to_grayscale(self.image)
		return self.imageButGray
	
	def update(self, mouse_pos):
		if self.rect.collidepoint(mouse_pos):
			self.scale_animation_errr_thing(1.1)
		else:
			self.scale_animation_errr_thing(1)
		
		# Tween animation
		if self.animating:
			t = (pygame.time.get_ticks() - self.start_time) / __class__.tweenDuration
			if t >= 1:
				t = 1
				self.animating = False
			eased_t = Tween.easeOutCirc(t)
			self.scale = self.start_scale + (self.target_scale - self.start_scale) * eased_t

		# Scale image
		self.image = pygame.transform.rotozoom(self.ogimage, 0, self.scale)
		self.imageButGray = None
		self.rect = self.image.get_rect(center=self.rect.center)
	
	def scale_animation_errr_thing(self, target_scale:float) -> None:
		if self.target_scale != target_scale:
			self.animating = True
			self.start_time = pygame.time.get_ticks()
			self.start_scale = self.scale
			self.target_scale = target_scale

	def draw(self, screen):
		toblit = self.image if not self.drawgrayscale else self.get_grayscale()
		screen.blit(toblit, self.rect)

class Box(pygame.sprite.Sprite):
	def __init__(self, rect:pygame.Rect, bgcolor:tuple[int,...]=(0,0,0,0), boardcolor:tuple[int,...]=(0,0,0), boardsize=0):
		self.rect = rect
		self.bgColor = bgcolor
		self.bdColor = boardcolor
		self.bdSize = boardsize
		self.image = None

		self.update()
	
	def update(self):
		daBox = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
		bgColor = (list(self.bgColor)+[255])[:4]
		bdColor = (list(self.bdColor)+[255])[:4]
		bdSize = self.bdSize
		if bdSize >= min(self.rect.size):
			daBox.fill(bdColor)
		else:
			daBox.fill(bgColor)
			if bdSize > 0:
				pygame.draw.rect(daBox,bdColor[:3],(0,0,self.rect.w,self.rect.h),bdSize)
		self.image = daBox

	def draw(self, screen):
		screen.blit(self.image, self.rect)

class Text(pygame.sprite.Sprite):
	def __init__(self, text='', textsize=24, textcolor:tuple[int,...]=(0,0,0), antialias=True, align: typing.Literal['left','middle','right']='middle'):
		self.text = str(text)
		self.textSize = textsize
		self.textColor = textcolor
		self.antialias = antialias
		self.align = align

		self.update(xy=(0,0))
	
	def update(self,newtext=None,xy:tuple[float,float]=None):
		if newtext is not None:
			self.text = newtext
		if xy is None:
			xy=self.rect.topleft
		self.image = renderTextWithLines(self.text,self.textColor,self.textSize,self.antialias,self.align)
		self.rect = self.image.get_rect(topleft=xy)
		return self

	def draw(self, screen):
		screen.blit(self.image, self.rect)

class TextBox:
	def __init__(self, box:Box|Image, text:Text, align:typing.Literal['left','middle','right']='middle'):
		self.box = box
		self.text = text
		self.align = align
		self.update()
	
	def update(self):
		self.image = self.box.image.copy()
		match self.align.lower():
			case 'left':
				padding = 5
				self.image.blit(self.text.image,(padding,self.box.rect.h/2-self.text.rect.h/2))
			case 'right':
				padding = 5
				self.image.blit(self.text.image,(self.box.rect.w-self.text.rect.w-padding,self.box.rect.h/2-self.text.rect.h/2))
			case _:
				self.image.blit(self.text.image,(self.box.rect.w/2-self.text.rect.w/2,self.box.rect.h/2-self.text.rect.h/2))

	def resize_fit(self,padding=0):
		new_rect = self.text.rect.inflate(padding*2,padding*2)
		self.box.rect.width = new_rect.width
		self.box.rect.height = new_rect.height
		self.aligncenter = True
		self.box.update()
		self.update()
		return self
	
	def draw(self, screen):
		screen.blit(self.image, self.box.rect)

class Interactable:
	def __init__(self, xy:tuple[float, float], *states:list[pygame.Rect|pygame.Surface], callback=None):
		"""---
		xy: (x,y)\n
		states: state0, state1, ...\n
		state: [pygame.Rect(0,0,width,height), imageSurface]
		"""
		self.x, self.y = xy
		self.hovered = False
		self.state = 0
		self.states = []
		self.callback = callback
		for state in states:
			daHitbox, daSprite = state
			self.states.append({'hitbox':daHitbox,'sprite':daSprite})
	
	def update(self, mouse_pos):
		self.hovered = self.curState()['hitbox'].move(self.x,self.y).collidepoint(mouse_pos)

	def curState(self):
		return self.states[self.state*2 + (1 if self.hovered else 0)]

	def draw(self,screen):
		screen.blit(self.curState().get('sprite').image, (self.x,self.y))
	
	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if self.hovered and self.callback:
				self.callback()

class SimpleButton(Interactable):
	def __init__(self, rect:pygame.Rect, *sprites:list[pygame.Surface], callback=None):
		super().__init__(rect.topleft,*[[pygame.Rect(0,0,rect.w,rect.h),*sprite] for sprite in sprites],callback=callback)

class CoolTextBox(Interactable):
	count = 0
	def __init__(self, box:Box|Image, text:Text, callback=None):
		CoolTextBox.count += 1
		self.BLINK_EVENT = pygame.USEREVENT + CoolTextBox.count
		pygame.time.set_timer(self.BLINK_EVENT, 545)

		hitbox = pygame.Rect(0,0,box.rect.w,box.rect.h)
		super().__init__(box.rect.topleft, [hitbox,Box(box.rect,box.bgColor,box.bdColor,0)], [hitbox,Box(box.rect,box.bgColor,box.bdColor,2)], [hitbox,Box(box.rect,box.bgColor,box.bdColor,3)], [hitbox,Box(box.rect,box.bgColor,box.bdColor,3)])
		self.focus = False
		self.hovered = False
		self.textcursorvisible = False

		self.callback = callback

		self.text = text
	
	def update(self, mouse_pos):
		self.hovered = self.curState()['hitbox'].move(self.x,self.y).collidepoint(mouse_pos)
		padding = 5
		self.text.update(xy=(self.x+padding, self.y+self.curState()['sprite'].rect.h/2-self.text.rect.h/2))

	def draw(self, screen):
		screen.blit(self.curState()['sprite'].image, (self.x,self.y))
		screen.blit(self.text.image, self.text.rect)
		if self.textcursorvisible:
			pygame.draw.line(screen, self.text.textColor, (self.text.rect.right+1,self.text.rect.top-5), (self.text.rect.right+1,self.text.rect.bottom+1), 1)
	
	def handle_event(self, event):
		if event.type == self.BLINK_EVENT and self.focus:
			self.textcursorvisible = not self.textcursorvisible
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			self.focus = self.hovered and not self.focus
			self.state = 1 if self.focus else 0
			self.textcursorvisible = self.focus

		elif self.focus and event.type == pygame.KEYDOWN:
			match pygame.key.name(event.key):
				case 'backspace':
					if len(self.text.text)>0:
						self.text.update(newtext=self.text.text[:-1])
				case 'return':
					if self.callback:
						self.callback()
					self.text.update(newtext='')
				case _:
					if event.unicode:
						self.text.update(newtext=self.text.text+event.unicode)

class VignetteLayer(Box):
	def __init__(self, game, color:tuple[int,...]=(0,0,0)):
		super().__init__(pygame.Rect(0,0,game.screen.get_width(),game.screen.get_height()), (list(color)+[100])[:4])

class ToolTip(Interactable):
	def __init__(self, icon:Image, textbox:TextBox):
		self.icon = icon
		darkicon = pygame.mask.from_surface(icon.image).to_surface(setcolor=(0,0,0,80),unsetcolor=(0,0,0,0))
		icon1 = Image(icon.image.copy(),(0,0))
		icon2 = Image(icon.image.copy(),(0,0))
		icon2.image.blit(darkicon,(0,0))
		super().__init__(icon.rect.topleft,*[[pygame.Rect(0,0,icon.rect.w,icon.rect.h),*sprite] for sprite in [[icon1],[icon2]]],callback=None)
		self.tooltip = textbox
		self.tooltipImage = Image(pygame.Surface((self.tooltip.box.rect.w,self.tooltip.box.rect.h+10),flags=pygame.SRCALPHA),(0,0))
		self.tooltipabove = True
		self.repostooltip()
		if self.tooltipabove:
			pygame.draw.polygon(self.tooltipImage.image,self.tooltip.box.bgColor,[(self.tooltipImage.rect.w/2-30,self.tooltipImage.rect.h-10),(self.tooltipImage.rect.w/2,self.tooltipImage.rect.h),(self.tooltipImage.rect.w/2+30,self.tooltipImage.rect.h-10)])
		else:
			pygame.draw.polygon(self.tooltipImage.image,self.tooltip.box.bgColor,[(self.tooltipImage.rect.w/2-30,10),(self.tooltipImage.rect.w/2,0),(self.tooltipImage.rect.w/2+30,10)])
		self.tooltip.draw(self.tooltipImage.image)

	def repostooltip(self):
		self.icon.rect.topleft = (self.x,self.y)
		self.tooltipImage.rect.midbottom = self.icon.rect.midtop
		self.tooltipImage.rect.bottom -= 5
		self.tooltip.box.rect.top = 0
		self.tooltipabove = True
		if self.tooltipImage.rect.top<0:
			self.tooltipImage.rect.midtop = self.icon.rect.midbottom
			self.tooltipImage.rect.top += 5
			self.tooltip.box.rect.top = 10
			self.tooltipabove = False

	def draw(self, screen):
		super().draw(screen)
		if self.hovered:
			self.tooltipImage.draw(screen)

class Tween:
	"tween lib at home"
	def easeOutQuad(t: float) -> float:
		return 1 - (1 - t)**2
	
	def easeInCubic(t: float) -> float:
		return t**3
	
	def easeOutCubic(t: float) -> float:
		return 1 - (1 - t)**3
	
	def easeOutCirc(t: float) -> float:
		return (1 - (t - 1)**2)**0.5

def renderTextWithLines(text:str,textColor:tuple[int,...]=(0,0,0),size=24,anti_alias=True, align:typing.Literal['left','middle','right']='middle') -> pygame.Surface:
	thefont = getFont(None, size)
	antialias = anti_alias
	if '\n' not in text:
		text_render = thefont.render(text,antialias,textColor)
		text_surface = text_render
	else:
		newlineOffY = thefont.size('A')[1]/8

		text_render = {(x:=thefont.render(minitext,antialias,textColor)):(x.get_width(),x.get_height()) for minitext in text.split('\n')}
		text_render_width = max([w for w,_ in text_render.values()])
		text_render_height = sum([h+newlineOffY for _,h in text_render.values()])-newlineOffY
		text_surface = pygame.Surface(pygame.Rect(0,0,text_render_width,text_render_height).size,flags=pygame.SRCALPHA)

		text_render_y = 0
		for minitext,(width,height) in text_render.items():
			match(align.lower()):
				case 'left':
					text_render_x = 0
				case 'middle':
					text_render_x = text_render_width/2-width/2
				case _:
					text_render_x = text_render_width-width
			text_surface.blit(minitext, (text_render_x, text_render_y))
			text_render_y += height+newlineOffY
	
	return text_surface

def to_grayscale(surface: pygame.Surface) -> pygame.Surface:
	"""
	Convert a Pygame surface to grayscale.
	Preserves alpha transparency if present.
	"""
	# Handle alpha
	has_alpha = surface.get_flags() & pygame.SRCALPHA

	# Convert to array
	arr = pygame.surfarray.array3d(surface)
	gray = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]).astype(np.uint8)
	gray3d = np.stack((gray,)*3, axis=-1)

	# Make grayscale surface
	gray_surface = pygame.surfarray.make_surface(gray3d)

	# If surface had transparency, copy alpha channel
	if has_alpha:
		alpha = pygame.surfarray.array_alpha(surface)
		gray_surface = gray_surface.convert_alpha()
		pygame.surfarray.pixels_alpha(gray_surface)[:] = alpha

	return gray_surface