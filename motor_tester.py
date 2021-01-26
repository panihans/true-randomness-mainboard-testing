from pathlib import Path
from time import sleep, time

import numpy as np
import serial

from serial_comms import Command


def send_receive(send):
    s = serial.Serial('COM3')
    s.write(send.pack())
    out = s.read(send.size)
    return Command().unpack(out)


def main():
    out_file = f'./motors_{time()}.txt'
    positive = np.arange(0, 65535, 100)
    negative = np.negative(positive)
    steps = positive.size

    for step in range(0, steps):
        send = Command()
        send.motor1 = positive[step]
        send.motor2 = positive[step]
        send.motor3 = positive[step]
        send_receive(send)
        sleep(0.1)
        receive = send_receive(send)
        out = f'{send.motor1}:{receive.motor1};{send.motor2}:{receive.motor2};{send.motor3}:{receive.motor3}'
        with open(Path(out_file), 'a') as file:
            file.write(out)
    print(f'done {out_file}!')


if __name__ == '__main__':
    main()
