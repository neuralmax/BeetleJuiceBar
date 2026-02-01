import sys,os
from os.path import join as opj
print(sys.executable)
import pygame as pg
from PIL import Image
from pygame.locals import RESIZABLE,VIDEORESIZE,HWSURFACE,DOUBLEBUF
from pygame import mixer
from random import randint
from time import sleep
from sceneXrayInit import xrayInit
from sceneXray import xray
from sceneXrayMsg import xrayMsg
from gizmo import pilImgToPgImg,pgImgToDisplayArr,sin,shimmerEffect

levels_black = 30     # shadows
levels_white = 220    # highlights
def levels(p):
	if p < levels_black:
		return 0
	if p > levels_white:
		return 255
	return int((p - levels_black) * 255 / (levels_white - levels_black))

#os.environ['SDL_VIDEO_CENTERED']='1'# You have to call this before pygame.init()
pg.init()
mixer.init()
info=pg.display.Info()#You have to call this before pygame.display.set_mode()
sizeFull=info.current_w,info.current_h
#size=(sizeFull[0],sizeFull[1]-30)
size=(1087,582)
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

#--=( load sprites )=--
spriteNames=os.listdir('sprites')
print(spriteNames)
sprites={sprite.split('.')[0]:Image.open(opj('sprites',sprite)) for sprite in spriteNames }
#--=( sounds )=--
mixer.music.load(opj('sounds','insame.mp3'))
mixer.music.set_volume(0.1)
mixer.music.play()
soundDot=pg.mixer.Sound(opj('sounds','dot.wav'))
soundDash=pg.mixer.Sound(opj('sounds','dash.wav'))

soundOpenbook=pg.mixer.Sound(opj('sounds','openbook.wav'))
soundBlender=pg.mixer.Sound(opj('sounds','blender.wav'))
soundDoor=pg.mixer.Sound(opj('sounds','door.wav'))
soundTasty=pg.mixer.Sound(opj('sounds','tasty.wav'))
soundJuck=pg.mixer.Sound(opj('sounds','juck.wav'))
soundTurnpage=pg.mixer.Sound(opj('sounds','turnpage.wav'))

#soundTap=pg.mixer.Sound(opj('sounds','double.wav'))
soundTap=pg.mixer.Sound(opj('sounds','single.wav'))
soundEmptybottle=pg.mixer.Sound(opj('sounds','emptybottle.wav'))

reqs=[['.','-'],['-','.','.','.'],['-','.','-','.']]
#bn      ['a','b','s','v','e']
coctails=[[0 , 1 , 1 , 1],
		  [1 , 1 , 1 , 0],
		  [1 , 0 , 0 , 1]]
reqsIdx=0
clientsPerDay=2
clientNr=0
clientIdx=-1
clientsSatisfied=0
clock=pg.time.Clock()
pg.display.set_caption('hw'+str(size))
fullScr=False
counter=0
counterMax=300
mainLoop=True
alpha=0.5
gamma=0.5
xplr=0
yplr=0
xtrg=0
ytrg=0
xrayLvlMaxDist=0
xrayLvlSize=20
scene='titleScreen'
#scene='xrayMsg'
#scene='score'
clientNr=0
clientDisplay='client'+str(clientNr)
closeMouthCounter=0
nextSoundCouner=0
morseOnScreen=[]
morseIdx=0
bookSection=0
bookPage=0
brewPage=0
brewStore=[1,1,1,1]
brewBlender=[0,0,0,0]
releasedKey=True
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
			elif event.key==pg.K_ESCAPE:
				mainLoop=False
			elif event.key==pg.K_BACKQUOTE:
				screeshotNames=os.listdir('screenshots')
				screeshotNrs=[int(n.split('.')[0].split('_')[1]) for n in screeshotNames]
				if len(screeshotNrs)>0:
					screeshotNr=max(screeshotNrs)+1
				else:
					screeshotNr=0
				pg.image.save(screen,opj('screenshots','screeshot_'+str(screeshotNr)+'.png'))
		elif event.type==pg.KEYUP:
			releasedKey=True
	mb1,mb2,mb3=pg.mouse.get_pressed()
	#pg.display.set_caption('hw'+str(size))
	keys=pg.key.get_pressed()
