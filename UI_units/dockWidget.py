__author__ = 'jie'
from PyQt5.QtWidgets import QDockWidget,QWidget,QVBoxLayout,QCheckBox,QDialogButtonBox,QGroupBox,QFormLayout,QMessageBox
from PyQt5 import QtCore
class DockWidget(QDockWidget):
    def __init__(self,mainWindow):
        super(DockWidget, self).__init__(None)
        self.mainWindow = mainWindow
        self.doc = mainWindow.doc
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
        if not self.isHidden():
            self.hide()
        else:
            self.setWindowTitle('Create Toehold')
            self.checkBox_3p = QCheckBox('create 3-prime toehold   ')
            self.checkBox_3p.stateChanged.connect(lambda:self.checkBoxStateChangedSlot(self.checkBox_3p))
            self.checkBox_5p = QCheckBox('create 5-prime toehold   ')
            self.checkBox_5p.stateChanged.connect(lambda:self.checkBoxStateChangedSlot(self.checkBox_5p))

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

    def buttonBoxAcceptedSlot(self):
        # undo all commands then add to undo_stack
        activeDomain = self.doc.activeDomain()
        activeDomain.toeholdChangeAccepted()
        self.hide()


    def buttonBoxRejectedSlot(self):
        # undo all commands in domain dict
        activeDomain = self.doc.activeDomain()
        activeDomain.toeholdChangeRejected()
        self.hide()

    def checkBoxStateChangedSlot(self,checkbox):
        print('state changed')
        doc = self.doc
        state = checkbox.checkState()
        checked = None
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
        activeDomain = self.doc.activeDomain()
        if activeDomain is None:
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

        if checked:
            if not activeDomain.canCreateToeholdAt(prime):
                msg = QMessageBox()
                msg.setText('Toehold already exists or not an end point')
                msg.exec_()
                checkbox.setChecked(False)
            else:
                activeDomain.toeholdChanged(prime,checked)
        else:
            activeDomain.toeholdChanged(prime,checked)

