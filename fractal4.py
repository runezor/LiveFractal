import numpy as np
import math
from decimal import *
import matplotlib.pyplot as plt
import threading
from multiprocessing import Process, Queue

def mandelbrot_point(creal,cimag,maxiter):
	real=creal
	imag=cimag

	for n in range(maxiter):
		real2=real*real		
		imag2=imag*imag
		if real2+imag2>8.0:
			return n
		imag=2*real*imag+cimag
		real=real2-imag2+creal		
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
	space=np.empty((512,512),dtype=int)

	def render(self,maxiter,resx=512,resy=512,threadCount=4):
		self.mandelbrot_space_init(resx,resy)

		threads={}
		queues={}

		for i in range(threadCount):
			queues[i]=Queue()
			threads[i]=Process(target=self.mandelbrot_space,args=[self.space,self.real,self.imag,resx,resy,maxiter,threadCount,i,queues[i]])
	

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

		self.space=np.zeros((height,width),dtype=int)

		for i in range(width):
			for j in range(height):
				self.real[i,j]=r1[i]
				self.imag[i,j]=r2[j]

		print("arrayspace initialised!")
		
	
	def mandelbrot_space(self,space_size,reals,imags,width,height,maxiter,threadCount,id,queue_id):
		returning=space_size

		for i in range(id, width, threadCount):
			for j in range(height):
				returning[j,i]=mandelbrot_point(reals[i,j],imags[i,j],maxiter)
			if math.floor((i/width)*10) != math.floor(((i-1)/width)*10):
				print(str(id+1)+": "+str(math.floor((i/width)*100))+"%")

		print(str(id+1)+" done!");
		queue_id.put(returning)
		

