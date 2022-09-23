"""
Connect to an Arduino running PIE MP2 Firmware.
"""

import ast
import serial
import serial.tools.list_ports as list_ports
import time

BAUDRATE = 115200
WAITTIME = 3

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


def scan(port=""):
    """
    Send a SCAN command to the Arduino.

    Raises an exception if no port is specified and no Arduino is found.

    Args:
        port: A serial port to connect to. If not specified, try to find an
            Arduino.

    Returns:
        A list of tuples representing datapoints.
    """
    if port == "":
        port = guess_port()

    with serial.Serial(port, BAUDRATE, timeout=1) as ser:
        # Sleep 1 second to let Arduino get ready
        time.sleep(WAITTIME) # seconds to wait
        ser.write(b"SCAN\n")

        data = ser.readline()
        # data is a bytestring, do some stuff to return it as a list
        return ast.literal_eval(data.decode("utf-8").strip())
