from PyQt4 import QtCore, QtGui
import shutil
import sys, time
import os
import layout_gene
import qdarkstyle
import pdf_to_img
import write_to_pdf
from pdf_to_img import ImageThread, ResultObj
from multiprocessing import Pool
from PyQt4.QtCore import *
from graphextract_returnArray1 import GraphThread, ReturnObj
import image_class
import numpy as np
#import image_class

import cv2

class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.btn_ok=QtGui.QPushButton("OK")
        #self.buttonBox.setStandardButtons(btn_ok)
        #self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.btn_ok.clicked.connect(self.close)
        self.setWindowTitle("Error in legend detection!!!!")
        self.textBrowser = QtGui.QTextBrowser(self)
        self.textBrowser.append("Enter the number of plots in the current graphs\nClick the X1,X2,Y1,Y2 buttons and mark consecutive markings on the axes. Also enter their corresponding values in the adjacentboxes")


        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.btn_ok)

class plotThread(QtCore.QThread):

    table_completed = QtCore.pyqtSignal(object)
    automatic_failed = QtCore.pyqtSignal(object)
    def __init__(self, plot, index,manual=False):
        QtCore.QThread.__init__(self)
        print("iniiiiiiiiiiiiit")
        self.plot=plot
        self.index=index
        self.manual=manual
        print(self.plot,self.index,self.manual)

    def run(self):
        print("starting")
        if self.manual:
            print("starting")
            self.plot.run_manual()
        else:
            res = self.plot.run()
            if res == -1:
                self.automatic_failed.emit(self.index)
                return

        table=self.plot.table
        print '^^^^^^^^^^$$$$$$######^^^^^^^^^'
        print table
        self.table_completed.emit(self.index)



        

