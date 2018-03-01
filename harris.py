# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:19:15 2018

@author: Student
"""
from PIL import Image
import numpy as np
from numpy.linalg import inv
from scipy.misc import toimage

im=Image.open('checkerboard.png')
size=im.size
s1=size[0]+3
s2=size[1]+3
a=im.convert('L')
Ix=np.zeros((s1,s2))
Iy=np.zeros((s1,s2))
Ixy=np.zeros((s1,s2))
for i in range(0,size[0]-2):
    for j in range(0,size[1]-2):
        a1=a.getpixel((i,j))
        a2=a.getpixel((i+1,j))
        a3=a.getpixel((i,j+1))
        a4=a.getpixel((i+1,j+1))
        Ix[i+3][j+3]=np.subtract(a2,a1)
        Iy[i+3][j+3]=np.subtract(a3,a1)
        #Ixy[i+3][j+3]=np.subtract(a4,a1)

a1=a.getpixel((i+1,j+1))
Ix[i+4][j+4]=-1*a1
Iy[i+4][j+4]=-1*a1
#Ixy[i+4][j+4]=-1*a1
   
toimage(Ix).save('Ix.png')
toimage(Iy).save('Iy.png')


Ixsq=np.dot(Ix,Ix)
Iysq=np.dot(Iy,Iy)
Ixy=np.dot(Ix,Iy)
toimage(Ixy).save('Ixy.png')
toimage(Ixsq).save('Ixsquare.png')
toimage(Iysq).save('Iysquare.png')

from scipy.signal import gaussian as gauss
import scipy.signal as ss
w=gauss(121,1)
w=w.reshape((11,11))
print('Gaussian window of std=1')
print(w)

Ax=ss.convolve2d(Ixsq,w)
Ay=ss.convolve2d(Iysq,w)
Axy=ss.convolve2d(Ixy,w)
corner=np.zeros((4000000,1))
p=q=0
k=0.05

for i in range(0,size[0]-1):
    for j in range(0,size[1]-1):
        M=np.ndarray((2,2))
        M[0][0]=Ax[i+3][j+3]
        M[0][1]=M[1][0]=Axy[i+3][j+3]
        M[1][1]=Ay[i+3][j+3]
        det=(M[0][0]*M[1][1])-(M[0][1]*M[1][0])
        trace=M[0][0]+M[1][1]
        R=det - k*trace
        if(R>25000):
            print('Corner')
            print(R)
            corner[p]=i
            corner[p+1]=j
            p=p+1
            
import matplotlib.pyplot as plt
fig,ax=plt.subplots()
imm=ax.imshow(a)
for i in range(0,p):
    ax.plot([corner[i]],[corner[i+1]],'o',color='yellow')
plt.show()        
        
        

