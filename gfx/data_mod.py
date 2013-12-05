import sys, os
import pickle
from . import graph_mod
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

        vboxlayout = QtGui.QVBoxLayout( )

        vboxlayout.addWidget(self.cb1)
        vboxlayout.addWidget(self.cb2)
        vboxlayout.addWidget(self.button)

        self.setLayout( vboxlayout )

        self.setFixedSize(200, 200)
        self.setWindowTitle('Data analysis')

        path = os.path.dirname(__file__)
        path = os.path.join(os.path.dirname(path), 'config/graph_data.pickle')
        with open(path, 'rb') as file:
            graph_data = pickle.load(file)
        self.fitGraphDialog = graph_mod.FitGraph(graph_data)
        self.solGraphDialog = graph_mod.SolGraph(graph_data)

        self.show()
    def generate_plots(self):
        if self.cb1.checkState() == QtCore.Qt.Checked:
            self.solGraphDialog.create()
            self.solGraphDialog.show()

        if self.cb2.checkState() == QtCore.Qt.Checked:
            self.fitGraphDialog.create()
            self.fitGraphDialog.show()


def main():


    app = QtGui.QApplication(sys.argv)
    ex = DataAnalysis()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