class popup(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.label=QtGui.QLabel()

class Example(QtGui.QMainWindow, layout_gene.Ui_MainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("PlotExt v1.0")
        self.cluster_label=QtGui.QLabel()
        self.cluster_label.setText("Enter the number of colours")
        self.clusters=QtGui.QLineEdit()
        self.horizontalLayout_6.addWidget(self.cluster_label)
        self.horizontalLayout_6.addWidget(self.clusters)
        #self.tables=[]
        self.pdfSelectBtn.clicked.connect(self.openfile)
        self.pdfSelectBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_x1.clicked.connect(self.Coordinate)
        self.btn_x2.clicked.connect(self.Coordinate)
        self.btn_y1.clicked.connect(self.Coordinate)
        self.btn_y2.clicked.connect(self.Coordinate)
        self.proceed_btn.clicked.connect(self.proceed_fun)
        self.delete_btn.clicked.connect(self.delete_item)
        self.selectAreaBtn.clicked.connect(self.enableDrag)
        self.pdflistWidget.itemClicked.connect(self.pdfItem_click)
        self.graphlistWidget.itemClicked.connect(self.graphItem_click)
        
        self.display_item.btnReleased.connect(self.manualAddGraph)
        self.runBtn.clicked.connect(self.getGraphs)
        self.display_item.resizeEvent = self.onResize
        self.manual.clicked.connect(self.manual_fun)
        self.contin.clicked.connect(self.getTables)
        
        self.graphlistWidget.itemSelectionChanged.connect(self.change_selected_item)
        self.pdflistWidget.itemSelectionChanged.connect(self.change_selected_pdf_item)
        self.savetable.clicked.connect(self.download_table)
        self.plotShowBtn.clicked.connect(self.show_plot)
        self.refresh_gui()
        
        self.btmx=[]
        self.btmy=[]
        self.btmpt=[]
        self.dialogTextBrowser = MyDialog(self)
        #self.dialogTextBrowser.exec_()

    def closeEvent(self, event):
        result = QtGui.QMessageBox.question(self,"Confirm Exit...","Are you sure you want to exit ?",QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
        event.ignore()

        if result==QtGui.QMessageBox.Yes:
            shutil.rmtree(image_class.Graph.outer_dir,ignore_errors=True)
            event.accept()

    def show_plot(self):
        items=self.graphlistWidget.selectedItems()
        item=items[0]
        ind = self.graphlistWidget.row(item)
        working_dir = self.plots[ind].working_dir
        img=cv2.imread(os.path.join(working_dir,'plot_from_data.png'))
        cv2.imshow('plot',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def download_table(self):
        '''still to add
        name of the plot
        names from legend in an array of strings
        call this function in a loop for all the generated graphs

        '''
        export_dialog = QtGui.QFileDialog()
        export_dialog.setWindowTitle('Save PDF')
        export_dialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        export_dialog.setNameFilter('PDF files (*.pdf)')
        export_dialog.setDefaultSuffix('pdf')
        export_dialog.show()
        #z=export_dialog.selectedFiles()
        tables=[]
        images=[]
        if export_dialog.exec_() == QtGui.QFileDialog.Accepted:
            location=export_dialog.selectedFiles()[0]
            print location
            c=write_to_pdf.createpdf(str(location))
            colours = []
            for i in range(len(self.plots)):
                tables.append(self.plots[i].table)
                images.append(self.plots[i].outer_image_file)
                new_color_list = []
                for color in self.plots[i].legend:
                    new_color_list.append(tuple(color[1]))
                colours.append(new_color_list)
            print(tables)
            print(colours)
            write_to_pdf.pdfoutput(c,tables,images,colours)
            # print(export_dialog.selectedFiles()[0])
            #self.x = QtGui.QFileDialog.getOpenFileName(self, 'OpenFile', filter='*pdf')
        # c=write_to_pdf.createpdf(xz)
        #write_to_pdf.pdfoutput(c,self.table)
        # write_to_pdf.pdfoutput(c,self.plots[0].table,self.plots[0].outer_image_file)


    def change_selected_pdf_item(self):
        items=self.pdflistWidget.selectedItems()
        item=items[0]
        self.pdfItem_click(item)
    def change_selected_item(self):
        items=self.graphlistWidget.selectedItems()
        item=items[0]
        self.graphItem_click(item)
    def getTables(self):

        # self.tables = [0 for plot in self.plots ]
        self.selectAreaBtn.hide()
        self.contin.setEnabled(False)
        self.gif.show()
        self.tableWidget.hide()
        #movie=QtGui.QMovie("loading.gif")
        movie=QtGui.QMovie("loading4.gif")
        self.gif.setMovie(movie)
        movie.start()
        
        for i in range(len(self.plots)):
            self.gif_check.append(0)
        self.thread_per_plot=[]
        for plot in self.plots:
            temp_thread=plotThread(plot,self.plots.index(plot))
            temp_thread.table_completed.connect(self.on_table_completion)
            temp_thread.automatic_failed.connect(self.automatic_failed)
            self.thread_per_plot.append(temp_thread)
            temp_thread.start()



    def automatic_failed(self,index):
        items=self.graphlistWidget.selectedItems()
        if(len(items)==0):
            return
        item = items[0]
        self.graphItem_click(item)


    def on_table_completion(self, index):
        #self.tables[index]=table
        
        self.gif_check[index]=1
        print '())()()())()^^^^^^()()()()()',self.gif_check
        items=self.graphlistWidget.selectedItems()
        if len(items)!=0:
            self.graphItem_click(items[0])

        self.contin.setEnabled(True)
        #print self.tables

        '''def table_progress(self, result):
        print '$$$$$$$'
        print result.table
        self.tableWidget.setColumnCount(len(result.table)) #rows and columns of table
        self.tableWidget.setRowCount(len(result.table[0]))
        for row in range(len(result.table[0])): # add items from array to QTableWidget
            for column in range(len(result.table)):
                #item = self.array[0] # each item is a QTableWidgetItem
                # add the QTableWidgetItem to QTableWidget, but exception thrown
                self.tableWidget.setItem(row, column, QtGui.QTableWidgetItem(result.table[column][row])) '''
                        
                

    def manual_fun(self):
        self.btn_x1.show()
        self.btn_x2.show()
        self.btn_y1.show()
        self.btn_y2.show()
        # self.contin.hide()
        self.manual.hide()
        self.lineEdit.show()
        self.lineEdit_2.show()
        self.lineEdit_3.show()
        self.lineEdit_4.show()
        self.label_2.show()
        self.proceed_btn.show()
        self.clusters.show()
        self.cluster_label.show()
        # self.selectAreaBtn.show()
        #self.tableWidget.hide()
    def onResize(self, event):
        items=self.pdflistWidget.selectedItems()
        if len(items)==0:
            return
        self.pdfItem_click(items[0])
    def removePlot(self,filename):
        print(self.plot_dic)
        print(self.plots)
        plot = (self.plot_dic[str(filename)])
        self.plots.remove(plot)
        print(self.plots)

    '''def changeEvent(self, event):
        QtGui.QMainWindow.changeEvent(self, event)
        if event.type() == QtCore.QEvent.WindowStateChange:
        #print QtCore.Qt.WindowFullScreen
            if self.windowState() & QtCore.Qt.WindowMaximized:
                print 'a'

                items=self.pdflistWidget.selectedItems()
                print items
                self.pdfItem_click(items[0])
            elif event.oldState() & QtCore.Qt.WindowMaximized:
                items=self.pdflistWidget.selectedItems()
                print items, 'b'
                self.pdfItem_click(items[0])'''

    
    #def loadingFinished(self):

    def progress_of_extract(self, result):
        images=result.list1
        files=result.list2
        inner_image_params = result.inner_list
        # images.append(result.list1)
        # files.append(result.list2)
        print result.page_no
        print result.list2
        print result.inner_list
        print "**************"
        new_list=[]
        for j in range(len(images)):
            plot = image_class.Graph(images[j],files[j],inner_image_params[j])
            #new_list.append(image_class.Graph(images[j],files[j]))
            #print new_list
            self.addGraphItem(plot)
            self.plot_dic[plot.outer_image_file]=plot
            self.plots.append(plot)
        self.progressBar.setValue(self.progressBar.value()+1)
        self.statusbar.showMessage('Extracting Graphs from '+str(result.page_no+2)+' page ...')

        print self.plots
    def finished_extracting(self, result):
        item = self.graphlistWidget.item(0)
        self.graphlistWidget.setItemSelected(item,True)
        self.statusbar.clearMessage()
        self.progressBar.hide()
        self.runBtn.hide()
        self.selectAreaBtn.show()
        self.contin.show()

    def getGraphs(self):
        self.graphlistWidget.clear()

        self.gthread = GraphThread(self.listOfFiles, self.progress_of_extract, self.finished_extracting)
        self.gthread.start()
        self.progressBar.show()
        self.progressBar.setValue(0)
        self.statusbar.showMessage('Extracting Graphs from 1 page ...')

        '''images,files = graphextract_returnArray1.PlotExtractor(self.listOfFiles).graphextract()
        for i in range(len(images)):
            new_list=[]
            print i,images[i]
            for j in range(len(images[i])):
                new_list.append(image_class.Graph(images[i][j],files[i][j]))
                self.addGraphItem(new_list[-1])
                self.plot_dic[new_list[-1].outer_image_file]=new_list[-1]
            self.plots.append(new_list)

        print self.plots'''


    def addGraphItem(self, plot):
        item=QtGui.QListWidgetItem(QtGui.QIcon(plot.outer_image_file), QString(plot.outer_image_file))
        self.graphlistWidget.addItem(item)

    def manualAddGraph(self):
        self.selectAreaBtn.setChecked(False)
        self.display_item.isEnabled=False
        rect=self.display_item.currentQRect
        pdf_item=self.pdflistWidget.selectedItems()
        pg_no=pdf_item[0].text()   #x stores the page no of pdf file currently selected
        self.graph_per_page[int(pg_no)-1]+=1


        filename = str(self.pdf_name)+str(int(pg_no)-1)+'.png'
        working_dir='plot_dir'
        filename= os.path.join(working_dir,filename)
        img = cv2.imread(filename)
        height, width = img.shape[:2]     # dimensions of original image
        #size of pixmap
        h=self.display_item.pixmap().height()
        w=self.display_item.pixmap().width()        
        #multiplying ratio to convert pixels of pixmap to original image
        y_ratio=float(height)/h            
        x_ratio=float(width)/w

        top_left=QtCore.QPoint(rect.topLeft())
        bottom_right=QtCore.QPoint(rect.bottomRight())
        xstart=int(top_left.x()*x_ratio)
        ystart=int(top_left.y()*y_ratio)
        xend=int(bottom_right.x()*x_ratio)
        yend=int(bottom_right.y()*y_ratio)
        graph = img[int(ystart):int(yend),int(xstart):int(xend)]
        p='graph'+str(pg_no)+str(self.graph_per_page[int(pg_no)-1])+'.png'  
        p=os.path.join(working_dir,p)
        cv2.imwrite(p, graph)
        item=QtGui.QListWidgetItem(QtGui.QIcon(p),QtCore.QString(p))
        self.graphlistWidget.addItem(item)
        plot = image_class.Graph(graph,p)
        self.plots.append(plot)
        self.plot_dic[p]=plot
        #print self.plots



    def enableDrag(self):
        self.display_item.isEnabled=True
        self.display_item.setCursor(QtCore.Qt.CrossCursor)
        

    def proceed_fun(self):
        #self.x1.setReadOnly(True)mg=cv2.imread("test.pdf0.jpg")
        
        #self.x2.setReadOnly(True)
        #self.y1.setReadOnly(True)
        #self.y2.setReadOnly(True)
        self.tableWidget.hide()
        self.manual_par[0][1]=float(self.lineEdit.text())
        self.manual_par[1][1]=float(self.lineEdit_2.text())
        self.manual_par[2][1]=float(self.lineEdit_3.text())
        self.manual_par[3][1]=float(self.lineEdit_4.text())
        self.manual_par[4] = float(self.clusters.text())
        items=self.graphlistWidget.selectedItems()
        item = items[0]
        plot = self.plot_dic[str(item.text())]

        h=self.display_item.pixmap().height()
        w=self.display_item.pixmap().width() 
        pdf_item=self.pdflistWidget.selectedItems()
        pg_no=pdf_item[0].text()   #x stores the page no of pdf file currently selected
        

        img = cv2.imread(plot.outer_image_file)
        


        height, width = img.shape[:2] 

        t1=self.manual_par[0][0]*float(height)/h
        t2=self.manual_par[1][0]*float(height)/h
        t3=self.manual_par[2][0]*float(width)/w
        t4=self.manual_par[3][0]*float(width)/w

        self.manual_par[0][0]=int(t1)
        self.manual_par[1][0]=int(t2)
        self.manual_par[2][0]=int(t3)
        self.manual_par[3][0]=int(t4)

        
        plot.set_manual(self.manual_par)
        print("proceeeeeeeeeeeeeeeeeeeeeeeeeeed")
        self.thread_per_plot2=[]
        temp_thread=plotThread(plot,self.plots.index(plot),True)
        self.thread_per_plot2.append(temp_thread)
        temp_thread.table_completed.connect(self.on_table_completion)
        print("before starting")
        temp_thread.start()
        self.gif.show()


        print self.manual_par

    def delete_item(self):
        items=self.graphlistWidget.selectedItems()
        for item in items:
            self.graphlistWidget.takeItem(self.graphlistWidget.row(item))
            self.deletedItems.append(item)
            self.removePlot(item.text())
        '''to change the display of custom Qlabel after delleting an item'''
        items=self.graphlistWidget.selectedItems()
        item=items[0]

        self.display_item.setPixmap(QtGui.QPixmap(item.text()).scaled(self.display_item.size(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        
    
    def Coordinate(self):
        def getPos(event):
            x = event.pos().x()
            y = event.pos().y()
            lx=[]    
            ly=[]
            sender.setChecked(False)
            if sender.text()=='X1':
                self.axes[0][0]=x
                self.axes[0][1]=y
                self.manual_par[0][0]=self.axes[0][0]
                print 'X1',self.axes[0]
            elif sender.text()=='X2':
                self.axes[1][0]=x
                self.axes[1][1]=y
                self.manual_par[1][0]=self.axes[1][0]
                y_x2=y
                print 'X2',self.axes[1]
            elif sender.text()=='Y1':
                self.axes[2][0]=x
                self.axes[2][1]=y
                self.manual_par[2][0]=self.axes[2][1]
                x_y1=x                
                print 'Y1',self.axes[2]
            else:
                self.axes[3][0]=x
                self.axes[3][1]=y
                self.manual_par[3][0]=self.axes[3][1]
                x_y2=x
                print 'Y2',self.axes[3]
            print "manual_par is",
            

            print self.manual_par 
            self.display_item.setCursor(QtCore.Qt.ArrowCursor)
            self.display_item.mousePressEvent=self.mousePressEvent
        sender=self.sender()
        if sender.isChecked():
            self.display_item.setCursor(QtCore.Qt.CrossCursor)
            self.display_item.mousePressEvent=getPos



    def graphItem_click(self, item):

        ind=self.graphlistWidget.row(item)
        if(self.plots[ind].legend_failed):
            #popup
            self.gif.hide()
            self.dialogTextBrowser.exec_()
            #hide automatic
            self.contin.hide()

            #display manual stuff
            #self.manual.show()
            self.btn_x1.show()
            self.btn_x2.show()
            self.btn_y1.show()
            self.btn_y2.show()
            self.lineEdit.show()
            self.lineEdit_2.show()
            self.lineEdit_3.show()
            self.lineEdit_4.show()
            self.proceed_btn.show()
            self.clusters.show()
            self.cluster_label.show()
        else:
            self.manual.hide()
            self.btn_x1.hide()
            self.btn_x2.hide()
            self.btn_y1.hide()
            self.btn_y2.hide()
            self.lineEdit.hide()
            self.lineEdit_2.hide()
            self.lineEdit_3.hide()
            self.lineEdit_4.hide()
            self.proceed_btn.hide()
            self.clusters.hide()
            self.cluster_label.hide()


        self.display_item.setPixmap(QtGui.QPixmap(item.text()).scaled(self.display_item.size(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        ind=self.graphlistWidget.row(item)
        self.selectAreaBtn.setEnabled(False)
        print ind
        print (self.plots)
        if(not hasattr( self.plots[ind],'table')):
            if len(self.gif_check)==0:
                return
            if self.gif_check[ind]==0 and not self.plots[ind].legend_failed:
                self.gif.show()
                self.tableWidget.hide()
                movie=QtGui.QMovie("loading4.gif")
                self.gif.setMovie(movie)
                movie.start()
                self.plotShowBtn.hide()
                self.manual.hide()
        # if self.gif_check[ind]==0:
        #   print '{{{{&&&******&&&'
        #   self.gif.show()
           #  self.tableWidget.hide()
           #  movie=QtGui.QMovie("loading.gif")
           #  self.gif.setMovie(movie)
           #  movie.start()
        if self.gif_check[ind]==1:
            # print '^^^*****#####^^^^'
            self.gif.hide()
            self.tableWidget.show()
            self.plotShowBtn.show()
            
            self.tableWidget.setColumnCount(len(self.plots[ind].table)) #rows and columns of table
            self.tableWidget.setRowCount(len(self.plots[ind].table[0])+1)
            itm=QtGui.QTableWidgetItem('X')
            self.tableWidget.setHorizontalHeaderItem(0,itm)
            # print "hello"
            for i in range(1,len(self.plots[ind].table)):
                itm1=QtGui.QTableWidgetItem('Y'+str(i))
                # b=self.plots[ind].legend[i-1][1][0]
                # g=self.plots[ind].legend[i-1][1][1]
                # r=self.plots[ind].legend[i-1][1][2]
                # print b, g, r
                # itm1.setTextColor(QtGui.QColor(r,g,b))
                # # brush = QtGui.QBrush(QtGui.QColor(r, g, b))
                # # brush.setStyle(QtCore.Qt.SolidPattern)
                # # itm.setBackground(brush)
                # self.tableWidget.setHorizontalHeaderItem(i,itm1)
                # print self.tableWidget.horizontalHeaderItem(i)
                # brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
                # brush.setStyle(QtCore.Qt.SolidPattern)
                # self.tableWidget.horizontalHeaderItem(i).setBackground(brush)
            # print "hellllllllo"
            print(self.plots[ind].legend)
            print(len(self.plots[ind].legend))
            print(len(self.plots[ind].table))
            for i in range(1,len(self.plots[ind].table)):
                print(i)
                b=self.plots[ind].legend[i-1][1][0]
                g=self.plots[ind].legend[i-1][1][1]
                r=self.plots[ind].legend[i-1][1][2]
                print r,g,b
                self.tableWidget.setItem(0, i, QtGui.QTableWidgetItem(" "))
                self.tableWidget.item(0, i).setBackground(QtGui.QColor(r,g,b))

            for column in range(len(self.plots[ind].table)): # add items from array to QTableWidget
                for row in range(len(self.plots[ind].table[0])):
                    self.tableWidget.setItem(row+1, column, QtGui.QTableWidgetItem(self.plots[ind].table[column][row]))
                    #self.tableWidget.item(row, column).setBackground(QtGui.QColor(self.plots[ind].legend[i-1][1][2],100,150))
            count=0
            # print "hellolllllllllllll"
            for i in range(len(self.plots)):
                if self.gif_check[i]==1:
                    count+=1
            if count==len(self.plots):
                self.savetable.show()
                # print '&&&&&&&&&&&&&&&&&&'
                # for i in range(len(self.plots[ind].table)-1):
                #     print self.plots[ind].legend[i][1]
                self.contin.hide()
            self.manual.show()
            
    def pdfItem_click(self, item):
        self.selectAreaBtn.setEnabled(True)
        working_dir='plot_dir'
        loc=self.pdf_name+str(int(item.text())-1)+"new.png"
        loc = os.path.join(working_dir,str(loc))
        self.display_item.setPixmap(QtGui.QPixmap(loc).scaled(self.display_item.size(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))

    def loadingFinished(self, result):
        self.statusbar.clearMessage()
        self.runBtn.setEnabled(True)
        self.btn_x1.setEnabled(True)
        self.btn_x2.setEnabled(True)
        self.btn_y1.setEnabled(True)
        self.btn_y2.setEnabled(True)
        self.proceed_btn.setEnabled(True)
        self.pdfSelectBtn.setEnabled(True)
        self.progressBar.hide()

    def progress_handle(self, result):
        
        working_dir = 'plot_dir'
        self.statusbar.showMessage(QString(' Loading '+str(result.val+2)+' page ....'))
        w=self.pdf_name+str(result.val)+"new.png"
        w = os.path.join(working_dir,str(w))
            
        self.item=QtGui.QListWidgetItem(QtGui.QIcon(w),QtCore.QString(str(result.val+1)))
        self.pdflistWidget.addItem(self.item)

        self.graph_per_page.append(0)

        w=self.pdf_name+str(result.val)+".png"
        w = os.path.join(working_dir,str(w))
        self.listOfFiles.append(str(w))

        if result.val==0:
            self.progressBar.setMaximum(result.numPages)
            self.progressBar.setValue(1)
            self.pdflistWidget.setItemSelected(self.pdflistWidget.item(0), True)
            file_name = self.pdf_name+"0new.png"
            file_name = os.path.join(working_dir,str(file_name))
            self.display_item.setPixmap(QtGui.QPixmap(file_name).scaled(self.display_item.size(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        else:
            self.progressBar.setValue(self.progressBar.value()+1)

    def refresh_gui(self):
        self.manual_par=[[0,0],[0,0],[0,0],[0,0],0]
        self.axes=[[0, 0], [0, 0], [0,0], [0,0]]
        self.axes_values=['','','','']
        self.plots=[]
        self.listOfFiles = []
        self.deletedItems=[]         # stores the deleted graphlistWidget items
        self.graph_per_page=[]
        self.plot_dic={}
        """disabling buttons before a pdf is chosen"""
        self.runBtn.setEnabled(False)
        self.btn_x1.setEnabled(False)
        self.btn_x2.setEnabled(False)
        self.btn_y1.setEnabled(False)
        self.btn_y2.setEnabled(False)
        self.proceed_btn.setEnabled(False)
        self.progressBar.hide()
        self.manual.hide()
        self.contin.hide()
        self.selectAreaBtn.hide()
        self.proceed_btn.hide()
        self.btn_x1.hide()
        self.btn_y2.hide()
        self.btn_y1.hide()
        self.btn_x2.hide()
        self.lineEdit.hide()
        self.lineEdit_2.hide()
        self.lineEdit_3.hide()
        self.lineEdit_4.hide()
        self.graphlistWidget.clear()
        self.pdflistWidget.clear()
        self.tableWidget.clear()
        self.runBtn.show()
        self.display_item.setPixmap(QtGui.QPixmap(''))
        self.label_2.hide()
        self.cluster_label.hide()
        self.clusters.hide()
        self.plotShowBtn.hide()
        self.savetable.hide()
        self.gif.hide()
        self.gif_check=[]
        self.tableWidget.hide() 

    def openfile(self):

        self.x = QtGui.QFileDialog.getOpenFileName(self, 'OpenFile', filter='*pdf')
        self.pdf_name = os.path.basename(str(self.x))
    
        #self.x stores the address of the chosen pdf
        print self.x
        if self.x=="":      # No file is Chosen
            return
        self.refresh_gui()
        
        
        z=QtCore.QFileInfo(self.x)     #z stores only the file name
        self.pdfSelectBtn.setEnabled(False)
        self.progressBar.show()
        self.statusbar.showMessage(QString(' Loading '+'1'+' page ....'))
        self.ithread = ImageThread(self.x,"300", self.loadingFinished, self.progress_handle)
        self.ithread.start()

class MySplashScreen(QtGui.QSplashScreen):
    def __init__(self, animation, flags=None):
        # run event dispatching in another thread
        QtGui.QSplashScreen.__init__(self, QtGui.QPixmap())
        self.movie = QtGui.QMovie(animation)
        #self.connect(self.movie, QtCore.SIGNAL('frameChanged(int)'), QtCore.SLOT('onNextFrame()'))
        self.movie.frameChanged.connect(self.onNextFrame)
        self.movie.start()

    #@pyqtSlot()
    def onNextFrame(self):
        pixmap = self.movie.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())

def longInitialization(arg):
    time.sleep(arg)
    return 0

def main():
    app=QtGui.QApplication(sys.argv)
    splash=MySplashScreen('splash.gif')
    splash.show()
    app.processEvents()
    # for count in range(1, 100):
    #     splash.showMessage(splash.tr('Processing %1...').arg(count),
    #                        QtCore.Qt.AlignBottom+20, QtCore.Qt.black)
    #     QtGui.QApplication.processEvents()
    #     QtCore.QThread.msleep(15)
    app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    # this event loop is needed for dispatching of Qt events
    '''Note, that you need to run your initialization code in a separate
     thread, since the main thread should dispatch Qt events.'''
    initLoop = QtCore.QEventLoop()
    pool = Pool(processes=1)
    pool.apply_async(longInitialization, [2], callback=lambda exitCode: initLoop.exit(exitCode))
    initLoop.exec_()

    ex=Example()
    ex.show()
    splash.finish(ex)
    app.exec_()
    
if __name__=='__main__':
    main()
