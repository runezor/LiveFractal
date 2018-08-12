import fractal5
import renderer4
import matplotlib.pyplot as plt
import random
from decimal import *

a=fractal5.mandelbrot()

a.x=Decimal(input("x"))
a.y=Decimal(input("y"))
a.w=Decimal(input("w"))
a.h=Decimal(input("h"))
i=int(input("Maxiter"))

res_x=int(4000)
res_y=int(4000)

r=a.render(i,resx=res_x,resy=res_y,threadCount=4)

r=r.astype(float)

asort=renderer4.array_sort(r)



"""Fikser weird mønstre"""
asort=asort.flatten()
for index, u in enumerate(r.flatten()):
	if u==0:
		asort[index]=res_x*res_y
asort=asort.reshape(r.shape)


maps=["hot","seismic","Spectral","PuOr","gnuplot2","gnuplot","nipy_spectral","gist_ncar","gist_heat","PiYG","PRGn","RdBu","coolwarm","RdYlGn","plasma","inferno","magma","nipy_spectral","jet","gist_earth"]

for map in maps:
	plt.imsave(map+".jpg",asort,cmap=plt.get_cmap(maps[random.randint(0,len(maps)-1)]))


