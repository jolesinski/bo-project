import sys
import pickle
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt


class Window(QtGui.QWidget):

    def __init__(self):
        '''
            Initializes all data and plats graph
        '''
        super().__init__()

        # Load colors for graph
        self.load_palette()

        # Load solution data
        self.load_solution()

        # Format solution data for graph
        self.format_data()

        # Configure ui window
        self.initUI()

        # Plot the solution
        self.plot()


    def initUI(self):
        '''
            Configures plot window.

            TODO: resolution changing
        '''
        # Change resolution and center window
        self.resize(1024, 768)
        self.centerWindow()

        # Figure instance for our plot
        self.figure = plt.figure()

        # Using canvas to display figure
        self.canvas = FigureCanvas(self.figure)

        # Set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


    def centerWindow(self):
        '''
            Based on rectangles from frameGeometry finds center of our
            window and its opened children and moves it there
        '''
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def load_palette(self):
        '''
            Loads previously created palette using pickle
        '''
        with open('config/palette_data.pickle', 'rb') as palette_data:
            self.palette = pickle.load(palette_data)


    def load_solution(self):
        '''
            Loads all necessary solution data using pickle
        '''
        with open('config/solution_data.pickle', 'rb') as solution_data:
            self.solution = pickle.load( solution_data )
        # !!! Dunno if necessery
        with open('config/sched_data.pickle', 'rb') as sched_file:
            conf_data = pickle.load( sched_file )

        self.proc_num = int(conf_data['proc_num'])
        self.task_num = int(conf_data['task_num'])

        with open('config/task_data.pickle', 'rb') as task_data:
            self.task_data = pickle.load( task_data )


    def format_data(self):
        '''
            Formats all data so it can be accepted as arguments for plot
            functions
        '''
        # List of lists for broken_barh constructor. Each sublist corresponds
        # to another processors xaxis list. Len(xaxis_val) = proc_num
        self.xaxis_val = []
        for i in range(self.proc_num):
            self.xaxis_val.append([])

        # Background colors for tasks in every pipe
        self.facecolors = []
        for i in range(self.proc_num):
            self.facecolors.append([])

        # Border colors for tasks in every pipe
        self.edgecolors = []
        for i in range(self.proc_num):
            self.edgecolors.append([])

        # length of each processor stream
        pipes_length = []
        for i in range(self.proc_num):
            pipes_length.append(0)

        # We go through every task tuple (task_id, proc_list). Proc list is
        # a binary vector. If task is being handled by n-th processor, n-th
        # value of proc_list is set to 1, otherwise to 0
        for task in self.solution:

            # set task_id
            # !!!! IF They start from 0 change to task[0]
            task_id = task[0] - 1

            # set proc_list for clarity
            processor_list = task[1]

            # Number of processors that process our task simultaneously
            parallel_count = processor_list.count(1)

            # Lengths of processing task on each processor
            task_lengths = self.task_data[task_id][parallel_count-1]

            # Length of the longest pipe responsible for current task
            max_plength = 0

            # Indexes of all processors responsible for processing current task
            active_processors = []

            # We iterate through binary processor list. If task is being
            # handled by n-th (index) processor add task length to pipe.
            # Also find longest pipe under consideration.
            for index, val in enumerate(processor_list):

                if (val == 1):
                    active_processors.append(index)

                    # adds (task_start, task_length) pair
                    self.xaxis_val[index].append((pipes_length[index],
                                                    task_lengths[index]))
                    # adds lenght of current task to previous pipe lenght
                    pipes_length[index] += task_lengths[index]

                    # finds longest pipe from pipes responsible for current
                    # task
                    if pipes_length[index] > max_plength:
                        max_plength = pipes_length[index]

                    self.facecolors[index].append(self.palette[task_id][0])
                    self.edgecolors[index].append('black')

            # add dead spaces for pipes that need to wait for synchro.
            for index in active_processors:
                if pipes_length[index] < max_plength:

                    # dspace_indexes[index].append( len(self.xaxis_val[index] ) )
                    dspace_length = max_plength - pipes_length[index]
                    self.xaxis_val[index].append((pipes_length[index],
                                                    dspace_length))
                    pipes_length[index] += dspace_length

                    self.facecolors[index].append('black')
                    self.edgecolors[index].append('black')

            # create y_labels for processors
            self.y_labels = []
            for i in range(self.proc_num):
                self.y_labels.append('processor no. ' + str(i + 1))



    def plot(self):
        '''
            Initializes and draws graph of solution

            TODO: automate xlim
                - automate x axis limit
        '''

        graph = self.figure.add_subplot(111)
        # min height for current pipe display
        height = 0

        # add pipes
        for i in range(self.proc_num):
            graph.broken_barh( self.xaxis_val[i], (height, 4),
                        facecolors=tuple(self.facecolors[i]),
                        edgecolors=tuple(self.edgecolors[i]) )
            height += 5

        # set limits for axes
        graph.set_ylim(0,height)
        graph.set_xlim(0,20)

        # set labels for axes
        graph.set_xlabel('time')
        graph.set_yticklabels(self.y_labels)

        # set ticks for axes
        graph.set_xticks(range(0, 20, 5))
        graph.set_yticks(range(2, height, 5))

        graph.grid(True)

        # refresh canvas
        self.canvas.draw()
