from PyQt5.QtGui import QPixmap,QIcon
import sys
import os
from PyQt5.QtWidgets import QMainWindow,QApplication,QGraphicsPixmapItem,QGraphicsScene,QGraphicsItem,QFileDialog,QMessageBox
from PyQt5.QtCore import QStringListModel
from main_win import Ui_MainWindow

class MyQWidget(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyQWidget,self).__init__(parent)
        self.UI()

    def UI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

def main():
    app = QApplication(sys.argv)
    w = MyQWidget()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()