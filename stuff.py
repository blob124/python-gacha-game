import pygame

pygame.init()

EXITTXT = pygame.font.SysFont(None, 24).render('Press Esc, it stands for Escape!', True, (255, 255, 255))

class Image(pygame.sprite.Sprite):
	def __init__(self,image,x,y):
		super().__init__()
		self.image = image
		self.imagegray = None
		self.rect = self.image.get_rect(topleft=(x, y))
		
		#self.get_grayscale()

	def get_grayscale(self):
		if self.imagegray is None:
			width,height = self.image.get_size()
			self.imagegray = pygame.Surface((width, height))
			pixelBG = self.image.get_at((0,0))[:3]
			for x in range(width):
				for y in range(height):
					r,g,b,*_ = self.image.get_at((x,y))
					h,s,v = RGBtoHSV(r,g,b)
					r0,g0,b0 = HSVtoRGB(0,0,v)
					self.imagegray.set_at((x,y), (r0,g0,b0))
		return self.imagegray
	
	def draw(self, screen, grayscale=False):
		toblit = self.image if not grayscale else self.get_grayscale()
		screen.blit(toblit, self.rect)
	
class Button:
	def __init__(self,sprite,rect,*states):
		self.rect = rect
		self.state = 0
		self.state_list = []
		if sprite is not None:
			self.state_list.append(sprite)
			dark_overlay = pygame.Surface(self.sprite.get_size(), flags=pygame.SRCALPHA)
			dark_overlay.fill((0,0,0,100))
			hsprite = sprite
			hsprite.blit(dark_overlay(0,0))
			self.state_list.append(hsprite)
		else:
			df_bgColor = states[0][0]
			df_text = states[0][1]
			df_textColor = states[0][2]
			df_textSize = states[0][3]

			for state in states:
				bgColor, text, textColor, textSize = state
				if bgColor is None:
					bgColor = df_bgColor
				if text is None:
					text = df_text
				if textColor is None:
					textColor = df_textColor
				if textSize is None:
					textSize = df_textSize
				
				sf = pygame.Surface(self.rect.size)
				sf.fill(bgColor)
				if text != '':
					text_render = renderText(text,textColor,textSize)
					sf.blit(text_render, (sf.get_width()/2-text_render.get_width()/2, sf.get_height()/2-text_render.get_height()/2))
		
				self.state_list.append(sf)
	
	def checkHover(self,mousepos):
		if self.rect.collidepoint(mousepos):
			self.state = 1
		else:
			self.state = 0
	
	def draw(self,screen):
		if self.state>len(self.state_list)-1:
			self.state = 0
		toblit = self.state_list[self.state]
		screen.blit(toblit, self.rect)

class TextBox:
	def __init__(self, rect, bgcolor=(255,255,255), text='', textcolor=(0,0,0), textsize=24):
		self.rect = rect
		self.bgColor = bgcolor
		self.text = None
		self.textColor = textcolor
		self.font = pygame.font.SysFont(None, textsize)

		self.haveBoarder = False
		self.boarder_size = 3
		self.boarder_color = self.textColor

		self.setText(text)

	def setText(self, newtext):
		if self.text != newtext:
			self.text = newtext
			self.text_render = self.font.render(self.text,True,self.textColor)
			self.update()
	
	def update(self):
		self.sprite = pygame.Surface(self.rect.size)
		if not self.haveBoarder:
			self.sprite.fill(self.bgColor)
		else:
			self.sprite.fill(self.boarder_color)
			idkwhattocall = pygame.Surface((self.rect.width-self.boarder_size*2, self.rect.height-self.boarder_size*2))
			idkwhattocall.fill(self.bgColor)
			self.sprite.blit(idkwhattocall, (self.boarder_size, self.boarder_size))
		self.sprite.blit(self.text_render, (5,self.sprite.get_height()/2-self.text_render.get_height()/2))
		
		
	def draw(self, screen):
		screen.blit(self.sprite, self.rect)

def renderText(text,textColor=(0,0,0),size=24,horizontal_align='Middle'):
	thefont = pygame.font.SysFont(None, size)
	if '\n' not in text:
		text_render = thefont.render(text,True,textColor)
		text_surface = text_render
	else:
		newlineOffY = size/8

		text_render = {(x:=thefont.render(minitext,True,textColor)):(x.get_width(),x.get_height()) for minitext in text.split('\n')}
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