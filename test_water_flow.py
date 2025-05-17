# test_water_flow.py
from pytest import approx
import pytest
from water_flow import water_column_height, pressure_gain_from_water_height, pressure_loss_from_pipe
from water_flow import pressure_loss_from_fittings, reynolds_number, pressure_loss_from_pipe_reduction
from water_flow import kPa_to_psi

def test_water_column_height():
    """Verify that the water_column_height function returns correct results."""
    assert water_column_height(0.0, 0.0) == approx(0.0)
    assert water_column_height(0.0, 10.0) == approx(7.5)
    assert water_column_height(25.0, 0.0) == approx(25.0)
    assert water_column_height(48.3, 12.8) == approx(57.9)

def test_pressure_gain_from_water_height():
    """Verify that the pressure_gain_from_water_height function returns correct results."""
    assert pressure_gain_from_water_height(0.0) == approx(0.0, abs=0.001)
    assert pressure_gain_from_water_height(30.2) == approx(295.628, abs=0.001)
    assert pressure_gain_from_water_height(50.0) == approx(489.450, abs=0.001)

def test_pressure_loss_from_pipe():
    """Verify that the pressure_loss_from_pipe function returns correct results."""
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.018, 1.75) == approx(-113.008, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.000, 1.75) == approx(0.000, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.018, 0.00) == approx(0.000, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.018, 1.75) == approx(-113.008, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.018, 1.65) == approx(-100.462, abs=0.001)
    assert pressure_loss_from_pipe(0.2868701, 1000.0, 0.013, 1.65) == approx(-61.576, abs=0.001)
    assert pressure_loss_from_pipe(0.2868701, 800.75, 0.013, 1.65) == approx(-49.312, abs=0.005)

def test_pressure_loss_from_fittings():
    """Verify that the pressure_loss_from_fittings function returns correct results."""
    assert pressure_loss_from_fittings(0.0, 3) == approx(0.0, abs=0.001)
    assert pressure_loss_from_fittings(1.65, 0) == approx(0.0, abs=0.001)
    assert pressure_loss_from_fittings(1.65, 2) == approx(-0.109, abs=0.001)
    assert pressure_loss_from_fittings(1.75, 2) == approx(-0.122, abs=0.001)
    assert pressure_loss_from_fittings(1.75, 5) == approx(-0.306, abs=0.001)

def test_reynolds_number():
    """Verify that the reynolds_number function returns correct results."""
    assert reynolds_number(0.048692, 0.0001) == approx(4.861, abs=0.1)
    assert reynolds_number(0.048692, 1.65) == approx(80069.1, abs=1.0)
    assert reynolds_number(0.048692, 1.75) == approx(84922.1, abs=1.0)
    assert reynolds_number(0.2868701, 1.65) == approx(471729.1, abs=1.0)
    assert reynolds_number(0.2868701, 1.75) == approx(500318.1, abs=1.0)

def test_pressure_loss_from_pipe_reduction():
    """Verify that the pressure_loss_from_pipe_reduction function returns correct results."""
    reynolds_low = reynolds_number(0.28687, 0.001)
    assert pressure_loss_from_pipe_reduction(0.28687, 0.001, reynolds_low, 0.048692) == approx(0.000, abs=0.001)
    reynolds_mid = reynolds_number(0.28687, 1.65)
    assert pressure_loss_from_pipe_reduction(0.28687, 1.65, reynolds_mid, 0.048692) == approx(-163.744, abs=0.001)
    reynolds_high = reynolds_number(0.28687, 1.75)
    assert pressure_loss_from_pipe_reduction(0.28687, 1.75, reynolds_high, 0.048692) == approx(-184.182, abs=0.001)

def test_kPa_to_psi():
    """Verify that the kPa_to_psi function returns correct results."""
    assert kPa_to_psi(0) == approx(0.0, abs=0.001)
    assert kPa_to_psi(100) == approx(14.5038, abs=0.001)
    assert kPa_to_psi(250) == approx(36.2595, abs=0.001)
    assert kPa_to_psi(-50) == approx(-7.2519, abs=0.001)

# Call the main function that is part of pytest
pytest.main(["-v", "--tb=line", "-rN", __file__])

# Copyright 2025. Alex Malunda. All rights reserved.