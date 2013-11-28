import sys
from PyQt4 import QtGui


class Example(QtGui.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setFixedSize(1024, 768)
        self.setWindowTitle('Data analysis')
        self.show()


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
