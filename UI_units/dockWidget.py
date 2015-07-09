__author__ = 'jie'
from PyQt5.QtWidgets import QDockWidget,QWidget,QVBoxLayout,QCheckBox,QDialogButtonBox,QGroupBox,QFormLayout
from PyQt5 import QtCore
class DockWidget(QDockWidget):
    def __init__(self,mainWindow):
        super(DockWidget, self).__init__(None)
        self.mainWindow = mainWindow
        self.setupUI()

    def setupUI(self):
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.AllDockWidgetFeatures)
        dockWidgetContents = QWidget()
        vLayout = QVBoxLayout()
        dockWidgetContents.setLayout(vLayout)
        self.setWidget(dockWidgetContents)
        self.hide()

    def actionCreate_toeholdTriggeredSlot(self):
        win = self.mainWindow
        dock = win.dockWidget
        dock.setWindowTitle('Create Toehold')
        checkBox_3p = QCheckBox('create 3-prime toehold   ')
        checkBox_5p = QCheckBox('create 5-prime toehold   ')

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        groupBox = QGroupBox()

        layout = QFormLayout()
        layout.addWidget(checkBox_3p)
        layout.addWidget(checkBox_5p)
        groupBox.setLayout(layout)

        dockWidgetContents = dock.widget()
        QWidget().setLayout(dockWidgetContents.layout())
        newLayout = QVBoxLayout()
        newLayout.addWidget(groupBox)
        newLayout.addWidget(buttonBox)
        dockWidgetContents.setLayout(newLayout)
        #self.addDockWidget(Qt.RightDockWidgetArea, dock)
        # self.viewMenu.addAction(dock.toggleViewAction())
        dock.show()