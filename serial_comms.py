import struct
import sys
from dataclasses import dataclass

import numpy as np
from PyQt5 import QtWidgets, uic, QtCore

import serial
from PyQt5.QtWidgets import QMainWindow

from mplqt5 import MyDynamicMplCanvas

motor1Points = []
motor2Points = []
motor3Points = []
throwerPoints = []


@dataclass
class Command:
    motor1: int = 0
    motor2: int = 0
    motor3: int = 0
    thrower: int = 0
    delimiter: int = 0xABCABC
    format = 'iiiii'
    size = struct.calcsize(format)

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
        self.mplTimer = QtCore.QTimer(self)
        self.mplTimer.timeout.connect(self.mpl_timer_elapsed)
        self.sendingCommands = False

        self.startStopButton.clicked.connect(self.startStopButton_clicked)

    def startStopButton_clicked(self):
        if self.sendingCommands:
            self.sendingCommands = False
            self.writeReadTimer.stop()
            self.mplTimer.stop()
            self.startStopButton.setText('start')
            self.sendSpinBox.setEnabled(True)
        else:
            self.sendingCommands = True
            self.writeReadTimer.start(int(self.sendSpinBox.value()))
            self.mplTimer.start(1000)
            self.startStopButton.setText('stop')
            self.sendSpinBox.setEnabled(False)

    def write_read_mainboard(self):
        c = Command()
        c.motor1 = int(self.motor1SpinBox.value())
        c.motor2 = int(self.motor2SpinBox.value())
        c.motor3 = int(self.motor3SpinBox.value())
        c.thrower = int(self.throwerSpinBox.value())
        s = serial.Serial('COM3')
        s.write(c.pack())
        out = s.read(c.size)
        f = Command()
        f.unpack(out)
        motor1Points.append(f.motor1)
        motor2Points.append(f.motor2)
        motor3Points.append(f.motor3)
        throwerPoints.append(f.thrower)
        print(f.motor1)

    def mpl_timer_elapsed(self):
        rr = lambda x: np.arange(0, len(motor1Points), 1)
        self.mplCanvas.update_figure(rr(motor1Points), motor1Points)
        while len(motor1Points) > 100:
            motor1Points.pop(0)
        #self.mplCanvas.update_figure(rr(motor2Points), motor2Points)
        #self.mplCanvas.update_figure(rr(motor3Points), motor3Points)
        #self.mplCanvas.update_figure(rr(throwerPoints), throwerPoints)


def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = QTWindow()
    widget.show()
    exit(app.exec_())


if __name__ == '__main__':
    main()
