import sys
import graph_mod
from PyQt4 import QtGui, QtCore


class DataAnalysis(QtGui.QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.cb1 = QtGui.QCheckBox('Solution')

        self.cb2 = QtGui.QCheckBox('Fitness function and median')

        self.button = QtGui.QPushButton('Generate')

        self.button.clicked.connect(self.generate_plots)

        # widget = QtGui.QWidget()

        vboxlayout = QtGui.QVBoxLayout( )

        vboxlayout.addWidget(self.cb1)
        vboxlayout.addWidget(self.cb2)
        vboxlayout.addWidget(self.button)

        self.setLayout( vboxlayout )

        self.setFixedSize(200, 200)
        self.setWindowTitle('Data analysis')

        self.show()
    def generate_plots(self):
        if self.cb1.checkState() == QtCore.Qt.Checked:
            fit_window = graph_mod.FitGraph()
            fit_window.show()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = DataAnalysis()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
