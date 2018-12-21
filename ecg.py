# encoding: utf-8
# Import packages

import neurokit as nk
import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QMainWindow,QApplication

class ECGData():
    def __init__(self):
        # Download data
        self.df = pd.read_csv("bio_100Hz.csv")
        
    def getData(self, start=0, end=400):
        return self.df.loc[start: end,['ECG']]

class Figure_ECG(FigureCanvas):   # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplot                                          lib的关键

    def __init__(self, parent=None, width=11, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure

        FigureCanvas.__init__(self, fig) # 初始化父类
        self.setParent(parent)

        self.axes = fig.add_subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法

    def test(self):
        # 打开交互模式
        plt.ion()

        for i in range(100):
            # 清除原有图像
            plt.cla()
            
            x = [1 + i,2,3,4,5,6,7,8,9]
            y = [23,21,32,13,3,132,13,3,1]
            self.axes.plot(x, y)

            plt.pause(0.1)

            # 关闭交互模式
            plt.ioff()
            # 显示图形
            plt.show()
