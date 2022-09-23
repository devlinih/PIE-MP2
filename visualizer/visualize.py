"""
Visualize data points from 3D scanner.
"""

import math
from matplotlib import pyplot as plt


def reading_to_voltage(reading):
    """
    Convert Arduino analogRead() to a voltage.

    Assumes 10 bit.
    """
    return reading * (5/1023)


def voltage_to_reading(voltage):
    """
    Convert a voltage to an Arduino reading.

    Assumes 10 bit.
    """
    return voltage * (1023/5)


# TODO: Refactor the whole voltage to distance system. Since we need to
# calibrate anyways, we can just use Arduino readings.
def voltage_to_distance(voltage):
    """
    Convert voltage to a distance in centemeters.

    Args:
        voltage: A number representing a voltage reading from the distance
            sensor.

    Returns:
        A float representing a distance in centemeters.
    """
    a = 217.7
    b = 1.044
    return a * math.exp(-b * voltage)


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
    pan, tilt, distance = point

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
    pan = math.radians(point[0])
    tilt = math.radians(90 - point[1])
    distance = voltage_to_distance(reading_to_voltage(point[2]))
    return spherical_to_cartesian((pan, tilt, distance))


def process_raw_points(points, cutoff_voltage=0.5, offset=0):
    """
    Process raw points from the scan program.

    Converts from spherical coordinates with voltages as distance to Cartesian
    coordinates in centemeters.

    Filters out points where no object was detected (reading below threshold).

    Args:
        points: A list of tuples containing three ints. These ints represent
            pan, tilt, and the analogRead() result from the distance sensor.
        cutoff_voltage: An int between 0 and 1023 representing the cutoff point
            where a reading is considered not a real point.
        offset: A number representing the distance of the sensor from the
            center of the tilt/pan mechanism.

    Returns:
        A list of tuples containing three numbers representing points in
        (x, y, z).
    """
    # This code is a mess
    threshold = voltage_to_reading(cutoff_voltage)

    return [process_raw_point(point, offset)
            for point in points]
            # if point[2] >= threshold]


def plot_data(points):
    """
    Produce a plot of processed data points.

    Args:
        points: A list of tuples containing processed datapoints.
    """
    # "unzip" a list of tuples into individual tuples.
    x, y, z = zip(*points)

    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot(projection="3d")
    ax.scatter(x, y, z)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


def plot_raw_data(raw_points):
    """
    Produce a plot from raw data points.

    Args:
        points: A list of tuples containing raw datapoints.
    """
    plot_data(process_raw_points(raw_points))
