import cv2
def h_scale(input_file,haxis_y,haxis_right,haxis_left):
	"""
	returns the horizontal unit scale
	takes the grayscaled image, the y-position of the horizontal axis
	and the left and right extremes of the horizontal axis as parameters


	"""
	img = cv2.imread(input_file,cv2.IMREAD_GRAYSCALE)
	#cv2.imshow("as",img)
	#cv2.waitKey(0)

	crop_img=img[haxis_y-20:haxis_y+20,haxis_left-20:haxis_right+20]		#crops the image to some area around the horizontal axis
	#cv2.imshow("Crop",crop_img)
	th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)  #using adaptive thresholding
	l=[]
	f1=0
	k=[]
	'''caxis_y=20
	caxis_left=20
	caxis_right=haxis_right-haxis_left+20
	'''
	y_trav=haxis_y-5
	#cv2.rectangle(crop_img,(22,20),(690,30),(0,255,0),2)
	#cv2.imshow("Crop",crop_img)
	for x in range(haxis_left-2,haxis_right+5):
		#print (str(th2[y_trav,x]))
		if(th2[y_trav,x]==0 and f1==0):
			f1=1
		 	lx=x
		if(th2[y_trav,x]==255 and f1==1):
			l.append((x+lx)/2)
			f1=0

	#cv2.imshow("th2",th2)
	
	print "Successive distances are",
	print l
	return l
	
	d = {}
	maxi = -1
	for i in range(len(l)-1,0,-1):
		k.append(l[i]-l[i-1])
		if not l[i]-l[i-1] in d :
			d[l[i]-l[i-1]] = 1
		else :
			d[l[i]-l[i-1]] = d[l[i]-l[i-1]] + 1
	for i in range(len(l)-1):
		if d[k[i]]>maxi :
			maxi = d[k[i]]
			mark = k[i]
	print 'the mark is'		
	print mark
	print l	
	print "Successive distances are",
	k.sort()
	print k
	return l
	'''
	if(len(k)%2==0):
		if(len(k)>0):
			final=(k[len(k)/2-1]+k[len(k)/2])/2
	else:
		final=k[len(k)/2]
	'''
	#return final


if __name__ == '__main__':
	img=cv2.imread('pic1.png',cv2.IMREAD_GRAYSCALE)
	haxis_y=524
	haxis_left=133
	haxis_right=852
	h_unit=h_scale('pic1.png',haxis_y,haxis_right,haxis_left)															#scale function call
	print "Unit scale is  "+str(h_unit)
	cv2.waitKey(0)
