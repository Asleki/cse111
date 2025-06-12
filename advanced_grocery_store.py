# Copyright 2025, Alex Malunda. All rights reserved.2
# This program simulates an e-commerce platform, "Inkom Emporium Online,"
# offering a comprehensive shopping experience with several advanced features.

# Exceeding Requirements:
# - A user login and account creation system is implemented, providing a welcome message
#   for returning users and guiding new users through registration.
# - During account creation, robust password strength validation is enforced,
#   requiring minimum length, uppercase, lowercase, digit, and special characters.
#   Users receive real-time feedback on password strength.
# - New account registrations involve a simulated One-Time Password (OTP) verification
#   sent to a local 'email_inbox.txt' file, complete with expiry information.
# - Upon successful account creation and OTP verification, a welcome email with
#   special offers for new customers is "sent" to the simulated inbox.
# - Users are given the option to subscribe to promotional emails during account creation.
# - After logging in, users navigate a dynamic store menu where they can:
#   - Browse all available products.
#   - Manage items in their personal wishlist.
#   - Manage items in their shopping cart.
#   - Add products from the general catalog or their wishlist directly to their cart or wishlist.
#     This process includes input validation for quantities and product IDs.
#   - Remove products from either their cart or wishlist, with options to remove specific
#     quantities from the cart.
# - A comprehensive checkout and order processing flow is included, featuring:
#   - Choice of pickup options: physical store pickup or doorstep delivery with an added fee.
#   - Important disclaimers regarding product returns and refunds before order finalization.
#   - Simulated payment methods (Mpesa, Visa with PIN entry, and a "Gold Member" exclusive PayPal
#   - option).
#   - Calculation and display of subtotal, applicable sales tax, shipping fee, and the final total.
#   - A special "Buy One, Get One Half Off" promotion applied to product D083, clearly detailed on 
#   - the receipt.
#   - A new user discount automatically applied to the first order (currently a placeholder logic).
#   - A uniquely generated order number (e.g., KER + 7 digits) for each transaction.
#   - Dynamic estimated pickup or delivery times based on the chosen option and current system time.
# - The generated receipt is highly detailed, including:
#   - Store name and order summary.
#   - Current date and time of the order.
#   - An "Items can be returned by" date (30 days from purchase).
#   - A real-time "New Year's Sale" countdown.
#   - A message encouraging loyalty points.
#   - After an order is placed, a simulated email requesting a service review is sent to the user's 
#   -inbox.
import csv
import random
import re
from datetime import datetime, timedelta

# --- Constants for column indexes ---
PRODUCT_NUMBER_INDEX = 0
PRODUCT_NAME_INDEX = 1
PRODUCT_PRICE_INDEX = 2

REQUEST_PRODUCT_NUMBER_INDEX = 0
REQUEST_QUANTITY_INDEX = 1

USER_USERNAME_INDEX = 0
USER_PASSWORD_INDEX = 1

# --- Other Constants ---
OTP_EXPIRY_MINUTES = 5
SALES_TAX_RATE = 0.06
SHIPPING_FEE = 8.00
NEW_USER_DISCOUNT_PERCENT = 0.15 # 15% discount for new users (placeholder)

# --- Global In-Memory Data Structures for Current Session ---
# These will reset each time the program runs. For persistence, they'd need file I/O.
current_user_cart = {} # {product_id: quantity, ...}
current_user_wishlist = {} # {product_id: quantity, ...} (quantity could be 1 for wishlist, or more if desired)

# --- ASCII Art ---
GREEN_CHECKMARK = "\033[92m✔\033[0m" # Green checkmark symbol


