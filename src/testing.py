import rotation
import cv2
import numpy as np
import math
import os
import sys
import y_scale_length
#import ocr_parse
from bs4 import BeautifulSoup

def extract_y_scale(input_file,coordinate,working_dir) :
	print(working_dir)
	img = cv2.imread(input_file,cv2.IMREAD_GRAYSCALE)
	rows,cols = img.shape
	img = img[0:rows,0:coordinate]
	temp_file = 'temp.png'
	temp_file = os.path.join(working_dir,temp_file)
	temp1_file = 'temp1.png'
	temp1_file = os.path.join(working_dir,temp1_file)
	cv2.imwrite(temp_file,img)
	cv2.imwrite(temp1_file,img)
	output_file = "test3.png"
	output_file = os.path.join(working_dir,output_file)
	testing_file = "rectangle_y.png"
	testing_file = os.path.join(working_dir,testing_file)
	rotation.rotate(temp_file,output_file,1)
	img = cv2.imread(output_file,cv2.IMREAD_GRAYSCALE)
	cv2.imwrite(temp1_file,img)
	rows,cols = img.shape
	out_hocr_file = os.path.join(working_dir,"out1")
	os.system("tesseract "+output_file+" "+out_hocr_file+" hocr")
	#os.rename('out.hocr','out.xml')
	output_array = []
	y_pos=[]
	f = open(out_hocr_file+".hocr",'r')
	data=f.read()
	soup = BeautifulSoup(data)
	'''
	i = soup.find('span',{'class':'ocr_line'})
	h= i.get('title').split(' ')
	k= h[1:5]
	k[-1]=k[-1][:-1]
	print k
	'''
	mini = 1000000000
	for i in soup.find_all('span',{'class':'ocr_line'}) :
		h= i.get('title').split(' ')
		k= h[1:5]
		k[-1]=k[-1][:-1]
		print k
		if int(k[3])<mini :
			mini = int(k[3])
	#cv2.rectangle(img,(int(k[0]),int(k[1])),(int(k[2]),int(k[3])),(0,255,0),3)
	#print min
	#cv2.rectangle(img,(294,60),(394,75),(0,255,0),3)
	#cv2.imwrite(temp1_file,img)	
	#cv2.rectangle(img,(int(k[0]),int(k[1])),(int(k[2]),int(k[3])),(0,255,0),3)
	#cv2.imwrite(output_file,img)
	
	img = img[mini:rows,0:cols]
	cv2.imwrite(temp_file,img)
	rotation.rotate(temp_file,output_file,0)
	out_hocr_file_2 = os.path.join(working_dir,"out")
	img1 = cv2.imread(output_file)
	os.system("tesseract "+output_file+" "+out_hocr_file_2+" hocr")
	f = open(out_hocr_file_2+".hocr",'r')
	data=f.read()
	a = []
	index = []
	soup = BeautifulSoup(data)
	count = 0
	for i in soup.find_all('span',{'class':'ocrx_word'}) :
		
		print 'ndns'
		print i.text
		h= i.get('title').split(' ')
		k= h[1:5]
		k[-1]=k[-1][:-1]
		cv2.rectangle(img1,(int(k[0])-1,int(k[1])+1),(int(k[2])+1,int(k[3])-1),(0,255,0),3)

		x = ''

		for char in i.text :
			if char == 'O' or char =='o':
				x+='0'
			else :
				x+=char	
		print x
		count = count+1		
		try :
			y = float(x)
			output_array.append(float(x))
			y_pos.append((int(k[1])+int(k[3]))/2)
			index.append(count)

		except :
			continue
	cv2.imwrite(testing_file,img1)
	y1 = output_array[0]
	y2 = output_array[1]
	pos1 = y_pos[0]
	pos2 = y_pos[1]
	scale = abs(y1-y2)/abs(index[0]-index[1])	
	return y1,y2,pos1,pos2,scale
	'''	
	h= i.get('title').split(' ')
	k= h[1:5]
	k[-1]=k[-1][:-1]
	t = (int(k[1])+int(k[3]))/2
	x = a[0] - a[1]

	leng = len(output_array)	
	y = a[leng-1]

	z = a[leng-2] - 2*a[leng-1]
	print z
	yl = y_scale_length.y_scale_length(output_file)
	if abs(xcoordinate - t>= 0.1*yl) :
		#print output_array[leng-1] - x
		output_array.append(z)
	'''



if __name__ == '__main__':
	array = []
	y0=0
	y1=0
	pos0=0
	pos1=0
	scale=0
	extract_y_scale('pic1.png',133,'test3.png',y0,y1,pos0,pos1,scale)


