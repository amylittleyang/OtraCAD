__author__ = 'jie'
class ToeholdItemController:
    '''
    handles event for toehold item;
    connect signals btw model toehold and toehold item
    '''
    def __init__(self,toehold_item,toehold_list):
        self._t_i = toehold_item
        self._m_t = toehold_list
        self.connectSignals()

    def connectSignals(self):
        self._m_t.toeholdRemovedFromSelectionSignal.connect(self._t_i.toeholdRemovedFromSelectionSlot)
        self._m_t.toeholdSelectedSignal.connect(self._t_i.toeholdSelectedSlot)

