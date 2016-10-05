import cv2
from sklearn.cluster import KMeans
import numpy as np 
import matplotlib.pyplot as plt


def centroid_histogram(clt):
	ret_labels=clt.labels_
	bw_labels=[]
	bw_labels=clt.predict([[0.0,0.0],[0.0,255.0]])
	labels=[]
	for i in range(len(ret_labels)):
		if(ret_labels[i] not in bw_labels):
			labels.append(ret_labels[i])
	numLabels = np.arange(0, len(np.unique(labels)))
	(hist, _) = np.histogram(labels, bins = numLabels)
	print hist
	hist = hist.astype("float")
	hist /= hist.sum()
	return hist,labels

def plot_colors(hist, centroids):
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
	for (percent, color) in zip(hist, centroids):
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
			color.astype("uint8").tolist(), -1)
		startX = endX
	return bar

def unique_intervals(labels,centres):
	unq=[]

	for i in labels:
		f=1
		for j in unq:
			if(centres[i][0]>centres[j][0]-5 and centres[i][0]<centres[j][0]+5):
				f=0
		if(f):
			unq.append(i)
			
	return unq

image=cv2.imread("p1.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
h,s,v=cv2.split(image)
hv=cv2.merge((h,v))
# show our image
plt.figure()
plt.axis("off")
plt.imshow(image)

image = hv.reshape((image.shape[0] * image.shape[1], 2))
clt = KMeans(n_clusters = 12)
clt.fit(image)

hist,labels = centroid_histogram(clt)
bar = plot_colors(hist, clt.cluster_centers_)
 
# show our color bart
plt.figure()
plt.axis("off")
plt.imshow(bar)
plt.show()

image=cv2.imread("p1.png")
image=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
centres=clt.cluster_centers_
labels=unique_intervals(labels,centres)
print labels
clt_image=clt.labels_.reshape((image.shape[0],image.shape[1],1))
for label in np.unique(labels):
	if(hist[label]>0):
		low=np.array((centres[label][0]-10,100,100),dtype="uint8")
		high=np.array((centres[label][0]+10,255,255),dtype="uint8")
		#mask=np.array(np.equal(clt_image,label),dtype=np.uint8)*255
		mask=cv2.inRange(image,low,high)
		cv2.imwrite("mask_%d.jpg"%label,mask)	


