import write_to_pdf
import numpy as np
a=np.zeros((80,10))
b=np.zeros((50,5))
ab=np.zeros((10,15))

img='a.jpg'

c=write_to_pdf.createpdf('newpdf.pdf')

write_to_pdf.pdfoutput(c,a)
write_to_pdf.pdfoutput(c,b)
write_to_pdf.pdfoutput(c,a)
write_to_pdf.pdfoutput(c,ab)
