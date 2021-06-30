# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QComboBox, QLabel
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"


class UI(QWidget):
    def __init__(self):
        super(UI, self).__init__()
        self.load_ui()
        self.load_elements()
        self.taskChanged(0)
        self.executeButton.clicked.connect(self.executeTask)
        self.taskMenu.currentIndexChanged.connect(self.taskChanged)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def test(self):
        print('test')

    def load_elements(self):
        self.executeButton = self.findChild(QPushButton, 'executeButton')
        self.parameter1 = self.findChild(QTextEdit, 'parameter1')
        self.parameter2 = self.findChild(QTextEdit, 'parameter2')
        self.parameter3 = self.findChild(QTextEdit, 'parameter3')
        self.parameter4 = self.findChild(QTextEdit, 'parameter4')
        self.label1 = self.findChild(QLabel, 'label_1')
        self.label2 = self.findChild(QLabel, 'label_2')
        self.label3 = self.findChild(QLabel, 'label_3')
        self.label4 = self.findChild(QLabel, 'label_4')
        self.taskMenu = self.findChild(QComboBox, 'taskMenu')

    def taskChanged(self, index):
        self.makeInvisible()
        self.currentTask = index + 1
        print("Current task is: {}".format(self.currentTask))
        getattr(self, "task{}Init".format(self.currentTask))()

    def executeTask(self):
        getattr(self, "task{}".format(self.currentTask))()

    def makeInvisible(self):
        for i in range(1, 5):
            getattr(self, "parameter{}".format(i)).setVisible(0)
            getattr(self, "label{}".format(i)).setVisible(0)

    def makeVisible(self, num):
        for i in range(1, num + 1):
            getattr(self, "parameter{}".format(i)).setVisible(1)
            getattr(self, "label{}".format(i)).setVisible(1)

    def task1Init(self):
        self.makeVisible(4)

    def task1(self):
        # print(self.parameter1.toPlainText() + ' surede kalkip ' + self.parameter2.toPlainText() + ' formasyonuna gecip ' +
        #       self.parameter3.toPlainText() + ' saniye bekleyip ' + self.parameter4.toPlainText() + ' surede in.')
        print('Execute task 1')

    def task2Init(self):
        self.makeVisible(3)

    def task2(self):
        print('Execute task 2')


if __name__ == "__main__":
    app = QApplication([])
    widget = UI()
    widget.show()
    sys.exit(app.exec_())
