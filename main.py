# encoding: utf-8
 
import sys, random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QApplication)


import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
# Uncomment this line before running, it breaks sphinx-gallery builds
# from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QMainWindow,QApplication

# project module
from ecg import ECGData
 
class MainWindow(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self)
        self.setWindowTitle('心臟電擊器模擬器')
        # ECG = displayECG()
        ECG = MyDynamicMplCanvas(self, width=5, height=4, dpi=100)
        toolBoxUP = controlToolBoxUP()
        toolBoxDown = controlToolBoxDown()
         
        grid = QGridLayout()
        vbox = QVBoxLayout()
        
        grid.addWidget(toolBoxUP, 1, 0)
        grid.addWidget(ECG, 2, 0, 3, 1)
        grid.addWidget(toolBoxDown, 5, 0)
    
        self.setLayout(grid)
        self.resize(480,320)
        
class controlToolBoxUP(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self)
        
        hbox = QHBoxLayout()
        A1 = QPushButton('A1', self)
        A1.setCheckable(True)
        A2 = QPushButton('A2', self)
        A2.setCheckable(True)       
        A3 = QPushButton('A3', self)
        A3.setCheckable(True)
        A4 = QPushButton('A4', self)
        A4.setCheckable(True)
        
        hbox.addWidget(A1)
        hbox.addWidget(A2)
        hbox.addWidget(A3)
        hbox.addWidget(A4)
        
        self.setLayout(hbox)
        
class controlToolBoxDown(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self)
        
        hbox = QHBoxLayout()
        B1 = QPushButton('B1', self)
        B1.setCheckable(True)
        B2 = QPushButton('B2', self)
        B2.setCheckable(True)        
        B3 = QPushButton('B3', self)
        B3.setCheckable(True)
        B4 = QPushButton('B4', self)
        B4.setCheckable(True)
        
        hbox.addWidget(B1)
        hbox.addWidget(B2)
        hbox.addWidget(B3)
        hbox.addWidget(B4)
        
        self.setLayout(hbox)

# 心電圖
class displayECG(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self)
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.resize(350,250)
        
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.drawBezierCurve(qp)
        qp.end()
        
    def drawBezierCurve(self, qp):

        path = QPainterPath()

# 心跳數
class displayBPM(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self)

# 動圖(testing)
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                    QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        self.MaxPoint = 400
        self.position = 0
        self.spaceWidth = 30

        self.dataPos = 0

        self.ecgData = ECGData()

        self.data = self.ecgData.getData(self.dataPos, self.MaxPoint).values
        
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(100)



    def compute_initial_figure(self):
        # 初始值，歸零
        l = [1 for i in range(0, self.MaxPoint)]
        self.axes.axis('off')
        self.axes.plot(l, l, 'r')
        pass

    def update_figure(self):

        l = [i for i in range(0, self.MaxPoint+1)]
        # cursor
        d = self.ecgData.getData(self.dataPos, self.dataPos + self.spaceWidth + 1).values

        for i in range(self.position, self.position + self.spaceWidth):
            self.data[(self.dataPos+i-self.position)%self.MaxPoint][0] = d[(i-self.position)%self.MaxPoint][0]
            l[i%self.MaxPoint] = None
        self.dataPos += 10
        self.position += 10
        self.position %= self.MaxPoint
        
        l[0] = 0
        l[self.MaxPoint] = self.MaxPoint
        
        self.axes.cla()
        self.axes.axis('off')
        self.axes.set_ylim((0, self.MaxPoint))
        self.axes.set_ylim((-0.5, 0.5))
        
        self.axes.plot(l, self.data, 'r')
        self.draw()

app = QApplication(sys.argv)
qb = MainWindow()
qb.show()
sys.exit(app.exec_())
