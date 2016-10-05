import cv2
import numpy as np
import math

def rotate(input_file,output_file,mode) :
	img = cv2.imread(input_file,cv2.IMREAD_GRAYSCALE)
	rows,cols= img.shape
	temp = np.zeros((cols,rows),np.uint8)
	cv2.transpose(img,temp)
	cv2.flip(temp,mode,temp)	
	cv2.imwrite(output_file,temp)
	

if __name__ == '__main__':
	rotate('im3.png','test1.png',1)
