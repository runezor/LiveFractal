import matplotlib.pyplot as plt
import fractal5
import numpy as np
import math
import operator
import upload
from decimal import *
import random


def sinemap(data,rOFF=2.1,rC=1./1000,gOFF=-3.5,gC=1./500,bOFF=5.,bC=1./3500):
	ret=np.zeros(np.append(data.shape,3))


	for x in range(0,data.shape[0]):
		for y in range(0,data.shape[1]):
			t=math.log(data[x][y]+1)
			ret[x][y][0]=np.sin(t*rC+rOFF)*0.5+0.5
			ret[x][y][1]=np.sin(t*gC+gOFF)*0.5+0.5
			ret[x][y][2]=np.sin(t*bC+bOFF)*0.5+0.5
			

	return ret


def sub(data,incc=2,incr=4):
	h, w = data.shape
	nrows=int(h/incr)
	ncols=int(w/incc)
	return (data.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1,nrows,ncols))

def randC():
	exp=random.randint(1,2)
	print(exp)
	ret=1./random.randint(10**exp,10**(exp+1))
	
	return ret


def randOFF():
	return random.randint(0,10000)/500.-1

def mask_hill(resx,resy,maxiter):
	return np.fromfunction(lambda x, y: 1.2/(3*((x/resx)*2-1)**2+3*((y/resy)*2-1)**2+1), (resx, resy), dtype=int)
	

def diff(data,maxiter):
	"""Awards equal distribution of iterations"""
	graph=np.zeros(maxiter)

	data_size=len(data.flat)

	returning=data_size

	for x in data.flat:
		graph[int(x)]+=1

	for x in graph:
		returning-=abs(data_size/maxiter-x)

	return returning	

def mask_fit(array,mask):
	quad=0
	a_f=array.flat;
	m_f=mask.flat;

	for i, m in enumerate(m_f):
		quad+=(a_f[i]-m)**2
	return quad

def mask_zoom(fractal,maxiter,data,pool=3,subx=8.0,suby=16.0,resx=256,resy=256):
	
	subdata=sub(data,incc=subx,incr=suby)
	dif_list=np.empty(int(subx*suby),dtype=object)


	mask=mask_hill(int(resx/subx),int(resy/suby),maxiter)

	"""print(subdata[0].shape);	
	print(mask.shape);"""

	for i, x in enumerate(subdata):
		dif_list[i]=mask_fit(int(x),mask)
	
	"""print(dif_list)"""

	"""Gives index table"""
	k=sorted(range(len(dif_list)),key=lambda x: dif_list[x])
	val=k[len(k)-1-random.randint(0,pool-1)]
	"""print(str(k) + " chose val: "+str(val))"""

	value=dif_list[val]

	"""Finds x and y"""
	x=(val)%subx
	y=(val-x)/subx

	"""print("x: "+str(x)+"; y: "+str(y))"""

	fractal_rec=fractal5.mandelbrot()
	fractal_rec.x=fractal.x+Decimal((-(subx-1)+2.0*x)/(subx*2)) * fractal.w
	fractal_rec.y=fractal.y+Decimal((-(suby-1)+2.0*y)/(suby*2)) * fractal.h
	fractal_rec.w=fractal.w/Decimal(4)
	fractal_rec.h=fractal.h/Decimal(4)

	return fractal_rec

def smart_zoom(fractal,maxiter,data,pool=3,resx=256,resy=256):
	subdata=sub(data,incr=4,incc=4)
	dif_list=np.empty(16,dtype=object)
	for i, x in enumerate(subdata):
		dif_list[i]=diff(x,maxiter)

	print(dif_list)

	"""Gives index table"""
	k=sorted(range(len(dif_list)),key=lambda x: dif_list[x])
	val=k[len(k)-1-random.randint(0,pool-1)]
	print(str(k) + " chose val: "+str(val))

	"""val, value=max(enumerate(dif_list), key=operator.itemgetter(1))	"""

	value=dif_list[val]	
	
	"""x=, y=0..3"""
	x=(val)%4
	y=(val-x)/4

	print("Interesting x: "+str(x))
	print("Interesting y: "+str(y))
	print(fractal.w)

	fractal_rec=fractal5.mandelbrot()

	fractal_rec.x=fractal.x+Decimal((-3.0+2.0*x)/8.0) * fractal.w
	fractal_rec.y=fractal.y+Decimal((-3.0+2.0*y)/8.0) * fractal.h
	fractal_rec.w=fractal.w/Decimal(4.0)
	fractal_rec.h=fractal.h/Decimal(4.0)
	
	print("x: "+str(fractal_rec.x))
	print("y: "+str(fractal_rec.y))
	print("w: "+str(fractal_rec.w))

	return fractal_rec
	
if __name__=="__main__":

	print("How many threads to use?")
	i_threads=int(input())	

	a=fractal5.mandelbrot()
	a.x=a.x
	a.y=a.y
	a.w=Decimal(8.0)
	a.h=Decimal(16.0)
	getcontext().prec=6
	for i in range(1,2048):
		dbx=str(a.x)
		dby=str(a.y)
		dbw=str(a.w)
		dbh=str(a.h)

		r=a.render(i*80,resx=108*2,resy=216*2,threadCount=i_threads)
		a=smart_zoom(a,i*80*1000,(r*10000).astype(int),resx=108*2,resy=216*2)

		sn=sinemap(r,randOFF(),2,randOFF(),3,randOFF(),4)
		

		plt.imsave("1.jpg",sn)
		if i%3==0:
			getcontext().prec+=2
		upload.upload(dbx,dby,dbw,dbh)
	
	
