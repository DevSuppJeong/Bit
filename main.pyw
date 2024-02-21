import sys
from PyQt5.QtWidgets import QApplication
from mainView import MainView

app = QApplication(sys.argv)

mainwindow = MainView()
mainwindow.show()

sys.exit(app.exec_())
