# water_flow.py
# Exceeded Requirements:
# 1. Defined constants for gravity, water density, and dynamic viscosity.
# 2. Implemented a kPa_to_psi conversion function.
# 3. Printed the final pressure in both kPa and psi in the main function.

EARTH_ACCELERATION_OF_GRAVITY = 9.80665
WATER_DENSITY = 998.2
WATER_DYNAMIC_VISCOSITY = 0.0010016

def water_column_height(tower_height, tank_height):
    """Calculates and returns the height of a column of water."""
    h = tower_height + (3 * tank_height) / 4
    return h

def pressure_gain_from_water_height(height):
    """Calculates and returns the pressure caused by Earth's gravity."""
    P = (WATER_DENSITY * EARTH_ACCELERATION_OF_GRAVITY * height) / 1000
    return P

def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor, fluid_velocity):
    """Calculates and returns the water pressure lost due to friction within a pipe."""
    P = -friction_factor * pipe_length * WATER_DENSITY * (fluid_velocity ** 2) / (2000 * pipe_diameter)
    return P

def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """Calculates the water pressure lost because of fittings in a pipeline."""
    P = -0.04 * WATER_DENSITY * (fluid_velocity ** 2) * quantity_fittings / 2000
    return P

def reynolds_number(hydraulic_diameter, fluid_velocity):
    """Calculates and returns the Reynolds number for a pipe."""
    R = (WATER_DENSITY * hydraulic_diameter * fluid_velocity) / WATER_DYNAMIC_VISCOSITY
    return R

def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    """Calculates the water pressure lost because of water moving from a larger to a smaller pipe."""
    k = (0.1 + (50 / reynolds_number)) * ((larger_diameter / smaller_diameter) ** 4 - 1)
    P = -k * WATER_DENSITY * (fluid_velocity ** 2) / 2000
    return P

def kPa_to_psi(kpa):
    """Converts pressure from kilopascals (kPa) to pounds per square inch (psi)."""
    psi = kpa * 0.145038
    return psi

def main():
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))

    water_height = water_column_height(tower_height, tank_height)
    pressure_kpa = pressure_gain_from_water_height(water_height)

    diameter = 0.28687  # PVC_SCHED80_INNER_DIAMETER
    friction = 0.013    # PVC_SCHED80_FRICTION_FACTOR
    velocity = 1.65     # SUPPLY_VELOCITY
    reynolds = reynolds_number(diameter, velocity)
    loss = pressure_loss_from_pipe(diameter, length1, friction, velocity)
    pressure_kpa += loss

    loss = pressure_loss_from_fittings(velocity, quantity_angles)
    pressure_kpa += loss

    loss = pressure_loss_from_pipe_reduction(diameter, velocity, reynolds, 0.048692) # HDPE_SDR11_INNER_DIAMETER
    pressure_kpa += loss

    diameter = 0.048692 # HDPE_SDR11_INNER_DIAMETER
    friction = 0.018   # HDPE_SDR11_FRICTION_FACTOR
    velocity = 1.75    # HOUSEHOLD_VELOCITY
    loss = pressure_loss_from_pipe(diameter, length2, friction, velocity)
    pressure_kpa += loss

    pressure_psi = kPa_to_psi(pressure_kpa)

    print(f"Pressure at house: {pressure_kpa:.1f} kilopascals")
    print(f"Pressure at house: {pressure_psi:.1f} psi")

if __name__ == "__main__":
    main()
    

# Copyright 2025. Alex Malunda. All rights reserved.