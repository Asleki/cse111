# Ever wondered how much air fits inside your car's tires?
# This program takes the tire's width, aspect ratio, and wheel diameter as input
# and calculates the approximate volume of air inside.
#
# But wait, there's more! After calculating the volume, the program will also
# show you a selection of available tire volumes (including the one you just calculated)
# with their prices, in case you're looking to buy.
#
# If you decide to purchase, you can select a tire, and the program will ask for
# your preferred contact method (phone or email) and your details so we can process your order.
#
# The program keeps a record of all tire calculations and any orders placed in a file named 'volumes.txt'.
# Each entry in this file will include the date of the calculation/order, the tire dimensions,
# the calculated volume, and if an order was placed, the volume of the tire ordered and
# the customer's contact information.
# If you enter "no" anything other than 'yes' when asked about buying, the program will print
# thank you for your inquiry and close without recording any order details.


import math
from datetime import datetime
import random

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

def generate_tire_suggestions(calculated_volume):
    """
    Generates a list of tire volumes, including the calculated volume.

    Args:
        calculated_volume (float): The calculated tire volume.

    Returns:
        list: A list of five or more tire volumes, including the calculated one.
    """
    # Initialize an empty set to store unique tire volume suggestions
    # and add the user's calculated volume (rounded).
    suggestions = set()
    suggestions.add(round(calculated_volume, 2))  # Ensure the calculated volume is included
    while len(suggestions) < 5:
        # Generate random volumes within a reasonable range
        random_volume = round(random.uniform(15, 50), 2)
        suggestions.add(random_volume)
    return list(suggestions)

def display_tire_prices(suggested_volumes):
    """
    Displays prices for the suggested tire volumes.

    Args:
        suggested_volumes (list): A list of suggested tire volumes.

    Returns:
        dict: A dictionary where keys are tire volumes and values are their prices.
    """
    tire_prices = {}
    for volume in suggested_volumes:
        # Assign random prices 
        tire_prices[volume] = round(random.uniform(50, 200), 2)
    return tire_prices

while True:
    try:
        width_str = input("Enter the width of the tire in mm (ex 205): ")
        width = int(width_str)
        aspect_ratio_str = input("Enter the aspect ratio of the tire (ex 60): ")
        aspect_ratio = int(aspect_ratio_str)
        diameter_str = input("Enter the diameter of the wheel in inches (ex 15): ")
        diameter = int(diameter_str)
        volume = calculate_tire_volume(width, aspect_ratio, diameter)
        print(f"The approximate volume is {volume:.2f} liters")

        # Generate tire suggestions
        available_tires = generate_tire_suggestions(volume)
        print("\nAvailable tire volumes (liters):")
        for i, tire_volume in enumerate(available_tires):
            print(f"{i+1}. {tire_volume}")

        buy_choice = input("Do you wish to buy a tire with these dimensions? (yes/no): ").lower()

        if buy_choice == "yes":
            tire_prices = display_tire_prices(available_tires)
            print("\nTire prices:")
            for i, (vol, price) in enumerate(tire_prices.items()):
                print(f"{i+1}. Volume: {vol} liters, Price: ${price:.2f}")

            while True:
                try:
                    selection = int(input("Select the tire number you wish to buy: "))
                    if 1 <= selection <= len(available_tires):
                        selected_tire_volume = available_tires[selection - 1]
                        print(f"\nYou have successfully selected {selected_tire_volume:.2f} liters.")
                        break
                    else:
                        print("Invalid selection. Please enter a number from the list.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            contact_method = ""
            while contact_method not in ["phone", "email"]:
                contact_method = input("Please provide your contact method (phone or email): ").lower()
                if contact_method not in ["phone", "email"]:
                    print("Invalid contact method. Please enter 'phone' or 'email'.")

            if contact_method == "phone":
                phone_number = input("Enter your phone number: ")
                contact_details = phone_number
            else:
                email = input("Enter your email address: ")
                contact_details = email

            print("Thanks for placing your order, you'll be contacted about how to receive your Item.")

        else:
            print("Thank you for your inquiry.")

        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Open the volumes.txt file in append mode
        with open("volumes.txt", "at") as volumes_file:
            # Append the data to the file
            volumes_file.write(f"{current_date}, {width}, {aspect_ratio}, {diameter}, {volume:.2f}\n")
            if buy_choice == "yes":
                volumes_file.write(f"Order placed for: {selected_tire_volume:.2f} liters, Contact: {contact_method} - {contact_details}\n")

        break  # Exit the loop if the input is valid
    except ValueError:
        print("Invalid input. Please enter integer values for width, aspect ratio, and diameter.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
# Copyright 2025. Alex Malunda. All rights reserved.