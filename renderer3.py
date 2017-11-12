import matplotlib.pyplot as plt
import fractal3
import numpy as np
import math
import operator
import upload
import random
from decimal import *

def sinemap(data,rOFF=2.1,rC=1./1000,gOFF=-3.5,gC=1./500,bOFF=5.,bC=1./3500):
	ret=np.ones(np.append(data.shape,3))

	for x in range(0,data.shape[0]):
		for y in range(0,data.shape[1]):
			t=data[x][y]

			ret[x][y][0]=np.sin(t*rC+rOFF)*128+128
			ret[x][y][1]=np.sin(t*gC+gOFF)*128+128
			ret[x][y][2]=np.sin(t*bC+bOFF)*128+128


	return ret

def randC():
	ret=1./random.randint(8000,20000)
	print(ret)
	return ret


def randOFF():
	return random.randint(0,1000)/500.-1


def sub(data,inc=4):
	h, w = data.shape
	nrows=int(h/inc)
	ncols=int(w/inc)
	return (data.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1,nrows,ncols))


def diff(data):
	"""+- algorithm med log"""
	timer=1
	returning=0
	for x in data.flat:
		returning=returning+x*timer
		timer=timer*(-1)

	return returning	

def smart_zoom(fractal,maxiter,render=0,pre=False):
	if pre==False:
		data=fractal.render(maxiter,resx=128,resy=128)
	else:
		data=render
	subdata=sub(data)
	dif_list=np.empty(16,dtype=object)
	for i, x in enumerate(subdata):
		dif_list[i]=diff(x)
	
	val, value=max(enumerate(dif_list), key=operator.itemgetter(1))	

	
	
	"""x=, y=0..3"""
	x=(val)%4
	y=(val-x)/4

	print(x)
	print(y)
	print(fractal.w)

	fractal_rec=fractal3.mandelbrot()

	fractal_rec.x=fractal.x+Decimal((-3.0+2.0*x)/8.0) * fractal.w
	fractal_rec.y=fractal.y+Decimal((-3.0+2.0*y)/8.0) * fractal.h
	fractal_rec.w=fractal.w/Decimal(4.0)
	fractal_rec.h=fractal.h/Decimal(4.0)
	
	print("x: "+str(fractal_rec.x))
	print("y: "+str(fractal_rec.y))
	print("w: "+str(fractal_rec.w))

	return fractal_rec
	

if __name__=="__main__":
	a=fractal3.mandelbrot()
	a.x=a.x+Decimal(0.05)
	getcontext().prec=6
	for i in range(1,100):
		r=a.render(i*100,resx=640,resy=640)
		a=smart_zoom(a,i*100,render=r,pre=True)

		sn=sinemap(r,randOFF(),randC(),randOFF(),randC(),randOFF(),randC())
		plt.imsave("1.jpg",sn)
		if i%3==0:
			getcontext().prec+=2
		upload.upload(1)

