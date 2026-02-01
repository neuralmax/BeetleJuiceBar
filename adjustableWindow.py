import sys,os
print(sys.executable)
import pygame as pg
from PIL import Image
from pygame.locals import RESIZABLE,VIDEORESIZE,HWSURFACE,DOUBLEBUF
from random import randint
from time import sleep
from math import sin as sinr
from math import radians
def sin(a):return sinr(radians(a))
#os.environ['SDL_VIDEO_CENTERED']='1'# You have to call this before pygame.init()
pg.init()
info=pg.display.Info()#You have to call this before pygame.display.set_mode()
sizeFull=info.current_w,info.current_h
#size=(sizeFull[0],sizeFull[1]-30)





size=(800,600)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
screen=pg.display.set_mode(size, RESIZABLE)
pixel=pg.image.load('pixel2.png').convert_alpha()
pixelgl=pg.image.load('pixel2glow.png').convert_alpha()
sz=size[0]//170
szs=9
pixelsm=pg.transform.smoothscale(pixel,(sz*szs,sz*szs))
pixelsmgl=pg.transform.smoothscale(pixelgl,(sz*szs,sz*szs))


imgor = Image.open("title.png")



clock=pg.time.Clock()
pg.display.set_caption('hw'+str(size))
fullScr=False
counter=0
mainLoop=True
while mainLoop:
	for event in pg.event.get():
		if event.type==pg.QUIT:
			mainLoop=False
		elif event.type==VIDEORESIZE:
			size=event.dict['size']
			screen=pg.display.set_mode(size,HWSURFACE|DOUBLEBUF|RESIZABLE)
			sz=size[0]//170
			pixelsm=pg.transform.smoothscale(pixel,(sz*szs,sz*szs))
			pixelsmgl=pg.transform.smoothscale(pixelgl,(sz*szs,sz*szs))
		elif event.type == pg.KEYDOWN:
			if event.key == pg.K_RETURN and pg.key.get_mods() & pg.KMOD_SHIFT:
				pg.display.set_caption('pressed: SHIFT + A ')
				print("pressed: SHIFT + K_RETURN")
				if fullScr:
					screen=pg.display.set_mode(size, RESIZABLE)
					fullScr=False
				else:
					pg.display.set_mode(sizeFull,pg.FULLSCREEN)
					fullScr=True
				sleep(1)
	mb1,mb2,mb3=pg.mouse.get_pressed()
	#pg.display.set_caption('hw'+str(size))
	counter+=1
	if counter>300:
		counter=0
	gamma=0.75+0.1*sin(counter/300*360)
	#gamma = 0.8  # <1 brightens mids, >1 darkens mids
	imgEther=imgor.point(lambda p: int(255 * ((p / 255) ** gamma)))
	imgdith=imgEther.convert("1")  # Floyd–Steinberg dithering
	imgrgb = imgdith.convert("RGB")
	data = imgrgb.tobytes()
	testimg=pg.image.fromstring(data,imgrgb.size,imgrgb.mode)
	skullarr=[[0 if testimg.get_at((x,y))[0]==0 else 1 for y in range(64)] for x in range(128)]


	screen.fill(BLACK)
	for y in range(64):
		for x in range(128):
			if skullarr[x][y]==1:
				screen.blit(pixelsmgl,(10+x*(sz+2),10+y*(sz+2)))
	for y in range(64):
		for x in range(128):
			if skullarr[x][y]==1:
				screen.blit(pixelsm,(10+x*(sz+2),10+y*(sz+2)))
			#elif randint(1,10)==1:
			#	screen.blit(pixelsm,(10+x*(sz+2),10+y*(sz+2)))
			#pg.draw.rect(screen, (50,50,200), (10+x*(sz+2),10+y*(sz+2),sz,sz))
	pg.display.update()
	clock.tick(30)
	pg.display.set_caption('hw'+str(size)+' gamma:'+str(gamma))

pg.quit()
