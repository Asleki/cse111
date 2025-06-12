import csv
from datetime import datetime, timedelta
import sys

# Define constants for the store.
STORE_NAME = "Inkom Emporium"
SALES_TAX_RATE = 0.06

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
                        print(f"Error: Invalid price format for product '{product_id}' in {filename}. Skipping row.", file=sys.stderr)
                        continue # Skip this row and continue with the next
                    products_dict[product_id] = [product_name, product_price]
                else:
                    # Warn if a row is malformed and skip it.
                    print(f"Warning: Skipping malformed row in {filename}: {row}", file=sys.stderr)
    except FileNotFoundError as e:
        # Handle the case where the products file is not found.
        print(f"Error: missing file\n{e}", file=sys.stderr)
        raise # Re-raise the exception to stop program execution gracefully
    except PermissionError as e:
        # Handle the case where there are no permissions to read the file.
        print(f"Error: permission denied to access file\n{e}", file=sys.stderr)
        raise # Re-raise the exception
    except Exception as e:
        # Catch any other unexpected errors during file processing.
        print(f"An unexpected error occurred while reading {filename}: {e}", file=sys.stderr)
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
            - list: A list of formatted strings, each representing an ordered item.
            - int: The total number of items ordered.
            - float: The subtotal of the order before tax.

    Raises:
        FileNotFoundError: If the specified request file does not exist.
        PermissionError: If the program does not have permission to read the file.
        KeyError: If a product ID in the request file is not found in the products_dict.
        ValueError: If quantity in the request file is not a valid integer.
        Exception: For any other unexpected errors during request processing.
    """
    ordered_items = []
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
                            print(f"Warning: Quantity for product '{product_id}' must be positive. Skipping row.", file=sys.stderr)
                            continue
                    except ValueError:
                        print(f"Error: Invalid quantity format for product '{product_id}' in {filename}. Skipping row.", file=sys.stderr)
                        continue # Skip this row and continue with the next

                    # Try to retrieve product information from the products dictionary.
                    # This will raise a KeyError if the product_id is not found.
                    product_name, product_price = products_dict[product_id]

                    item_total_price = quantity * product_price
                    discount_message = ""

                    # Exceeding Requirements: Implement "buy one, get one half off" for item D083.
                    # For every two items, one is full price and one is half price.
                    # Any odd item remaining is full price.
                    if product_id == "D083" and quantity >= 2:
                        # Calculate how many items are full price and how many are half price.
                        full_price_items = quantity // 2 + (quantity % 2)
                        half_price_items = quantity // 2
                        
                        # Calculate the total cost with the discount.
                        discounted_price_per_item = product_price / 2
                        item_total_price = (full_price_items * product_price) + \
                                           (half_price_items * discounted_price_per_item)
                        discount_message = " (BOGO 50% Off Applied)"

                    # Append the formatted item string to the list of ordered items.
                    ordered_items.append(f"{product_name}: {quantity} @ {product_price:.2f}{discount_message}")
                    # Accumulate total items and subtotal.
                    total_items += quantity
                    subtotal += item_total_price
                else:
                    # Warn if a row is malformed and skip it.
                    print(f"Warning: Skipping malformed row in {filename}: {row}", file=sys.stderr)
    except FileNotFoundError as e:
        # Handle the case where the request file is not found.
        print(f"Error: missing file\n{e}", file=sys.stderr)
        raise # Re-raise the exception
    except PermissionError as e:
        # Handle the case where there are no permissions to read the file.
        print(f"Error: permission denied to access file\n{e}", file=sys.stderr)
        raise # Re-raise the exception
    except KeyError as e:
        # Handle the case where a product ID from the request file is not in the products dictionary.
        print(f"Error: unknown product ID in the request.csv file\n'{e}'", file=sys.stderr)
        raise # Re-raise the exception
    except ValueError as e:
        # Handle cases where quantity is not a valid integer.
        print(f"Error: invalid data in request.csv (e.g., non-integer quantity or non-float price)\n{e}", file=sys.stderr)
        raise # Re-raise the exception
    except Exception as e:
        # Catch any other unexpected errors during request processing.
        print(f"An unexpected error occurred while processing {filename}: {e}", file=sys.stderr)
        raise # Re-raise the exception
    return ordered_items, total_items, subtotal

def main():
    """
    Main function to run the grocery store receipt program.
    It orchestrates reading data, processing requests, and printing the receipt.
    """
    print(STORE_NAME)
    print("-" * len(STORE_NAME)) # A simple separator for the store name

    try:
        # Read product data from products.csv.
        products = read_products("products.csv")
        # Process the customer's request from request.csv.
        ordered_items, num_items, subtotal = process_request("request.csv", products)

        # Print each ordered item on the receipt.
        for item in ordered_items:
            print(item)

        # Calculate sales tax and total amount.
        sales_tax = subtotal * SALES_TAX_RATE
        total = subtotal + sales_tax

        # Print the summary of the order.
        print(f"\nNumber of Items: {num_items}")
        print(f"Subtotal: {subtotal:.2f}")
        print(f"Sales Tax: {sales_tax:.2f}")
        print(f"Total: {total:.2f}")

        # Print a thank you message.
        print(f"\nThank you for shopping at the {STORE_NAME}.")

        # Get and print the current date and time.
        current_date_and_time = datetime.now()
        # Format the date and time to match the example output: "Wed Nov  4 05:10:30 2020"
        print(f"{current_date_and_time:%a %b %d %H:%M:%S %Y}")

        # Exceeding requirements: Print a "return by" date.
        # Calculate the return date as 30 days from now.
        return_by_date = current_date_and_time + timedelta(days=30)
        # Set the time to 9:00 PM (21:00) on the return date.
        return_by_date = return_by_date.replace(hour=21, minute=0, second=0, microsecond=0)
        print(f"\nReturn by: {return_by_date:%A, %B %d, %Y at %I:%M %p}")

        # --- Exceeding requirements: New Year's Sale countdown ---
        # Get the current year
        current_year = current_date_and_time.year
        # Define New Year's Day for the current year
        new_years_day_current_year = datetime(current_year, 1, 1)

        # If current date is past New Year's Day, set target to next year's New Year's Day
        if current_date_and_time > new_years_day_current_year:
            new_years_day_target = datetime(current_year + 1, 1, 1)
        else:
            new_years_day_target = new_years_day_current_year

        # Calculate the difference in days
        days_until_new_year_sale = (new_years_day_target - current_date_and_time).days

        print(f"\nNew Year's Sale begins in {days_until_new_year_sale} days!")
        # --- End of New Year's Sale countdown ---

    except (FileNotFoundError, PermissionError, KeyError, ValueError):
        # These exceptions are caught and handled with specific messages
        # in the `read_products` and `process_request` functions,
        # so we just let the program exit here after the error message is printed.
        pass
    except Exception as e:
        # Catch any other unhandled exceptions at the main level.
        print(f"An unhandled error occurred during receipt generation: {e}", file=sys.stderr)

# Ensure the main function is called only when the script is executed directly.
if __name__ == "__main__":
    main()

