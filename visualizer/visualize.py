"""
Visualize data points from 3D scanner.
"""

import math
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


# Convert voltages to Arduino readings
DATASHEET_READINGS = list(map(lambda v: v*1023/5, [2.5, 2, 1.5, 1.25, 1,
                                                    0.75, 0.5]))
DATASHEET_DISTANCES = [20, 30, 40, 50, 60, 90, 130]


def find_fit(readings, distances):
    """
    Find a rational curve fit for measured readings against known distances.

    Args:
        readings: A list of numbers representing readings.
        distances: A list of known distances.

    Returns:
        A tuple of coefficients (a and b) for a rational curve fit.
    """
    def rational_fit(x, a, b):
        return a/(b + x)
    param, _ = curve_fit(rational_fit, readings, distances)
    return tuple(param)


def reading_to_distance(reading, fit):
    """
    Convert voltage to a distance in centemeters.

    Args:
        reading: A number representing a voltage reading from the distance
            sensor, between 0 and 1023.
        fit: A tuple containing the coefficients a and b for a rational curve fit.

    Returns:
        A float representing a distance in centemeters.
    """
    a, b = fit
    return a/(b + reading)


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


def process_raw_point(point, fit, offset):
    """
    Process a raw point from the scan program.

    Convert raw point from (pan, tilt, voltage) to (x, y, z).

    Args:
        point: A tuple of three ints representing (pan, tilt, voltage).
        fit: A tuple containg coefficients a and b for a rational fit.
        offset: A number representing the distance of the sensor from the
            center of the tilt/pan mechanism.

    Returns:
        A tuple of three numbers representing a position in x, y, z.
    """
    pan = math.radians(point[0])
    tilt = math.radians(90 - point[1])
    distance = reading_to_distance(point[2], fit)
    return spherical_to_cartesian((pan, tilt, distance))


def process_raw_points(points, fit, offset=0):
    """
    Process raw points from the scan program.

    Converts from spherical coordinates with voltages as distance to Cartesian
    coordinates in centemeters.

    Filters out points where no object was detected (reading below threshold).

    Args:
        points: A list of tuples containing three ints. These ints represent
            pan, tilt, and the analogRead() result from the distance sensor.
        fit: A tuple of coefficients a and b for a rational fit.
        offset: A number representing the distance of the sensor from the
            center of the tilt/pan mechanism.

    Returns:
        A list of tuples containing three numbers representing points in
        (x, y, z).
    """
    return [process_raw_point(point, fit, offset)
            for point in points]


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


def plot_raw_data(raw_points, fit):
    """
    Produce a plot from raw data points.

    Args:
        points: A list of tuples containing raw datapoints.
        fit: A tuple containing coefficients a and b for a rational fit.
    """
    plot_data(process_raw_points(raw_points, fit))
