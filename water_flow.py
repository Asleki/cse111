# water_flow.py

def water_column_height(tower_height, tank_height):
    """Calculates and returns the height of a column of water.

    Args:
        tower_height (float): The height of the tower in meters.
        tank_height (float): The height of the walls of the tank in meters.

    Returns:
        float: The height of the water column in meters.
    """
    h = tower_height + (3 * tank_height) / 4
    return h

def pressure_gain_from_water_height(height):
    """Calculates and returns the pressure caused by Earth's gravity
    pulling on the water stored in an elevated tank.

    Args:
        height (float): The height of the water column in meters.

    Returns:
        float: The pressure in kilopascals.
    """
    rho = 998.2  # density of water in kilogram / meter3
    g = 9.80665  # acceleration from Earth's gravity in meter / second2
    P = (rho * g * height) / 1000
    return P

def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor, fluid_velocity):
    """Calculates and returns the water pressure lost due to friction within a pipe.

    Args:
        pipe_diameter (float): The diameter of the pipe in meters.
        pipe_length (float): The length of the pipe in meters.
        friction_factor (float): The pipe's friction factor.
        fluid_velocity (float): The velocity of the water in meters / second.

    Returns:
        float: The lost pressure in kilopascals.
    """
    rho = 998.2  # density of water in kilogram / meter3
    P = -friction_factor * pipe_length * rho * (fluid_velocity ** 2) / (2000 * pipe_diameter)
    return P

if __name__ == "__main__":
    # You can add some example usage here if you want
    pass

# Copyright 2025. Alex Malunda. All rights reserved.