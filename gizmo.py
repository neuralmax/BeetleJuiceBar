from math import sin as sinr
from math import radians

def pilImgToPgImg(pg,imgEther):
	imgdith=imgEther.convert("1")  # Floyd–Steinberg dithering
	imgrgb = imgdith.convert("RGB")
	data = imgrgb.tobytes()
	testimg=pg.image.fromstring(data,imgrgb.size,imgrgb.mode)
	return testimg

def pgImgToDisplayArr(testimg):
	skullarr=[[0 if testimg.get_at((x,y))[0]==0 else 1 for y in range(64)] for x in range(128)]
	return skullarr

def sin(a):return sinr(radians(a))


def shimmerEffect(counter,counterMax,imgor):
	counter+=1
	if counter>300:
		counter=0
	gamma=0.75+0.1*sin(counter/300*360)
	imgEther=imgor.point(lambda p: int(255 * ((p / 255) ** gamma)))
	return counter,imgEther