#--=( scene manager )==-
	if not pg.mixer.music.get_busy():
		mixer.music.play()
	if scene=='titleScreen':
		counter,imgEther=shimmerEffect(counter,counterMax,sprites['title'])
		testimg=pilImgToPgImg(pg,imgEther)
		skullarr=pgImgToDisplayArr(testimg)
		if keys[pg.K_k]:
			scene='xrayInit'
	elif scene=='xrayInit':
		xplr,yplr,xtrg,ytrg,skullarr,xrayLvlMaxDist,scene=xrayInit(pg,sprites,xrayLvlSize)
		clientNr+=1
		reqsIdx+=1
		clientIdx+=1
		brewStore=[1,1,1,1]
		brewBlender=[0,0,0,0]
		bookPage=0
		brewPage=0
		'''
		soundTasty=pg.mixer.Sound(opj('sounds','tasty.wav'))
		soundJuck=pg.mixer.Sound(opj('sounds','juck.wav'))
		'''
	elif scene=='xray':
		skullarr,xplr,yplr,xtrg,ytrg,counter,scene=xray(pg,sprites,keys,scene,xplr,yplr,xtrg,ytrg,counter,counterMax,xrayLvlSize,xrayLvlMaxDist,clientIdx)
	elif scene=='xrayMsg':
		closeMouthCounter,counter,morseOnScreen,morseIdx,skullarr,scene,nextSoundCouner=xrayMsg(pg,closeMouthCounter,clientNr,counter,counterMax,sprites,morseOnScreen,morseIdx,reqs,reqsIdx,soundDot,soundDash,scene,nextSoundCouner,keys,clientIdx,soundOpenbook,soundDoor)
	elif scene=='book':
		if keys[pg.K_a] and releasedKey:
			soundTurnpage.play()
			releasedKey=False
			bookPage-=1
			if bookPage<0:
				bookPage=0
		if keys[pg.K_d] and releasedKey:
			soundTurnpage.play()
			releasedKey=False
			bookPage+=1
			if bookPage>2:
				bookPage=2
		if keys[pg.K_w] and releasedKey:
			soundTurnpage.play()
			releasedKey=False
			bookSection=1
			bookPage=0
		if keys[pg.K_s] and releasedKey:
			soundTurnpage.play()
			releasedKey=False
			bookSection=0
			bookPage=0
		if keys[pg.K_i]:
			scene='xrayMsg'
		if keys[pg.K_l]:
			scene='brew'
			soundDoor.play()
		bv=['m','r']
		bh=['a','b','c']
		bookname='book'+bv[bookSection]+bh[bookPage]
		counter,imgEther=shimmerEffect(counter,counterMax,sprites[bookname])
		testimg=pilImgToPgImg(pg,imgEther)
		skullarr=pgImgToDisplayArr(testimg)
	elif scene=='brew':
		'''
		soundEmptybottle
		'''
		if keys[pg.K_a] and releasedKey:
			releasedKey=False
			soundTap.play()
			brewPage-=1
			if brewPage<0:
				brewPage=0
		if keys[pg.K_d] and releasedKey:
			releasedKey=False
			soundTap.play()
			brewPage+=1
			if brewPage>4:
				brewPage=4
		if keys[pg.K_i] and releasedKey:
			scene='xrayMsg'
		if keys[pg.K_j] and releasedKey:
			scene='book'
			soundOpenbook.play()
		if keys[pg.K_k] and releasedKey:
			releasedKey=False
			if brewPage<4:
				if brewStore[brewPage]==1:
					soundBlender.play()
					brewStore[brewPage]=0
					brewBlender[brewPage]=1
				else:
					soundEmptybottle.play()
			else:
				if brewBlender==coctails[reqsIdx]:
					scene='success'
					clientsSatisfied+=1
					soundTasty.play()
				else:
					scene='fail'
					soundJuck.play()
		bn=      ['a','b','s','v','e']
		if brewPage==4 or brewStore[brewPage]==1:
			brewname='brew'+bn[brewPage]
		else:
			brewname='brew'
		counter,imgEther=shimmerEffect(counter,counterMax,sprites[brewname])
		testimg=pilImgToPgImg(pg,imgEther)
		skullarr=pgImgToDisplayArr(testimg)
	elif scene=='success':
		if keys[pg.K_k] and releasedKey:
			if clientNr<clientsPerDay:
				scene='xrayInit'
			else:
				scene='score'
		counter,imgEther=shimmerEffect(counter,counterMax,sprites['client'+str(clientIdx)+'happy'])
		testimg=pilImgToPgImg(pg,imgEther)
		skullarr=pgImgToDisplayArr(testimg)
	elif scene=='fail':
		if keys[pg.K_k] and releasedKey:
			if clientNr<clientsPerDay:
				scene='xrayInit'
			else:
				scene='score'
		counter,imgEther=shimmerEffect(counter,counterMax,sprites['client'+str(clientIdx)+'sad'])
		testimg=pilImgToPgImg(pg,imgEther)
		skullarr=pgImgToDisplayArr(testimg)
	elif scene=='score':
		counter,imgEther=shimmerEffect(counter,counterMax,sprites['background'])
		testimg=pilImgToPgImg(pg,imgEther)
		basicFont = pg.font.SysFont(None, 40)
		text = basicFont.render(str(clientsSatisfied)+' / '+str(clientsPerDay), True, WHITE)
		textRect = text.get_rect()
		textRect.centerx = testimg.get_rect().centerx
		textRect.centery = testimg.get_rect().centery
		#pg.draw.rect(testimg, RED, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40),1)
		testimg.blit(text, textRect)
		skullarr=pgImgToDisplayArr(testimg)

		#xrayLvlMaxDist
#--=( display )=--
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
	pg.display.set_caption('hw'+str(size)+' gamma:'+str(gamma)+' scene:'+scene+' alpha:'+str(alpha)+' xplr:'+str(xplr)+' yplr:'+str(yplr)+' xtrg:'+str(xtrg)+' ytrg:'+str(ytrg)+''.join(morseOnScreen))

	#pg.image.save(screen,'frame'+str(counter)+'.png')
pg.quit()
