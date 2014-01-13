import sys, os
import pickle
from . import graph_mod
from PyQt4 import QtGui, QtCore

class DataMainWindow(QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        proc_label = QtGui.QLabel('Quantity of processors:')
        task_label = QtGui.QLabel('Quantity of tasks:')
        mutop_label = QtGui.QLabel('Mutation operator version:')
        xop_label = QtGui.QLabel('Crossover operator version:')

        self.proc_edit = QtGui.QLineEdit()
        self.task_edit = QtGui.QLineEdit()

        self.proc_edit.setText('4')
        self.task_edit.setText('20')

        self.mutop_combo = QtGui.QComboBox()
        self.mutop_combo.addItem("Version 1")
        self.mutop_combo.addItem("Version 2")

        self.xop_combo = QtGui.QComboBox()
        self.xop_combo.addItem("Version 1")
        self.xop_combo.addItem("Version 2")

        self.button = QtGui.QPushButton('Generate')
        self.button.clicked.connect(self.generate_problem)


        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget( proc_label, 0, 0)
        grid.addWidget( task_label, 2, 0)
        grid.addWidget( mutop_label, 0, 1)
        grid.addWidget( xop_label, 0, 2)
        grid.addWidget( self.proc_edit, 1, 0)
        grid.addWidget( self.task_edit, 3, 0)
        grid.addWidget( self.mutop_combo, 1, 1)
        grid.addWidget( self.xop_combo, 1, 2)
        grid.addWidget( self.button, 3, 2)

        self.setLayout(grid)

        self.setFixedSize(450, 150)
        self.show()

    def generate_problem(self):
        proc_num = int(self.proc_edit.displayText())
        task_num = int(self.task_edit.displayText())

        mutop_operator = self.mutop_combo.currentIndex()
        xop_operator = self.xop_combo.currentIndex()




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
