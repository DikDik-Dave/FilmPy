import math
import numpy


def angle_to_radians(angle) -> float:
    """
    Converts an angles into a radians

    :param angle: Angle in degrees
    :return: Radian value of angle
    """
    return angle * (numpy.pi / 180)

def color_distance(color1, color2):
    """
    Calculate the Euclidean distance between two RGB colors

    :param color1: 1st color to compare
    :param color2: 2nd color to compare

    :return float: distance between the two colors
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)

def get_nearest_color(color_to_compare, palette:list):
    """
    Finds the nearest RGB color in the RBG palette to the color_to_compare provided

    :param color_to_compare: Color we want to find the nearest color for
    :param palette: List of RGB colors that make up the palette to compare against

    :return tuple: RBG color from the palette nearest to the given color
    """
    nearest_color = None
    min_distance = float('inf')
    for palette_color in palette:
        distance = color_distance(color_to_compare, palette_color)
        if distance < min_distance:
            min_distance = distance
            nearest_color = palette_color
    return nearest_color