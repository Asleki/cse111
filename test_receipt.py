import sys
import os
import io
import subprocess # Import subprocess module
from datetime import datetime

# Assume the main program is in 'receipt.py'

def create_csv_file(filename, content):
    """Creates a CSV file with the given content."""
    try:
        with open(filename, "w") as f:
            f.write(content)
    except Exception as e:
        print(f"Error creating file {filename}: {e}", file=sys.stderr)
        sys.exit(1)

def clean_up_files(files):
    """Deletes specified files."""
    for filename in files:
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Error cleaning up file {filename}: {e}", file=sys.stderr)

def run_receipt_program():
    """
    Runs the receipt.py program as a subprocess and captures its stdout and stderr.
    This provides a clean execution environment for each test.
    """
    try:
        # Run receipt.py as a subprocess.
        # capture_output=True captures stdout and stderr.
        # text=True decodes stdout/stderr as text.
        # sys.executable ensures the same Python interpreter is used.
        result = subprocess.run(
            [sys.executable, 'receipt.py'],
            capture_output=True,
            text=True,
            check=False # Do not raise CalledProcessError for non-zero exit codes; we want to capture stderr
        )
        stdout = result.stdout
        stderr = result.stderr
    except FileNotFoundError:
        # This handles cases where 'python' command itself is not found, or receipt.py doesn't exist.
        # In our case, it's more likely due to a missing receipt.py.
        stdout = ""
        stderr = "Error: receipt.py not found. Make sure it's in the same directory as test_receipt.py\n"
    except Exception as e:
        stdout = ""
        stderr = f"An unexpected error occurred while trying to run receipt.py: {e}\n"

    return stdout, stderr

def test_scenario(name, products_content, request_content, expected_output_substrings=None, expected_error_substrings=None, files_to_clean=('products.csv', 'request.csv')):
    """
    Runs a test scenario, creates CSV files, executes the program,
    and checks its output/errors.
    """
    print(f"\n--- Running Test: {name} ---")
    
    # Ensure a clean slate before each test
    clean_up_files(files_to_clean)

    # Create necessary CSV files
    if products_content is not None:
        create_csv_file('products.csv', products_content)
    if request_content is not None:
        create_csv_file('request.csv', request_content)

    # Run the receipt program and capture output
    stdout, stderr = run_receipt_program()

    # Check for expected output
    passed = True
    if expected_output_substrings:
        for substring in expected_output_substrings:
            if substring not in stdout:
                print(f"FAIL: Expected output '{substring}' not found in stdout.")
                passed = False
    
    # Check for expected errors
    if expected_error_substrings:
        for substring in expected_error_substrings:
            if substring not in stderr:
                print(f"FAIL: Expected error '{substring}' not found in stderr.")
                passed = False

    # Optional: Print actual output for debugging failed tests
    if not passed:
        print("\n--- Actual STDOUT ---")
        print(stdout)
        print("\n--- Actual STDERR ---")
        print(stderr)
    
    if passed:
        print(f"Test '{name}': PASS")
    else:
        print(f"Test '{name}': FAIL")
    
    # Clean up after test
    clean_up_files(files_to_clean)
    return passed

