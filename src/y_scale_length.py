import cv2
import numpy as np
import math
import os
import sys
#import ocr_parse
from bs4 import BeautifulSoup

def y_scale_length(input_file) :
	os.system("tesseract "+input_file+" out1 hocr")
	#os.rename('out.hocr','out.xml')
	arr = []
	f = open('out1.hocr','r')
	data=f.read()
	soup = BeautifulSoup(data)
	for i in soup.find_all('span',{'class':'ocrx_word'}) :
		h= i.get('title').split(' ')
		k= h[1:5]
		k[-1]=k[-1][:-1]
		#print k
		arr.append((int(k[1])+int(k[3]))/2)
	sum = 0
	h= 1
	while (h<len(arr)) :
		print arr[h]
		sum = sum + arr[h]-arr[h-1]
		h=h+1		
	output = sum/(len(arr)-1)
	return output

if __name__ == '__main__':
	out = y_scale_length('test3.png')
	print 'length is '
	print str(out)	

