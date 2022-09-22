"""
Visualize data points from 3D scanner.
"""

import math
from matplotlib import pyplot as plt


def voltage_to_distance(voltage):
    """
    Convert reading from Arduino analogWrite to a distance in inches.

    Args:
        voltage: An integer from 0 to 4095 representing a reading from the
            distance sensor.

    Returns:
        A float representing a distance in inches.
    """
    # TODO: Need to figure out transfer function.
    return voltage


def spherical_to_cartesian(point):
    """
    Convert a point in spherical coordinates to a point in cartesian coordinates.

    Args:
        point: A tuple of three numbers in the form (pan, tilt, distance),
            where pan and tilt are in degrees.

    Returns:
        A tuple of three numbers in the form (x, y, z). The units are dependant
        on the unit of the originally passed distance.
    """
    pan = math.radians(point[0])  # theta
    tilt = math.radians(point[1]) # phi
    distance = point[2]           # rho

    x = distance * math.sin(tilt) * math.cos(pan)
    y = distance * math.sin(tilt) * math.sin(pan)
    z = distance * math.cos(tilt)

    return x, y, z


def process_raw_point(point, offset):
    """
    Process a raw point from the scan program.

    Convert raw point from (pan, tilt, voltage) to (x, y, z).

    Args:
        point: A tuple of three ints representing (pan, tilt, voltage).
        offset: A number representing the distance of the sensor from the
            center of the tilt/pan mechanism.

    Returns:
        A tuple of three numbers representing a position in x, y, z.
    """
    pan, faux_tilt, voltage = point
    distance = voltage_to_distance(voltage) + offset
    tilt = 90 - faux_tilt # 0 degrees should be vertical, not horizontal.

    return spherical_to_cartesian((pan, tilt, offset))


def process_raw_points(points, cutoff_voltage, offset):
    """
    Process raw points from the scan program.

    Converts from spherical coordinates with voltages as distance to Cartesian
    coordinates in inches.

    Filters out points where no object was detected (reading below threshold).

    Args:
        points: A list of tuples containing three ints. These ints represent
            pan, tilt, and the analogRead() result from the distance sensor.
        cutoff_voltage: An int between 0 and 4095 representing the cutoff point
            where a reading is considered not a real point.
        offset: A number representing the distance of the sensor from the
            center of the tilt/pan mechanism.

    Returns:
        A list of tuples containing three numbers representing points in
        (x, y, z).
    """
    return [process_raw_point(point, offset)
            for point in points
            if point[2] <= cutoff_voltage]
