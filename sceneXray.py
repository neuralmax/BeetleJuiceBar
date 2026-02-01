from PIL import Image
from gizmo import pilImgToPgImg,pgImgToDisplayArr,sin,shimmerEffect
def xray(pg,sprites,keys,scene,xplr,yplr,xtrg,ytrg,counter,counterMax,xrayLvlSize,xrayLvlMaxDist,clientIdx):
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	#--=( control )==--

	if keys[pg.K_w]:
		yplr-=1
		if yplr<0:
			yplr=0
	elif keys[pg.K_s]:
		yplr+=1
		if yplr>xrayLvlSize:
			yplr=xrayLvlSize

	elif keys[pg.K_a]:
		xplr-=1
		if xplr<0:
			xplr=0
	elif keys[pg.K_d]:
		xplr+=1
		if xplr>xrayLvlSize:
			xplr=xrayLvlSize
	xrayLvlCurDist=abs(xtrg-xplr)+abs(ytrg-yplr)

	#--=( special effects )==-

	#gamma = 0.8  # <1 brightens mids, >1 darkens mids

	if xrayLvlCurDist>xrayLvlMaxDist:
		xrayLvlCurDist=xrayLvlMaxDist
	alpha=xrayLvlCurDist/xrayLvlMaxDist
	imgor=Image.blend(sprites['client'+str(clientIdx)],sprites['client'+str(clientIdx)+'mask'], alpha)

	counter,imgEther=shimmerEffect(counter,counterMax,imgor)
	#imgEther=imgEther.point(levels)
	#--=( hud )=--
	testimg=pilImgToPgImg(pg,imgEther)

	pg.draw.circle(testimg, BLACK, (xplr/xrayLvlSize*64,yplr/xrayLvlSize*64),3,0)
	pg.draw.circle(testimg, WHITE, (xplr/xrayLvlSize*64,yplr/xrayLvlSize*64),2,1)
	yl=64-alpha*64
	pg.draw.line(testimg, WHITE,(122,yl),(127,yl),1)
	pg.draw.line(testimg, WHITE,(124,yl+3),(127,yl),1)
	pg.draw.line(testimg, WHITE,(124,yl-3),(127,yl),1)

	skullarr=pgImgToDisplayArr(testimg)
	if xrayLvlCurDist<=2:
		scene='xrayMsg'
		counter=0
	return skullarr,xplr,yplr,xtrg,ytrg,counter,scene
