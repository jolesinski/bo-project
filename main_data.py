import sys
import gfx.data_mod as data_mod

def main():


    app = data_mod.QtGui.QApplication(sys.argv)
    ex = data_mod.DataMainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
