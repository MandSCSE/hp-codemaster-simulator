# encoding: utf-8
 
import sys
import  enum
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QApplication)


import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
# Uncomment this line before running, it breaks sphinx-gallery builds
# from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# project module
from ecg import ECGData
# from audio import audio
 
class MainWindow(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self)
        self.setWindowTitle('心臟電擊器模擬器')
        # ECG = displayECG()
        ECG = MyDynamicMplCanvas(self, width=5, height=4, dpi=100)
        toolBoxUP = controlToolBoxUP()
        toolBoxUP.setECG(ECG)
        toolBoxDown = controlToolBoxDown()
         
        grid = QGridLayout()
        
        grid.addWidget(toolBoxUP, 1, 0)
        grid.addWidget(ECG, 2, 0, 3, 1)
        grid.addWidget(toolBoxDown, 5, 0)
    
        self.setLayout(grid)
        self.resize(480,320)
        
class controlToolBoxUP(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self)
        
        hbox = QHBoxLayout()
        A1 = QPushButton('A1 stop', self)
        A1.clicked.connect(self.A1Clicked) 
        
        A2 = QPushButton('A2 resume', self)
        A2.clicked.connect(self.A2Clicked) 
        
        A3 = QPushButton('A3', self)
        A4 = QPushButton('A4', self)
        
        hbox.addWidget(A1)
        hbox.addWidget(A2)
        hbox.addWidget(A3)
        hbox.addWidget(A4)
        
        self.setLayout(hbox)
    def A1Clicked(self):
        self.ECG.setState(ECGCanvasState.STOP)
    def A2Clicked(self):
        self.ECG.setState(ECGCanvasState.NORMAL_DATA)
    def setECG(self,  ecg):
        self.ECG  = ecg
        
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
        

# 心跳數
class displayBPM(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self)
        
class ECGCanvasState(enum.IntEnum):
    STOP = 1
    NORMAL_DATA = 2

# 動圖(testing)
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # background color : #444444 (black)
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True, facecolor="#444444")
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
        self.MaxPoint = 420
        self.position = 0
        self.spaceWidth = 30
        self.dataPos = 0
        self.ecgData = ECGData()
        self.currentState = ECGCanvasState.NORMAL_DATA
        
        #self.currentState = ECGCanvasState.STOP

        self.data = self.ecgData.getData(self.dataPos, self.MaxPoint).values
        
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(100)
        
    def setState(self,  state):
        self.currentState = state;
        
    def update_ECGData(self):
        d = self.ecgData.getData(self.dataPos, self.dataPos + self.spaceWidth + 1).values
        for i in range(self.position, self.position + self.spaceWidth):
            self.data[(self.dataPos+i-self.position)%self.MaxPoint][0] = d[(i-self.position)%self.MaxPoint][0]
        self.dataPos += 10
        
    def clear_display(self):
        for i in range(self.position, self.position + self.spaceWidth):
            self.data[(self.dataPos+i-self.position)%self.MaxPoint][0] = 0
        self.dataPos += 10
        
    def update_figure(self):

        l = [i for i in range(0, self.MaxPoint+1)]
        
        # cursor
        for i in range(self.position, self.position + self.spaceWidth):
            l[i%self.MaxPoint] = None
       
        self.position += 10
        self.position %= self.MaxPoint
        
        li = {
            ECGCanvasState.STOP : self.clear_display,
            ECGCanvasState.NORMAL_DATA : self.update_ECGData
        }
        switch = li[self.currentState]
        switch()
        
        # 音效
        #audio.beep()
        
        # 使圖片不會左右亂跳
        l[0] = 0
        l[self.MaxPoint] = self.MaxPoint
        
        self.axes.cla()
        # 移除標籤
        self.axes.axis('off')
        self.axes.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off', labeltop='off', labelright='off', labelbottom='off')
        
        # 使繪製的圖比例不會跑掉
        self.axes.set_ylim((0, self.MaxPoint))
        self.axes.set_ylim((-0.5, 0.5))
        
        #hide_labels(self, self.axes)

        # line color : #ffff00 (yellow)
        self.axes.plot(l, self.data, color='#ffff00')
        self.draw()

app = QApplication(sys.argv)
qb = MainWindow()
qb.show()
sys.exit(app.exec_())
