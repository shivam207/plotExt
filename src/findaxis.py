import cv2
import numpy as np


def aspectRatio(w,h):
    #print w,h
    if(h*1.0/w >= 4 or w*1.0/h >= 4):
        return False
    return True

def find_if_close(cnt1,cnt2):
    row1,row2 = cnt1.shape[0],cnt2.shape[0]
    for i in xrange(row1):
        for j in xrange(row2):
            dist = np.linalg.norm(cnt1[i]-cnt2[j])
            if abs(dist) < 50 :
                return True
            elif i==row1-1 and j==row2-1:
                return False

def findaxis(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    h,w,channel = img.shape
    gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,11,7)
    kernel = np.zeros((5,5),np.uint8)
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    #gray = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
    #gray = cv2.filter2D(gray,-1,kernel)
    #gray = cv2.blur(gray,(5,5))
    #gray = cv2.medianBlur(gray,5)
    #gray = cv2.bilateralFilter(gray,9,75,75)
    gray = cv2.GaussianBlur(gray,(3,3),0)
    #edges = cv2.Canny(gray,50,150,apertureSize = 3)
    lines = cv2.HoughLinesP(gray,0.25,np.pi/180,100,100,30)
    im2 = np.zeros((h,w,channel),np.uint8)
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(im2,(x1,y1),(x2,y2),(0,255,0),2)
    cv2.imwrite("houghp.png",im2)

    gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
    # cv2.imwrite(graphfolder+"/gray.png",gray)
    cnts1 = cv2.findContours(gray, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
    # print temp
    # cnts1 = []
    # for t in temp[0]:
    #     if cv2.contourArea(t) >threshArea:
    #         cnts1.append(t)
    LENGTH = len(cnts1)
    status = np.zeros((LENGTH,1))

    h,w,channel = img.shape
    hi,wi = h,w

    
    for i,cnt1 in enumerate(cnts1):
        x_,y_,w_,h_  = cv2.boundingRect(cnt1)
        if h_ >= 0.95*hi or w_ >= 0.95*wi:
            continue
        x = i    
        
        if i != LENGTH-1:
            for j,cnt2 in enumerate(cnts1[i+1:]):
                x_,y_,w_,h_  = cv2.boundingRect(cnt2)
                if h_ >= 0.95*hi or w_ >= 0.95*wi:
                    continue
                x = x+1
                dist = find_if_close(cnt1,cnt2)
                if dist == True:
                    val = min(status[i],status[x])
                    status[x] = status[i] = val
                else:
                    if status[x]==status[i]:
                        status[x] = i+1

    cnts = []
    maximum = int(status.max())+1
    for i in xrange(maximum):
        pos = np.where(status==i)[0]
        if pos.size != 0:
            cont = np.vstack(cnts1[i] for i in pos)
            hull = cv2.convexHull(cont)
            cnts.append(hull)
    
    
        
    x = []
    y = []
    w = []
    h = []
    cont = []
    cflag = []

    # print len(cnts1)
    for c in cnts1:
        # if cv2.contourArea(c) >threshArea:
        # cv2.drawContours(img, [c], -1, (0, 0, 255), 2)
        if 1:
            approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
            if len(approx)<10 and len(approx)>2:
                x_,y_,w_,h_  = cv2.boundingRect(c)
                
                if(aspectRatio(w_,h_) == True and h_ < 0.95*hi and w_ < 0.95*wi):
                    
                    cont.append([c])
                    x.append(x_)
                    y.append(y_)
                    h.append(h_)
                    w.append(w_)
                    cflag.append("1")

    for i in range(len(x)):
        if(cflag[i]==0):
            continue
        x_,y_,w_,h_ = x[i],y[i],w[i],h[i]
        for j in range(len(x)):
            if j==i:
                continue
            if cflag[j] == 0:
                continue
            if x_>=x[j] and y_>=y[j] and (x_+w_)<=(x[j]+w[j]) and (y_+h_)<=(y[j]+h[j]):
                cflag[i]="0"
    # print"r"
    # print len(cflag)
    for i in range(len(cflag)): 
        if(cflag[i]=="0"):
            continue
        else:
            # print "s"
            # graph = img[y[i]:y[i]+h[i],x[i]:x[i]+w[i]]
            # cv2.imwrite("test.png",graph)
            return int(x[i]),int(x[i]+w[i]),int(y[i]),int(y[i]+h[i])



# f = raw_input()
# findaxis(cv2.imread(f))