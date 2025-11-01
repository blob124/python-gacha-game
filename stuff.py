import pygame

pygame.init()

EXITTXT = pygame.font.SysFont(None, 24).render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Scene:
	def __init__(page,game):
		page.game = game

		page.bg = pygame.Surface(page.game.screen.get_size())
		page.bg.fill((100,100,100))
		page.bg.blit(EXITTXT,(20,20))

		page.bg.blit(renderTextWithLines('Scene\nTemplate',size=67),(432,234))

		page.images = {}
		page.buttons = {}
		page.groups = {	0:page.images,
				 		1:page.buttons}
	
	def enter(page):
		pass

	def handle_events(page, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					page.game.change_scene(page.game.scenes['GachaPlace'])
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # detect mouseclick
				pass

	def update(page):
		for _,obj in page.buttons.items():
			obj.state = 1 if obj.isHover(page.game.mousepos) else 0

	def draw(page):
		page.game.screen.blit(page.bg,(0,0))

		for _,group in sorted(page.groups.items()):
			for _,obj in group.items():
				obj.draw(page.game.screen)

class Image(pygame.sprite.Sprite):
	def __init__(self,image,topleft):
		super().__init__()
		self.sprite = image
		self.spriteButGray = None
		self.rect = self.sprite.get_rect(topleft=topleft)
		
		#self.get_grayscale()

	def get_grayscale(self):
		if self.spriteButGray is None:
			width,height = self.sprite.get_size()
			self.spriteButGray = pygame.Surface((width, height),flags=pygame.SRCALPHA)
			pixelBG = self.sprite.get_at((0,0))[:3]
			for x in range(width):
				for y in range(height):
					r,g,b,*_ = self.sprite.get_at((x,y))
					h,s,v = RGBtoHSV(r,g,b)
					r0,g0,b0 = HSVtoRGB(0,0,v)
					self.spriteButGray.set_at((x,y), (r0,g0,b0))
		return self.spriteButGray
	
	def draw(self, screen, grayscale=False):
		toblit = self.sprite if not grayscale else self.get_grayscale()
		screen.blit(toblit, self.rect)

class TextBox:
	def __init__(self, rect, bgcolor=(0,0,0,0), boardcolor=(0,0,0), boardsize=0, text='', textsize=24, textcolor=(0,0,0), aligncenter=False, antialias=True):
		self.rect = rect
		self.box = {'sprite':None,'bgColor':bgcolor,'boarderColor':boardcolor,'boarderSize':boardsize}
		self.text = {'sprite':None,'string':text,'textColor':textcolor,'textSize':textsize,'font':pygame.font.SysFont(None, textsize),'antialias':antialias}
		self.aligncenter = aligncenter

		self.renderBox()
		self.renderText()
		self.updateSprite()

	def renderBox(self,update=False):
		daBox = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
		bgColor = (list(self.box.get('bgColor'))+[255])[:4]
		bdColor = (list(self.box.get('boarderColor'))+[255])[:4]
		bdSize = self.box.get('boarderSize')
		if bdSize >= min(self.rect.size):
			daBox.fill(bdColor)
		else:
			daBox.fill(bgColor)
			if bdSize > 0:
				pygame.draw.rect(daBox,bdColor[:3],(0,0,self.rect.w,self.rect.h),bdSize)
		self.box['sprite'] = daBox
		if update:
			self.updateSprite()
	
	def renderText(self,update=False):
		textString = self.text.get('string')
		textColor = self.text.get('textColor')
		textSize = self.text.get('textSize')
		textFont = self.text.get('font')
		antiAlias = self.text.get('antialias')
		self.text['sprite'] = renderTextWithLines(textString,textColor,textSize,textFont,antiAlias)
		if update:
			self.updateSprite()
	
	def updateSprite(self):
		self.sprite = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
		sprBox = self.box.get('sprite')
		sprText = self.text.get('sprite')
		self.sprite.blit(sprBox,(0,0))
		if self.aligncenter:
			self.sprite.blit(sprText,(self.rect.w/2-sprText.get_width()/2,self.rect.h/2-sprText.get_height()/2))
		else:
			padding = 5
			self.sprite.blit(sprText,(padding,self.rect.h/2-sprText.get_height()/2))
	
	def resize_fit(self,padding=0):
		old_topleft = self.rect.topleft
		self.rect = self.text['sprite'].get_rect().inflate(padding*2,padding*2)
		self.rect.topleft = old_topleft
		self.aligncenter = True
		self.renderBox(update=True)
		return self

	def draw(self, screen):
		screen.blit(self.sprite, self.rect)

class Interactable:
	def __init__(self,xy,*states):
		"""---
		xy: (x,y)\n
		states: state0, state1, ...\n
		state: [pygame.Rect(0,0,width,height), imageSurface]
		"""
		self.x, self.y = xy
		self.state = 0
		self.states = []
		for state in states:
			daHitbox, daSprite = state
			self.states.append({'hitbox':daHitbox,'sprite':daSprite})

	def curState(self):
		return self.states[self.state]
	
	def isHover(self,mousepos):
		return self.curState()['hitbox'].move(self.x,self.y).collidepoint(mousepos)

	def draw(self,screen):
		screen.blit(self.curState().get('sprite').sprite, (self.x,self.y))

class SimpleButton(Interactable):
	def __init__(self,rect,*sprites):
		"""---
		rect: pygame.Rect(x,y,width,height)\n
		sprites: state0, state1, ...\n
		sprite: [imageSurface]
		"""
		super().__init__(rect.topleft,*[[pygame.Rect(0,0,rect.w,rect.h),*sprite] for sprite in sprites])

def renderTextWithLines(text,textColor=(0,0,0),size=24,font=pygame.font.SysFont(None, 24),anti_alias=True,horizontal_align='Middle'):
	thefont = pygame.font.SysFont(None, size)
	antialias = anti_alias
	if '\n' not in text:
		text_render = thefont.render(text,antialias,textColor)
		text_surface = text_render
	else:
		newlineOffY = size/8

		text_render = {(x:=thefont.render(minitext,antialias,textColor)):(x.get_width(),x.get_height()) for minitext in text.split('\n')}
		text_render_width = max([w for w,_ in text_render.values()])
		text_render_height = sum([h+newlineOffY for _,h in text_render.values()])-newlineOffY
		text_surface = pygame.Surface(pygame.Rect(0,0,text_render_width,text_render_height).size,flags=pygame.SRCALPHA)

		text_render_y = 0
		for minitext,(width,height) in text_render.items():
			match(horizontal_align.lower()):
				case 'middle':
					text_render_x = text_render_width/2-width/2
				case 'right':
					text_render_x = text_render_width-width
				case _:
					text_render_x = 0
			text_surface.blit(minitext, (text_render_x, text_render_y))
			text_render_y += height+newlineOffY
	
	return text_surface

def RGBtoHSV(r,g,b):
	r0,g0,b0 = r/255,g/255,b/255
	cMax = max(r0,g0,b0)
	cMin = min(r0,b0,g0)
	delta = cMax-cMin
	if delta==0:
		h = 0
	elif cMax==r0:
		h = 60*((g0-b0)/delta)%6
	elif cMax==g0:
		h = 60*((b0-r0)/delta+2)%6
	elif cMax==b0:
		h = 60*((r0-g0)/delta+4)%6
	
	s = 0 if cMax==0 else delta/cMax
	v = cMax
	return h,s,v

def HSVtoRGB(h,s,v):
	c = v*s
	x = c*(1-abs((h/60)%2-1))
	m = v-c
	if h<60:
		r0,g0,b0 = c,x,0
	elif h<120:
		r0,g0,b0 = x,c,0
	elif h<180:
		r0,g0,b0 = 0,c,x
	elif h<240:
		r0,g0,b0 = 0,x,c
	elif h<300:
		r0,g0,b0 = x,0,c
	else:
		r0,g0,b0 = c,0,x

	r,g,b = (r0+m)*255,(g0+m)*255,(b0+m)*255
	return r,g,b