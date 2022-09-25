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
from visualize import (plot_raw_data,
                       DEFAULT_READINGS,
                       DEFAULT_DISTANCES,
                       find_fit,
                       plot_fit_curve)

INITTIME = 3


class ArduinoShell(cmd.Cmd):
    """
    Define command user interface for Arduino scanner.
    """
    intro = "Welcome to 3D scanner shell. Type help or ? to list commands.\n"
    prompt = "command> "
    ser = None  # Will be a serial connection
    data = [(0, 0, 0)]  # Will be the scan data
    fit = find_fit(DEFAULT_READINGS, DEFAULT_DISTANCES)

    # Collect calibration data
    cal_readings = []
    cal_distances = []

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

    # Arduino commands
    def do_scan1(self, arg):
        """
        Start scan operation.
        """
        self.data = send_command(self.ser, "SCAN1")

    def do_scan2(self, arg):
        """
        Start scan operation.
        """
        self.data = send_command(self.ser, "SCAN2")

    def do_calibrate(self, arg):
        """
        Grab a datapoint for calibration at distance ARG.

        calibrate DISTANCE
        """
        try:
            distance = int(arg.strip())
        except:
            print("Invalid distance argument, assuming 20cm")
            distance = 20

        reading = send_command(self.ser, "CALIBRATE")[0][2]
        self.cal_readings.append(reading)
        self.cal_distances.append(distance)

        print(f"Distances {self.cal_distances}")
        print(f"Readings {self.cal_readings}")

    # Plot commands

    def do_new_calibration_fit(self, arg):
        """
        Generate new fit data from collected calibration points.
        """
        self.fit = find_fit(self.cal_readings, self.cal_distances)

    def do_show_calibration_fit(self, arg):
        """
        Plot the current calibration curve.
        """
        plot_fit_curve(self.fit)

    def do_plot(self, arg):
        """
        Visualize data in a matplotlib plot.

        Takes a threshold argument.
        """
        try:
            threshold = int(arg.strip())
        except:
            threshold = 50

        plot_raw_data(self.data, self.fit, threshold)

    # Exit commands
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
