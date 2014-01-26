import sys, os
import pickle
from . import graph_mod

from  scheduler.Scheduler import Scheduler
from  scheduler.Task import Problem


from PyQt4 import QtGui, QtCore

class DataMainWindow(QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.ready_to_solve = False

        sol_label = QtGui.QLabel('Initial problem parameters')
        proc_label = QtGui.QLabel('Quantity of processors:')
        task_label = QtGui.QLabel('Quantity of tasks:')

        alg_label = QtGui.QLabel('Algorithm parameters')
        iter_label = QtGui.QLabel('Number of iterations:')
        mutop_label = QtGui.QLabel('Mutation operator version:')
        xop_label = QtGui.QLabel('Crossover operator version:')
        test_label = QtGui.QLabel('Number of tests:')
        crossp_label = QtGui.QLabel('Crossover op. usage probability:')
        parents_label = QtGui.QLabel('Fraction of old population in new:')


        self.proc_edit = QtGui.QLineEdit()
        self.task_edit = QtGui.QLineEdit()
        self.proc_edit.setMaximumWidth(50)
        self.task_edit.setMaximumWidth(50)
        self.proc_edit.setText('2')
        self.task_edit.setText('20')

        self.iter_edit = QtGui.QLineEdit()
        self.iter_edit.setMaximumWidth(50)
        self.iter_edit.setText('5000')

        self.test_edit = QtGui.QLineEdit()
        self.test_edit.setMaximumWidth(50)
        self.test_edit.setText('1')

        self.crossp_edit = QtGui.QLineEdit()
        self.crossp_edit.setMaximumWidth(50)
        self.crossp_edit.setText('0.5')

        self.parents_edit = QtGui.QLineEdit()
        self.parents_edit.setMaximumWidth(50)
        self.parents_edit.setText('0.2')




        self.mutop_combo = QtGui.QComboBox()
        self.mutop_combo.addItem("Version 1")
        self.mutop_combo.addItem("Version 2")
        self.mutop_combo.addItem("Version 3")
        self.mutop_combo.addItem("Version 4")
        self.mutop_combo.addItem("Version 5")

        self.xop_combo = QtGui.QComboBox()
        self.xop_combo.addItem("Version 1")
        self.xop_combo.addItem("Version 2")
        self.xop_combo.addItem("Version 3")
        self.xop_combo.addItem("Version 4")
        self.xop_combo.addItem("Version 5")

        self.buttonpr = QtGui.QPushButton('Generate')
        self.buttonpr.clicked.connect(self.generate_problem)

        self.buttonsol = QtGui.QPushButton('Solve')
        self.buttonsol.clicked.connect(self.solve_problem)

        self.statusBar = QtGui.QLabel('Ready')

        grid = QtGui.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget( sol_label, 0, 0)
        grid.addWidget( proc_label, 1, 0)
        grid.addWidget( task_label, 3, 0)

        grid.addWidget( mutop_label, 1, 2)
        grid.addWidget( xop_label, 1, 3)


        grid.addWidget( self.proc_edit, 2, 0)
        grid.addWidget( self.task_edit, 4, 0)

        grid.addWidget( alg_label, 0, 2)
        grid.addWidget( iter_label, 3, 2)
        grid.addWidget( test_label, 3, 3)
        grid.addWidget( crossp_label, 5, 3)
        grid.addWidget( parents_label, 5, 2)
        grid.addWidget( self.iter_edit, 4, 2)
        grid.addWidget( self.parents_edit, 6, 2)
        grid.addWidget( self.crossp_edit, 6, 3)
        grid.addWidget( self.test_edit, 4, 3)
        grid.addWidget( self.mutop_combo, 2, 2)
        grid.addWidget( self.xop_combo, 2, 3)
        grid.addWidget( self.buttonpr, 5, 0)
        grid.addWidget( self.buttonsol, 7, 2)

        grid.addWidget( self.statusBar, 8, 0, 1, 4)

        self.setLayout(grid)

        self.setFixedSize(600, 250)
        self.show()

    def generate_problem(self):
        proc_num = int(self.proc_edit.displayText())
        task_num = int(self.task_edit.displayText())

        self.statusBar.setText('Generating problem..')
        prob = Problem.Random( proc_num, task_num)

        self.statusBar.setText('Saving data..')
        prob.Save()

        self.ready_to_solve = True
        self.statusBar.setText('Ready to solve!')

    def solve_problem(self):
        if self.ready_to_solve:
            mutop_operator = self.mutop_combo.currentIndex()
            xop_operator = self.xop_combo.currentIndex()

            self.statusBar.setText('Loading problem data...')
            prob = Problem.Load()

            self.statusBar.setText('Initializing scheduler...')
            sched = Scheduler(20, prob)

            self.statusBar.setText('Solving...')

            iter_num = int(self.iter_edit.displayText())
            test_q = int(self.iter_edit.displayText())
            cross_pr = float(self.crossp_edit.displayText())
            parent_f = float(self.parents_edit.displayText())

            sched.SetOperators(mutationOp = mutop_operator,
                               crossingOp = xop_operator)
            sched.setSelectionParams(parentsInNewPop = parent_f,
                                     mutationProb = cross_pr)

            sched.Trials = int(self.test_edit.displayText())
            sched.solution = sched.Solve(iterations = iter_num)

            self.statusBar.setText('Saving...')
            sched.SaveGraphData()

            self.statusBar.setText('Calling graph gui...')
            self.DataAnalysisDialog = DataAnalysis()
            self.DataAnalysisDialog.create()
            self.DataAnalysisDialog.show()
            self.statusBar.setText('Ready')




class DataAnalysis(QtGui.QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.cb1 = QtGui.QCheckBox('Solution')

        self.cb2 = QtGui.QCheckBox('Fitness function and median')

        self.cb3 = QtGui.QCheckBox('Operators data')

        self.button = QtGui.QPushButton('Generate')
        self.button.clicked.connect(self.generate_plots)

        vboxlayout = QtGui.QVBoxLayout( )

        vboxlayout.addWidget(self.cb1)
        vboxlayout.addWidget(self.cb2)
        vboxlayout.addWidget(self.cb3)
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
        self.opGraphDialog = graph_mod.PopulationGraph(graph_data)

        self.show()


    def generate_plots(self):
        if self.cb1.checkState() == QtCore.Qt.Checked:
            self.solGraphDialog.create()
            self.solGraphDialog.show()

        if self.cb2.checkState() == QtCore.Qt.Checked:
            self.fitGraphDialog.create()
            self.fitGraphDialog.show()

        if self.cb3.checkState() == QtCore.Qt.Checked:
            self.opGraphDialog.create()
            self.opGraphDialog.show()


def main():


    app = QtGui.QApplication(sys.argv)
    ex = DataAnalysis()
    sys.exit(app.exec_())

