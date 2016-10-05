print "import custom_Qlabel"
with open('layout_outline.py') as f:
    lines = f.readlines()
    # print len(lines)
    count=0
    for line in lines:
    	line = line[:-1]
    	# count+=1
    	# if count==87:
    	# 	print line
    	if line=="        self.display_item = QtGui.QLabel(self.centralwidget)":
    		print "        self.display_item = custom_Qlabel.customLabel(self.centralwidget)"
    	else:
    		print line
