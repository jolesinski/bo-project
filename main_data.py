import sys
import data_mod

def main():


    app = data_mod.QtGui.QApplication(sys.argv)
    ex = data_mod.DataAnalysis()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
