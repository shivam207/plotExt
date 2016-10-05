import xml.etree.ElementTree
from bs4 import BeautifulSoup
e = xml.etree.ElementTree.parse('out.xml').getroot()

import script
f = open('out.xml','r')
data=f.read()

soup = BeautifulSoup(data)
#print soup.prettify()
rect=[]
for i in soup.find_all('span',{'class':'ocrx_word'}) :
		h= i.get('title').split(' ')
		if(i.text.strip(" ")==""):
			continue
		k= h[1:5]
		k[-1]=k[-1][:-1]
		k=[int(x) for x in k]
		rect.append(k)
		print k,i.text,len(i.text)
script.draw_rectangles("graph.png",rect)


#print e
#for atype in e.findall('div',{'class':'ocr_page'}):
#    print(atype)