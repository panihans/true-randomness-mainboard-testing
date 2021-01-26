from pathlib import Path
from time import sleep, time

import numpy as np
import serial

from serial_comms import Command
import matplotlib.pyplot as plt


def send_receive(send):
    s = serial.Serial('COM3')
    s.write(send.pack())
    out = s.read(send.size)
    return Command().unpack(out)


def main():
    in_file = input('input file: ')
    data = {}
    with open(Path(in_file), 'a') as file:
        lines = file.readlines()
        for line in lines:
            for index, motor in enumerate(line.split(';')):
                pwm, enc = line.split(':')
                if index not in data:
                    data[index] = {'x': [], 'y': []}
                data[index]['x'].append(pwm)
                data[index]['y'].append(enc)
    for i in range(3):
        plt.plot(data[i]['x'], data[i]['y'], label=f'motor {i}')
    plt.xlabel('pwm')
    plt.ylabel('encoder')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
