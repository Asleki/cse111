#This program reads from the keyboard the three numbers for a tire and computes and outputs 
# the volume of space inside that tire.

import math
def calculate_tire_volume(width, aspect_ratio, diameter):
    """
    Calculates the approximate volume of space inside a tire.

    Args:
        width (int): The width of the tire in millimeters.
        aspect_ratio (int): The aspect ratio of the tire.
        diameter (int): The diameter of the wheel in inches.

    Returns:
        float: The approximate volume of the tire in liters.
    """
    v = (math.pi * width**2 * aspect_ratio * (width * aspect_ratio + 2540 * diameter)) / 10000000000
    return v
   
width = int(input("Enter the width: "))
aspect_ratio = int(input("Enter the aspect ratio: "))
diameter = int(input("Enter the diameter: "))
volume = calculate_tire_volume(width, aspect_ratio, diameter)
print(f"The approximate volume is {volume:.2f} liters")
