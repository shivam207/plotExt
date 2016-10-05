import cv2
def v_scale(input_file,vaxis_x,vaxis_top,vaxis_lef):
	"""
	returns the vertical unit scale
	takes the grayscaled image, the x-position of the vertical axis
	and the top and bottom extremes of the vetical axis as parameters


	"""
	img=cv2.imread(input_file,cv2.IMREAD_GRAYSCALE)
	#cv2.imshow("as",img)
	crop_img=img[vaxis_top-20:vaxis_bot+20,vaxis_x-20:vaxis_x+20]		#crops the image to some area around the vertical axis
	#cv2.imshow("Crop",crop_img)
	th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)  #using adaptive thresholding
	l=[]
	f1=0
	k=[]
	'''caxis_x=20
	caxis_top=20
	caxis_bot=vaxis_bot-vaxis_top+20
	'''

	x_trav=vaxis_x+5
	#cv2.rectangle(crop_img,(22,20),(690,30),(0,255,0),2)
	#cv2.imshow("Crop",crop_img)
	
	for x in range(vaxis_top-2,vaxis_bot+5):
		print (str(th2[x,x_trav]))
		if(th2[x,x_trav]==0 and f1==0):
			f1=1
		 	lx=x
		if(th2[x,x_trav]==255 and f1==1):
			l.append((x+lx)/2)
			f1=0
	#cv2.imshow("th2",th2)
	print "Successive distances are",
	print l
	return l


	'''
	for i in range(len(l)-1,0,-1):
		k.append(l[i]-l[i-1])
	
	k.sort()
	print k
	if(len(k)%2==0):
		final=(k[len(k)/2-1]+k[len(k)/2])/2
	else:
		final=k[len(k)/2]
	
	cv2.rectangle(th2,(10,19),(30,44),(0,255,0),2)
	cv2.imshow("th-rect",th2)
	return final
	'''

if __name__ == '__main__':
	img=cv2.imread('axistest.png',cv2.IMREAD_GRAYSCALE)
	vaxis_x=62
	vaxis_top=20
	vaxis_bot=365
	#cv2.rectangle(img,(62,20),(100,107),(0,255,0),2)
	#cv2.imshow("rect",img)

	v_unit=v_scale('axistest.png',vaxis_x,vaxis_top,vaxis_bot)															#scale function call
	print "Vertical Unit scale is  "+str(v_unit)
	cv2.waitKey(0)
