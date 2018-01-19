import fractal5
import renderer4
from decimal import *

a=fractal5.mandelbrot()

a.x=Decimal(input("x"))
a.y=Decimal(input("y"))
a.w=Decimal(input("w"))
a.h=Decimal(input("h"))
i=int(input("Maxiter"))

res_x=int(7680/4)
res_y=int(4320/4)

r=a.render(i*80,resx=res_x,resy=res_y,threadCount=4)

r=r.astype(float)

asort=array_sort(r)



"""Fikser weird mønstre"""
asort=asort.flatten()
for index, u in enumerate(r.flatten()):
	if u==0:
		asort[index]=w*h
asort=asort.reshape(r.shape)

plt.imshow(asort)
plt.show()
