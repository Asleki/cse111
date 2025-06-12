# This program generates a grocery store receipt, fulfilling the W05 Project requirements
# and includes several exceeding features for enhanced functionality:
#
# Exceeding Requirements:
# 1.  "Buy One, Get One Half Off" (BOGO 50% Off) discount implemented for product 'D083'.
#     For every two D083 items, one is full price, and the other is 50% off.
# 2.  A reminder at the bottom of the receipt showing the number of days until the next New Year's Sale (January 1st).
# 3.  A "return by" date printed on the receipt, set to 9:00 PM 30 days from the current date.
# 4.  Loyalty Points System: Customers earn loyalty points based on their total spending.
#     (1 point for every $5 spent, displayed as an integer).
# 5.  Item-Specific Serving Suggestions: For selected products, a "Tip" is printed under the item
#     on the receipt offering a serving suggestion or extra information.
# 6.  Future Purchase Coupon: A randomly generated alphanumeric coupon code is displayed at the end
#     of the receipt, valid for 7 days.

import csv
from datetime import datetime, timedelta
import sys
import random # Import random for coupon generation

# --- Color Codes for Terminal Output (Copied from familiabank.py) ---
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BRIGHT_BLACK = "\033[90m" # Used for faint input prompts in familiabank.py, can be used for subtle text

GREEN_CHECKMARK = f"{GREEN}\u2713{RESET}" # Green checkmark
RED_X = f"{RED}\u2717{RESET}"             # Red X
BLUE_INFO = f"{BLUE}i{RESET}"             # Blue info icon

# Define constants for the store.
STORE_NAME = "Inkom Emporium"
SALES_TAX_RATE = 0.06
LOYALTY_POINTS_RATE = 0.2 # 1 point for every $5 spent (0.2 points per $1)

# Item-specific suggestions/tips
# Updated to match the product IDs from your provided products.csv
ITEM_SUGGESTIONS = {
    "W112": "Try warming it up for fresh toast!",     # For wheat bread
    "D083": "Perfect with fresh berries!",            # For 1 cup yogurt (D083)
    "W231": "Add to your morning smoothie for extra crunch!", # For 32 oz granola
    "C013": "A classic treat for any time of day!"    # For twix candy bar (C013)
}

def read_products(filename="products.csv"):
    """Reads product data from a CSV file and returns a dictionary.

    The returned dictionary will have product IDs as keys and a list
    containing the product name and price as values.

    Args:
        filename (str): The name of the CSV file to read. Defaults to "products.csv".

    Returns:
        dict: A dictionary of products. The keys are product IDs (strings),
              and the values are lists containing [product_name (string),
              product_price (float)].

    Raises:
        FileNotFoundError: If the specified products file does not exist.
        PermissionError: If the program does not have permission to read the file.
        Exception: For any other unexpected errors during file reading or parsing.
    """
    products_dict = {}
    try:
        # Open the CSV file for reading.
        with open(filename, "rt") as products_file:
            # Create a CSV reader object.
            reader = csv.reader(products_file)
            # Skip the header row.
            next(reader)
            # Read each row from the CSV file.
            for row in reader:
                # Ensure the row has the expected number of columns (product_id, name, price).
                if len(row) == 3:
                    product_id = row[0]
                    product_name = row[1]
                    try:
                        product_price = float(row[2])
                    except ValueError:
                        # Use RED_X for error messages
                        print(f"{RED_X} Error: Invalid price format for product '{product_id}' in {filename}. Skipping row.{RESET}", file=sys.stderr)
                        continue # Skip this row and continue with the next
                    products_dict[product_id] = [product_name, product_price]
                else:
                    # Use YELLOW for warning messages
                    print(f"{YELLOW}Warning: Skipping malformed row in {filename}: {row}{RESET}", file=sys.stderr)
    except FileNotFoundError as e:
        # Use RED_X for error messages
        print(f"{RED_X} Error: missing file\n{e}{RESET}", file=sys.stderr)
        raise # Re-raise the exception to stop program execution gracefully
    except PermissionError as e:
        # Use RED_X for error messages
        print(f"{RED_X} Error: permission denied to access file\n{e}{RESET}", file=sys.stderr)
        raise # Re-raise the exception
    except Exception as e:
        # Use RED_X for unexpected errors
        print(f"{RED_X} An unexpected error occurred while reading {filename}: {e}{RESET}", file=sys.stderr)
        raise # Re-raise the exception
    return products_dict

