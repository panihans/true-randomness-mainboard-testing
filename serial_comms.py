import struct
import ctypes
import sys
from dataclasses import dataclass
from PyQt5 import QtWidgets, uic, QtCore

import serial
from PyQt5.QtWidgets import QMainWindow

from mplqt5 import MyDynamicMplCanvas


@dataclass
class Command:
    motor1: int = 0
    motor2: int = 0
    motor3: int = 0
    thrower: int = 0
    led: int = 0
    delimiter: int = 0xBAD
    format = 'hhhhh'

    def pack(self):
        return struct.pack(
            self.format,
            self.motor1,
            self.motor2,
            self.motor3,
            self.thrower,
            self.delimiter)

    def unpack(self, packed):
        unpacked = struct.unpack(self.format, packed)
        self.motor1 = unpacked[0]
        self.motor2 = unpacked[1]
        self.motor3 = unpacked[2]
        self.thrower = unpacked[3]


class QTWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('serial_comms.ui', self)
        self.mplWidget = QtWidgets.QWidget(self)
        self.mplLayout = QtWidgets.QVBoxLayout(self.mplWidget)
        self.mplCanvas = MyDynamicMplCanvas(self.mplWidget, width=320, height=320, dpi=100)
        self.mplLayout.addWidget(self.mplCanvas)
        self.controlsPlotContainer.addWidget(self.mplWidget)

        self.writeReadTimer = QtCore.QTimer(self)
        self.writeReadTimer.timeout.connect(self.write_read_mainboard)

        self.startStopButton.clicked.connect(self.startStopButton_clicked)

    def startStopButton_clicked(self):
        if self.writeReadTimer.isActive():
            self.writeReadTimer.stop()
            self.startStopButton.setText('start')
            self.writeReadTimerPeriod.setEnabled(True)
        else:
            self.writeReadTimer.start(int(self.writeReadTimerPeriod.value()))
            self.startStopButton.setText('stop')
            self.writeReadTimerPeriod.setEnabled(False)

    def write_read_mainboard(self):
        # c = Command()
        # c.motor1 = 250
        # c.motor2 = 250
        # c.motor3 = 250
        # s = serial.Serial('COM3')
        # s.write(c.pack())
        # out = s.read(10)
        # f = Command()
        # f.unpack(out)
        # print(f)
        self.mplCanvas.update_figure([0, 1, 2, 3], [9, 5, 7, 10])


def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = QTWindow()
    widget.show()
    exit(app.exec_())


if __name__ == '__main__':
    main()
