import cv2
import numpy as np
import math
#import extract_plots
import testing
import x_scale
import sys
import axis
import h_scale
import traceback
import os
def final_scale(img,working_dir,yaxis1,yaxis2,xaxis1,xaxis2,clusters=2) :
	
	#img = cv2.imread(input_file)
	xarr=[]
	yarr=[]
	output_file = 'houghlines3.png'
	output_file = os.path.join(working_dir,output_file)
	input_file ='input.png'
	input_file = os.path.join(working_dir,input_file)
	#cv2.imwrite(input_file,img)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,80,120)
	rows, cols ,channels= img.shape
	print rows
	print cols
	cv2.imwrite(input_file,img)
	image1 = img
	image2 = img
	tempimg = img
	
	#cv2.line(image2,(ypt1[0][0],ypt1[0][1]),(ypt1[1][0],ypt1[1][1]),(0,0,255),2)
	#ans1,ans3,ans2,ans = axis.axis(img,working_dir)
	ans1 = yaxis1
	ans3 = yaxis2
	ans2 = xaxis1
	ans = xaxis2 

	bot_left = (ans1,ans)
	top_right = (ans3,ans2)
	#cv2.rectangle(tempimg,(bot_left),(top_right),(0,255,0),3)
	#cv2.line(img,(855,0),(855,rows),(0,0,255),2)
	#cv2.imwrite(input_file,img)
	#print 'the end points are adskandsnfjsnfjsdf'
	print bot_left
	print top_right
	image2 = image2[ans2+2:ans-2,ans1+2:ans3-2]
	temp_file = 'line5.png'
	temp_file = os.path.join(working_dir,temp_file)
	cv2.imwrite(temp_file,image2)
	#cv2.line(image1,(bot_left),(top_right),(0,0,255),2)
	y_pos = []
	x_pos = []
	#cv2.rectangle(tempimg,(bot_left),(top_right),(0,255,0),3)
	#cv2.imwrite('temp6.jpg',tempimg)
	markings = h_scale.h_scale(input_file,ans,ans3,ans1)
	y0=0
	y1=1
	pos0=0
	pos1=1
	scale_y=1
	y_pos0=bot_left[1]
	y_pos1=top_right[1]

	try :
		
		#testing.extract_y_scale(input_file,int(ans1),'test3.png',yarr,int(ans),y_pos)
		y0,y1,y_pos0,y_pos1,scale_y = testing.extract_y_scale(input_file,int(ans1),working_dir)
	except Exception, e :
		traceback.print_exc()
		y0 = 0
		y1 = 1
		scale_y = 1
		y_pos0=bot_left[1]
		y_pos1=top_right[1]
	
	try:
		count = 1
		while len(markings)<3 and count < 30:
			#print 'doing it'
			markings = h_scale.h_scale(input_file,ans-count,ans3,ans1)
			print markings
			count = count+1
		x_scale.extract_x_scale(input_file,int(ans)-2,xarr,x_pos,working_dir)
		print 'dnsidnfisnfisdnf'
		print len(xarr)
		temp = xarr[1]
		#cv2.imwrite('line4.jpg',image1)
	#cv2.imwrite('line5.jpg',image2)
		
		#scale_y = abs(float(yarr[2])-float(yarr[1]))
		
	except Exception, e :
		traceback.print_exc()
		print 'error occured'
		scale_x=1.0/(len(markings)+1)
		x0=2*scale_x
		x1=3*scale_x
		#return markings
		#return 'line5.jpg',bot_left,top_right,scale_x,scale_y,xarr[x_len-1],xarr[x_len-2],yarr[0],yarr[1],x_pos[x_len-1],x_pos[x_len-2],y_pos[0],y_pos[1]
		return temp_file,bot_left,top_right,scale_x,scale_y,x0,x1,y0,y1,markings[1],markings[2],y_pos0,y_pos1	
	'''
	print 'x scale'
	print scale_x
	print bot_left
	print x_pos[len(xarr)-1]
	print 'y scale'
	print scale_y
	print top_right
	print y_pos[0]
	'''
	
	

	print 'markings are'
	print markings
	#cv2.imwrite('houghlines3.jpg',img)
	[x,y,z ] = image2.shape
	print (x,y)
	print (ans1,ans3)
	print (ans2,ans)
	
	x_len = len(xarr)
	print bot_left,top_right
	print 'x scales are '
	#print yarr[0]
	for i in xarr :
			print i,

	i = x_len-1
	
	while i >=1 :
		try :
			x1 = float(xarr[i])
			x2 = float(xarr[i-1])
			break
		except :
			i = i-1
	l = len(markings)
	scale_x = abs(float(xarr[i])-float(xarr[i-1]))		
	for j in range(l) :
		if markings[j]<x_pos[i][1] and markings[j]>x_pos[i][0] :
			pos1 = j		
	#print 'the position issadasfsafasf'
	print pos1
	print x1
	print y0
	print y1
	print float(x1)-float(scale_x)
	print markings[pos1]
	print markings[pos1-1]
	print y_pos0
	print y_pos1
	#return 'line5.jpg',bot_left,top_right,scale_x,scale_y,xarr[x_len-1],xarr[x_len-2],yarr[0],yarr[1],x_pos[x_len-1],x_pos[x_len-2],y_pos[0],y_pos[1]
	return temp_file,bot_left,top_right,scale_x,scale_y,float(x1)-float(scale_x),x1,y0,y1,markings[pos1-1],markings[pos1],y_pos0,y_pos1
	#cv2.imwrite(output_file,img)

if __name__ == '__main__':
	print 'hi'
	x = sys.argv[1]
	xarr = []
	yarr = []
	print x
	img = cv2.imread(x)
	out = final_scale(img)
	print out
	
	
	
