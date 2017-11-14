import matplotlib.pyplot as plt
import fractal3
import numpy as np
import math
import operator
from decimal import *
from random import randint

def sinemap(data,l):
	siner=lambda t: np.sin(t/math.pi*1/l)+1
	data=np.array([siner(x) for x in data])

def sub(data,inc=4):
	h, w = data.shape
	nrows=int(h/inc)
	ncols=int(w/inc)
	return (data.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1,nrows,ncols))


def mask_hill(resx,resy,maxiter):
	return np.fromfunction(lambda x, y: 1.2/(3*((x/resx)*2-1)**2+3*((y/resy)*2-1)**2+1), (resx, resy), dtype=int)
	

def diff(data,maxiter):
	"""Awards equal distribution of iterations"""
	graph=np.zeros(maxiter)

	data_size=len(data.flat)

	returning=data_size

	for x in data.flat:
		graph[x]+=1

	for x in graph:
		returning-=abs(data_size/maxiter-x)

	return returning	

def mask_fit(array,mask):
	quad=0
	a_f=array.flat;
	m_f=mask.flat;

	for i, a in enumerate(a_f):
		quad+=(a-m_f[i])**2
	return quad

def mask_zoom(fractal,maxiter,pool=3,subs=4.0,resx=256,resy=256):
	data=fractal.render(maxiter,resx=resx,resy=resy)
	subdata=sub(data,inc=subs)
	dif_list=np.empty(int(subs)**2,dtype=object)
	
	mask=mask_hill(int(resx/subs),int(resy/subs),maxiter)
	for i, x in enumerate(subdata):
		dif_list[i]=mask_fit(x,mask)
	
	print(dif_list)

	"""Gives index table"""
	k=sorted(range(len(dif_list)),key=lambda x: dif_list[x])
	val=k[len(k)-1-randint(0,pool-1)]
	print(str(k) + " chose val: "+str(val))

	value=dif_list[val]

	"""Finds x and y"""
	x=(val)%subs
	y=(val-x)/subs

	fractal_rec=fractal3.mandelbrot()
	fractal_rec.x=fractal.x+Decimal((-3.0+2.0*x)/8.0) * fractal.w
	fractal_rec.y=fractal.y+Decimal((-3.0+2.0*y)/8.0) * fractal.h
	fractal_rec.w=fractal.w/Decimal(subs)
	fractal_rec.h=fractal.h/Decimal(subs)

	return fractal_rec

def smart_zoom(fractal,maxiter,pool=3,resx=256,resy=256):
	data=fractal.render(maxiter,resx=resx,resy=resy)
	subdata=sub(data)
	dif_list=np.empty(16,dtype=object)
	for i, x in enumerate(subdata):
		dif_list[i]=diff(x,maxiter)

	print(dif_list)

	"""Gives index table"""
	k=sorted(range(len(dif_list)),key=lambda x: dif_list[x])
	val=k[len(k)-1-randint(0,pool-1)]
	print(str(k) + " chose val: "+str(val))

	"""val, value=max(enumerate(dif_list), key=operator.itemgetter(1))	"""

	value=dif_list[val]	
	
	"""x=, y=0..3"""
	x=(val)%4
	y=(val-x)/4

	print("Interesting x: "+str(x))
	print("Interesting y: "+str(y))
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
	
