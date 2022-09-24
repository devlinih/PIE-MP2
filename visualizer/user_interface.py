"""
Command User Interface for scanner.
"""

import cmd
import sys  # For interface
import serial
import time

from arduino import (guess_port,
                     send_command,
                     ARDUINO_TIMEOUT,
                     BAUDRATE,)
from visualize import plot_raw_data

INITTIME = 3


class ArduinoShell(cmd.Cmd):
    """
    Define command user interface for Arduino scanner.
    """
    intro = "Welcome to 3D scanner shell. Type help or ? to list commands.\n"
    prompt = "command> "
    ser = None  # Will be a serial connection
    data = [(0, 0, 0)]  # Will be the scan data

    def preloop(self):
        """
        Initialize before loop starts.
        """
        port = guess_port()
        self.ser = serial.Serial(port, BAUDRATE,
                                 timeout=ARDUINO_TIMEOUT)
        print(f"Connecting to {port}, please wait")
        time.sleep(INITTIME)

    def postloop(self):
        """
        Close after exit.
        """
        self.ser.close()
        print("Thank you for using our 3D scanner!")

    # Commands

    def do_scan(self, arg):
        """
        Start scan operation.
        """
        self.data = send_command(self.ser, "SCAN")

    def do_plot(self, arg):
        """
        Visualize data in a matplotlib plot.
        """
        plot_raw_data(self.data)

    def do_exit(self, arg):
        """
        End program.
        """
        return True

    def do_EOF(self, arg):
        """
        End program on C-d.
        """
        return True


if __name__ == '__main__':
    ArduinoShell().cmdloop()
