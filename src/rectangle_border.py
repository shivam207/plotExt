import cv2

def draw_rectangles(filename,pos):

	#pos=[[0 2 0 3],[0 2 0 4]]
	img=cv2.imread(filename,cv2.IMREAD_COLOR)
	#print img
	for x in pos:
		cv2.rectangle(img,(x[0],x[1]),(x[2],x[3]),(0,255,0),2)

	cv2.imshow("as",img)
	k = cv2.waitKey(0)
	