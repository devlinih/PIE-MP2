"""
Connect to an Arduino running PIE MP2 Firmware.

All Arduino related code is here.
"""

import ast
import serial
import serial.tools.list_ports as list_ports

BAUDRATE = 115200
ARDUINO_TIMEOUT = 3

# List of Arduino IDs provided by Brad
# https://github.com/bminch/PIE/blob/main/Serial_cmd.py
ARDUINO_IDS = ((0x2341, 0x0043), (0x2341, 0x0001),
               (0x2A03, 0x0043), (0x2341, 0x0243),
               (0x0403, 0x6001), (0x1A86, 0x7523))



def guess_port():
    """
    Try to find an Arduino connected to the computer.

    Returns:
        A string representing the port of the first Arduino found. Returns the
        empty string if no Arduino is found.
    """
    devices = list_ports.comports()
    for device in devices:
        if (device.vid, device.pid) in ARDUINO_IDS:
            return device.device
    return ""


def scan(ser:serial.Serial):
    """
    Send a SCAN command to the Arduino.

    Raises an exception if no port is specified and no Arduino is found.

    Args:
        ser: A serial connection to an Arduiono.

    Returns:
        A list of tuples representing datapoints.
    """
    ser.write(b"SCAN\n")
    data = ser.readline()
    # data is a bytestring, do some stuff to return it as a list
    return ast.literal_eval(data.decode("utf-8").strip())


# TODO: Add code to interface with calibration command