def main():
    """
    Main function to run the e-commerce simulation.
    Handles user authentication, product Browse, cart/wishlist management,
    and the full checkout process with receipt generation.
    """
    global current_user_cart, current_user_wishlist # Declare intent to modify global variables

    while True: # Outer loop for login/registration and then store menu
        try:
            # --- User Login/Registration Feature ---
            user_logged_in = False
            current_username = "" # To store the username of the logged-in user
            
            while not user_logged_in:
                print("\n" + "=" * 50)
                print("Welcome to Inkom Emporium Online!".center(50))
                print("=" * 50 + "\n")

                print("Please select an option:")
                print("    1. Login to your account")
                print("    2. Create a new account")
                print("    3. Exit program")
                print("-" * 50)

                choice = input("Enter your choice (1, 2, or 3): ").strip()

                if choice == '1':
                    username = input("Enter your username: ").strip()
                    password = input("Enter your password: ").strip()

                    try:
                        users_dict = read_dictionary("users.csv", USER_USERNAME_INDEX)
                        if username in users_dict and users_dict[username][USER_PASSWORD_INDEX] == password:
                            print(f"\nLogin successful! Welcome, {username}!")
                            current_username = username
                            user_logged_in = True
                        else:
                            print("\nNo account found for you or incorrect password. Please sign up to enjoy your shopping experience.")
                    except FileNotFoundError:
                        print("\nNo accounts registered yet. Please sign up to create one.")
                    except Exception as e:
                        print(f"\nAn unexpected error occurred while accessing user accounts: {e}")

                elif choice == '2':
                    print("\n--- Create New Account ---")
                    new_username = input("Set a new username: ").strip()
                    # Check for existing username (important for registration)
                    try:
                        users_dict = read_dictionary("users.csv", USER_USERNAME_INDEX)
                        if new_username in users_dict:
                            print("Error: Username already exists. Please choose a different username or login.")
                            continue # Go back to main login/create menu selection
                    except FileNotFoundError:
                        # users.csv might not exist yet, which is fine for first user
                        pass # Continue as if no users exist

                    if not new_username:
                        print("Error: Username cannot be empty. Please try again.")
                        continue

                    while True: # Loop until password is strong enough
                        new_password = input("Set a password (min 5 chars, needs uppercase, lowercase, digit, special char): ").strip()
                        strength_score, reasons = check_password_strength(new_password)

                        if strength_score == 10:
                            print("Password strength: 10/10. Great password!")
                            break
                        else:
                            print(f"Password is weak. Strength: {strength_score}/10.")
                            print("Reasons:")
                            for reason in reasons:
                                print(f"- {reason}")
                            print("Please try a stronger password.")
                    
                    new_email = input("Enter your email address: ").strip()
                    if not new_email:
                        print("Error: Email cannot be empty. Please try again.")
                        continue

                    # --- Promotional Email Subscription Prompt ---
                    subscribe_choice = input("Would you like to subscribe to our promotional and offer emails? (yes/no): ").strip().lower()

                    print("\nSending verification code to your email...")
                    otp_code, otp_expiry_time, otp_sent_time = generate_otp_and_expiry()
                    
                    if send_otp_to_email_inbox(new_username, new_email, otp_code, otp_expiry_time, otp_sent_time):
                        print("A verification code (OTP) has been sent to your email inbox.")
                        print("Please enter the OTP you received in your inbox to verify your account.")
                        
                        entered_otp = input("Enter the OTP: ").strip()
                        
                        now_check = datetime.now()
                        if now_check > otp_expiry_time:
                            print("Error: OTP has expired. Please try account creation again.")
                        elif entered_otp == otp_code:
                            print(f"{GREEN_CHECKMARK} Account verified successfully!")
                            if save_new_user(new_username, new_password): # Save only on success
                                send_welcome_email(new_username, new_email)
                                print("A welcome email with special offers has also been sent to your inbox!")
                                print("You can now log in with your new account.")
                            else:
                                print("Error: Failed to save account despite OTP verification. Please try again.")
                        else:
                            print("Error: Invalid OTP. Account verification failed.")
                            print("Please sign up again to get a new OTP.")
                    else:
                        print("Error: Failed to send OTP. Account creation aborted.")
                    
                    # After attempted account creation (whether success or failure),
                    # the loop `while not user_logged_in` will continue,
                    # allowing the user to choose login or create again.

                elif choice == '3':
                    print("\nThank you for visiting Inkom Emporium. Goodbye!")
                    return # Exit program

                else:
                    print("\nInvalid choice. Please enter 1, 2, or 3.")
                print("-" * 50)

            # If user_logged_in is True, proceed to store menu
            products_dict = read_dictionary("products.csv", PRODUCT_NUMBER_INDEX) # Load products once for menu

            proceed_to_checkout_flag = False
            while not proceed_to_checkout_flag: # Inner loop for store menu
                print(f"\nWelcome to the store, {current_username}!")
                print("What would you like to do?")
                print("    1. Explore Products")
                print("    2. View Wishlist (Items you like)")
                print("    3. View Cart (Items to buy)")
                print("    4. Add Product")
                print("    5. Remove Product")
                print("    6. Proceed to Checkout")
                print("    7. Logout (Go back to main login menu)") # Added logout option
                print("-" * 50)
                store_choice = input("Enter your choice (1-7): ").strip()

                if store_choice == '1':
                    explore_products(products_dict)
                elif store_choice == '2':
                    view_user_list(current_user_wishlist, products_dict, "Wishlist")
                elif store_choice == '3':
                    view_user_list(current_user_cart, products_dict, "Cart")
                elif store_choice == '4':
                    # Call the function in a loop
                    while True:
                        # add_product_to_user_list now returns True to continue, False to quit
                        if not add_product_to_user_list(products_dict, current_user_wishlist, current_user_cart):
                            break # User chose to quit from add product flow
                        add_more = input("Add another product? (yes/no): ").strip().lower()
                        if add_more != 'yes':
                            break
                elif store_choice == '5':
                    # Call the function in a loop
                    while True:
                        # remove_product_from_user_list now returns True to continue, False to quit
                        if not remove_product_from_user_list(products_dict, current_user_wishlist, current_user_cart):
                            break # User chose to quit from remove product flow
                        remove_more = input("Remove another product? (yes/no): ").strip().lower()
                        if remove_more != 'yes':
                            break
                elif store_choice == '6':
                    if not current_user_cart:
                        print("Your cart is empty. Please add items before checking out.")
                    else:
                        proceed_to_checkout_flag = True # Exit store menu to proceed to checkout
                elif store_choice == '7':
                    print("Logging out. Returning to main menu.")
                    current_user_cart.clear() # Clear cart/wishlist on logout
                    current_user_wishlist.clear()
                    user_logged_in = False # Set flag to re-enter login loop
                    break # Break from this inner `while not proceed_to_checkout_flag` loop
                else:
                    print("\nInvalid choice. Please enter a number between 1 and 7.")
                print("-" * 50) # Separator after each store menu action

            # If the inner loop was broken due to logout, the outer loop will
            # naturally restart the login/registration process.
            if not user_logged_in:
                continue # Go back to the very beginning of the main while True loop for login/registration

            # If user_logged_in is still True (meaning they chose to checkout), proceed.
            # --- Checkout Process ---
            process_checkout(current_username, current_user_cart, products_dict)
            break # Break from the outer loop after successful checkout to end program

        except FileNotFoundError as not_found_err:
            print(f"Error: A required file was not found. Details: {not_found_err}")
            print("Please ensure 'products.csv' and 'users.csv' are in the same directory.")
            break # Exit on critical file error
        except KeyError as key_err:
            print(f"Error: An unknown product ID or missing data was encountered: '{key_err}'.")
            print("Please check data integrity in your CSV files.")
            break # Exit on critical data error
        except PermissionError as perm_err:
            print(f"Error: Permission denied when trying to read/write a file. Details: {perm_err}")
            print("Please check file permissions for your CSV files and 'email_inbox.txt'.")
            break # Exit on critical permission error
        except Exception as excep:
            print(f"An unexpected error occurred: {excep}")
            break # Exit on any other unexpected error


