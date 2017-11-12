import numpy as np
from decimal import *
import matplotlib.pyplot as plt

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

def mandelbrot_space(x,y,xsize,ysize,width,height,maxiter):
	r1=linespace(x-xsize/2, x+xsize/2, width)
	r2=linespace(y-ysize/2, y+ysize/2, height)	

	real=np.empty((width,height),dtype=object)
	imag=np.empty((width,height),dtype=object)
	returning=np.empty((width,height),dtype=int)
	
	for i in range(width):
		for j in range(height):
			real[i,j]=r1[i]
			imag[i,j]=r2[j]

	print("arrayspace initialised!")

	for i in range(width):
		for j in range(height):
			returning[j,i]=mandelbrot_point(real[i,j],imag[i,j],maxiter)

	return returning



def linespace(x1,x2,width):
	unit=(x2-x1)/width
	return([x1+unit*i for i in range(width)])

class mandelbrot:
	x=Decimal(0)
	y=Decimal(0)
	w=Decimal(2)
	h=Decimal(2)
	def render(self,maxiter,resx=512,resy=512):
		return(mandelbrot_space(self.x,self.y,self.w,self.h,resx,resy,maxiter))
