import csv

# Define constants for column indexes in products.csv
PRODUCT_NUMBER_INDEX = 0
PRODUCT_NAME_INDEX = 1
PRODUCT_PRICE_INDEX = 2

# Define constants for column indexes in request.csv
REQUEST_PRODUCT_NUMBER_INDEX = 0
REQUEST_QUANTITY_INDEX = 1

def main():
    """
    Reads product data from products.csv into a dictionary,
    then reads customer requests from request.csv,
    and prints a receipt of the requested items.
    """
    try:
        # Call the read_dictionary function and store the compound dictionary
        # in a variable named products_dict.
        products_dict = read_dictionary("products.csv", PRODUCT_NUMBER_INDEX)

        # Print the products_dict for verification.
        print("All Products")
        print(products_dict)
        print() # Print a blank line for readability

        print("Requested Items")

        # Open the request.csv file for reading.
        with open("request.csv", "rt") as request_file:
            # Use the csv module to create a reader object that will read
            # from the opened CSV file.
            reader = csv.reader(request_file)

            # Skip the first line of the request.csv file because it contains
            # column headings.
            next(reader)

            # Use a loop that reads and processes each row from the request.csv file.
            for row_list in reader:
                # Ensure the row is not empty before processing
                if len(row_list) != 0:
                    # Extract the requested product number and quantity from the current row.
                    product_number = row_list[REQUEST_PRODUCT_NUMBER_INDEX]
                    quantity = int(row_list[REQUEST_QUANTITY_INDEX])

                    # Use the requested product number to find the corresponding item
                    # in the products_dict.
                    if product_number in products_dict:
                        product_info = products_dict[product_number]
                        product_name = product_info[PRODUCT_NAME_INDEX]
                        product_price = float(product_info[PRODUCT_PRICE_INDEX])

                        # Print the product name, requested quantity, and product price.
                        # Example format: "wheat bread: 2 @ 2.55"
                        print(f"{product_name}: {quantity} @ {product_price:.2f}")
                    else:
                        # Optional: Handle cases where product number from request is not found
                        print(f"Error: Product with number '{product_number}' not found in products catalog.")

    except FileNotFoundError as not_found_err:
        print(f"Error: one of the required files was not found. {not_found_err}")
        print("Please ensure 'products.csv' and 'request.csv' are in the same directory.")
    except Exception as excep:
        print(f"An unexpected error occurred: {excep}")


def read_dictionary(filename, key_column_index):
    """
    Read the contents of a CSV file into a compound dictionary and return the dictionary.

    Parameters:
        filename: The name of the CSV file to read.
        key_column_index: The index of the column to use as the keys in the dictionary.
    Return:
        A compound dictionary that contains the contents of the CSV file.
    """
    # Create an empty dictionary that will store the data from the CSV file.
    dictionary = {}

    # Open the CSV file for reading and store a reference
    # to the opened file in a variable named csv_file.
    with open(filename, "rt") as csv_file:
        # Use the csv module to create a reader object
        # that will read from the opened CSV file.
        reader = csv.reader(csv_file)

        # The first row of the CSV file contains column
        # headings and not data, so this statement skips
        # the first row of the CSV file.
        next(reader)

        # Read the rows in the CSV file one row at a time.
        # The reader object returns each row as a list.
        for row_list in reader:
            # If the current row is not blank, add the
            # data from the current to the dictionary.
            if len(row_list) != 0:
                # From the current row, retrieve the data
                # from the column that contains the key.
                key = row_list[key_column_index]

                # Store the data from the current
                # row into the dictionary.
                # The value will be the entire row_list.
                dictionary[key] = row_list

    # Return the dictionary.
    return dictionary

# Call main to start this program.
if __name__ == "__main__":
    main()