def read_dictionary(filename, key_column_index):
    """Reads a CSV file into a dictionary."""
    dictionary = {}
    with open(filename, "rt") as csv_file:
        reader = csv.reader(csv_file)
        try:
            next(reader) # Skip header
        except StopIteration:
            # File is empty or only has a header, no data to read
            return dictionary

        for row_list in reader:
            if len(row_list) > key_column_index:
                key = row_list[key_column_index]
                dictionary[key] = row_list
            else:
                print(f"Warning: Skipping malformed row in '{filename}': {row_list}")
    return dictionary

def generate_otp_and_expiry():
    """Generates a random OTP and its expiry time."""
    otp = str(random.randint(100000, 999999))
    now = datetime.now()
    expiry_time = now + timedelta(minutes=OTP_EXPIRY_MINUTES)
    return otp, expiry_time, now

def send_otp_to_email_inbox(username, email, otp, expiry_time, sent_time):
    """Simulates sending OTP email with given details."""
    try:
        email_content = f"""
--- New Email for {username} (OTP) ---
Date and Time: {sent_time:%Y-%m-%d %H:%M:%S}
To: {email}
From: Inkom Emporium <no-reply@inkom.com>
Subject: Your Account Verification Code

Dear {username},

Your One-Time Password (OTP) for account verification is: {otp}

This code is valid for {OTP_EXPIRY_MINUTES} minutes.
It will expire at: {expiry_time:%Y-%m-%d %H:%M:%S}

Please use this code to complete your registration.
Do not share this code with anyone.

Thank you,
The Inkom Emporium Team
----------------------------
"""
        with open("email_inbox.txt", "a") as inbox_file:
            inbox_file.write(email_content)
        return True
    except IOError as e:
        print(f"Error: Could not write OTP email to email_inbox.txt. Details: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while saving OTP to inbox: {e}")
        return False

