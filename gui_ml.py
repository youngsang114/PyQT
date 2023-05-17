from PyQt5.QtWidgets import *
import sys,pickle

from PyQt5 import uic, QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QWidget

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("./mainwindow.ui",self)
        self.show()

        self.Browse = self.findChild(QPushButton,"Browse")     # 등록하는 방법 self.findChild(객체,'이름')
        self.column_list = self.findChild(QListWidget,'column_list')

        self.Browse.clicked.connect(self.getCSV)              # clicked.connect(함수): 눌렀을때 어떤 행동을 할지

    def getCSV(self):
        self.column_list.clear()
        self.column_list.addItems(["브라우져",'브라우승','브라질'])



if __name__ == '__main__':        ## 파이썬에서 실행할때, 가장먼저 시키고 싶을때
    app=QApplication(sys.argv)
    window = UI()
    app.exec_()