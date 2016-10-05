
import os
import sys
import Image
import xml.etree.ElementTree
from bs4 import BeautifulSoup

def parse(img):
    """
    Do OCR of the image, outputs hocr, converts hocr to xml and finally
    prints the exact rectangular coordinates of every OCR text
    """

	os.system("tesseract "+img+" out hocr")
	os.rename('out.hocr','out.xml')

	e = xml.etree.ElementTree.parse('out.xml').getroot()
	f = open('out.xml','r')
	data=f.read()
	soup = BeautifulSoup(data)

	for i in soup.find_all('span',{'class':'ocrx_word'}) :
			h= i.get('title').split(' ')
			if(i.text.strip(" ")==""):
				continue
			k= h[1:5]
			k[-1]=k[-1][:-1]
			k=[int(x) for x in k]
			#rect.append(k)
			print k,i.text,len(i.text)

if __name__ == '__main__':
	img=sys.argv[1]
	"""
	Takes an input image from command line whose OCR we want
	"""
	parse(img)