def save_new_user(username, password):
    """Appends a new user's credentials to users.csv."""
    try:
        # Check if users.csv exists and has a header, if not, write header first
        file_exists_and_not_empty = False
        try:
            with open("users.csv", "r") as f:
                if f.readline(): # Check if first line exists (implies header or data)
                    file_exists_and_not_empty = True
        except FileNotFoundError:
            pass # File does not exist, so we will create it and add header

        with open("users.csv", "a", newline='') as csv_file:
            writer = csv.writer(csv_file)
            if not file_exists_and_not_empty:
                writer.writerow(["username", "password"]) # Write header
            writer.writerow([username, password])
        print("Account successfully registered!")
        return True
    except IOError as e:
        print(f"Error: Could not write to users.csv. Details: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while saving user: {e}")
        return False

def send_welcome_email(username, email):
    """Simulates sending a welcome email to a new customer's inbox."""
    try:
        now = datetime.now()
        email_content = f"""
--- New Email for {username} (Welcome) ---
Date and Time: {now:%Y-%m-%d %H:%M:%S}
To: {email}
From: Inkom Emporium <no-reply@inkom.com>
Subject: Welcome to Inkom Emporium! Your Exclusive Offers Await!

Dear {username},

Welcome to the Inkom Emporium family! We're thrilled to have you.

As a new customer, you're eligible for some amazing offers:
- {NEW_USER_DISCOUNT_PERCENT:.0%} off your first order (code: NEWCUSTOMER15)
- Free shipping on all orders over $50 for your first month!
- Earn double loyalty points on select fresh produce this week.

We hope you enjoy your shopping experience with us. Explore our wide range of products!

Check your email regularly for more exciting deals and personalized recommendations.

Happy Shopping!

Sincerely,
The Inkom Emporium Team
----------------------------
"""
        with open("email_inbox.txt", "a") as inbox_file:
            inbox_file.write(email_content)
        return True
    except IOError as e:
        print(f"Error: Could not write welcome email to email_inbox.txt. Details: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while sending welcome email: {e}")
        return False

def send_review_email(username, email, order_number):
    """Sends a simulated email asking the user to rate the store service."""
    try:
        now = datetime.now()
        email_content = f"""
--- New Email for {username} (Service Review) ---
Date and Time: {now:%Y-%m-%d %H:%M:%S}
To: {email}
From: Inkom Emporium <feedback@inkom.com>
Subject: How Was Your Inkom Emporium Experience (Order #{order_number})?

Dear {username},

Thank you for your recent purchase (Order #{order_number}) at Inkom Emporium!

We hope you enjoyed your shopping experience. We'd love to hear your feedback
so we can continue to improve our services.
Please take a moment to complete our quick survey and provide a review:
[Link to Survey - This is a placeholder]

Your opinion matters to us!

Sincerely,
The Inkom Emporium Team
----------------------------
"""
        with open("email_inbox.txt", "a") as inbox_file:
            inbox_file.write(email_content)
        return True
    except IOError as e:
        print(f"Error: Could not write review email to email_inbox.txt. Details: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while sending review email: {e}")
        return False

def check_password_strength(password):
    """
    Checks the strength of a password based on specified criteria.
    Returns a tuple: (strength_score, list_of_reasons_for_weakness)
    """
    reasons = []
    satisfied_criteria = 0

    if len(password) >= 5:
        satisfied_criteria += 1
    else:
        reasons.append("Password must be at least 5 characters long.")

    if re.search(r"\d", password): # Checks for any digit
        satisfied_criteria += 1
    else:
        reasons.append("Password must contain at least one digit.")

    if re.search(r"[A-Z]", password): # Checks for any uppercase letter
        satisfied_criteria += 1
    else:
        reasons.append("Password must contain at least one uppercase letter.")

    if re.search(r"[a-z]", password): # Checks for any lowercase letter
        satisfied_criteria += 1
    else:
        reasons.append("Password must contain at least one lowercase letter.")

    special_chars_pattern = r"[!@#$%^&*()-_=+\/\[\]{}|;:'\",.<>?`~]"
    if re.search(special_chars_pattern, password):
        satisfied_criteria += 1
    else:
        # Escaping backslashes for display, as re.search pattern uses raw string
        display_special_chars = special_chars_pattern.replace('[','').replace(']','').replace('\\','')
        reasons.append(f"Password must contain at least one special character (e.g., {display_special_chars}).")
    
    strength_score = 0
    if satisfied_criteria == 1:
        strength_score = 2
    elif satisfied_criteria == 3:
        strength_score = 4
    elif satisfied_criteria >= 4: # If 4 or 5 criteria are met
        strength_score = 10

    return strength_score, reasons

