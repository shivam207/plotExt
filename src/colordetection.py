import cv2
import numpy as np
def colordetect(img,x1,y1,x2,y2):
	d={}






	





	return d
if __name__ == '__main__':

	color={}
	#color=colordetect(img,x1,y1,x2,y2)
	img=cv2.imread("color.jpg")
	img_hsv=cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
	print img_hsv.shape
	h,s,v=cv2.split(img_hsv)
	M = cv2.calcHist([img_hsv],[0], None, [360], [0, 360] )
	#print(M.shape)
	print np.max(M),np.argmax(M)
	M=np.delete(M,np.argmax(M))
	print np.argmax(M)
	h2,dst=cv2.threshold(h, np.argmax(M), 180, cv2.THRESH_BINARY)
	lower_blue = np.array([110,50,50])
	upper_blue = np.array([130,255,255])
    # Threshold the HSV image to get only blue colors
	mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
	cv2.imshow("hsv",mask)
	cv2.waitKey(0)
	print np.max(M),np.argmax(M)
	M=np.delete(M,np.argmax(M))
	print np.max(M),np.argmax(M)


	matrix = np.zeros((360,1200,3),np.uint8)
	for i in range(len(M)):
		#print(M[i])
		if(M[i]<1200):
			matrix[i,int(M[i])]=tuple((255,0,0))
		else:
			#print M[i]
			pass
	print matrix.shape
	cv2.imwrite("hist_plot.jpg",matrix)
	exit()
	#cv2.imshow("hist",matrix)
	print "boo"
	cv2.waitKey(0)
	cv2.destroyWindows()
	exit()
	cv2.rectangle(img,(5,10),(630,400),(0,255,0),2)
	cv2.imshow("rec",img)
	print img[1][1]
	
	d={}
	d[0]=1
	print d[0]
	
	hexcolor = (img[1][1][0] << 16) + (img[1][1][1] << 8) + img[1][1][2]
	print str(hexcolor)
	cv2.waitKey(0)