def main_test_runner():
    """Defines and runs all test cases."""
    all_tests_passed = True

    # --- Test Case 1: Normal Operation ---
    products_normal = """id,name,price
111,wheat bread,2.55
222,1 cup yogurt,0.75
333,32 oz granola,3.21
444,twix candy bar,0.85
D083,Inkom Special,5.00
"""
    request_normal = """id,quantity
111,2
222,4
333,1
444,2
222,3
D083,3
"""
    # Note: The exact date/time output will vary, so we only check static parts.
    expected_output_normal = [
        "Inkom Emporium",
        "wheat bread: 2 @ 2.55",
        "1 cup yogurt: 4 @ 0.75",
        "32 oz granola: 1 @ 3.21",
        "twix candy bar: 2 @ 0.85",
        "1 cup yogurt: 3 @ 0.75",
        "Inkom Special: 3 @ 5.00 (BOGO 50% Off Applied)", # Check for BOGO message
        "Number of Items: 15", 
        # Subtotal calculation for verification:
        # 2*2.55 (wheat bread) = 5.10
        # 4*0.75 (1 cup yogurt) = 3.00
        # 1*3.21 (32 oz granola) = 3.21
        # 2*0.85 (twix candy bar) = 1.70
        # 3*0.75 (1 cup yogurt) = 2.25
        # D083,3 (Inkom Special BOGO): 2 full price (2*5.00=10.00) + 1 half price (1*2.50=2.50) = 12.50
        # Total Subtotal = 5.10 + 3.00 + 3.21 + 1.70 + 2.25 + 12.50 = 27.76
        "Subtotal: 27.76",
        # Sales Tax = 27.76 * 0.06 = 1.6656 -> 1.67 (rounded)
        "Sales Tax: 1.67",
        # Total = 27.76 + 1.67 = 29.43
        "Total: 29.43",
        "Thank you for shopping at the Inkom Emporium.",
        "Return by:", # Check for return by date message
        "New Year's Sale begins in", # Check for New Year's countdown message
    ]
    all_tests_passed &= test_scenario("Normal Operation", products_normal, request_normal, expected_output_normal)

    # --- Test Case 2: KeyError (Unknown Product ID in request.csv) ---
    request_key_error = """id,quantity
111,2
R002,5
"""
    expected_error_key_error = [
        "Error: unknown product ID in the request.csv file",
        "'R002'"
    ]
    all_tests_passed &= test_scenario("KeyError (Unknown Product ID)", products_normal, request_key_error, 
                                      expected_error_substrings=expected_error_key_error)

    # --- Test Case 3: FileNotFoundError (Missing products.csv) ---
    # We will pass None for products_content to simulate missing file
    expected_error_file_not_found = [
        "Error: missing file",
        "No such file or directory: 'products.csv'"
    ]
    all_tests_passed &= test_scenario("FileNotFoundError (Missing products.csv)", None, request_normal, 
                                      expected_error_substrings=expected_error_file_not_found,
                                      files_to_clean=('request.csv',)) # products.csv won't exist to clean

    # --- Test Case 4: FileNotFoundError (Missing request.csv) ---
    # We will pass None for request_content to simulate missing file
    expected_error_request_not_found = [
        "Error: missing file",
        "No such file or directory: 'request.csv'"
    ]
    all_tests_passed &= test_scenario("FileNotFoundError (Missing request.csv)", products_normal, None, 
                                      expected_error_substrings=expected_error_request_not_found,
                                      files_to_clean=('products.csv',)) # request.csv won't exist to clean
    
    # --- Test Case 5: ValueError (Invalid quantity in request.csv) ---
    request_value_error_qty = """id,quantity
111,abc
"""
    expected_error_value_error_qty = [
        "Error: Invalid quantity format for product '111' in request.csv. Skipping row.",
        # The next error message is also printed to stderr by receipt.py if a ValueError is raised
        "Error: invalid data in request.csv (e.g., non-integer quantity or non-float price)"
    ]
    all_tests_passed &= test_scenario("ValueError (Invalid Quantity)", products_normal, request_value_error_qty,
                                      expected_error_substrings=expected_error_value_error_qty)

    # --- Test Case 6: ValueError (Invalid price in products.csv) ---
    products_value_error_price = """id,name,price
111,test item,invalid_price
"""
    request_value_error_price = """id,quantity
111,1
"""
    # For invalid price, the error is printed to stderr, and the item is skipped.
    # The subtotal would then be 0.00 if no other valid items are processed.
    expected_output_value_error_price = [
        "Subtotal: 0.00" # This comes from stdout
    ]
    expected_error_value_error_price = [
        "Error: Invalid price format for product '111' in products.csv. Skipping row." # This comes from stderr
    ]
    all_tests_passed &= test_scenario("ValueError (Invalid Price)", products_value_error_price, request_value_error_price,
                                      expected_output_substrings=expected_output_value_error_price,
                                      expected_error_substrings=expected_error_value_error_price)
    
    # --- Final Summary ---
    print("\n" + "="*30)
    if all_tests_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")
    print("="*30)

if __name__ == "__main__":
    main_test_runner()