def process_request(filename="request.csv", products_dict={}):
    """Processes customer requests from a CSV file and calculates order details.

    Args:
        filename (str): The name of the CSV file containing customer requests.
                        Defaults to "request.csv".
        products_dict (dict): A dictionary of available products, typically obtained
                              from the read_products function.

    Returns:
        tuple: A tuple containing:
            - list: A list of tuples, each containing (formatted_item_string, product_id_for_suggestion).
            - int: The total number of items ordered.
            - float: The subtotal of the order before tax.

    Raises:
        FileNotFoundError: If the specified request file does not exist.
        PermissionError: If the program does not have permission to read the file.
        KeyError: If a product ID in the request file is not found in the products_dict.
        ValueError: If quantity in the request file is not a valid integer.
        Exception: For any other unexpected errors during request processing.
    """
    ordered_items_details = [] # Will store (formatted_string, product_id)
    total_items = 0
    subtotal = 0.0

    try:
        # Open the CSV file for reading.
        with open(filename, "rt") as request_file:
            # Create a CSV reader object.
            reader = csv.reader(request_file)
            # Skip the header row.
            next(reader)
            # Read each row from the CSV file.
            for row in reader:
                # Ensure the row has the expected number of columns (product_id, quantity).
                if len(row) == 2:
                    product_id = row[0]
                    try:
                        quantity = int(row[1])
                        if quantity <= 0: # Ensure quantity is positive
                            # Use YELLOW for warnings
                            print(f"{YELLOW}Warning: Quantity for product '{product_id}' must be positive. Skipping row.{RESET}", file=sys.stderr)
                            continue
                    except ValueError:
                        # Use RED_X for error messages
                        print(f"{RED_X} Error: Invalid quantity format for product '{product_id}' in {filename}. Skipping row.{RESET}", file=sys.stderr)
                        continue # Skip this row and continue with the next

                    # Try to retrieve product information from the products dictionary.
                    # This will raise a KeyError if the product_id is not found.
                    product_name, product_price = products_dict[product_id]

                    item_total_price = quantity * product_price
                    discount_message = ""

                    # Exceeding Requirements: Implement "buy one, get one half off" for item D083.
                    if product_id == "D083" and quantity >= 2:
                        full_price_items = quantity // 2 + (quantity % 2)
                        half_price_items = quantity // 2
                        
                        discounted_price_per_item = product_price / 2
                        item_total_price = (full_price_items * product_price) + \
                                           (half_price_items * discounted_price_per_item)
                        discount_message = " (BOGO 50% Off Applied)"

                    # Append the formatted item string and product_id to the list.
                    ordered_items_details.append((f"{product_name}: {quantity} @ {product_price:.2f}{discount_message}", product_id))
                    # Accumulate total items and subtotal.
                    total_items += quantity
                    subtotal += item_total_price
                else:
                    # Use YELLOW for warning messages
                    print(f"{YELLOW}Warning: Skipping malformed row in {filename}: {row}{RESET}", file=sys.stderr)
    except FileNotFoundError as e:
        # Use RED_X for error messages
        print(f"{RED_X} Error: missing file\n{e}{RESET}", file=sys.stderr)
        raise # Re-raise the exception
    except PermissionError as e:
        # Use RED_X for error messages
        print(f"{RED_X} Error: permission denied to access file\n{e}{RESET}", file=sys.stderr)
        raise # Re-raise the exception
    except KeyError as e:
        # Use RED_X for error messages
        print(f"{RED_X} Error: unknown product ID in the request.csv file\n'{e}'{RESET}", file=sys.stderr)
        raise # Re-raise the exception
    except ValueError as e:
        # Use RED_X for error messages
        print(f"{RED_X} Error: invalid data in request.csv (e.g., non-integer quantity or non-float price)\n{e}{RESET}", file=sys.stderr)
        raise # Re-raise the exception
    except Exception as e:
        # Use RED_X for unexpected errors
        print(f"{RED_X} An unexpected error occurred while processing {filename}: {e}{RESET}", file=sys.stderr)
        raise # Re-raise the exception
    return ordered_items_details, total_items, subtotal

