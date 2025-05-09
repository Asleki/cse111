# This program reads from the keyboard the three numbers for a tire and computes and outputs
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

while True:
    try:
        width_str = input("Enter the width: ")
        width = int(width_str)
        aspect_ratio_str = input("Enter the aspect ratio: ")
        aspect_ratio = int(aspect_ratio_str)
        diameter_str = input("Enter the diameter: ")
        diameter = int(diameter_str)
        volume = calculate_tire_volume(width, aspect_ratio, diameter)
        print(f"The approximate volume is {volume:.2f} liters")
        break  # Exit the loop if the input is valid
    except ValueError:
        print("Invalid input. Please enter integer values for width, aspect ratio, and diameter.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