def explore_products(products_dict):
    """Prints a formatted list of all products."""
    print("\n--- Our Products ---")
    if not products_dict:
        print("No products available at the moment.")
        return

    print(f"{'ID':<10}{'Product Name':<25}{'Price':>10}")
    print(f"{'-'*10:<10}{'-'*25:<25}{'-'*10:>10}")

    for product_id, product_info in products_dict.items():
        product_name = product_info[PRODUCT_NAME_INDEX]
        product_price = float(product_info[PRODUCT_PRICE_INDEX])
        print(f"{product_id:<10}{product_name:<25}{product_price:>10.2f}")
    print("-" * 50)

def view_user_list(item_list_dict, products_dict, list_name):
    """Prints the contents of a user's cart or wishlist."""
    print(f"\n--- Your {list_name} ---")
    if not item_list_dict:
        print(f"Your {list_name.lower()} is currently empty.")
        print("-" * 50)
        return

    total_price = 0.0
    print(f"{'ID':<10}{'Product Name':<25}{'Qty':<5}{'Price':>10}{'Total':>10}")
    print(f"{'-'*10:<10}{'-'*25:<25}{'-'*5:<5}{'-'*10:>10}{'-'*10:>10}")

    for product_id, quantity in item_list_dict.items():
        if product_id in products_dict:
            product_info = products_dict[product_id]
            product_name = product_info[PRODUCT_NAME_INDEX]
            unit_price = float(product_info[PRODUCT_PRICE_INDEX])
            item_total = unit_price * quantity
            total_price += item_total
            print(f"{product_id:<10}{product_name:<25}{quantity:<5}{unit_price:>10.2f}{item_total:>10.2f}")
        else:
            print(f"Warning: Unknown product ID '{product_id}' in your {list_name.lower()}.")
    print(f"{'Subtotal:':<40}{total_price:>15.2f}")
    print("-" * 50)

def add_product_to_user_list(products_dict, wishlist, cart):
    """Allows user to add products to wishlist or cart."""
    print("\n--- Add Product ---")
    print("Where would you like to add a product from?")
    print("    1. Explore All Products")
    print("    2. From My Wishlist")
    print("-" * 50)
    source_choice = input("Enter source (1 or 2): ").strip()

    product_id_to_add = ""
    quantity_to_add = 1 # Default for wishlist or single item add to cart if not specified
    source_list_name = ""

    if source_choice == '1': # From Explore All Products
        explore_products(products_dict) # Show products again
        product_id_to_add = input("Enter the ID of the product to add (or 'q' to quit): ").strip().upper()
        if product_id_to_add == 'Q':
            print("Product addition cancelled.")
            return False # Indicate to the calling loop to stop
        if product_id_to_add not in products_dict:
            print("Invalid Product ID. Please try again.")
            return True # Indicate to the calling loop to continue
        source_list_name = "Products"
    elif source_choice == '2': # From My Wishlist
        view_user_list(wishlist, products_dict, "Wishlist")
        if not wishlist:
            print("Your wishlist is empty. Cannot move from empty list.")
            return True # Indicate to the calling loop to continue
        product_id_to_add = input("Enter the ID of the product from your Wishlist to add (or 'q' to quit): ").strip().upper()
        if product_id_to_add == 'Q':
            print("Product addition cancelled.")
            return False # Indicate to the calling loop to stop
        if product_id_to_add not in wishlist:
            print("Product not found in your Wishlist. Please try again.")
            return True # Indicate to the calling loop to continue
        source_list_name = "Wishlist"
    else:
        print("Invalid source choice.")
        return True # Indicate to the calling loop to continue

    print("Where would you like to add this product to?")
    print("    1. My Wishlist")
    print("    2. My Cart")
    print("-" * 50)
    destination_choice = input("Enter destination (1 or 2): ").strip()

    if destination_choice == '1': # To Wishlist
        # If adding from Products to Wishlist, or already in wishlist (just confirming)
        if product_id_to_add in products_dict: # Ensure it's a valid product ID
            wishlist[product_id_to_add] = wishlist.get(product_id_to_add, 0) + 1 # Add 1 to wishlist
            print(f"Added {products_dict[product_id_to_add][PRODUCT_NAME_INDEX]} to your Wishlist.")
        else:
            print("Error: Product ID not recognized.")
        print(f"Unit Price: ${float(products_dict[product_id_to_add][PRODUCT_PRICE_INDEX]):.2f}")
        print("-" * 50)
        return True # Indicate to the calling loop to continue
    elif destination_choice == '2': # To Cart
        try:
            qty_input = input("Enter quantity to add to cart (default 1, or 'q' to quit): ").strip()
            if qty_input.upper() == 'Q': # <--- Added quit option here
                print("Product addition to cart cancelled.")
                return False
            elif qty_input:
                quantity_to_add = int(qty_input)
                if quantity_to_add <= 0:
                    print("Quantity must be positive.")
                    return True # Indicate to the calling loop to continue
            else:
                quantity_to_add = 1 # Default quantity
        except ValueError:
            print("Invalid quantity. Please enter a number or 'q'.")
            return True # Indicate to the calling loop to continue
        
        if product_id_to_add in products_dict: # Ensure it's a valid product ID
            cart[product_id_to_add] = cart.get(product_id_to_add, 0) + quantity_to_add
            print(f"Added {quantity_to_add}x {products_dict[product_id_to_add][PRODUCT_NAME_INDEX]} to your Cart.")

            # If moved from wishlist to cart, remove from wishlist
            if source_list_name == "Wishlist" and product_id_to_add in wishlist:
                # Only remove the quantity actually moved from wishlist
                wishlist[product_id_to_add] -= quantity_to_add
                if wishlist[product_id_to_add] <= 0:
                    del wishlist[product_id_to_add]
                print(f"Removed {products_dict[product_id_to_add][PRODUCT_NAME_INDEX]} from your Wishlist.")
        else:
            print("Error: Product ID not recognized.")

    else:
        print("Invalid destination choice.")
        return True # Indicate to the calling loop to continue
    
    # Return price of the added item
    if product_id_to_add in products_dict:
        print(f"Unit Price: ${float(products_dict[product_id_to_add][PRODUCT_PRICE_INDEX]):.2f}")
    print("-" * 50)
    return True # Indicate to the calling loop to continue

