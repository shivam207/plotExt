import cv2
import numpy as np

img = cv2.imread('0001.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(5,5),0)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
#cv2.imshow("image",edges)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

h,w,channel = img.shape
print h,w,channel

p = np.zeros((h,w,channel),np.uint8)
q = np.zeros((h,w,channel),np.uint8)

l = []

lines = cv2.HoughLines(edges,1,np.pi/180,500)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    #print a,b
    x0 = a*rho
    y0 = b*rho
    
    x=x0
    y=y0
    while x<w and y<h and x>=-0.1 and y>=-0.1:
    	p[y,x] = tuple((0,0,255))
    	#l.append(tuple(x,y))
    	x = int(x + (-b))
    	y = int(y + (a))
    	
    x = x0
    y= y0
    while x>=-0.1 and y>=-0.1 and x<w and y<h:
    	p[y,x] = tuple((0,0,255))
    	#l.append(tuple(x,y))
    	x = int(x - (-b))
    	y = int(y - (a))
    	

    #print p
    '''	
    x1 = int(x0 + 5000*(-b))
    y1 = int(y0 + 5000*(a))
    x2 = int(x0 - 5000*(-b))
    y2 = int(y0 - 5000*(a))
    '''
    #cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

for i in range(w):
	for j in range(h): 
		if p[j,i][2]==255 and img[j,i][2]<20:
			print "reach"
			p[j,i]=tuple((255,0,0))
		else:
			p[j,i]=tuple((0,0,0))

cv2.imshow("image",p)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('points.jpg',p)
cv2.imwrite('houghlines7.jpg',img)