import cv2
from sklearn.cluster import KMeans
import numpy as np 

def extract_plots(filename,clusters):
	image=cv2.imread(filename)
	print filename
	#image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	image=cv2.dilate(cv2.erode(image,(5,5)),(5,5))

	img_array = image.reshape((image.shape[0] * image.shape[1], 3))

	clt = KMeans(n_clusters = clusters)
	
	clt.fit(img_array)

	ret_labels=clt.labels_

	#Uncomment
	bw_labels=[]
	bw_labels=clt.predict([[0.0,0.0,0.0],[255.0,255.0,255.0]])

	labels=[]
	for i in range(len(ret_labels)):
		if(ret_labels[i] not in bw_labels):
			labels.append(ret_labels[i])

	clt_image=clt.labels_.reshape((image.shape[0],image.shape[1],1))
	#return clt_image,bw_labels
	mask_names=[]
	masks=[]
	for label in np.unique(labels):
		mask=np.array(np.equal(clt_image,label),dtype=np.uint8)*255
		mask_name="mask_%d_%s"%(label,filename)
		mask_names.append(mask_name)
		masks.append(mask)
		cv2.imwrite(mask_name,mask)
	print mask_names	
	return clt_image,bw_labels,mask_names,masks

#extract_plots("pic5.png")


#res = cv2.bitwise_and(image,image, mask= mask)


