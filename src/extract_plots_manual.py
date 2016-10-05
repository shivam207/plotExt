import numpy as np
import cv2
import sys
import os
import copy
import math
import tables

def getKey(item):
	return item[1]


def plot(img,t_):
	masks=[]
	img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	h,s,v=cv2.split(img_hsv)
	for k in range(len(t_)):
		img1=np.zeros((len(img),len(img[0])),np.uint8)
		print t_[k]
		for i in range(len(h)):
			for j in range(len(h[0])):
				if(h[i,j]>t_[k]-5)and(h[i,j]<t_[k]+5)and(s[i,j]>20)and(s[i,j]<240):
					img1[i,j]=255
				if(180-h[i,j]+t_[k]<5)and(s[i,j]<240)and(s[i,j]>20):
					img1[i,j]=255
				if(h[i,j]+180-t_[k]<5)and(s[i,j]<240)and(s[i,j]>20):
					img1[i,j]=255			
		masks.append(img1)
	return masks



def hue_hist(img):
	max=len(img)*len(img[0])
	h_final=[]
	h_=[]
	a=[]
	h_sorted=[]
	for i in range(181):
		h_.append(0)
	img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	h,s,v=cv2.split(img_hsv)
	for i in range(len(h)):
		for j in range(len(h[0])):
			if(s[i,j]<240)and(s[i,j]>20):
				h_[h[i,j]]+=1
	for i in range(len(h_)):
		if(h_[i]>0.75*max):
			h_[i]=0
	for i in range(len(h_)):
		a.append([i,h_[i]])
	h_sorted=sorted(a,key=getKey)
	i=len(h_sorted)-1
	while(i>=0):
		h_final.append(h_sorted[i][0])
		i-=1
	return h_final



def topClusters(h_final,clusters):
	b=[]
	prev=[]
	count=0
	i=0
	while(count<clusters):
		if(i==len(h_final)):
			break
		cnt=0
		for j in range(len(prev)):
			if (h_final[i]<prev[j]+5)and(h_final[i]>prev[j]-5):
				cnt+=1
			if (h_final[i]+180-prev[j]<5):
				cnt+=1
			if (180-h_final[i]+prev[j]<5):
				cnt+=1

		if(cnt==0):
			count+=1
			b.append(h_final[i])
			prev.append(h_final[i])
		i+=1
	return b



def run_manual(input_file,bottom_left,top_right,scale_x,scale_y,x1,x2,y1,y2,p_x1,p_x2,p_y1,p_y2,clusters,working_dir):
	img=cv2.imread(input_file,cv2.IMREAD_COLOR)
	h_final=hue_hist(img)
	t_=topClusters(h_final,clusters)
	bgr=[]
	img1=np.zeros((1,1,3),np.uint8)
	sat=125
	val=125
	for i in range(len(t_)):
		img1[0,0]=(t_[i],sat,val)
		img_bgr=cv2.cvtColor(img1,cv2.COLOR_HSV2BGR)
		bgr.append(img_bgr[0])
	
	print "Detecting colours"
	masks=plot(img,t_)
	print "Done"
	print "Finding parameters"
	print(input_file,bottom_left,top_right,scale_x,scale_y,x1,x2,y1,y2,p_x1,p_x2,p_y1,p_y2,clusters)
	(ppdiv_x,ppdiv_y,rectsize_x,rectsize_y,start_x,start_y,scale_x,scale_y) = tables.findParameters(x1,int(p_x1),y1,int(p_y1),x2,int(p_x2),y2,int(p_y2),scale_x,scale_y,bottom_left,top_right)
	print "Done"
	print "Finding tables"
	print "Returned bgr values :"	
	print bgr
	legend = []
	for color in bgr:
		legend.append([[],tuple(color[0])])
	print(legend)
	return tables.findTables(masks,ppdiv_x,ppdiv_y,rectsize_x,rectsize_y,start_x,start_y,scale_x,scale_y,working_dir,legend),legend



