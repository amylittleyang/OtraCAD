__author__ = 'jie'
from PyQt5.QtWidgets import QDockWidget,QWidget,QVBoxLayout,QCheckBox,QDialogButtonBox,QGroupBox,QFormLayout,QMessageBox
from PyQt5 import QtCore
class DockWidget(QDockWidget):
    '''
    Panel on the right of main window;
    container for GUI objects that provide options for transformation;
    panel renewed when new operation is selected in tool Bar
    '''
    def __init__(self,mainWindow):
        super(DockWidget, self).__init__(None)
        self.mainWindow = mainWindow
        self.doc = mainWindow.doc
        self.setupUI()
        self.activeDomain = None
        self.can_update = False

    def setupUI(self):
        # set up layout for dock widget
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.AllDockWidgetFeatures)
        dockWidgetContents = QWidget()
        vLayout = QVBoxLayout()
        dockWidgetContents.setLayout(vLayout)
        self.setWidget(dockWidgetContents)
        self.hide()

    def actionCreate_toeholdTriggeredSlot(self):
        '''
        prepare dockWidget for create toehold command:
        create checkbox3p, checkbox5p,buttonBox;
        apply layout;
        '''

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
            self.can_update = True
            self.show()
            # update appearance of checkboxes based on state of active domain
            self.updateCheckBoxState()

    def updateCheckBoxState(self):
        # notified by document when an active domain is selected;
        # check box appearance updated to show allowable operations;
            if self.activeDomain is not None and self.can_update:
                 if self.activeDomain.canCreateToeholdAt(3): # true if 3' domain on oligo has no toehold or xover
                    self.checkBox_3p.setCheckable(True)
                    self.checkBox_3p.setStyleSheet("background-color:#eee")
                 if self.activeDomain.canCreateToeholdAt(5): # true if 5' domain on oligo has no toehold or xover
                    self.checkBox_5p.setCheckable(True)
                    self.checkBox_5p.setStyleSheet("background-color:#eee")


    def buttonBoxAcceptedSlot(self):
        # save changes to macro;
        # undo all commands;
        # add all commands to undo_stack
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
        # undo all commands;
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
        # triggered when new active domain is selected; notified by document
        self.activeDomain = domain
        # update check box state for the new active domain
        self.updateCheckBoxState()



    def checkBoxStateChangedSlot(self,checkbox):
        # triggered when a check box is checked or unchecked

        # interpret checkbox message
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

        # notify active domain of check box message
        self.activeDomain.toeholdChanged(prime,checked)

