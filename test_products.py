import csv # This line brings in the 'csv' module, which helps us work with CSV files.

# These are like labels for the columns in our 'products.csv' file.
# They help us remember what number goes with what piece of information.
PRODUCT_NUMBER_INDEX = 0 # Product number is in the first column (index 0).
PRODUCT_NAME_INDEX = 1   # Product name is in the second column (index 1).
PRODUCT_PRICE_INDEX = 2  # Product price is in the third column (index 2).

# These are labels for the columns in our 'request.csv' file.
REQUEST_PRODUCT_NUMBER_INDEX = 0 # Product number is in the first column here too.
REQUEST_QUANTITY_INDEX = 1       # The quantity a customer wants is in the second column.

def main():
    """
    This is the main part of our program!
    It reads all the product info, then reads a customer's order,
    and finally prints out a simple receipt.
    """
    try:
        # First, we call a special function 'read_dictionary' to get all our
        # product details from 'products.csv'. We tell it to use the product
        # number as the main 'key' for each item in our product list.
        products_dict = read_dictionary("products.csv", PRODUCT_NUMBER_INDEX)

        # Let's print out all the products we have in our 'products_dict'
        # just to see what's inside.
        print("All Products")
        print(products_dict)
        print() # This just prints an empty line to make the output easier to read.

        print("Requested Items") # Now we'll show what the customer ordered.

        # We're opening the 'request.csv' file here. The 'with' part
        # makes sure the file closes itself automatically when we're done.
        with open("request.csv", "rt") as request_file:
            # We use 'csv.reader' to help us read the CSV file row by row.
            reader = csv.reader(request_file)

            # The very first line in 'request.csv' is just headings (like "Product Number"),
            # not actual order data. So, 'next(reader)' skips that first line.
            next(reader)

            # Now we go through each row in the customer's order file, one by one.
            for row_list in reader:
                # We check if the row isn't empty before trying to use it.
                if len(row_list) != 0:
                    # We grab the product number and the quantity the customer wants
                    # from the current row. We turn the quantity into a whole number.
                    product_number = row_list[REQUEST_PRODUCT_NUMBER_INDEX]
                    quantity = int(row_list[REQUEST_QUANTITY_INDEX])

                    # Now we use the product number from the customer's request
                    # to look up the full product details in our 'products_dict'.
                    if product_number in products_dict:
                        product_info = products_dict[product_number]
                        product_name = product_info[PRODUCT_NAME_INDEX]
                        # We turn the price into a decimal number.
                        product_price = float(product_info[PRODUCT_PRICE_INDEX])

                        # Finally, we print out what the customer ordered,
                        # showing the name, how many they want, and the price per item.
                        # It'll look something like: "wheat bread: 2 @ 2.55"
                        print(f"{product_name}: {quantity} @ {product_price:.2f}")
                    else:
                        # If for some reason a product number in the request isn't found
                        # in our products list, we'll print an error message.
                        print(f"Error: Product with number '{product_number}' not found in products catalog.")

    # This part handles problems that might come up.
    # If the file isn't found (like if 'products.csv' or 'request.csv' is missing).
    except FileNotFoundError as not_found_err:
        print(f"Error: We couldn't find one of the files needed. Details: {not_found_err}")
        print("Please make sure 'products.csv' and 'request.csv' are in the same folder as this program.")
    # This catches any other unexpected errors that might happen during the program's run.
    except Exception as excep:
        print(f"Oops! An unexpected error happened: {excep}")


def read_dictionary(filename, key_column_index):
    """
    This function reads data from a CSV file and puts it into a special
    kind of list called a 'dictionary'.

    Parameters:
        filename (str): The name of the CSV file we want to read (e.g., "products.csv").
        key_column_index (int): This tells the function which column in the CSV
                                should be used as the unique identifier (the 'key')
                                for each item in our dictionary.
    Returns:
        dict: A dictionary where each 'key' is a unique product ID,
              and the 'value' is a list containing all the info
              for that product from the CSV row.
    """
    # We start with an empty dictionary. This is where we'll put all our product data.
    dictionary = {}

    # We open the CSV file to read it. Again, 'with' makes sure the file closes itself.
    with open(filename, "rt") as csv_file:
        # 'csv.reader' helps us read the file, splitting it into rows and columns.
        reader = csv.reader(csv_file)

        # We skip the very first line because it usually just has headings like "Product Name".
        next(reader)

        # Now we go through each row in the CSV file, one by one.
        for row_list in reader:
            # We check if the row isn't completely blank.
            if len(row_list) != 0:
                # We grab the part of the row that we want to use as our unique 'key'
                # (like the product number).
                key = row_list[key_column_index]

                # We add this row's data to our dictionary. The 'key' is the product number,
                # and the 'value' is the entire list of details for that product.
                dictionary[key] = row_list

    # Once we've gone through all the rows, we give back the dictionary full of data.
    return dictionary

# This line is important! It tells Python to run the 'main' function
# only when this script is run directly (not when it's just imported
# as a helper into another script).
if __name__ == "__main__":
    main()
    
# Copyright 2025, Alex Malunda. All rights reserved.