# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget, QComboBox, QRadioButton, QListWidget, QLabel, QPushButton, QTextEdit, QCheckBox, QListWidgetItem
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class main(QWidget):
    currentTask = 0
    radioButtonControl = 18 * [0]
    taskParameterCount = [4, 2, 1, 2, 1, 2, 1, 1, 2]
    taskQueue = []
    element = {}

    def __init__(self):
        super(main, self).__init__()
        self.load_ui()
        self.load_elements()
        self.radioBoxInit()
        for i in range(1, 19):
            self.element['d'+str(i)+'d'].pressed.connect(
                lambda i=i: self.executeRadioButton(i, 0))
            self.element['d'+str(i)+'s1'].pressed.connect(
                lambda i=i: self.executeRadioButton(i, 1))
            self.element['d'+str(i)+'s2'].pressed.connect(
                lambda i=i: self.executeRadioButton(i, 2))

        self.element["selectTask"].currentIndexChanged.connect(self.switch_task)
        self.element["addToQueue"].clicked.connect(self.addToQueueButton)
        self.element["taskListUp"].clicked.connect(self.upTask)
        self.element["taskListDown"].clicked.connect(self.downTask)
        self.element["taskListRemove"].clicked.connect(self.removeTask)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def load_elements(self):
        for i in range(1, 19):
            self.element['d' +
                         str(i)+'d']  = self.findChild(QRadioButton, 'd'+str(i)+'d')
            self.element['d' +
                         str(i)+'s1'] = self.findChild(QRadioButton, 'd'+str(i)+'s1')
            self.element['d' +
                         str(i)+'s2'] = self.findChild(QRadioButton, 'd'+str(i)+'s2')
                         
        self.element["taskLabel1"] = self.findChild(QLabel, 'taskLabel1')
        self.element["taskLabel2"] = self.findChild(QLabel, 'taskLabel2')
        self.element["taskLabel3"] = self.findChild(QLabel, 'taskLabel3')
        self.element["taskLabel4"] = self.findChild(QLabel, 'taskLabel4')

        self.element["addToQueue"]     = self.findChild(QPushButton, 'addToQueue')
        self.element["executeButton"]  = self.findChild(QPushButton, 'executeButton')
        self.element["taskListDown"]   = self.findChild(QPushButton, 'taskListDown')
        self.element["taskListRemove"] = self.findChild(QPushButton, 'taskListRemove')
        self.element["taskListUp"]     = self.findChild(QPushButton, 'taskListUp')
        
        self.element["taskParameter1"] = self.findChild(QTextEdit, "taskParameter1")
        self.element["taskParameter2"] = self.findChild(QTextEdit, "taskParameter2")
        self.element["taskParameter3"] = self.findChild(QTextEdit, "taskParameter3")
        self.element["taskParameter4"] = self.findChild(QTextEdit, "taskParameter4")

        self.element["selectTask"]  = self.findChild(QComboBox, "selectTask")
        self.element["selectSwarm"] = self.findChild(QComboBox, "selectSwarm")
        
        self.element["taskList"]       = self.findChild(QListWidget, "taskList")
        self.element["taskCheckBox"]   = self.findChild(QCheckBox, "taskCheckBox")

    def switch_task(self):
        self.currentTask = self.element["selectTask"].currentIndex()
        if self.element["selectTask"].currentIndex() == 0:
            self.swarmNavigationInit()
        elif self.element["selectTask"].currentIndex() == 1:
            self.takeoffInit()
        elif self.element["selectTask"].currentIndex() == 2:
            self.landingInit()
        elif self.element["selectTask"].currentIndex() == 3:
            self.changeFormationInit()
        elif self.element["selectTask"].currentIndex() == 4:
            self.hoverInit()
        elif self.element["selectTask"].currentIndex() == 5:
            self.addDroneInit()
        elif self.element["selectTask"].currentIndex() == 6:
            self.swarmSeperationInit()
        elif self.element["selectTask"].currentIndex() == 7:
            self.swarmCombinationInit()
        elif self.element["selectTask"].currentIndex() == 8:
            self.swarmRotationInit()

    def radioBoxInit(self):
        for i in range(1, 19):
            self.element['d'+str(i)+'d'].setChecked(1)
            self.element['d'+str(i)+'s1'].setChecked(0)
            self.element['d'+str(i)+'s2'].setChecked(0)
    
    def showParameters(self,n):
        for i in range(1,n+1):
            self.element["taskParameter"+str(i)].setVisible(1)
            self.element["taskParameter"+str(i)].clear()
            self.element["taskLabel"+str(i)].setVisible(1)    
        for i in range(n+1,5):
            self.element["taskParameter"+str(i)].setVisible(0)
            self.element["taskLabel"+str(i)].setVisible(0)
        self.element["taskCheckBox"].setVisible(0)

    def swarmNavigationInit(self):
        self.showParameters(4)
        self.element["taskCheckBox"].setVisible(1)
        self.element["taskLabel2"].setText("Coordinate x")
        self.element["taskLabel3"].setText("Coordinate y")
        self.element["taskLabel4"].setText("Coordinate z")

    def takeoffInit(self):
        self.showParameters(2)
        self.element["taskLabel2"].setText("Height")

    def changeFormationInit(self):
        self.showParameters(2)
        self.element["taskLabel2"].setText("Formation")

    def landingInit(self):
        self.showParameters(1)

    def hoverInit(self):
        self.showParameters(1)
        
    def swarmSeperationInit(self):
        self.showParameters(1)
        
    def swarmCombinationInit(self):
        self.showParameters(1)

    def swarmRotationInit(self):
        self.showParameters(2)
        self.element["taskLabel2"].setText("Angle")

    def addDroneInit(self):
        self.showParameters(2)
        self.element["taskLabel2"].setText("Drone ID")
        
    def executeRadioButton(self, drone_id, swarm_id):
        if self.radioButtonControl[drone_id-1] == swarm_id:
            if swarm_id > 0:
                self.element['d'+str(drone_id)+'s'+str(swarm_id)].setChecked(0)
            else:
                self.element['d'+str(drone_id)+'d'].setChecked(0)
            return

        self.radioButtonControl[drone_id-1] = swarm_id

        if swarm_id == 0:
            self.element['d'+str(drone_id)+'s1'].setChecked(0)
            self.element['d'+str(drone_id)+'s2'].setChecked(0)

        if swarm_id == 1:
            self.element['d'+str(drone_id)+'d'].setChecked(0)
            self.element['d'+str(drone_id)+'s2'].setChecked(0)

        if swarm_id == 2:
            self.element['d'+str(drone_id)+'d'].setChecked(0)
            self.element['d'+str(drone_id)+'s1'].setChecked(0)

    def addToQueueButton(self):
        self.addTask()
    
    def addTask(self):
        tmp = [self.currentTask]
        for i in range(self.taskParameterCount[self.currentTask]):
            tmp = tmp + [self.element["taskParameter"+str(i+1)].toPlainText()]
        if self.currentTask == 0:
            tmp = tmp + [self.element["taskCheckBox"].isChecked()]
        self.element["taskList"].addItem(str(tmp))
        self.taskQueue.append(tmp)
        print(self.taskQueue)
    
    def removeTask(self):
        rowNum = self.element['taskList'].currentRow()
        if rowNum >= 0 and rowNum < len(self.taskQueue):
            self.element['taskList'].takeItem(rowNum)
            del self.taskQueue[rowNum]
    
    def upTask(self):
        rowNum = self.element['taskList'].currentRow()
        if rowNum > 0:
            upperTask = self.element['taskList'].item(rowNum - 1).text()
            theTask = self.element['taskList'].item(rowNum).text()
            self.element['taskList'].item(rowNum - 1).setText(theTask)
            self.element['taskList'].item(rowNum).setText(upperTask)
            self.taskQueue[rowNum], self.taskQueue[rowNum - 1] = self.taskQueue[rowNum - 1], self.taskQueue[rowNum]
            self.element['taskList'].setCurrentRow(rowNum - 1)

    def downTask(self):
        rowNum = self.element['taskList'].currentRow()
        if rowNum < len(self.taskQueue) - 1:
            upperTask = self.element['taskList'].item(rowNum + 1).text()
            theTask = self.element['taskList'].item(rowNum).text()
            self.element['taskList'].item(rowNum + 1).setText(theTask)
            self.element['taskList'].item(rowNum).setText(upperTask)
            self.taskQueue[rowNum], self.taskQueue[rowNum + 1] = self.taskQueue[rowNum + 1], self.taskQueue[rowNum]
            self.element['taskList'].setCurrentRow(rowNum + 1)

    def printItem(self):
        print(self.element['taskList'].currentItem().text())
        print(self.element['taskList'].currentItem())

    def addToSwarm(self, swarm_id, drone_id):
        pass
    
    def removeFromSwarm(self, swarm_id, drone_id):
        pass

if __name__ == "__main__":
    app = QApplication([])
    widget = main()
    widget.show()
    sys.exit(app.exec_())
