import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSpinBox

class RangedSpinBox(QSpinBox):
    # Replaces the valueChanged signal
    newValueChanged = pyqtSignal(int)

    def __init__(self, values: list, parent=None):
        super(RangedSpinBox, self).__init__(parent=parent)

        self.values = values
        self.n = len(values)
        self.valueChanged.connect(self.onValueChanged)
        self.before_value = self.value()
        self.newValueChanged.connect(self.slot)

    def onValueChanged(self, i):
        if i in self.values:
            self.setValue(i)
            self.before_value = i
            self.newValueChanged.emit(i)
            return 0
        if i > self.before_value:
            # GO UP
            next_index = (self.values.index(self.before_value) + 1) % self.n
        else:
            next_index = (self.values.index(self.before_value) - 1) % self.n

        self.setValue(self.values[next_index])
        self.before_value = self.values[next_index]
        self.newValueChanged.emit(self.values[next_index])


    def slot(self, value):
        # print(value)
        pass