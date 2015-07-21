__author__ = 'jie'
class ToeholdItemController:
    '''
    handles event for toehold item;
    connect signals btw model toehold and toehold item
    '''
    def __init__(self,toeholdItem):
        self._toehold_item = toeholdItem
        self.connectSignals()

    def connectSignals(self):
        pass
