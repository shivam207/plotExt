import cv2
import numpy as np
import math
img = cv2.imread('im3.png',cv2.IMREAD_GRAYSCALE)
#x, y, z = .shape
rows,cols= img.shape
#Mat dst(cols,rows)
#cv2.imshow("jj",dst)
#cv2.waitKey(0)
dig = rows*rows + cols*cols
dig = math.sqrt(dig)
dig = int(dig)+1
dst = np.ones((dig,dig),np.uint8)*255
M1 = np.float32([[1,0,(dig-cols)/2],[0,1,(dig-rows)/2]])
dst = cv2.warpAffine(img,M1,(dig,dig),dst)
cv2.imwrite("test11.png",dst)
M = cv2.getRotationMatrix2D((dig/2,dig/2),270,1)
dst = cv2.warpAffine(dst,M,(dig,dig))

temp = np.zeros((cols,rows),np.uint8)
cv2.transpose(img,temp)
cv2.flip(temp,1,temp)
rows,cols = temp.shape
temp = temp[47:rows,0:cols]
rows,cols = temp.shape

temp1 = np.zeros((cols,rows),np.uint8)
cv2.transpose(temp,temp1)
cv2.flip(temp1,0,temp1)

rows,cols = temp1.shape
temp1 = temp1[0:rows,0:65]
cv2.imshow("jj",temp1)
cv2.imwrite('testing11.png',temp1)
#cv2.imwrite("test1.png",crop)
cv2.waitKey(0)
#M2 =np.multiply(M,M1)
#dst = cv2.warpAffine(dst,M1,(rows,cols))
'''
i=0
j=0

while i<cols:
	j=0
	while j<rows:
		dst[i][j]=img[j][i]
		j=j+1
	i=i+1
'''
#M = cv2.getRotationMatrix2D((rows/2,cols/2),180,1)
#dst = cv2.warpAffine(dst,M,(rows,cols))
cv2.imwrite("test3.png",dst)

crop_image = dst[215:dig,0:dig]

cv2.imwrite("test2.png",crop_image)

rows,cols= crop_image.shape
dig = rows*rows + cols*cols
dig = math.sqrt(dig)
dig = int(dig)+1
M1 = np.float32([[1,0,(dig-cols)/2],[0,1,(dig-rows)/2]])
dst = cv2.warpAffine(crop_image,M1,(dig,dig))

M = cv2.getRotationMatrix2D((dig/2,dig/2),90,1)
dst = cv2.warpAffine(dst,M,(dig,dig))
cv2.imwrite("test5.png",dst)
i=0
while dst[cols-10][i] ==0 :
	i=i+1

crop = dst[0:cols,0:210]
#cv2.imshow("jj",crop)
#cv2.imwrite("test1.png",crop)
#cv2.waitKey(0)