def generate_coupon_code(length=8):
    """Generates a random alphanumeric coupon code."""
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(characters) for i in range(length))

def main():
    """
    Main function to run the grocery store receipt program.
    It orchestrates reading data, processing requests, and printing the receipt.
    """
    # Use BOLD for the store name
    print(f"{BOLD}{STORE_NAME}{RESET}")
    # Use YELLOW for separators
    print(f"{YELLOW}-" * len(STORE_NAME) + f"{RESET}")

    try:
        # Read product data from products.csv.
        products = read_products("products.csv")
        # Process the customer's request from request.csv.
        ordered_items_details, num_items, subtotal = process_request("request.csv", products)

        # Print each ordered item on the receipt, and add suggestions
        for item_string, product_id in ordered_items_details:
            print(item_string)
            if product_id in ITEM_SUGGESTIONS:
                # Use BLUE_INFO for tips/suggestions
                print(f"  {BLUE_INFO} Tip: {ITEM_SUGGESTIONS[product_id]}{RESET}") # Indent suggestion for readability

        # Calculate sales tax and total amount.
        sales_tax = subtotal * SALES_TAX_RATE
        total = subtotal + sales_tax

        # Print the summary of the order. Use BLUE for labels, default for values
        print(f"\n{BLUE}Number of Items:{RESET} {num_items}")
        print(f"{BLUE}Subtotal:{RESET} {subtotal:.2f}")
        print(f"{BLUE}Sales Tax:{RESET} {sales_tax:.2f}")
        # Use BOLD for the Total
        print(f"{BOLD}Total:{RESET} {total:.2f}")

        # --- Unique Feature 1: Loyalty Points ---
        loyalty_points_earned = int(total * LOYALTY_POINTS_RATE)
        # Use GREEN for loyalty points
        print(f"\n{GREEN}Loyalty Points Earned:{RESET} {loyalty_points_earned}")

        # Print a thank you message. Use GREEN_CHECKMARK for positive confirmation
        print(f"\n{GREEN_CHECKMARK} Thank you for shopping at the {STORE_NAME}.{RESET}")

        # Get and print the current date and time. Use CYAN
        current_date_and_time = datetime.now()
        print(f"{CYAN}{current_date_and_time:%a %b %d %H:%M:%S %Y}{RESET}")

        # Exceeding requirements: Print a "return by" date. Use CYAN
        return_by_date = current_date_and_time + timedelta(days=30)
        return_by_date = return_by_date.replace(hour=21, minute=0, second=0, microsecond=0)
        print(f"\n{CYAN}Return by:{RESET} {return_by_date:%A, %B %d, %Y at %I:%M %p}")

        # Exceeding requirements: New Year's Sale countdown. Use YELLOW
        current_year = current_date_and_time.year
        new_years_day_current_year = datetime(current_year, 1, 1)

        if current_date_and_time > new_years_day_current_year:
            new_years_day_target = datetime(current_year + 1, 1, 1)
        else:
            new_years_day_target = new_years_day_current_year

        days_until_new_year_sale = (new_years_day_target - current_date_and_time).days
        print(f"\n{YELLOW}New Year's Sale begins in {days_until_new_year_sale} days!{RESET}")

        # --- Unique Feature 2: Future Purchase Coupon ---
        coupon_code = generate_coupon_code()
        # Use BOLD and CYAN for the section header, GREEN for the code itself
        print(f"\n{BOLD}{CYAN}--- Special Offer! ---{RESET}")
        print(f"Get 10% off your next purchase using code: {GREEN}{coupon_code}{RESET}")
        print(f"Valid until {current_date_and_time + timedelta(days=7):%b %d, %Y}")
        print(f"{BOLD}{CYAN}--------------------{RESET}")


    except (FileNotFoundError, PermissionError, KeyError, ValueError):
        # These exceptions are caught and handled with specific messages
        # in the `read_products` and `process_request` functions,
        # so we just let the program exit here after the error message is printed.
        pass
    except Exception as e:
        # Catch any other unhandled exceptions at the main level.
        print(f"{RED_X} An unhandled error occurred during receipt generation: {e}{RESET}", file=sys.stderr)

# Ensure the main function is called only when the script is executed directly.
if __name__ == "__main__":
    main()