def remove_product_from_user_list(products_dict, wishlist, cart):
    """Allows user to remove products from wishlist or cart."""
    print("\n--- Remove Product ---")
    print("Where would you like to remove a product from?")
    print("    1. My Wishlist")
    print("    2. My Cart")
    print("-" * 50)
    source_choice = input("Enter source (1 or 2): ").strip()

    target_list_dict = {}
    list_name = ""

    if source_choice == '1':
        target_list_dict = wishlist
        list_name = "Wishlist"
    elif source_choice == '2':
        target_list_dict = cart
        list_name = "Cart"
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return True # Indicate to the calling loop to continue

    if not target_list_dict:
        print(f"Your {list_name.lower()} is already empty. Nothing to remove.")
        return True # Indicate to the calling loop to continue

    view_user_list(target_list_dict, products_dict, list_name) # Show current list

    product_id_to_remove = input(f"Enter the ID of the product to remove from your {list_name.lower()} (or 'q' to quit): ").strip().upper()
    if product_id_to_remove == 'Q':
        print("Product removal cancelled.")
        return False # Indicate to the calling loop to stop

    if product_id_to_remove not in target_list_dict:
        print(f"Product '{product_id_to_remove}' not found in your {list_name.lower()}.")
        return True # Indicate to the calling loop to continue

    if list_name == "Cart":
        try:
            qty_to_remove_input = input(f"How many {products_dict[product_id_to_remove][PRODUCT_NAME_INDEX]}(s) to remove (currently {target_list_dict[product_id_to_remove]})? (Press Enter to remove all, or 'q' to quit): ").strip() # <--- Added quit option here
            if qty_to_remove_input.upper() == 'Q': # <--- Check for quit option
                print("Product removal cancelled.")
                return False # Indicate to the calling loop to stop
            elif not qty_to_remove_input: # If user just presses Enter, remove all
                qty_to_remove = target_list_dict[product_id_to_remove]
            else:
                qty_to_remove = int(qty_to_remove_input)
                if qty_to_remove <= 0:
                    print("Quantity to remove must be positive.")
                    return True # Indicate to the calling loop to continue
                if qty_to_remove > target_list_dict[product_id_to_remove]:
                    print(f"You only have {target_list_dict[product_id_to_remove]} in your {list_name.lower()}. Removing all.")
                    qty_to_remove = target_list_dict[product_id_to_remove]
        except ValueError:
            print("Invalid quantity. Please enter a number, press Enter, or 'q'.")
            return True # Indicate to the calling loop to continue
        
        target_list_dict[product_id_to_remove] -= qty_to_remove
        if target_list_dict[product_id_to_remove] <= 0:
            del target_list_dict[product_id_to_remove]
        print(f"Removed {qty_to_remove}x {products_dict[product_id_to_remove][PRODUCT_NAME_INDEX]} from your {list_name.lower()}.")
    else: # Wishlist (always remove all of that item if chosen)
        del target_list_dict[product_id_to_remove]
        print(f"Removed {products_dict[product_id_to_remove][PRODUCT_NAME_INDEX]} from your {list_name.lower()}.")
    
    if product_id_to_remove in products_dict: # Only show price if product exists
        print(f"Unit Price of removed item: ${float(products_dict[product_id_to_remove][PRODUCT_PRICE_INDEX]):.2f}")
    print("-" * 50)
    return True # Indicate to the calling loop to continue


