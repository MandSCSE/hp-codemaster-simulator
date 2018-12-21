import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QMainWindow,QApplication
import sys
import time

import neurokit as nk
import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt


class Figure_Canvas(FigureCanvas):   # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplot                                          lib的关键

    def __init__(self, parent=None, width=11, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure

        FigureCanvas.__init__(self, fig) # 初始化父类
        self.setParent(parent)

        self.axes = fig.add_subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法

    def test(self):

        for i in range(100):
            # 清除原有图像
            self.axes.cla()
            
            x = [1,2,3,4,5,6,7,8,9]
            y = [23 + i*10,21,32,13,3,132,13,3,1]
            self.axes.plot(x, y)
            time.sleep(0.01)

            self.draw_idle()

            # 显示图形
            self.axes.plot()


    def test2(self, a):
        self.axes.cla()
        x = [1,2,3,4,5,6,7,8,9]
        y = [13 + a,11 +a,22,3,3,32,443,3,1]
        self.axes.plot(x, y)

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
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
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

        
class Mytest(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle('My First App')
        self.setFixedSize(800, 600)
       
        # ===通过graphicview来显示图形
        self.graphicview = QtWidgets.QGraphicsView()  # 第一步，创建一个QGraphicsView
        self.graphicview.setObjectName("graphicview")

        self.dr = Figure_Canvas()
        #实例化一个FigureCanvas
        self.dr.test()  # 画图
        
        graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        graphicscene.addWidget(self.dr)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.graphicview.setScene(graphicscene)  # 第五步，把QGraphicsScene放入QGraphicsView
        self.graphicview.show()  # 最后，调用show方法呈现图形！Voila!!
        self.setCentralWidget(self.graphicview)
        self.graphicview.setFixedSize(800,600)

    def d_test(self):
        self.dr.test()

    def d_draw(self):
        for i in range(0, 10):
            self.dr.test2(i)
            time.sleep(0.5)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mytest=Mytest()


    mytest.show()

    mytest.d_test()
    #mytest.d_draw()
    app.exec_()


