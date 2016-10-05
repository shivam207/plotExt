import xml.etree.ElementTree	
import os
from bs4 import BeautifulSoup
import numpy as np
import cv2
#from sklearn.cluster import KMeans
import warnings


#generating the hocr file



#current_color = []

def draw_rectangles(img,pos):	
	for x in pos:
		cv2.rectangle(img,(x[0],x[1]),(x[2],x[3]),(0,255,0),2)
	

def min(a,b):
	if(a<b):
		return a
	return b

def mod(a):
	if(a<0):
		return -a
	return a

#returns true is the vertical strip contains only white or black pixels
def isWhiteOrBlack(x,y,height,image,image_orig,colour_found,current_color):
	cnt = 0
	if(x>=image.shape[1] or y+height>=image.shape[0] or x<=0 or y<=0):
		return 1

	for i in range(height):	
		#curr_label = clt.predict([image[y+i][x][0],image[y+i][x][1],image[y+i][x][2]])
		#if(curr_label != w and curr_label != b):
		

		if((image[y+i][x][2]>20 or image[y+i][x][1]>20) and (image[y+i][x][1]>20 or image[y+i][x][2]<200) ):
			if(colour_found == 0):
				del current_color[:]
				current_color.append(image_orig[y+i][x][0])
				current_color.append(image_orig[y+i][x][1])
				current_color.append(image_orig[y+i][x][2])
			cnt = cnt+1

	if(cnt>0):
		return 0			
	return 1
def isBlack(x,y,height,image):
	cnt = 0
	if(x>=image.shape[1] or y+height>=image.shape[0] or x<=0 or y<=0):
		return 0

	for i in range(height):	
		#print x,y,height,image.shape
		#curr_label = clt.predict([image[y+i][x][0],image[y+i][x][1],image[y+i][x][2]])
		if((image[y+i][x][2]<20 and image[y+i][x][1]<20)):
			cnt = cnt+1
	if(cnt>0):
		return 1			
	return 0

def isPresent(rect, y, height):
	for i in range(len(rect)):
		mid = (rect[i][1]+rect[i][3])/2
		if(y<mid and y+height>mid):
			return 1
	return 0

def makeWhite(x,y,height,image):
	for i in range(height):
		image[y+i][x][0] = 255
		image[y+i][x][1] = 255
		image[y+i][x][2] = 255


