__author__ = 'jie'
from UI_units.rip_off_dialog import RipOffDialog
class PathToolbarController:
    def __init__(self,loader):
        self.ui_loader = loader
        self.mainWindow = loader.mainWindow

    def connect(self):
        self.mainWindow.actionRip_off.triggered.connect(self.action_Rip_off_Triggered_Slot)

    def action_Rip_off_Triggered_Slot(self):
        self.ripOffDialog = RipOffDialog()
        self.ripOffDialog.exec_()
