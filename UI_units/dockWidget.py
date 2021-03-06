__author__ = 'jie'
from PyQt5.QtWidgets import QLabel,QLineEdit,QDockWidget,QWidget,QHBoxLayout,QVBoxLayout,QCheckBox,QDialogButtonBox,QGroupBox,QFormLayout,QMessageBox
from PyQt5 import QtCore
import cadnano.util as util
from cadnano.oligo.removeoligocmd import RemoveOligoCommand

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
        self.toehold = None
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


###   CREATE TOEHOLD METHODS
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
            #self.checkBox_3p.setStyleSheet("background-color:#ddd")
            #self.checkBox_5p.setStyleSheet("background-color:#ddd")

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
                    #self.checkBox_3p.setStyleSheet("background-color:#eee")
                 if self.activeDomain.canCreateToeholdAt(5): # true if 5' domain on oligo has no toehold or xover
                    self.checkBox_5p.setCheckable(True)
                    #self.checkBox_5p.setStyleSheet("background-color:#eee")


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
            self.activeDomain.toeholdChangeRejected()
            if self.can_update:
                self.checkBox_3p.setCheckable(False)
                self.checkBox_5p.setCheckable(False)
                self.checkBox_3p.setStyleSheet("background-color:#ddd")
                self.checkBox_5p.setStyleSheet("background-color:#ddd")
                self.activeDomain = None
        self.hide()

    def updateActiveDomain(self,domain):
        # triggered when new active domain is selected; notified by document
        if self.can_update and (not self.activeDomain == domain) and self.activeDomain is not None:
            self.buttonBoxRejectedSlot()
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

### RESIZE TOEHOLD METHODS
    def actionResizeToeholdTriggeredSlot(self):
        '''
        prepare dock widget for resize toehold panel
        :return:
        '''
        if not self.isHidden():
            self.hide()
        elif self.doc == None or self.doc.selectedToehold().__len__()==0:
            msg = QMessageBox()
            msg.setText("No toehold selected.")
            msg.exec_()
        elif self.doc.selectedToehold().__len__() is not 1:
            msg = QMessageBox()
            msg.setText("Select only one toehold")
            msg.exec_()
        else:
            # prepare dock widget for resize toehold window
            self.can_update = False # disable createToehold widget update
            self.setWindowTitle('Resize Toehold')
            text_label= QLabel()
            default_label = QLabel()
            nt_label = QLabel()
            default_label.setText("default: 5 nt")
            nt_label.setText("nt")
            text_label.setText("Toehold Length: ")
            groupBox = QGroupBox()
            buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
            buttonBox.accepted.connect(self.resizeToeholdAcceptedSlot)
            buttonBox.rejected.connect(self.resizeToeholdRejectedSlot)
            form = QFormLayout()
            horizontal = QHBoxLayout()
            self.line_edit = QLineEdit()
            list = self.doc.selectedToehold()
            toeholdList = list[0]
            toehold = toeholdList._toehold_list[0]
            self.toehold = toehold
            self.line_edit.setText(str(toehold.length()))
            horizontal.addWidget(text_label)
            horizontal.addWidget(self.line_edit)
            horizontal.addWidget(nt_label)
            groupBox.setLayout(horizontal)
            form.setAlignment(QtCore.Qt.AlignRight)
            form.addWidget(groupBox)
            form.addWidget(default_label)
            form.addWidget(buttonBox)
            dockWidgetContents = self.widget()
            QWidget().setLayout(dockWidgetContents.layout())
            dockWidgetContents.setLayout(form)
            self.show()

    def resizeToeholdAcceptedSlot(self):
        list = self.doc.selectedToehold()
        toeholdList = list[0]
        toehold = toeholdList._toehold_list[0]
        newLen = self.line_edit.text()
        if not newLen.isdigit():
            msg = QMessageBox()
            msg.setText("Invalid Input")
            msg.exec_()
            self.hide()
            return
        else:
            newLen = int(newLen)
            toehold.setLength(newLen)
            self.hide()



    def resizeToeholdRejectedSlot(self):
        self.hide()

    def actionRipOffTriggeredSlot(self):

        # check if can apply operation
        if self.doc is None:
            return
        domain = self.doc.activeDomain()
        self.activeDomain = domain
        if domain is None:
            msg = QMessageBox()
            msg.setText("Must select one strand")
            msg.exec_()
            return
        oligo = domain.oligo()
        if oligo.isLoop():
            msg = QMessageBox()
            msg.setText("Can't rip off loop strand")
            msg.exec_()
            return
        if not oligo.hasToehold():
            msg = QMessageBox()
            msg.setText("Strand does not have overhang toehold")
            msg.exec_()
            return
        if self.isVisible():
            self.RipOffRejectedSlot()
            self.hide()
            return
        else:
            self.show()
        # prepare dock widget for rip off panel
        self.can_update = False # disable createToehold widget update
        self.setWindowTitle("Rip Off Strand")
        text0 = QLabel()
        text0.setText("Selected Strand:")
        text1 = QLabel()
        d5p = oligo.strand5p()
        d3p = oligo.domain3p()
        dcurr = d5p
        s = d5p._name
        dcurr = dcurr.connection3p()
        while(dcurr!=None):
            s = s +"_"+dcurr._name
            dcurr = dcurr.connection3p()
        if d5p.toehold5p() is not None:
            t_list_5 = d5p.toehold5p()._toehold_list
            for t in t_list_5:
                s = t._name+"_"+s
        if d3p.toehold3p() is not None:
            t_list_3 = d3p.toehold3p()._toehold_list
            for t in t_list_3:
                s = s+"_"+t._name
        text1.setText("strand %s on helix %d   " % (s, d5p._vhNum))
        text2 = QLabel()
        text2.setText("length: %s" % oligo._length)
        text3 = QLabel()
        text3.setText("Complement Strand: (5' to 3')  ")
        text4 = QLabel()
        d3p = oligo.domain3p()
        s = d3p._name
        dcurr = d3p.connection5p()
        while(dcurr!=None):
            s = s + "_"+dcurr._name
            dcurr = dcurr.connection5p()
        if d5p.toehold5p() is not None:
            t_list_5 = d5p.toehold5p()._toehold_list
            for t in t_list_5:
                s = s+"_"+t._name
        if d3p.toehold3p() is not None:
            t_list_3 = d3p.toehold3p()._toehold_list
            for t in t_list_3:
                s = t._name+"_"+s

        text4.setText("%s" % s)
        buttonBox =QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.RipOffAcceptedSlot)
        buttonBox.rejected.connect(self.RipOffRejectedSlot)

        form = QFormLayout()
        form.addWidget(text0)
        form.addWidget(text1)
        form.addWidget(text2)
        form.addWidget(text3)
        form.addWidget(text4)
        form.addWidget(buttonBox)
        dockWidgetContents = self.widget()
        QWidget().setLayout(dockWidgetContents.layout())
        dockWidgetContents.setLayout(form)
        self.show()
        # create previewRipOffCommand to preview operation
        domain.oligo().previewRipOff()

    def RipOffAcceptedSlot(self):
        self.doc.undoStack().undo() # undo preview_rip_off_command before applying rip_off_command
        cmds =[]
        cmd = RemoveOligoCommand(self.activeDomain.oligo())
        cmds.append(cmd)
        d = '%s rip off' % self.activeDomain._name
        util.execCommandList(self.activeDomain,cmds,d,use_undostack=True)
        self.hide()


    def RipOffRejectedSlot(self):
        self.hide()
        self.doc.undoStack().undo()