def parse_hocr(filename, x_min, x_max, y_min, y_max, img):

	warnings.filterwarnings("ignore")

	e = xml.etree.ElementTree.parse(filename).getroot()

	f = open(filename,'r')
	data=f.read()

	soup = BeautifulSoup(data)
	rect=[]
	first = 0;
	count = 0;
	for i in soup.find_all('span',{'class':'ocrx_word'}) :
			h= i.get('title').split(' ')
			if(i.text.strip(" ")==""):
				continue	
			
			#removes words which contain no alphabet
			
			word = i.text.strip(" ")			
			flag = 0
			dashcount=0
			for j in range(len(word)):
				if(word[j]>='a' and word[j]<='z'):
					flag = 1
					break;
				if(word[j]>='A' and word[j]<='Z'):
					flag = 1
					break				
				if(ord(word[j]) >= 5000):
					dashcount+=1
			if(flag==0 or dashcount>0):
				continue
			
			#remove ends

			count += 1
			k= h[1:5]
			k[-1]=k[-1][:-1]
			k=[int(x) for x in k]
			rect.append(k)
			#print k,i.text,len(i.text)



	image=cv2.imread(img,cv2.IMREAD_COLOR)

	
	
	image=cv2.dilate(cv2.erode(image,(5,5)),(5,5))	

	image_orig = image
	'''
	draw_rectangles(image_orig,rect)
	cv2.imshow("as",image_orig)
	cv2.waitKey(0)
	'''
	image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	#KMeans
	'''
	img_array = image.reshape(image.shape[0] * image.shape[1], 3)

	clt = KMeans(n_clusters = 6)
	
	clt.fit(img_array)

	ret_labels=clt.labels_

	bw_labels=clt.predict([[0.0,0.0,255.0], [0.0,0.0,0.0]])	
	b = clt.predict([0.0,0.0,0.0])
	

	print clt.cluster_centers_[b]

	#print bw_labels
	'''
	
	#removes rectangles which contain coloured pixels

	to_remove = []


	#this part may be corrected later
	
	
	'''
	for k in range(len(rect)):
		r = rect[k]
		cnt = 0
		height = r[3]-r[1]
		for i in range(r[0], r[2]):
			if(isWhiteOrBlack(i,r[1],height,image,image_orig,1)==0):
				cnt += 1
		print cnt
		if(cnt > 10):			
			to_remove.append(k)
	'''
	
	'''
	draw_rectangles(image_orig, rect)
	cv2.imshow("as",image_orig)
	cv2.waitKey(0)
	'''
	
	
	mid_rect = []
	for i in range(len(rect)):
		found = 0
		for j in range(len(to_remove)):
			if(i==j):
				found = 1
				break
		if(found == 0):
			mid_rect.append(rect[i])
	
	
	
	#coordinates of the bounding box

	#horizontal is x
	#out_x = bound_x
	#out_y = bound_y
	out = []

	#removes text outside the bounding box
	for i in range(len(mid_rect)):
		if(mid_rect[i][0]>x_min and mid_rect[i][1]<y_max and mid_rect[i][0]<x_max and mid_rect[i][1]>y_min):
			out.append(i)

	#temp_rect contains the text only inside the bounding box
	temp_rect = []
	for i in range(len(out)):
		temp_rect.append(mid_rect[out[i]])

	print "After removal of boundary"
	print len(temp_rect)



	#we create a array of sets to merge text in the same line
	arr=[]
	for i in range(len(temp_rect)):		
		for j in range(i+1,len(temp_rect)):			
			if(mod(temp_rect[i][1]-temp_rect[j][1])<(temp_rect[i][3]-temp_rect[i][1])):
				found = 0
				for k in range(len(arr)):
					for l in range(len(arr[k])):
						if(arr[k][l]==i or arr[k][l]==j):
							found = 1
							if(arr[k].count(i)==0):
								arr[k].append(i)
							if(arr[k].count(j)==0):
								arr[k].append(j)
				if(found == 0):
					row = []
					row.append(i)
					row.append(j)
					arr.append(row)

	for i in range(len(temp_rect)):
		found = 0;
		for k in range(len(arr)):
			for l in range(len(arr[k])):
				if(arr[k][l]==i):
					found = 1;
					break
			if(found == 1):
				break;
		if(found == 0):
			row = []
			row.append(i)
			arr.append(row)

	#final words are in this new_rect
	new_rect = []
	for i in range(len(arr)):
		min_x = temp_rect[arr[i][0]][0]
		min_y = temp_rect[arr[i][0]][1]
		max_x = temp_rect[arr[i][0]][2]
		max_y = temp_rect[arr[i][0]][3]
		for j in range(len(arr[i])):
			if(min_x > temp_rect[arr[i][j]][0]):
				min_x = temp_rect[arr[i][j]][0]
			if(min_y > temp_rect[arr[i][j]][1]):
				min_y = temp_rect[arr[i][j]][1]
			if(max_x < temp_rect[arr[i][j]][2]):
				max_x = temp_rect[arr[i][j]][2]
			if(max_y < temp_rect[arr[i][j]][3]):
				max_y = temp_rect[arr[i][j]][3]
		rect_bound = []
		rect_bound.append(min_x)
		rect_bound.append(min_y)
		rect_bound.append(max_x)
		rect_bound.append(max_y)
		new_rect.append(rect_bound)

	
	print "After merging"
	print new_rect
	
	
	
	#code for detecting legends not detected by ocr


	#if nothing i detected
	if(len(new_rect)==0):
		empty = []
		return image,empty

	maxY = new_rect[0][1]
	pos = 0
	for i in range(len(new_rect)):
		if(maxY < new_rect[i][1]):
			maxY = new_rect[i][1]
			pos = i

	height = new_rect[pos][3]-new_rect[pos][1]
	max_diff = 0
	for i in range(len(new_rect)):
		for j in range(len(new_rect)):
			if(new_rect[i][1]<new_rect[j][1]):
				if(height > (new_rect[j][1]-new_rect[i][3])):
					if(max_diff < (new_rect[j][1]-new_rect[i][3])):
						max_diff = (new_rect[j][1]-new_rect[i][3])
			else:
				if(height > (new_rect[i][1]-new_rect[j][3])):
					if(max_diff < (new_rect[i][1]-new_rect[j][3])):
						max_diff = (new_rect[i][1]-new_rect[j][3])

	height += max_diff
	mid = (new_rect[pos][2]+new_rect[pos][0])/2
	y = maxY

	#moving down
	while(1):
		y = y+height
		not_found = 0
		if(y+height < y_max):
			if(isPresent(new_rect,y,height)==1):
				continue
			else:
				temp_x = mid
				cnt1 = 0
				cnt2 = 0
				while(1):
					if(isBlack(temp_x,y,height,image)==0):
						cnt1 = cnt1+1
						temp_x += 1
						if(cnt1>20):
							not_found = 1
							break
					else:
						cnt2 = cnt2+1
						temp_x += 1
						if(cnt2>5):
							break;
				if(not_found==1):
					break
				else:	
					quad = []	

					#move_right								
					cnt=0
					temp_x = mid
					while(1):
						if(isBlack(temp_x,y,height,image)==0):
							cnt += 1
							temp_x += 1
							if(cnt>20):
								break
						else:
							cnt = 0
							temp_x += 1

					x2 = temp_x

					#move_left
					cnt=0
					temp_x = mid
					while(1):
						if(isBlack(temp_x,y,height,image)==0):
							cnt += 1
							temp_x -= 1
							if(cnt>20):
								break
						else:
							cnt = 0
							temp_x -= 1

					x1 = temp_x
					quad.append(x1)
					quad.append(y)
					quad.append(x2)
					quad.append(y+height)
					new_rect.append(quad)

		else:
			break

	#moving_up
	y = maxY

	while(1):
		y = y-height
		not_found = 0
		#draw_rectangles(image_orig, new_rect[0][0], y, new_rect[0][2], y+height)
		#cv2.rectangle(image_orig,(new_rect[0][0], y),( new_rect[0][2], y+height),(0,255,0),2)
		

		if(y-height > y_min):
			if(isPresent(new_rect,y,height)==1):
				continue
			else:
				temp_x = mid
				cnt1 = 0
				cnt2 = 0
				while(1):					
					if(isBlack(temp_x,y,height,image)==0):
						cnt1 = cnt1+1
						temp_x += 1
						if(cnt1>20):
							print "pass"
							not_found = 1
							break
					else:
						cnt2 = cnt2+1
						temp_x += 1
						if(cnt2>0):
							break;
				if(not_found==1):
					break
				else:	
					quad = []	

					#move_right								
					cnt=0
					temp_x = mid
					while(1):
						if(isBlack(temp_x,y,height,image)==0):
							cnt += 1
							temp_x += 1
							if(cnt>20):
								break
						else:
							cnt = 0
							temp_x += 1

					x2 = temp_x

					#move_left
					cnt=0
					temp_x = mid
					while(1):
						if(isBlack(temp_x,y,height,image)==0):
							cnt += 1
							temp_x -= 1
							if(cnt>20):
								break
						else:
							cnt = 0
							temp_x -= 1

					x1 = temp_x
					quad.append(x1)
					quad.append(y)
					quad.append(x2)
					quad.append(y+height)
					new_rect.append(quad)

		else:
			break



	#code for removing the legend
	#first we traverse left and right to see where the legend is
	#then we go on making the legend white till we encounter a continuos strip of 40 white pixels

	print "after up down"
	print new_rect


	'''
	draw_rectangles(image, new_rect)
	
	cv2.imshow("as",image_orig)
	cv2.waitKey(0)
	'''
	colors = []
	max_extent = -1
	ignore = []
	extent = []
	for i in range(len(new_rect)):
		x1 = new_rect[i][0]
		y1 = new_rect[i][1]
		x2 = new_rect[i][2]
		y2 = y1
		height = new_rect[i][3]-new_rect[i][1]
		j=10
		pos = 0
		one_ext = []
		temp_x = 0
		current_color = []
		while(1):
			if(x1-j<0 or x2+j>=image.shape[1]):
				break
			if(isWhiteOrBlack(x1-j,y1,height,image, image_orig,1,current_color)==0):
				for z in range(3):
					isWhiteOrBlack(x1-j,y1,height,image, image_orig,0,current_color) #just for storing the color
				pos = 1
				#one_ext.append(x1-j)
				temp_x = x1-j
				#one_ext.append(y1)
				break
			if(isWhiteOrBlack(x2+j,y2,height,image, image_orig,1,current_color)==0):
				for z in range(3):
					isWhiteOrBlack(x2+j,y2,height,image, image_orig,0,current_color) #just for storing the color				
				pos = 2		
				one_ext.append(x2+j)
				one_ext.append(y2)		
				break
			j = j+1

		if(pos==0):
			continue
		if(pos==1):
			cnt = 0
			while(cnt<40):
				if(isWhiteOrBlack(x1-j,y1,height,image, image_orig,1,current_color)==0):	
					#makeWhite(x1-j,y1,height,image_orig)
					pass
				j= j+1
				if(isWhiteOrBlack(x1-j,y1,height,image, image_orig,1,current_color)!=0):
					cnt = cnt+1
			if(x1-j <= 0):
				one_ext.append(image_orig.shape[1])
			else:
				one_ext.append(x1-j+35)
			one_ext.append(y1)
			one_ext.append(temp_x)

		if(pos==2):
			cnt = 0
			while(cnt<40):
				if(isWhiteOrBlack(x2+j,y2,height,image, image_orig,1,current_color)==0):			
					#makeWhite(x2+j,y2,height,image_orig)
					pass
				j = j+1
				if(isWhiteOrBlack(x2+j,y2,height,image, image_orig,1,current_color)!=0):
					cnt = cnt+1
			if(x2+j >= image_orig.shape[1]):
				one_ext.append(image_orig.shape[1]-2)
			else:
				one_ext.append(x2+j-35)


		if(max_extent == -1):
			max_extent = j
		
		#if(abs(j-max_extent)>40):
		   # ignore.append(i)

		one_ext.append(y1+height)
		extent.append(one_ext)
		colors.append(list(current_color))

	
	removal_rect = []
	for i in range(len(new_rect)):
		removal_rect.append(new_rect[i])

	for i in range(len(extent)):
		removal_rect.append(extent[i])

	

	minx = removal_rect[0][0]
	miny = removal_rect[0][1]
	maxx = removal_rect[0][2]
	maxy = removal_rect[0][3]

	for r in (removal_rect):
		if(r[0]<minx):
			minx = r[0]
		if(r[1]<miny):
			miny = r[1]
		if(r[2]>maxx):
			maxx = r[2]
		if(r[3]>maxy):
			maxy = r[3]

	image = image_orig
	

	#this part removes complete rectangle
	for i in range(miny, maxy):
		for j in range(minx, maxx):
			image[i][j][0] = 255
			image[i][j][1] = 255
			image[i][j][2] = 255
	

	final_rect = []
	for i in range(len(new_rect)):
		flag = 0
		for j in range(len(ignore)):
			if(i==j):
				flag = 1
				break
		if(flag==0):
			final_rect.append(new_rect[i])

	#removing the text
	print final_rect
	for i in range(len(final_rect)):
		for j in range(final_rect[i][1], final_rect[i][3]):
			for k in range(final_rect[i][0], final_rect[i][2]):
				image[j][k][0] = 255;
				image[j][k][1] = 255;
				image[j][k][2] = 255;

	#cv2.imwrite("out.jpg", image);
	legend_info = []
	for i in range(len(final_rect)):
		temp = []
		temp.append(final_rect[i])
		temp.append(colors[i])
		legend_info.append(temp)


	

	#draw_rectangles(image,extent)
	return image,legend_info

#horizontal is x
def legend_detect(img, x_min, x_max, y_min, y_max,working_dir):
	#image=cv2.imread(img,cv2.IMREAD_COLOR)
	# cv2.imshow("lol",image)
	out_hocr_file = "scan"
	out_hocr_file = os.path.join(working_dir,out_hocr_file)
	os.system("tesseract " + img + " "+out_hocr_file+" hocr")
	return parse_hocr(out_hocr_file+".hocr", x_min, x_max, y_min, y_max, img)

#legend_detect("graph1.jpg", 150,800,35,500,"")


	


	
