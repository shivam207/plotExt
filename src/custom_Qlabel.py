from PyQt4.QtGui import *
from PyQt4.QtCore import *

class customLabel(QLabel):
    btnReleased=pyqtSignal()
    def __init__(self, parent = None):
    
        QLabel.__init__(self, parent)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.isEnabled = False
        self.currentQRect=QRect()
        
    
    def mousePressEvent(self, event):
        if self.isEnabled:
            if event.button() == Qt.LeftButton:

                self.origin = QPoint(event.pos())
                self.rubberBand.setGeometry(QRect(self.origin, QSize()))
                self.rubberBand.show()
    
    def mouseMoveEvent(self, event):
        if self.isEnabled:
            if not self.origin.isNull():
                self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
    
    def mouseReleaseEvent(self, event):
        if self.isEnabled:
            if event.button() == Qt.LeftButton:
                self.rubberBand.hide()
                self.currentQRect = self.rubberBand.geometry()
                self.btnReleased.emit()
