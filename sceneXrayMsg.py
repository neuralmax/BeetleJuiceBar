from gizmo import pilImgToPgImg,pgImgToDisplayArr,sin,shimmerEffect
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
def xrayMsg(pg,closeMouthCounter,clientNr,counter,counterMax,sprites,morseOnScreen,morseIdx,reqs,reqsIdx,soundDot,soundDash,scene,nextSoundCouner,keys,clientIdx,soundOpenbook,soundDoor):
	if keys[pg.K_j]:
		scene='book'
		soundOpenbook.play()
	if keys[pg.K_l]:
		scene='brew'
		soundDoor.play()

	if closeMouthCounter>0:
		closeMouthCounter-=1
		clientDisplay='client'+str(clientIdx)+'open'
	else:
		clientDisplay='client'+str(clientIdx)

	counter,imgEther=shimmerEffect(counter,counterMax,sprites[clientDisplay])
	testimg=pilImgToPgImg(pg,imgEther)
	morseSize=0
	if len(morseOnScreen)>1:
		for c in morseOnScreen:
			if c=='.':
				morseSize+=10
			elif c=='-':
				morseSize+=15
	curMorseOffset=0
	for i,c in enumerate(morseOnScreen):
		if c=='.':
			pg.draw.circle(testimg,BLACK,(128//2-morseSize//2+curMorseOffset,61),2,0)
			pg.draw.circle(testimg,WHITE,(128//2-morseSize//2+curMorseOffset,61),1,0)
			curMorseOffset+=10
		elif c=='-':
			pg.draw.line(testimg,BLACK,(128//2-3-morseSize//2+curMorseOffset,60),(128//2+8-morseSize//2+curMorseOffset,60),4)
			pg.draw.line(testimg,WHITE,(128//2-2-morseSize//2+curMorseOffset,60),(128//2+7-morseSize//2+curMorseOffset,60),2)
			curMorseOffset+=15
	skullarr=pgImgToDisplayArr(testimg)
	#darsh =0.5s, dot=0.15s
	if counter==1:
		#reset sequence
		nextSoundCouner=1
		morseOnScreen=[]
		morseIdx=0
	if counter==nextSoundCouner and morseIdx<len(reqs[reqsIdx]):
		if reqs[reqsIdx][morseIdx]=='.':
			soundDot.play()
			nextSoundCouner+=10
			closeMouthCounter=5
			morseOnScreen.append('.')
		elif reqs[reqsIdx][morseIdx]=='-':
			soundDash.play()
			nextSoundCouner+=20
			closeMouthCounter=15
			morseOnScreen.append('-')
		morseIdx+=1
	return closeMouthCounter,counter,morseOnScreen,morseIdx,skullarr,scene,nextSoundCouner
