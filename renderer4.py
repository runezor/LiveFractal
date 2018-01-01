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

def sortmap(data):
	return np.argsort(data)

def polymap(data,zoom):
	ret=np.zeros(np.append(data.shape,3))


	for x in range(0,data.shape[0]):
		for y in range(0,data.shape[1]):
			t=math.log(data[x][y]+1)
			ret[x][y][0]=1*(1-t)*t**3*(0.4**(1+zoom))+0
			ret[x][y][1]=1*(1-t)*t**3*(0.4**(2+zoom))
			ret[x][y][2]=1*(1-t)*t**3*(0.4**(3+zoom))
			

	return ret


def sub(data,incc=2,incr=4):
	h, w = data.shape
	nrows=int(h/incr)
	ncols=int(w/incc)
	return (data.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1,nrows,ncols))

def randC():
	exp=random.randint(0,5)
	ret=random.randint(0,1000)/(1000.0)*(10**exp)
	
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
		graph[x]+=1

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
		dif_list[i]=mask_fit(x,mask)
	
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
	subdata=sub(data)
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
	
def array_sort(a):

	shape=a.shape


	b=a.flatten()
	c=np.argsort(b)
	e=np.zeros(c.size)

	
	for index, i in enumerate(c):
		e[i]=index
	d=e.reshape(shape)

	return d

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
		w=1080
		h=2160


		dbx=str(a.x)
		dby=str(a.y)
		dbw=str(a.w)
		dbh=str(a.h)

		r=a.render(i*80,resx=w,resy=h,threadCount=i_threads)
		a=mask_zoom(a,i*80,r,resx=w,resy=h,pool=4)
		r=r.astype(float)

		"""Forhindrer log(0)"""
		shape=r.shape
		r=r.flatten()
		for index, u in enumerate(r):
			if u==0:
				r[index]=1
		r=r.reshape(shape)


		r=np.log(r)
		asort=array_sort(r)

		
		"""Fikser weird mønstre"""
		asort=asort.flatten()
		for index, u in enumerate(r.flatten()):
			if u==0:
				asort[index]=w*h

		asort=asort.reshape(r.shape)




		"""sn=sinemap(asort,randOFF(),randC()*0.999**i,randOFF(),randC()*0.999**i,randOFF(),randC()*0.999**i)"""
		"""sn=polymap(r,i)"""

		maps=["hot","seismic","Spectral","PuOr","flag","prism","gnuplot2","gnuplot","nipy_spectral","gist_ncar","cool","gist_heat","PiYG","PRGn","RdBu","coolwarm","RdYlGn","cool","plasma","inferno","magma"]

		"""Sin funktion"""

		"""plt.imsave("1.jpg",sn,cmap=plt.get_cmap(maps[random.randint(0,len(maps)-1)]))"""
		plt.imsave("1.jpg",asort,cmap=plt.get_cmap(maps[random.randint(0,len(maps)-1)]))


		if i%3==0:
			getcontext().prec+=2
			print("context: "+str(getcontext().prec))


		
		upload.upload(dbx,dby,dbw,dbh)
		print("i: "+str(i))
	
	

	
