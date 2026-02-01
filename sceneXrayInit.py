from random import randint
from gizmo import pilImgToPgImg,pgImgToDisplayArr,sin
def xrayInit(pg,sprites,xrayLvlSize):
	lvl=randint(0,3)
	# 0 1
	# 2 3

	sa=[         0,xrayLvlSize-xrayLvlSize//3]
	sb=[xrayLvlSize//3,xrayLvlSize           ]
	if lvl==0:
		xplr=randint(sa[0],sb[0])
		yplr=randint(sa[0],sb[0])
		xtrg=randint(sa[1],sb[1])
		ytrg=randint(sa[1],sb[1])
	if lvl==1:
		xplr=randint(sa[1],sb[1])
		yplr=randint(sa[0],sb[0])
		xtrg=randint(sa[0],sb[0])
		ytrg=randint(sa[1],sb[1])
	if lvl==2:
		xplr=randint(sa[0],sb[0])
		yplr=randint(sa[1],sb[1])
		xtrg=randint(sa[1],sb[1])
		ytrg=randint(sa[0],sb[0])
	if lvl==3:
		xplr=randint(sa[1],sb[1])
		yplr=randint(sa[1],sb[1])
		xtrg=randint(sa[0],sb[0])
		ytrg=randint(sa[0],sb[0])
	xrayLvlMaxDist=abs(xtrg-xplr)+abs(ytrg-yplr)
	scene='xray'
	testimg=pilImgToPgImg(pg,sprites['title'])
	skullarr=pgImgToDisplayArr(testimg)
	return xplr,yplr,xtrg,ytrg,skullarr,xrayLvlMaxDist,scene
