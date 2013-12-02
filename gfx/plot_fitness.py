import graph_mod

def main():
    app = graph_mod.QtGui.QApplication(graph_mod.sys.argv)

    main_window = graph_mod.FitGraph()
    main_window.show()

    graph_mod.sys.exit(app.exec_())


if __name__ == '__main__':
    main()
