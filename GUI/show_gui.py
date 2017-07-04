#! coding:utf-8
__author = 'steven{steven@nenyah.com}'
from PyQt5 import QtWidgets
from form import Ui_Form

class mywindow(QtWidgets.QWidget):
    def __init__(self):
        super(mywindow,self).__init__()
        self.new=Ui_Form()
        self.new.setupUi(self)

if __name__=="__main__":
    import sys

    app=QtWidgets.QApplication(sys.argv)
    myshow=mywindow()
    myshow.show()
    sys.exit(app.exec_())
