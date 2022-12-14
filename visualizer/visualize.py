"""
Visualize data points from 3D scanner.
"""

import math

from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# Convert voltages to Arduino readings
DEFAULT_READINGS = [520, 389, 272, 206]
DEFAULT_DISTANCES = [15, 30, 45, 60]


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


def plot_fit_curve(fit):
    """
    Produce a plot of the fit curve.

    Args:
        fit: A tuple representing coefficients a and b for rational curve fit.
    """
    readings = range(80, 1023)
    voltages = [reading*5/1023 for reading in readings]
    distances = [reading_to_distance(reading, fit) for reading in readings]

    fig = plt.figure()
    plt.plot(voltages, distances, "r")
    plt.xlim([0, 5])
    plt.ylim([0, 200])
    plt.xlabel("Measured Voltage (V)", fontsize=12)
    plt.ylabel("Calculated Distance (cm)", fontsize=12)
    plt.show()


def plot_fit_curve_error(fit, readings, distances):
    """
    Produce a plot of the fit curve against datapoints.

    Args:
        fit: A tuple representing coefficients a and b for rational curve fit.
        readings: Known Arduino readings.
        distances: Known measured distances.
    """
    readings_theory = range(80, 1023)
    voltages_theory = [reading*5/1023 for reading in readings_theory]
    distances_theory = [reading_to_distance(reading, fit)
                        for reading in readings_theory]

    voltages = [reading*5/1023 for reading in readings]

    fig = plt.figure()
    plt.plot(voltages_theory, distances_theory, "r",
             label="Calibration Curve")
    plt.plot(voltages, distances, "ok",
             label="Actual Datapoints")
    plt.legend()
    plt.xlim([0, 5])
    plt.ylim([0, 200])
    plt.xlabel("Measured Voltage (V)", fontsize=12)
    plt.ylabel("Calculated Distance (cm)", fontsize=12)
    plt.show()


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


def process_raw_point(point, fit):
    """
    Process a raw point from the scan program.

    Convert raw point from (pan, tilt, voltage) to (x, y, z).

    Args:
        point: A tuple of three ints representing (pan, tilt, voltage).
        fit: A tuple containg coefficients a and b for a rational fit.

    Returns:
        A tuple of three numbers representing a position in x, y, z.
    """
    pan = math.radians(point[0] + 8)
    tilt = math.radians(point[1] + 30)
    distance = reading_to_distance(point[2], fit)
    return spherical_to_cartesian((pan, tilt, distance))


def process_raw_points(points, fit, threshold):
    """
    Process raw points from the scan program.

    Converts from spherical coordinates with voltages as distance to Cartesian
    coordinates in centemeters.

    Filters out points where no object was detected (reading below threshold).

    Args:
        points: A list of tuples containing three ints. These ints represent
            pan, tilt, and the analogRead() result from the distance sensor.
        fit: A tuple of coefficients a and b for a rational fit.

    Returns:
        A list of tuples containing three numbers representing points in
        (x, y, z).
    """
    return [process_raw_point(point, fit)
            for point in points
            if point[2] >= threshold]


def plot_data(points):
    """
    Produce a plot of processed data points.

    Args:
        points: A list of tuples containing processed datapoints.
    """
    # "unzip" a list of tuples into individual tuples.
    try:
        x, y, z = zip(*points)
    except:
        print("Error, no datapoints (try adjusting threshold)")
        return

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.scatter(x, y, z)
    ax.axis("equal")
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


def plot_raw_data(raw_points, fit, threshold):
    """
    Produce a plot from raw data points.

    Args:
        points: A list of tuples containing raw datapoints.
        fit: A tuple containing coefficients a and b for a rational fit.
    """
    plot_data(process_raw_points(raw_points, fit, threshold))
