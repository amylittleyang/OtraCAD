__author__ = 'jie'
from PyQt5.QtWidgets import QDockWidget,QWidget,QVBoxLayout,QCheckBox,QDialogButtonBox,QGroupBox,QFormLayout,QMessageBox
from PyQt5 import QtCore
class DockWidget(QDockWidget):
    def __init__(self,mainWindow):
        super(DockWidget, self).__init__(None)
        self.mainWindow = mainWindow
        self.doc = mainWindow.doc
        self.setupUI()
        self.activeDomain = None

    def setupUI(self):
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.AllDockWidgetFeatures)
        dockWidgetContents = QWidget()
        vLayout = QVBoxLayout()
        dockWidgetContents.setLayout(vLayout)
        self.setWidget(dockWidgetContents)
        self.hide()

    def actionCreate_toeholdTriggeredSlot(self):
        if not self.isHidden():
            self.hide()
        else:
            self.setWindowTitle('Create Toehold')
            self.checkBox_3p = QCheckBox('create 3-prime toehold   ')
            self.checkBox_3p.stateChanged.connect(lambda:self.checkBoxStateChangedSlot(self.checkBox_3p))
            self.checkBox_5p = QCheckBox('create 5-prime toehold   ')
            self.checkBox_5p.stateChanged.connect(lambda:self.checkBoxStateChangedSlot(self.checkBox_5p))
            self.checkBox_3p.setCheckable(False)
            self.checkBox_5p.setCheckable(False)
            self.checkBox_3p.setStyleSheet("background-color:#ddd")
            self.checkBox_5p.setStyleSheet("background-color:#ddd")

            self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
            self.buttonBox.accepted.connect(self.buttonBoxAcceptedSlot)
            self.buttonBox.rejected.connect(self.buttonBoxRejectedSlot)
            groupBox = QGroupBox()

            layout = QFormLayout()
            layout.addWidget(self.checkBox_3p)
            layout.addWidget(self.checkBox_5p)
            groupBox.setLayout(layout)

            dockWidgetContents = self.widget()
            QWidget().setLayout(dockWidgetContents.layout())
            newLayout = QVBoxLayout()
            newLayout.addWidget(groupBox)
            newLayout.addWidget(self.buttonBox)
            dockWidgetContents.setLayout(newLayout)
            self.show()
            self.updateCheckBoxState()

    def updateCheckBoxState(self):
            if self.activeDomain is not None:
                 if self.activeDomain.canCreateToeholdAt(3):
                    self.checkBox_3p.setCheckable(True)
                    self.checkBox_3p.setStyleSheet("background-color:#eee")
                 if self.activeDomain.canCreateToeholdAt(5):
                    self.checkBox_5p.setCheckable(True)
                    self.checkBox_5p.setStyleSheet("background-color:#eee")


    def buttonBoxAcceptedSlot(self):
        # undo all commands then add to undo_stack
        if self.doc is not None and self.doc.activeDomain() is not None:
            activeDomain = self.doc.activeDomain()
            activeDomain.toeholdChangeAccepted()
            self.checkBox_3p.setCheckable(False)
            self.checkBox_5p.setCheckable(False)
            self.checkBox_3p.setStyleSheet("background-color:#ddd")
            self.checkBox_5p.setStyleSheet("background-color:#ddd")
            self.activeDomain = None
        self.hide()


    def buttonBoxRejectedSlot(self):
        # undo all commands in domain dict
        if self.activeDomain is not None:
            activeDomain = self.doc.activeDomain()
            activeDomain.toeholdChangeRejected()
            self.checkBox_3p.setCheckable(False)
            self.checkBox_5p.setCheckable(False)
            self.checkBox_3p.setStyleSheet("background-color:#ddd")
            self.checkBox_5p.setStyleSheet("background-color:#ddd")
            self.activeDomain = None
        self.hide()

    def updateActiveDomain(self,domain):
        if self.activeDomain is not None:
            self.activeDomain.toeholdChangeRejected()
            self.checkBox_3p.setCheckable(False)
            self.checkBox_5p.setCheckable(False)
            self.checkBox_3p.setStyleSheet("background-color:#ddd")
            self.checkBox_5p.setStyleSheet("background-color:#ddd")
        self.activeDomain = domain
        if not self.isHidden():
            self.updateCheckBoxState()



    def checkBoxStateChangedSlot(self,checkbox):
        state = checkbox.checkState()
        if state == 0:
            checked = False
        else:
            checked = True

        if self.doc is None:
            msg = QMessageBox()
            msg.setText('Import .json before applying transformation.')
            msg.exec_()
            checkbox.setChecked(False)
            return

        if self.activeDomain is None:
            msg = QMessageBox()
            msg.setText('Select a domain')
            msg.exec_()
            checkbox.setChecked(False)
            return
        checkbox_text = checkbox.text()
        if checkbox_text.__contains__('3'):
            prime = 3
        else:
            prime = 5

        self.activeDomain.toeholdChanged(prime,checked)