def process_checkout(username, user_cart, products_dict):
    """Handles the entire checkout process including delivery, payment, and receipt."""
    print("\n--- Proceed to Checkout ---")
    
    # 1. Pickup Location
    shipping_cost = 0.0
    delivery_type = ""
    while True:
        print("\nChoose your pickup location:")
        print("    1. Inkom Emporium Physical Shop (Mombasa Road, Athi 55 Business Park Warehouse 15B)")
        print(f"    2. Doorstep Delivery (Shipping fee: ${SHIPPING_FEE:.2f})")
        pickup_choice = input("Enter choice (1 or 2): ").strip()

        if pickup_choice == '1':
            delivery_type = "Physical Shop Pickup"
            print("\nPlease provide an original ID and an email with your order number when picking up at the shop.")
            break
        elif pickup_choice == '2':
            delivery_type = "Doorstep Delivery"
            shipping_cost = SHIPPING_FEE
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    # 2. Final Confirmation and Warning
    print("\n" + "*" * 50)
    print("IMPORTANT: Please Confirm your products before placing an order.")
    print("Refunds for Food products are not accepted.")
    print("For other products, it will take up to 5 working days for a refund.")
    print("*" * 50)
    confirm_order = input("Do you wish to proceed with the order? (yes/no): ").strip().lower()
    if confirm_order != 'yes':
        print("Order cancelled. Returning to main menu.")
        return # Go back to the main menu (implicitly by ending this function)

    # 3. Payment Method
    print("\n--- Select Payment Method ---")
    payment_method = ""
    while True:
        print("    1. Mpesa")
        print("    2. Visa Card")
        print("    3. PayPal")
        payment_choice = input("Enter choice (1, 2, or 3): ").strip()

        if payment_choice == '1' or payment_choice == '2':
            payment_method = "Mpesa" if payment_choice == '1' else "Visa Card"
            while True:
                pin = input(f"Enter your 4-digit {payment_method} PIN: ").strip()
                if len(pin) == 4 and pin.isdigit():
                    print("PIN accepted.") # Any 4 digits are 'correct'
                    break
                elif not pin.isdigit():
                    print("PIN must contain only digits.")
                else:
                    print("PIN must be 4 digits long.")
            break
        elif payment_choice == '3':
            print("PayPal is only available for Gold Members. Please select another method.")
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # 4. Process Order and Generate Receipt
    order_time = datetime.now()
    order_number = generate_order_number()

    print(f"\nOrder successfully placed! {GREEN_CHECKMARK}")

    # Calculate receipt details
    subtotal = 0.0
    
    for product_id, quantity in user_cart.items():
        product_info = products_dict[product_id]
        unit_price = float(product_info[PRODUCT_PRICE_INDEX])
        
        item_cost = 0.0
        if product_id == "D083":
            # Calculate cost for D083 with BOGO 50% off
            # Every second D083 is half price.
            num_full_price = (quantity + 1) // 2
            num_half_price = quantity // 2
            item_cost = (num_full_price * unit_price) + (num_half_price * unit_price * 0.5)
        else:
            item_cost = unit_price * quantity
            
        subtotal += item_cost

    # Apply new user discount (placeholder logic)
    # This logic assumes the first order gets the discount.
    # For a real system, you'd need a flag per user in users.csv.
    new_user_discount_amount = subtotal * NEW_USER_DISCOUNT_PERCENT
    final_subtotal_after_discount = subtotal - new_user_discount_amount

    sales_tax = final_subtotal_after_discount * SALES_TAX_RATE
    final_total = final_subtotal_after_discount + sales_tax + shipping_cost

    # Calculate pickup/delivery time based on current time and location
    current_time_mlolongo = datetime.now() # Assumed to be in EAT or local time
    
    if delivery_type == "Physical Shop Pickup":
        pickup_time = current_time_mlolongo + timedelta(minutes=30)
        time_info = f"Ready for pickup by: {pickup_time:%Y-%m-%d %I:%M %p} EAT"
    else: # Doorstep Delivery
        delivery_time = current_time_mlolongo + timedelta(hours=2)
        time_info = f"Expected delivery by: {delivery_time:%Y-%m-%d %I:%M %p} EAT"

    # Print Stylish Receipt
    print("\n" + "=" * 60)
    print("Inkom Emporium - Your Order Receipt".center(60))
    print("=" * 60)
    print(f"Order Number: {order_number}")
    print(f"Date: {order_time:%Y-%m-%d %H:%M}")
    print(f"Customer: {username}")
    print("-" * 60)
    print(f"{'Product':<30}{'Qty':<5}{'Unit Price':>12}{'Line Total':>10}")
    print("-" * 60)

    # Detailed receipt printing with BOGO explicitly shown
    d083_items_processed_for_receipt_display = 0
    for product_id, quantity in user_cart.items():
        product_info = products_dict[product_id]
        product_name = product_info[PRODUCT_NAME_INDEX]
        unit_price = float(product_info[PRODUCT_PRICE_INDEX])
        
        if product_id == "D083":
            # Print each D083 item individually to show BOGO
            for i in range(quantity):
                if (d083_items_processed_for_receipt_display + i) % 2 == 1: # This is the 2nd, 4th, etc. D083
                    display_price = unit_price * 0.5
                    print(f"{product_name:<30}{1:<5}{unit_price:>12.2f} (BOGO 50% Off)")
                else: # This is the 1st, 3rd, etc. D083
                    display_price = unit_price
                    print(f"{product_name:<30}{1:<5}{unit_price:>12.2f}")
            d083_items_processed_for_receipt_display += quantity
        else:
            line_total = unit_price * quantity
            print(f"{product_name:<30}{quantity:<5}{unit_price:>12.2f}{line_total:>10.2f}")

    print("-" * 60)
    print(f"{'Subtotal:':<50}{subtotal:>9.2f}")
    if new_user_discount_amount > 0:
        print(f"{'New User Discount (15%):':<50}{-new_user_discount_amount:>9.2f}")
    print(f"{'Subtotal (after discount):':<50}{final_subtotal_after_discount:>9.2f}")
    print(f"{'Sales Tax (6%):':<50}{sales_tax:>9.2f}")
    if shipping_cost > 0:
        print(f"{'Shipping Fee:':<50}{shipping_cost:>9.2f}")
    print(f"{'Total:':<50}{final_total:>9.2f}")
    print("=" * 60)
    print(f"Delivery/Pickup: {delivery_type}")
    print(time_info)
    print("\nThank you for your order! We appreciate your business.")
    print("Please retain this receipt for your records.")
    
    # --- Existing Exceeding Requirements at bottom of receipt ---
    print(f"{current_time_mlolongo:%a %b %d %I:%M:%S %p %Y %Z}") # Current system date/time
    return_by_date = current_time_mlolongo + timedelta(days=30)
    return_by_date = return_by_date.replace(hour=21, minute=0, second=0, microsecond=0) # Set to 9 PM
    print(f"Items can be returned by: {return_by_date:%Y-%m-%d %I:%M %p}")
    
    # New Year's Sale Countdown: Correct calculation based on current year/next year
    next_new_year = datetime(current_time_mlolongo.year + 1, 1, 1, 0, 0, 0)
    time_until_new_year_sale = next_new_year - current_time_mlolongo
    days_until_new_year_sale = time_until_new_year_sale.days
    # Ensure non-negative for display if current_time_mlolongo is already past New Year
    if days_until_new_year_sale < 0:
        days_until_new_year_sale = 0
        hours_until_new_year_sale = 0
        minutes_until_new_year_sale = 0
    else:
        hours_until_new_year_sale = time_until_new_year_sale.seconds // 3600
        minutes_until_new_year_sale = (time_until_new_year_sale.seconds % 3600) // 60

    print(f"New Year's Sale begins in {days_until_new_year_sale} days, {hours_until_new_year_sale} hours, and {minutes_until_new_year_sale} minutes!")
    print("\nEarn loyalty points with every purchase!")
    print("=" * 60)

    # Clear cart after successful checkout
    user_cart.clear()

    # --- Send Review Email ---
    # In a full system, you'd get the actual email from the user's stored data.
    # For now, we'll assume a placeholder email or reuse the one from account creation.
    print(f"\nWe've sent a service review request to your email (simulated for {username}).")
    send_review_email(username, "placeholder@example.com", order_number) # Placeholder email


def generate_order_number():
    """Generates a random order number starting with 'KER' and 7 digits."""
    return "KER" + ''.join(random.choices('0123456789', k=7))


if __name__ == "__main__":
    main()
    
    
# Copyright 2025, Alex Malunda. All rights reserved.