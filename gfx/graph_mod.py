import sys, os
import pickle
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt


class Graph(QtGui.QWidget):
    def __init__(self):

        super().__init__()

        # Configure ui window
        self.initUI()


    def centerWindow(self):
        '''
            Based on rectangles from frameGeometry finds center of our
            window and its opened children and moves it there
        '''
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def initUI(self):
        '''
            Configures plot window.
        '''
        # Change resolution and center window
        self.resize(1024, 600)
        self.centerWindow()

        # Figure instance for our plot
        self.figure = plt.figure()

        # Using canvas to display figure
        self.canvas = FigureCanvas(self.figure)

        # Set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class FitGraph(Graph):
    def __init__(self, data):
        super().__init__()
        self.data = data

        self.init_data()

        self.plot()


    def init_data(self):

        fitness_data = self.data['fitness_data']
        self.fitness_vals = fitness_data[0]
        self.fitness_med = fitness_data[1]
        self.popul_list = range(1, len(self.fitness_vals)  + 1 )


    def plot(self):
        graph = self.figure.add_subplot(2, 1, 1)
        graph.plot( self.popul_list, self.fitness_vals, '-')
        graph.set_xlabel('population number')
        graph.set_ylabel('fitness function value')

        graph = self.figure.add_subplot(2, 1, 2)
        graph.plot( self.popul_list, self.fitness_med, '-')
        graph.set_xlabel('population number')
        graph.set_ylabel('median of fitness function\n values in each population')

        self.canvas.draw()



class SolGraph(Graph):

    def __init__(self, data):
        super().__init__()
        self.data = data

        self.init_data()

        self.plot()


    def init_data(self):
        # Load colors for graph
        self.palette = self.data['palette_data']

        # Load solution data
        self.solution = self.data['solution_data']

        path =  os.path.dirname(__file__)
        path = os.path.join(os.path.dirname(path), 'config/sched_data.pickle')
        with open(path, 'rb') as file:
            conf_data = pickle.load(file)
        self.proc_num = int(conf_data['proc_num'])
        self.task_num = int(conf_data['task_num'])

        self.task_data = self.data['task_data']

        # Format solution data for graph
        self.format_data()


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

        self.task_ids = []
        for i in range(self.proc_num):
            self.task_ids.append([])

        # Background colors for tasks in every pipe
        self.facecolors = []
        for i in range(self.proc_num):
            self.facecolors.append([])

        # Texts colors for tasks in every pipe
        self.textcolors = []
        for i in range(self.proc_num):
            self.textcolors.append([])

        # Border colors for tasks in every pipe
        self.edgecolors = []
        for i in range(self.proc_num):
            self.edgecolors.append([])

        # length of each processor stream
        pipes_length = []
        for i in range(self.proc_num):
            pipes_length.append(0)

        # create y_labels for processors
        self.y_labels = []
        for i in range(self.proc_num):
            self.y_labels.append('processor no. ' + str(i + 1))

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
                    self.textcolors[index].append(self.palette[task_id][1])
                    self.edgecolors[index].append('black')
                    self.task_ids[index].append('Task no.' + str( task_id + 1 ))

            # add dead spaces for pipes that need to wait for synchro.
            for index in active_processors:
                if pipes_length[index] < max_plength:

                    # dspace_indexes[index].append( len(self.xaxis_val[index] ) )
                    dspace_length = max_plength - pipes_length[index]
                    self.xaxis_val[index].append((pipes_length[index],
                                                    dspace_length))
                    pipes_length[index] += dspace_length

                    self.facecolors[index].append('grey')
                    self.textcolors[index].append('black')
                    self.edgecolors[index].append('black')
                    self.task_ids[index].append('')

        self.x_limit = max(pipes_length) + 5

    def plot(self):
        '''
            Initializes and draws graph of solution
        '''

        graph = self.figure.add_subplot( 1, 1, 1 )
        # min height for current pipe display
        height = 0

        # add pipes
        for proc_id in range(self.proc_num):
            graph.broken_barh( self.xaxis_val[proc_id], (height, 4),
                        facecolors=tuple(self.facecolors[proc_id]),
                        edgecolors=tuple(self.edgecolors[proc_id]))

            for index, val in enumerate(self.xaxis_val[proc_id]):
                label_x = val[0]
                label_y = height + 2
                graph.annotate(self.task_ids[proc_id][index],
                            xy=(label_x, label_y),
                            textcoords='data',
                            color=self.textcolors[proc_id][index],
                            weight='bold',
                            fontsize=14)
            height += 5

        # set limits for axes
        graph.set_ylim(0, height)
        graph.set_xlim(0, self.x_limit)

        # set labels for axes
        graph.set_xlabel('time')
        graph.set_yticklabels(self.y_labels)

        # set ticks for axes
        graph.set_xticks(range(0, self.x_limit, 5))
        graph.set_yticks(range(2, height, 5))

        graph.grid(True)

        # refresh canvas
        self.canvas.draw()
