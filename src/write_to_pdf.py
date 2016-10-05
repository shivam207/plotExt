#mine
#outside reprository
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch,cm
from reportlab.lib.utils import ImageReader
import numpy as np

width, height=A4
z=0

def createpdf(x):
	#Size of Canvas
	global z
	z=0	
	c=canvas.Canvas(x,pagesize=A4)
	return c

def pdfoutput(c,ans,img,clrs=None,plot=None,title=None):
	#Name of Output PDF
	global z
	global width
	global height
	# ar=[['0']*len(an)]*len(an[0])
	print clrs
	if plot==None:
		plot=["Plot %s"%(i+1) for i in range(len(ans))]
        print(plot)
	
	if len(ans)==len(img) and len(ans)==len(plot):
		for an in ans:
			ar=[['0' for x in range(len(an))] for x in range(len(an[0]))] 
	
			for e in xrange(len(an)):
				# f=0
				for f in xrange(len(an[e])):
					# print "an is "+an[e][f]+"at e,f"+str(e)+" "+str(f)
					ar[f][e]=an[e][f]
					# break
	
			for e in range(len(ar)):
				for f in range(len(ar[0])):
					if ar[e][f]!="--":
						ar[e][f]=str(round(float(ar[e][f]),4))

			try:
			    #New Page...
			    #c.translate(0,height)

			    #Image Print
			    im=ImageReader(img[z])
			    w=im.getSize()[0]
			    h=im.getSize()[1]
			    r=(width-2*cm)/w
			    w= width-2*cm
			    c.drawImage(im,(width-w)/2,height-(height+h*r)/2,w,r*h)
			    c.setFont("Times-Roman", 30)
			    c.drawCentredString(width/2,height-0.5*inch,"Input Page "+ str(z+1))
			    c.setFont("Times-Roman", 14)
			    #Save Page
			    c.showPage()
			except:
			    print ("can't add image")


			#New Page
			c.translate(0,height)
			c.setFont("Times-Roman", 30)
			c.drawCentredString(width/2,-.3*inch,"Output Page "+ str(z+1))
			c.setFont("Times-Roman",14)
			#Array to be printed
			W = width/(len(ar[0])+2)
			H = (height-inch)/(len(ar)+2)
			if H>.5*inch:
				H=.5*inch

			#Title of the Graph
			#c.drawString(width/3,-.9*inch,"Title of the Plot")
			c.drawCentredString(width/2, -.9*inch, plot[z])

			c.setFont("Times-Roman", max(16-.1*len(ar),6))
			fontsize=max(16-.1*len(ar),6)
			if len(ar[0])>6 and len(ar)<40:
				c.setFont("Times-Roman", 15-.5*len(ar[0]))
				fontsize=15-.5*len(ar[0])

			#Title of X and Y axes
			if title==None:
				title=['X Value']
				for i in xrange(len(ar[0])-1):
					title.append('Y ' + str(i+1) + " Value")
			for t in xrange(len(title)):
				if W/(len(title[t])*fontsize) < .55:
					maxtext=int(W/(fontsize*.55)) - 1
					title[t]=title[t].replace(title[t][maxtext:],"...")
			for i in xrange(len(ar[0])):
				if clrs!=None:	
					if i==0:
						c.setFillColorRGB(0,0,0)
					else :
						c.setFillColorRGB(clrs[z][i-1][2]/255.0,clrs[z][i-1][1]/255.0,clrs[z][i-1][0]/255.0)
				c.drawCentredString((i+1.5)*W,-inch-.7*H,title[i])
				c.setFillColorRGB(0,0,0)
			#Size of the Grid
			xlist=[]
			for i in xrange(len(ar[0])+1):
				xlist.append(W*(i+1))
			ylist=[]
			for i in xrange(len(ar)+2):
				ylist.append(-i*H-inch)
			#Creating the Grid
			c.grid(xlist, ylist)

			#Printing the Output Array
			for i in xrange(len(ar)):
				for j in xrange(len(ar[0])):
					c.drawCentredString((j+1.5)*W,-H*(1.7+i)-inch,ar[i][j])

			c.showPage()
			z=z+1
	else:
		print "Error: Length of each List (table, img, plot) must be same"

	#Save PDF
	c.save()
	#z=z+1

if __name__ == '__main__':
	cc=createpdf('testing.pdf')
	img=[]
	plot=[]
	for m in xrange(5):	
		img.append("a.jpg")
	for m in xrange(5):
		plot.append("table of a")
	
	#an=[[["--","13.2524145741","12.25"],["1.20","--","125.120214"]],[["--","13.2524145741","12.25"],["1.20","--","125.120214"]],[["--","13.2524145741","12.25"],["1.20","--","125.120214"]],[["--","13.2524145741","12.25"],["1.20","--","125.120214"]],[["--","13.2524145741","12.25"],["1.20","--","125.120214"]]]
	ar=np.zeros((5,10))
	an=[ar,ar,ar,ar,ar]
	clr=[(255,0,0),(0,255,0),(0,0,255),(0,255,255)]
	clrs=[]
	for m in xrange(5):	
		clrs.append(clr)

	pdfoutput(cc,an,img,clrs,plot)
