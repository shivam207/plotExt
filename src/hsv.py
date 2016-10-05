import numpy as np
import cv2
import sys
import os
import copy
import math

def findHue(b,g,r):
	img1=np.zeros((1,1,3),np.uint8)
	img1[0,0,0]=b
	img1[0,0,1]=g
	img1[0,0,2]=r
	img_=cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
	h,s,v=cv2.split(img_)
	return h[0,0],s[0,0],v[0,0]

def mark(img,b,g,r):
	(hue,sat,val)=findHue(b,g,r)
	img1=np.zeros((len(img),len(img[0])),np.uint8)
	img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	h,s,v=cv2.split(img_hsv)
	for i in range(len(h)):
		for j in range(len(h[0])):
			if(h[i,j]<=hue+5)and(h[i,j]>=hue-5)and(s[i,j]<=240)and(s[i,j]>=20):
				img1[i,j]=255
	
	return img1
