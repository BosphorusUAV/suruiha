# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget, QComboBox, QRadioButton
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class main(QWidget):
    element = {}

    def __init__(self):
        super(main, self).__init__()
        self.load_ui()
        self.load_elements()
        self.cosmetic_shit()
        for i in range(1, 19):
            self.element['d'+str(i)+'d'].pressed.connect(
                lambda i=i: self.executeRadioButton('d'+str(i)+'d'))
            self.element['d'+str(i)+'s1'].pressed.connect(
                lambda i=i: self.executeRadioButton('d'+str(i)+'s1'))
            self.element['d'+str(i)+'s2'].pressed.connect(
                lambda i=i: self.executeRadioButton('d'+str(i)+'s2'))

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def cosmetic_shit(self):
        for i in range(1, 19):
            self.element['d'+str(i)+'d'].setChecked(1)
            self.element['d'+str(i)+'s1'].setChecked(0)
            self.element['d'+str(i)+'s2'].setChecked(0)

    def load_elements(self):
        for i in range(1, 19):
            self.element['d' +
                         str(i)+'d'] = self.findChild(QRadioButton, 'd'+str(i)+'d')
            self.element['d' +
                         str(i)+'s1'] = self.findChild(QRadioButton, 'd'+str(i)+'s1')
            self.element['d' +
                         str(i)+'s2'] = self.findChild(QRadioButton, 'd'+str(i)+'s2')
        self.findChild(QRadioButton, 'label_'+str())

    def addToSwarm(self, swarm_id, drone_id):
        pass

    def executeRadioButton(self, x):
        print('Bana bastiginiz icin tesekkur ederim efendi melih')
        if x[-1] == 'd':
            self.element[x[:-1]+'s1'].setChecked(0)
            self.element[x[:-1]+'s2'].setChecked(0)
        if x[-1] == '1':
            self.element[x[:-2]+'d'].setChecked(0)
            self.element[x[:-2]+'s2'].setChecked(0)
        if x[-1] == '2':
            self.element[x[:-2]+'d'].setChecked(0)
            self.element[x[:-2]+'s1'].setChecked(0)


if __name__ == "__main__":
    app = QApplication([])
    widget = main()
    widget.show()
    sys.exit(app.exec_())
