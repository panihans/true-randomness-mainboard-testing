import struct
import ctypes
from dataclasses import dataclass

import serial


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


def main():
    c = Command()
    c.motor1 = 250
    c.motor2 = 250
    c.motor3 = 250
    s = serial.Serial('COM3')
    s.write(c.pack())
    out = s.read(10)
    f = Command()
    f.unpack(out)
    print(f)


if __name__ == '__main__':
    main()
