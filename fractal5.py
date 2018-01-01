import numpy as np
import math
from decimal import *
import matplotlib.pyplot as plt
import threading
from multiprocessing import Process, Queue

def mandelbrot_point(creal,cimag,maxiter, smooth=True, bailout=4.0):
	real=creal
	imag=cimag

	bailout**=2
	
	for n in range(maxiter):
		real2=real*real		
		imag2=imag*imag
	
		magnitude=real2+imag2
	
		if magnitude>bailout:
			if smooth:
				"""Smooth coloring algorithm"""
				nsmooth=n+1-math.log(math.log(math.sqrt(magnitude)))/math.log(2)
								
			return nsmooth
		imag=2*real*imag+cimag
		real=real2-imag2+creal		
	return 0

def mandelbrot_trig_point(creal,cimag,maxiter, bailout=4.0):
	sum=0
	sum2=0
	
	ac=0
	il=0
	lp=0

	real=creal
	imag=cimag

	bailout**=2
	
	"""Triangle inequality average coloring"""
	sum=0
	sum2=0
	ac=math.sqrt(real**2+imag**2)
	il=1.0/math.log(2.0)
	lp=math.log(math.log(bailout)/2.0)
	az2=0.0
	lowbound=0
	f=0
	index=0

	for n in range(maxiter):
		"""Standard formular"""		
		real2=real*real		
		imag2=imag*imag
		
		imag=2*real*imag+cimag
		real=real2-imag2+creal	
		"""Standard formular slut"""

		"""TIA"""
		sum2=sum
		if ((n!=0) and (n!=maxiter-1)):
			tr=real-creal
			ti=imag-cimag
			az2=math.sqrt(tr*tr+ti*ti)
			lowbound=abs(az2-ac)

			"""print("az2: "+str(az2)+"; ac: "+str(ac)+"; lowbound: "+str(lowbound));"""

			"""FIKS"""
			if (az2+ac-lowbound!=0):
				sum+=((math.sqrt(real*real+imag*imag)-lowbound)/(az2+ac-lowbound))


		if real2+imag2>bailout:
			"""TIA OBS n+2 skal være n og n+1 være n-1"""
			sum=sum/(n+1)
			sum2=sum2/(n+1)
			f=il*lp-il*math.log(math.log(math.sqrt(real*real+imag*imag)))
			index=sum2+(sum-sum2)*(f+1.0)
			realiters=255*index
			"""OBS"""
			colval1=int(realiters+255)%255
			colval2=int(realiters+255)%255
			
			tweenval=realiters-int(realiters)

			ntrig=colval1+((colval2-colval1)*tweenval)+0.01;
					
			print(ntrig/255.0)			
			return ntrig/255.0
	return 0



def linespace(x1,x2,width):
	unit=(x2-x1)/width
	return([x1+unit*i for i in range(width)])

class mandelbrot:
	x=Decimal(0)
	y=Decimal(0)
	w=Decimal(2)
	h=Decimal(2)
	
	real=np.empty((512,512),dtype=object)
	imag=np.empty((512,512),dtype=object)
	space=np.empty((512,512),dtype=object)

	def render(self,maxiter,resx=512,resy=512,threadCount=4,smooth=True):
		self.mandelbrot_space_init(resx,resy)

		threads={}
		queues={}

		for i in range(threadCount):
			queues[i]=Queue()
			threads[i]=Process(target=self.mandelbrot_space,args=[self.space,self.real,self.imag,resx,resy,maxiter,threadCount,i,smooth,queues[i]])
	

		for i in range(threadCount):
			threads[i].start()
		



		for i in range(threadCount):
			self.space=np.add(self.space,queues[i].get())
			print("Adding que: " + str(i+1));


		for i in range(threadCount):
			threads[i].join()

		for i in range(threadCount):
			threads[i].terminate()
		
		"""self.mandelbrot_space(resx,resy,maxiter,1,0)"""

		print("Render succesful")
		return (self.space)

	def mandelbrot_space_init(self,width,height):
		r1=linespace(self.x-self.w/2, self.x+self.w/2, width)
		r2=linespace(self.y-self.h/2, self.y+self.h/2, height)

		self.real=np.empty((width,height),dtype=object)
		self.imag=np.empty((width,height),dtype=object)

		self.space=np.zeros((height,width),dtype=object)

		for i in range(width):
			for j in range(height):
				self.real[i,j]=r1[i]
				self.imag[i,j]=r2[j]

		print("arrayspace initialised!")
		
	
	def mandelbrot_space(self,space_size,reals,imags,width,height,maxiter,threadCount,id,smooth,queue_id):
		returning=space_size

		for i in range(id, width, threadCount):
			for j in range(height):
				returning[j,i]=mandelbrot_point(reals[i,j],imags[i,j],maxiter)
			if math.floor((i/width)*10) != math.floor(((i-1)/width)*10):
				print(str(id+1)+": "+str(math.floor((i/width)*100))+"%")

		print(str(id+1)+" done!");
		queue_id.put(returning)
		

