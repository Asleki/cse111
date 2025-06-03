import csv
import random
import re
import datetime
import time # For OTP simulation
import json # For serializing/deserializing complex user data

# --- Constants for CSV column indexes ---
# For bank_accounts.csv
ACCOUNT_USERNAME_INDEX = 0
ACCOUNT_PASSWORD_INDEX = 1
ACCOUNT_BALANCE_INDEX = 2
ACCOUNT_DETAILS_INDEX = 3 # Stores a JSON string of all other user details

# For bank_transactions.csv
TRANSACTION_TIMESTAMP_INDEX = 0
TRANSACTION_USERNAME_INDEX = 1
TRANSACTION_TYPE_INDEX = 2
TRANSACTION_AMOUNT_INDEX = 3
TRANSACTION_OTHER_ACCOUNT_INDEX = 4 # Used for transfers

# --- File Names ---
ACCOUNTS_FILE = "bank_accounts.csv"
TRANSACTIONS_FILE = "bank_transactions.csv"
EMAIL_INBOX_FILE = "email_inbox.txt" # New constant for email inbox file

# --- ASCII Art / Symbols ---
GREEN_CHECKMARK = "\033[92m✔\033[0m"
RED_X = "\033[91m✖\033[0m"
BLUE_INFO = "\033[94mℹ\033[0m"

# --- Global Bank Information (Not user-specific, so can be global) ---
BANK_NAME = "La Familia Bank"
BANK_TAGLINE = "Your Trusted Financial Partner"
NO_REPLY_EMAIL = "no-reply@lafamiliabank.com"
FEEDBACK_EMAIL = "feedback@lafamiliabank.com"

OUR_BRANCHES = [
    "La Familia Mombasa Road Branch",
    "La Familia Nairobi CBD Branch",
    "La Familia Nairobi Moi Avenue Branch",
    "La Familia Nairobi Afya Centre Branch",
    "La Familia Kisumu Branch"
]

# --- Helper Functions for Data Persistence ---

def read_accounts():
    """
    Reads account data from the ACCOUNTS_FILE CSV into a dictionary.
    Each account's details (beyond username, password, balance) are stored as a JSON string.
    Returns:
        dict: A dictionary where keys are usernames and values are dictionaries
              containing 'password', 'balance', and 'details' (a dict).
    """
    accounts = {}
    try:
        with open(ACCOUNTS_FILE, "rt", newline='') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader, None) # Read header, or None if file is empty
            if header is None:
                return accounts # File is empty, return empty dict
            
            # Expected header: ["username", "password", "balance", "details"]
            if len(header) <= ACCOUNT_DETAILS_INDEX or header[ACCOUNT_DETAILS_INDEX] != "details":
                print(f"{RED_X} Warning: {ACCOUNTS_FILE} header might be incomplete or malformed. Expected 'details' column.")

            for row in reader:
                if len(row) > ACCOUNT_DETAILS_INDEX:
                    username = row[ACCOUNT_USERNAME_INDEX]
                    password = row[ACCOUNT_PASSWORD_INDEX]
                    
                    # Ensure balance is stored as a float
                    try:
                        balance = float(row[ACCOUNT_BALANCE_INDEX])
                    except ValueError:
                        print(f"{RED_X} Warning: Invalid balance for user '{username}'. Setting to 0.0.")
                        balance = 0.0
                    
                    # Deserialize user details from JSON string
                    try:
                        details = json.loads(row[ACCOUNT_DETAILS_INDEX])
                    except json.JSONDecodeError:
                        print(f"{RED_X} Warning: Invalid JSON for user '{username}' details. Initializing empty details.")
                        details = {}
                    
                    accounts[username] = {
                        "password": password,
                        "balance": balance,
                        "details": details # This will hold all the extensive user data
                    }
                else:
                    print(f"{RED_X} Warning: Skipping malformed row in '{ACCOUNTS_FILE}': {row}")
    except FileNotFoundError:
        pass # This is expected if the file doesn't exist yet
    return accounts

def save_accounts(accounts_data):
    """
    Saves account data from a dictionary to the ACCOUNTS_FILE CSV.
    Serializes the 'details' dictionary into a JSON string before saving.
    Args:
        accounts_data (dict): The dictionary of account data to save.
    """
    try:
        with open(ACCOUNTS_FILE, "wt", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["username", "password", "balance", "details"]) # Write header
            for username, data in accounts_data.items():
                # Serialize user details to JSON string
                details_json = json.dumps(data["details"])
                writer.writerow([username, data["password"], data["balance"], details_json])
    except IOError as e:
        print(f"{RED_X} Error: Could not write to {ACCOUNTS_FILE}. Details: {e}")
    except Exception as e:
        print(f"{RED_X} An unexpected error occurred while saving accounts: {e}")

def read_transactions():
    """
    Reads transaction data from the TRANSACTIONS_FILE CSV.
    Returns:
        list: A list of lists, where each inner list represents a transaction row.
    """
    transactions = []
    try:
        with open(TRANSACTIONS_FILE, "rt", newline='') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader, None) # Read header, or None if file is empty
            if header is None:
                return transactions
            
            # Basic validation for header columns
            if len(header) <= max(TRANSACTION_TIMESTAMP_INDEX, TRANSACTION_USERNAME_INDEX, TRANSACTION_TYPE_INDEX, TRANSACTION_AMOUNT_INDEX, TRANSACTION_OTHER_ACCOUNT_INDEX):
                print(f"{RED_X} Warning: {TRANSACTIONS_FILE} header might be incomplete.")

            for row in reader:
                if len(row) > TRANSACTION_AMOUNT_INDEX: # Minimum columns for a valid transaction
                    transactions.append(row)
                else:
                    print(f"{RED_X} Warning: Skipping malformed row in '{TRANSACTIONS_FILE}': {row}")
    except FileNotFoundError:
        pass # This is expected if the file doesn't exist yet
    return transactions

def save_transaction(timestamp, username, transaction_type, amount, other_account=None):
    """
    Appends a single transaction record to the TRANSACTIONS_FILE CSV.
    Args:
        timestamp (str): The timestamp of the transaction.
        username (str): The username associated with the transaction.
        transaction_type (str): Type of transaction (e.g., 'deposit', 'withdraw', 'transfer_out', 'transfer_in').
        amount (float): The amount of the transaction.
        other_account (str, optional): The other account involved in a transfer. Defaults to None.
    """
    try:
        # Check if file exists and has a header, if not, write header first
        file_exists_and_not_empty = False
        try:
            with open(TRANSACTIONS_FILE, "r") as f:
                if f.readline(): # Check if first line exists (implies header or data)
                    file_exists_and_not_empty = True
        except FileNotFoundError:
            pass # File does not exist, so we will create it and add header

        with open(TRANSACTIONS_FILE, "a", newline='') as csv_file:
            writer = csv.writer(csv_file)
            if not file_exists_and_not_empty:
                writer.writerow(["timestamp", "username", "type", "amount", "other_account"]) # Write header
            writer.writerow([timestamp, username, transaction_type, amount, other_account if other_account else "N/A"])
    except IOError as e:
        print(f"{RED_X} Error: Could not write transaction to {TRANSACTIONS_FILE}. Details: {e}")
    except Exception as e:
        print(f"{RED_X} An unexpected error occurred while saving transaction: {e}")

# --- Validation Functions ---

def is_valid_email(email):
    """
    Checks if the given email address is valid using a regular expression.
    Args:
        email (str): The email address to validate.
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None

def is_valid_kra_pin(kra_pin):
    """
    Checks if the given KRA PIN is valid using a regular expression.
    The KRA PIN should start with a capital letter, followed by 5 digits,
    and end with a capital letter.
    Args:
        kra_pin (str): The KRA PIN to validate.
    Returns:
        bool: True if the KRA PIN is valid, False otherwise.
    """
    kra_pin_regex = r"^[A-Z]\d{5}[A-Z]$"
    return re.match(kra_pin_regex, kra_pin) is not None

def check_password_strength(password):
    """
    Checks the strength of a password based on specified criteria.
    Returns a tuple: (strength_score, list_of_reasons_for_weakness)
    """
    reasons = []
    satisfied_criteria = 0

    if len(password) >= 8: # Increased minimum length for bank app
        satisfied_criteria += 1
    else:
        reasons.append("Password must be at least 8 characters long.")

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

# --- Input Handling ---

def get_user_input(prompt, input_type=str):
    """
    Gets user input with a specified prompt and input type. Handles 'M' for Main Menu
    and 'P' for Previous Menu, and potential errors.
    Args:
        prompt (str): The prompt to display to the user.
        input_type (type, optional): The expected input type (e.g., str, int, float).
                                     Defaults to str.
    Returns:
        The user's input, converted to the specified input type. Returns 'M', 'P',
        or None on error/EOF.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input.upper() == 'M':
                return 'M'  # Return 'M' for main menu
            if user_input.upper() == 'P':
                return 'P' # Return 'P' for previous menu
            if input_type == int:
                return int(user_input)
            elif input_type == float:
                return float(user_input)
            elif input_type == str:
                return user_input
            else:
                return user_input
        except ValueError:
            print(f"{RED_X} Invalid input. Please enter the correct type of value.")
        except EOFError:
            print(f"{RED_X} No input received. Exiting.")
            return None  # Or some other sentinel value to indicate termination

# --- Email Simulation Functions ---

def write_email_to_inbox(subject, to_email, from_email, body):
    """Helper function to write a formatted email to the simulated inbox file."""
    try:
        now = datetime.datetime.now()
        email_content = f"""
--- New Email ---
Date and Time: {now:%Y-%m-%d %H:%M:%S}
To: {to_email}
From: {from_email}
Subject: {subject}
Bank: {BANK_NAME} - {BANK_TAGLINE}

{body}

Sincerely,
The {BANK_NAME} Team
--------------------
"""
        with open(EMAIL_INBOX_FILE, "a") as inbox_file:
            inbox_file.write(email_content)
        return True
    except IOError as e:
        print(f"{RED_X} Error: Could not write email to {EMAIL_INBOX_FILE}. Details: {e}")
        return False
    except Exception as e:
        print(f"{RED_X} An unexpected error occurred while saving email to inbox: {e}")
        return False

def send_otp(email, otp):
    """
    Sends an OTP to the provided email address (simulated by writing to file).
    Args:
        email (str): The email address to send the OTP to.
        otp (str): The OTP to send.
    Returns:
        bool: True if email was "sent" successfully, False otherwise.
    """
    subject = f"Your {BANK_NAME} Account Verification Code"
    body = f"""Dear Customer,

Your One-Time Password (OTP) for account verification is: {otp}

This code is valid for a short period. Please use it to complete your process.
Do not share this code with anyone.
"""
    print(f"{BLUE_INFO} Sending OTP to {email} (check {EMAIL_INBOX_FILE}).")
    return write_email_to_inbox(subject, email, NO_REPLY_EMAIL, body)

def send_application_form_email(email):
    """
    Sends a simulated application form email to the provided email address.
    Args:
        email (str): The email address to send the form to.
    Returns:
        bool: True if email was "sent" successfully, False otherwise.
    """
    subject = f"Your {BANK_NAME} Account Application Form"
    body = f"""Dear Customer,

We appreciate your interest in starting a financial journey with {BANK_NAME}.

Attached to this email is your application form. Please download it, fill it carefully,
and then scan the completed copy back to us.

You can download the form from this simulated link:
[Simulated Download Link: {BANK_NAME}_Application_Form.pdf]

We look forward to welcoming you to the {BANK_NAME} family!
"""
    print(f"{BLUE_INFO} Sending application form to {email} (check {EMAIL_INBOX_FILE}).")
    return write_email_to_inbox(subject, email, NO_REPLY_EMAIL, body)

def send_welcome_email(username, email, account_number):
    """
    Sends a simulated welcome email to a new customer.
    Args:
        username (str): The username of the new customer.
        email (str): The email address of the new customer.
        account_number (str): The newly created account number.
    Returns:
        bool: True if email was "sent" successfully, False otherwise.
    """
    subject = f"Welcome to {BANK_NAME}, {username}! Your Account is Ready!"
    body = f"""Dear {username},

Welcome to the {BANK_NAME} family! We are thrilled to have you.

Your new account has been successfully opened. Here are your details:
Account Number: {account_number}
Bank Branch: {BANK_NAME}

You can now log in to our online banking platform using your username and password to manage your finances.

We hope you enjoy your banking experience with us.

Sincerely,
The {BANK_NAME} Team
"""
    print(f"{BLUE_INFO} Sending welcome email to {email} (check {EMAIL_INBOX_FILE}).")
    return write_email_to_inbox(subject, email, NO_REPLY_EMAIL, body)

def send_review_email(username, email, transaction_id="N/A"):
    """
    Sends a simulated email asking the user to rate the store service.
    Args:
        username (str): The username of the customer.
        email (str): The email address of the customer.
        transaction_id (str, optional): An optional transaction ID for context. Defaults to "N/A".
    Returns:
        bool: True if email was "sent" successfully, False otherwise.
    """
    subject = f"How Was Your {BANK_NAME} Experience (Transaction ID: {transaction_id})?"
    body = f"""Dear {username},

Thank you for your recent interaction with {BANK_NAME}!

We hope you had a positive experience. We'd love to hear your feedback
so we can continue to improve our services.
Please take a moment to complete our quick survey and provide a review:
[Link to Survey - This is a placeholder]

Your opinion matters to us!

Sincerely,
The {BANK_NAME} Team
"""
    print(f"{BLUE_INFO} Sending service review request to {email} (check {EMAIL_INBOX_FILE}).")
    return write_email_to_inbox(subject, email, FEEDBACK_EMAIL, body)


# --- Menu Display Functions ---

def display_main_menu(logged_in_status):
    """Displays the main menu options to the user."""
    print("\n" + "=" * 50)
    print(f"{BANK_NAME} - {BANK_TAGLINE}".center(50))
    print("=" * 50)
    print("MAIN MENU".center(50))
    print("=" * 50)
    print("1. Open A bank account")
    print("2. Explore our offers")
    if logged_in_status:
        print("3. Account Services")
        print("4. Logout")
    else:
        print("3. Login to your account") # Added login option for non-logged-in users
        print("4. Exit program")
    print("-" * 50)

def display_account_opening_menu():
    """Displays the menu for opening a bank account."""
    print("\n" + "=" * 50)
    print("Open a Bank Account".center(50))
    print("=" * 50)
    print("1. Open a bank account online")
    print("2. Visit the nearest Bank branch")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_offers_menu():
    """Displays the menu for exploring bank offers."""
    print("\n" + "=" * 50)
    print("Explore Our Offers".center(50))
    print("=" * 50)
    print("1. Bank accounts")
    print("2. Our Cards")
    print("3. ATM locator")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_bank_accounts_menu():
    """Displays the menu for available bank accounts."""
    print("\n" + "=" * 50)
    print("Available Bank Accounts".center(50))
    print("=" * 50)
    print("1. Current Bank account")
    print("2. Club Account")
    print("3. PayGo account")
    print("4. Sapphire Multi currency account")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_cards_menu():
    """Displays the menu for available cards."""
    print("\n" + "=" * 50)
    print("Our Cards".center(50))
    print("=" * 50)
    print("1. Debit Cards")
    print("2. Prepaid Cards")
    print("3. Credit Cards")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_debit_cards():
    print("\n" + "=" * 50)
    print("Debit Cards".center(50))
    print("=" * 50)
    print("1. Club Debit MasterCard")
    print("2. Debit Visa")
    print("3. Gold MasterCard")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_prepaid_cards():
    print("\n" + "=" * 50)
    print("Prepaid Cards".center(50))
    print("=" * 50)
    print("1. Multi Currency Prepaid MasterCard")
    print("2. Sapphire Prepaid Visa")
    print("3. Safari prepaid Visa")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_credit_cards():
    print("\n" + "=" * 50)
    print("Credit Cards".center(50))
    print("=" * 50)
    print("1. Gold Visa Credit Card")
    print("2. Bronze Credit MasterCard")
    print("3. Diamond Credit Card")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_token_machine_menu():
    """Displays the menu for the token machine services."""
    print("\n" + "=" * 50)
    print("Select Service".center(50))
    print("=" * 50)
    print("1. Open a New Bank Account")
    print("2. Close a Bank Account")
    print("3. Reactivate A Bank Account")
    print("4. Statement Enquiry")
    print("5. Cheque Book")
    print("6. Cheque Deposit")
    print("7. Cash Withdrawal")
    print("8. Cash Deposit")
    print("9. Currency Conversion")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_account_details_info(account_type):
    """
    Displays the details of a selected bank account type.
    Args:
        account_type (int): The account type selected by the user.
    Returns:
        dict: A dictionary of account details, or None if invalid type.
    """
    details = None
    if account_type == 1:
        details = {"Account Name": "Current Bank account", "Currency": "Ksh", "Opening balance": 0, "Monthly maintenance fee": 0,
                   "Minimum balance": 0, "Bank Transfers fees": 0.5, "ATM withdrawal charges": 0.3,
                   "Free monthly e-statements": True, "Debit card": 5}
    elif account_type == 2:
        details = {"Account Name": "Club Account", "Currency": "Ksh", "Opening balance": 59, "Monthly maintenance fee": 12,
                   "Minimum balance": 0, "Bank Transfers fees": 0.5, "ATM withdrawal charges": 0.3,
                   "Free monthly e-statements": True, "Free Debit MasterCard": True, "Free Cheque book": True}
    elif account_type == 3:
        details = {"Account Name": "PayGo account", "Currency": "Ksh", "Opening balance": 0, "Monthly maintenance fee": 0,
                   "Minimum balance": 0, "Bank Transfers fees": 0.5, "ATM withdrawal charges": 0.3,
                   "Free monthly e-statements": True, "Free Debit MasterCard": True, "Free Cheque book": True}
    elif account_type == 4:
        details = {"Account Name": "Sapphire Multi Currency Account", "Currency": "USD,GBP,EURO,YEN", "Opening balance": 100,
                   "Monthly maintenance fee": 0, "Minimum balance": 0, "Bank Transfers fees": 0.5,
                   "ATM withdrawal charges": 0.3, "Free monthly e-statements": True, "Free Debit MasterCard": True,
                   "Free Cheque book": True}
    else:
        print(f"{RED_X} Invalid account type.")
        return None

    if details:
        print(f"\n--- {details['Account Name']} Overview ---")
        for key, value in details.items():
            if key != "Account Name":
                print(f"{key}: {value}")
    return details

def display_card_details_info(card_type, specific_card=None):
    """
    Displays the details of a selected card type or a specific card.
    Args:
        card_type (int): The card type (1: Debit, 2: Prepaid, 3: Credit).
        specific_card (int, optional): The specific card selected by the user.
                                      Defaults to None.
    Returns:
        dict: A dictionary of card details, or None if invalid.
    """
    details = None
    if card_type == 1: # Debit Cards
        if specific_card == 1:
            details = {"Card Name": "Club Debit MasterCard", "Overview": "This card can be issued to all bank account holders",
                       "Currency": "Ksh", "Card issuance fee": 5, "Card annual fee": 0, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 2:
            details = {"Card Name": "Debit Visa", "Overview": "This card can be issued to all bank account holders",
                       "Currency": "Ksh", "Card issuance fee": 5, "Card annual fee": 0, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 3:
            details = {"Card Name": "Gold MasterCard", "Overview": "This card can be issued to all bank account holders",
                       "Currency": "Ksh", "Card issuance fee": 10, "Card annual fee": 1, "Card replacement fee": 10,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        else:
            display_debit_cards()
            return None
    elif card_type == 2: # Prepaid Cards
        if specific_card == 1:
            details = {"Card Name": "Multi Currency Prepaid MasterCard", "Overview": "This card is issued to only Sapphire Multi Currency Account Holders",
                       "Currency": "USD, GBP, EURO,YEN", "Card issuance fee": 12, "Card annual fee": 1, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 2:
            details = {"Card Name": "Sapphire Prepaid Visa", "Overview": "This card can be issued to all bank account holders",
                       "Currency": "Ksh", "Card issuance fee": 5, "Card annual fee": 0, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 3:
            details = {"Card Name": "Safari prepaid Visa", "Overview": "This card can be issued to all bank account holders",
                       "Currency": "Ksh", "Card issuance fee": 5, "Card annual fee": 0, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        else:
            display_prepaid_cards()
            return None
    elif card_type == 3: # Credit Cards
        if specific_card == 1:
            details = {"Card Name": "Gold Visa Credit Card", "Overview": "This card can be issued to all bank account holders with loan limits.",
                       "Currency": "Ksh", "Card issuance fee": 5, "Card annual fee": 0, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 2:
            details = {"Card Name": "Bronze Credit MasterCard", "Overview": "This card can be issued to only Multi Currency bank account holders with loan limits.",
                       "Currency": "Ksh", "Card issuance fee": 10, "Card annual fee": 20, "Card replacement fee": 10,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 3:
            details = {"Card Name": "Diamond Credit Card", "Overview": "This card is only issued to Multi Currency Bank account holders with good transaction history and have an accumulative loan limit.",
                       "Currency": "Ksh", "Card issuance fee": 100, "Card annual fee": 10, "Card replacement fee": 199,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        else:
            display_credit_cards()
            return None
    else:
        print(f"{RED_X} Invalid card type.")
        return None

    if details:
        print(f"\n--- {details['Card Name']} Overview ---")
        for key, value in details.items():
            if key != "Card Name":
                print(f"{key}: {value}")
    return details

def display_atm_locations_menu(): # Renamed to avoid conflict with display_atm_locations logic
    """
    Displays the ATM locations menu for a selected bank branch.
    """
    print("\n" + "=" * 50)
    print("ATM Locations".center(50))
    print("=" * 50)
    for i, branch_name in enumerate(OUR_BRANCHES, 1):
        print(f"{i}. {branch_name}")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_request_services_menu():
    """Displays the menu for request services."""
    print("\n" + "=" * 50)
    print("Request Services".center(50))
    print("=" * 50)
    print("1. Cards")
    print("2. Edit My Profile")
    print("3. ATM locator")
    print("4. Add Beneficiary")
    print("5. Add a payment method")
    print("6. Contact Customer Care")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_cards_request_menu():
    """Displays the menu for card-related requests."""
    print("\n" + "=" * 50)
    print("Cards".center(50))
    print("=" * 50)
    print("1. Request for a new card")
    print("2. Activate My Card")
    print("3. Add funds to my Card")
    print("4. Check My Card Details")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_payment_methods_menu():
    """Displays the menu for adding payment methods"""
    print("\n" + "=" * 50)
    print("Add a payment method".center(50))
    print("=" * 50)
    print("1. Mobile money")
    print("2. PayPal")
    print("3. Crypto Currency")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_mobile_money_menu():
    """Displays the menu for Mobile Money Options"""
    print("\n" + "=" * 50)
    print("Mobile Money Options".center(50))
    print("=" * 50)
    print("1. Airtel Money")
    print("2. M-pesa")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_crypto_platforms():
    """Displays the menu for Crypto Currency Platforms"""
    print("\n" + "=" * 50)
    print("Available Crypto Currency platforms".center(50))
    print("=" * 50)
    print("1. Binance")
    print("2. Bybit")
    print("3. Bitget")
    print("4. OKX")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_payments_menu():
    """Displays the menu for Payments"""
    print("\n" + "=" * 50)
    print("Payments".center(50))
    print("=" * 50)
    print("1. Withdraw")
    print("2. Add Funds")
    print("3. Send money")
    print("4. My Payment methods")
    print("5. My Beneficiaries")
    print("6. Withdraw at ATM")
    print("7. Make Purchases")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_withdraw_options():
    """Displays the menu for Withdraw Options"""
    print("\n" + "=" * 50)
    print("Withdraw".center(50))
    print("=" * 50)
    print("1. Withdraw to M-pesa")
    print("2. Withdraw to Airtel Money")
    print("3. Withdraw to PayPal")
    print("4. Withdraw to Crypto Wallet")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_add_funds_options():
    """Displays the menu for Add Funds Options"""
    print("\n" + "=" * 50)
    print("Add Funds".center(50))
    print("=" * 50)
    print("1. Add from M-pesa")
    print("2. Add from PayPal")
    print("3. Add from Airtel Money")
    print("4. Add from Crypto Wallet")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_send_money_options():
    """Displays the menu for Send Money Options"""
    print("\n" + "=" * 50)
    print("Send money".center(50))
    print("=" * 50)
    print("1. Send to Beneficiary")
    print("2. Send to Mobile Money")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_account_services_menu():
    """Displays the menu for account services."""
    print("\n" + "=" * 50)
    print("Account Services".center(50))
    print("=" * 50)
    print("1. View Account Details")
    print("2. Make a Deposit")
    print("3. Make a Withdrawal")
    print("4. View Transaction History")
    print("5. Manage Cards")
    print("6. Request Services")
    print("7. Make Payments")
    print("8. Check Loan Balance/Limit")
    print("9. Logout") # Changed from "Go back to main menu" for clarity
    print("-" * 50)

# --- OTP and Token Functions ---

def get_service_name(service_number):
    """
    Returns the name of the service based on the service number.
    Args:
        service_number (int): The number of the service.
    Returns:
        str: The name of the service.
    """
    services = {
        1: "Open a New Bank Account", 2: "Close a Bank Account",
        3: "Reactivate A Bank Account", 4: "Statement Enquiry",
        5: "Cheque Book", 6: "Cheque Deposit",
        7: "Cash Withdrawal", 8: "Cash Deposit",
        9: "Currency Conversion"
    }
    return services.get(service_number, "Unknown Service")

def display_token(service):
    """
    Displays a stylish token with service details.
    Args:
        service (int): The selected service.
    """
    token_number = random.randint(1, 30)
    service_desk = random.randint(1, 30)
    customers_ahead = token_number - 1 if token_number > 1 else 0

    token_header = "Your Token"
    token_width = 40
    header_padding = (token_width - len(token_header)) // 2

    print("\n" + "#" * token_width)
    print(f"#{' ' * header_padding}{token_header}{' ' * (token_width - len(token_header) - header_padding)}#")
    print("#" * token_width)
    print(f"{'Service:':<15} {get_service_name(service)}")
    
    if 6 <= service <= 9:  # Services 6 to 9 don't have token numbers, desk numbers, or customers ahead.
        print(f"{'Token Number:':<15} N/A")
        print(f"{'Service Desk:':<15} N/A")
        print(f"{'Customers Ahead:':<15} N/A")
    else:
        print(f"{'Token Number:':<15} {token_number}")
        print(f"{'Service Desk:':<15} {service_desk}")
        print(f"{'Customers Ahead:':<15} {customers_ahead}")

    print("\nAdditional Information:")
    if service == 1:
        print("- Have an original ID")
        print("- Have a valid KRA PIN")
        print("- Download the online banking app")
        print("- Have a functional email")
    elif service == 2:
        print("- Have your Bank account details")
        print("- Have original ID")
        print("- 2 recent passport photos")
    elif service == 3:
        print("- Have original ID")
        print("- Download the online banking app")
        print("- Have your old account Bank details")
    elif service == 4:
        print("- Have access to your email address used to register the bank account")
        print("- Have the online banking app")
    elif service == 5:
        print("- Have an existing active Bank Account")
    elif 6 <= service <= 9:
        print("- Proceed to the Customer Care desk for further assistance.")
    print("#" * token_width)
    input("Press Enter to continue...") # Pause for user to read

# --- Core Banking Operations (Adapted for new data structure) ---

def check_balance(current_username):
    """Displays the current balance for the given user."""
    accounts_data = read_accounts()
    if current_username in accounts_data:
        balance = accounts_data[current_username]["balance"]
        print(f"\nYour current balance is: ${balance:.2f}")
    else:
        print(f"{RED_X} Error: Account for '{current_username}' not found.")
    input("Press Enter to continue...")

def deposit(current_username):
    """Allows the user to deposit funds into their account."""
    print("\n--- Deposit Funds ---")
    accounts_data = read_accounts()
    
    if current_username not in accounts_data:
        print(f"{RED_X} Error: Account for '{current_username}' not found.")
        return

    while True:
        amount = get_user_input("Enter amount to deposit: ", float)
        if amount == 'M' or amount == 'P': return amount
        if amount is None: return None # Handle EOFError
        if amount <= 0:
            print(f"{RED_X} Deposit amount must be positive.")
        else:
            break
    
    accounts_data[current_username]["balance"] += amount
    save_accounts(accounts_data)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_transaction(timestamp, current_username, "deposit", amount)
    
    print(f"{GREEN_CHECKMARK} Successfully deposited ${amount:.2f} into your account.")
    check_balance(current_username) # Show updated balance
    return True

def withdraw(current_username):
    """Allows the user to withdraw funds from their account."""
    print("\n--- Withdraw Funds ---")
    accounts_data = read_accounts()

    if current_username not in accounts_data:
        print(f"{RED_X} Error: Account for '{current_username}' not found.")
        return

    current_balance = accounts_data[current_username]["balance"]

    while True:
        amount = get_user_input("Enter amount to withdraw: ", float)
        if amount == 'M' or amount == 'P': return amount
        if amount is None: return None # Handle EOFError
        if amount <= 0:
            print(f"{RED_X} Withdrawal amount must be positive.")
        elif amount > current_balance:
            print(f"{RED_X} Insufficient funds. Your current balance is ${current_balance:.2f}.")
        else:
            break
    
    accounts_data[current_username]["balance"] -= amount
    save_accounts(accounts_data)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_transaction(timestamp, current_username, "withdraw", amount)

    print(f"{GREEN_CHECKMARK} Successfully withdrew ${amount:.2f} from your account.")
    check_balance(current_username) # Show updated balance
    return True

def transfer(current_username):
    """Allows the user to transfer funds to another account."""
    print("\n--- Transfer Funds ---")
    accounts_data = read_accounts()

    if current_username not in accounts_data:
        print(f"{RED_X} Error: Your account '{current_username}' not found.")
        return

    recipient_username = get_user_input("Enter recipient's username: ").strip()
    if recipient_username == 'M' or recipient_username == 'P': return recipient_username
    if recipient_username is None: return None # Handle EOFError

    if recipient_username == current_username:
        print(f"{RED_X} Error: Cannot transfer funds to your own account. Please use deposit instead.")
        return True
    if recipient_username not in accounts_data:
        print(f"{RED_X} Error: Recipient account '{recipient_username}' not found.")
        return True

    current_balance = accounts_data[current_username]["balance"]

    while True:
        amount = get_user_input("Enter amount to transfer: ", float)
        if amount == 'M' or amount == 'P': return amount
        if amount is None: return None # Handle EOFError
        if amount <= 0:
            print(f"{RED_X} Transfer amount must be positive.")
        elif amount > current_balance:
            print(f"{RED_X} Insufficient funds. Your current balance is ${current_balance:.2f}.")
        else:
            break
    
    # Perform the transfer
    accounts_data[current_username]["balance"] -= amount
    accounts_data[recipient_username]["balance"] += amount
    save_accounts(accounts_data)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_transaction(timestamp, current_username, "transfer_out", amount, recipient_username)
    save_transaction(timestamp, recipient_username, "transfer_in", amount, current_username)

    print(f"{GREEN_CHECKMARK} Successfully transferred ${amount:.2f} to '{recipient_username}'.")
    check_balance(current_username) # Show updated balance
    return True

def view_transaction_history(current_username):
    """Displays the transaction history for the given user."""
    print(f"\n--- Transaction History for {current_username} ---")
    transactions = read_transactions()
    
    user_transactions = [t for t in transactions if t[TRANSACTION_USERNAME_INDEX] == current_username]

    if not user_transactions:
        print("No transactions found for this account.")
        input("Press Enter to continue...")
        return

    print(f"{'Timestamp':<20}{'Type':<15}{'Amount':>12}{'Other Account':<15}")
    print(f"{'-'*20:<20}{'-'*15:<15}{'-'*12:>12}{'-'*15:<15}")

    for t in user_transactions:
        timestamp = t[TRANSACTION_TIMESTAMP_INDEX]
        trans_type = t[TRANSACTION_TYPE_INDEX]
        amount = float(t[TRANSACTION_AMOUNT_INDEX])
        other_account = t[TRANSACTION_OTHER_ACCOUNT_INDEX] if len(t) > TRANSACTION_OTHER_ACCOUNT_INDEX else "N/A"

        # Format amount with sign based on transaction type
        display_amount = f"${amount:.2f}"
        if trans_type in ["withdraw", "transfer_out"]:
            display_amount = f"-${amount:.2f}"
        elif trans_type in ["deposit", "initial_deposit", "transfer_in"]:
            display_amount = f"+${amount:.2f}"

        print(f"{timestamp:<20}{trans_type:<15}{display_amount:>12}{other_account:<15}")
    print("-" * 62) # Adjusted length for formatting
    input("Press Enter to continue...")

# --- Account Creation and Login ---

def create_account():
    """
    Guides the user through creating a new bank account.
    Prompts for username and password, performs validation, and saves the new account.
    Collects extensive user details and stores them persistently.
    """
    print("\n--- Create New Account ---")
    
    accounts_data = read_accounts() # Load existing accounts to check for duplicates

    while True:
        new_username = get_user_input("Set a new username: ").strip()
        if new_username == 'M' or new_username == 'P': return new_username
        if new_username is None: return None
        if not new_username:
            print(f"{RED_X} Error: Username cannot be empty. Please try again.")
            continue
        if new_username in accounts_data:
            print(f"{RED_X} Error: Username '{new_username}' already exists. Please choose a different username or login.")
            continue
        break # Valid username

    while True: # Loop until password is strong enough
        new_password = get_user_input("Set a password (min 8 chars, needs uppercase, lowercase, digit, special char): ").strip()
        if new_password == 'M' or new_password == 'P': return new_password
        if new_password is None: return None
        strength_score, reasons = check_password_strength(new_password)

        if strength_score == 10:
            print(f"{GREEN_CHECKMARK} Password strength: 10/10. Great password!")
            break
        else:
            print(f"{RED_X} Password is weak. Strength: {strength_score}/10.")
            print("Reasons:")
            for reason in reasons:
                print(f"- {reason}")
            print("Please try a stronger password.")
    
    # Collect extensive user details
    print("\nPlease provide the following details for your new account:")
    name = get_user_input("Enter your full name: ")
    if name == 'M' or name == 'P': return name
    if name is None: return None

    nationality = get_user_input("Enter your nationality (Kenyan, Ugandan, Tanzanian): ").capitalize()
    if nationality == 'M' or nationality == 'P': return nationality
    if nationality is None: return None
    while nationality not in ["Kenyan", "Ugandan", "Tanzanian"]:
        print(f"{RED_X} Invalid nationality. Please enter Kenyan, Ugandan, or Tanzanian.")
        nationality = get_user_input("Enter your nationality (Kenyan, Ugandan, Tanzanian): ").capitalize()
        if nationality == 'M' or nationality == 'P': return nationality
        if nationality is None: return None

    country_code = "+254" if nationality == "Kenyan" else "+256" if nationality == "Ugandan" else "+255"
    phone_number = get_user_input(f"Enter your phone number (e.g., 712345678 for Kenyan): ")
    if phone_number == 'M' or phone_number == 'P': return phone_number
    if phone_number is None: return None
    
    email = get_user_input("Enter your email address: ")
    if email == 'M' or email == 'P': return email
    if email is None: return None
    while not is_valid_email(email):
        print(f"{RED_X} Invalid email address. Please enter a valid email.")
        email = get_user_input("Enter your email address: ")
        if email == 'M' or email == 'P': break # Allow breaking from validation loop
        if email is None: return None
    if email == 'M' or email == 'P': return email # If loop broke due to M/P, propagate

    kra_pin = get_user_input("Enter your KRA PIN (e.g., A12345B): ")
    if kra_pin == 'M' or kra_pin == 'P': return kra_pin
    if kra_pin is None: return None
    while not is_valid_kra_pin(kra_pin):
        print(f"{RED_X} Invalid KRA PIN. Please enter a valid KRA PIN (e.g., A12345B).")
        kra_pin = get_user_input("Enter your KRA PIN: ")
        if kra_pin == 'M' or kra_pin == 'P': break # Allow breaking from validation loop
        if kra_pin is None: return None
    if kra_pin == 'M' or kra_pin == 'P': return kra_pin # If loop broke due to M/P, propagate
    
    reason = get_user_input("Enter the reason for opening a bank account (Regular transactions, Savings, For Business, Oversea Bank Transactions): ")
    if reason == 'M' or reason == 'P': return reason
    if reason is None: return None
    while reason not in ["Regular transactions", "Savings", "For Business", "Oversea Bank Transactions"]:
        print(f"{RED_X} Invalid reason. Please select from the list.")
        reason = get_user_input("Enter the reason for opening a bank account (Regular transactions, Savings, For Business, Oversea Bank Transactions): ")
        if reason == 'M' or reason == 'P': break
        if reason is None: return None
    if reason == 'M' or reason == 'P': return reason

    occupation = get_user_input("Enter your occupation (Student, Employed, Self-employed): ")
    if occupation == 'M' or occupation == 'P': return occupation
    if occupation is None: return None
    while occupation not in ["Student", "Employed", "Self-employed"]:
        print(f"{RED_X} Invalid occupation. Please select from the list.")
        occupation = get_user_input("Enter your occupation (Student, Employed, Self-employed): ")
        if occupation == 'M' or occupation == 'P': break
        if occupation is None: return None
    if occupation == 'M' or occupation == 'P': return occupation

    source_of_income = get_user_input("Enter your source of income (Salary, Savings, Business, Sponsorship, Family and Relatives): ")
    if source_of_income == 'M' or source_of_income == 'P': return source_of_income
    if source_of_income is None: return None
    while source_of_income not in ["Salary", "Savings", "Business", "Sponsorship", "Family and Relatives"]:
        print(f"{RED_X} Invalid source of income. Please select from the list.")
        source_of_income = get_user_input("Enter your source of income (Salary, Savings, Business, Sponsorship, Family and Relatives): ")
        if source_of_income == 'M' or source_of_income == 'P': break
        if source_of_income is None: return None
    if source_of_income == 'M' or source_of_income == 'P': return source_of_income
    
    monthly_deposits = get_user_input("Enter number of monthly deposits: ", int)
    if monthly_deposits == 'M' or monthly_deposits == 'P': return monthly_deposits
    if monthly_deposits is None: return None

    monthly_withdrawals = get_user_input("Enter number of monthly withdrawals: ", int)
    if monthly_withdrawals == 'M' or monthly_withdrawals == 'P': return monthly_withdrawals
    if monthly_withdrawals is None: return None
    while monthly_withdrawals > monthly_deposits:
        print(f"{RED_X} Withdrawals should not be more than deposits. Please enter again.")
        monthly_withdrawals = get_user_input("Enter number of monthly withdrawals: ", int)
        if monthly_withdrawals == 'M' or monthly_withdrawals == 'P': break
        if monthly_withdrawals is None: return None
    if monthly_withdrawals == 'M' or monthly_withdrawals == 'P': return monthly_withdrawals
    
    monthly_balance = get_user_input("Enter monthly balance you intend to maintain: ", float)
    if monthly_balance == 'M' or monthly_balance == 'P': return monthly_balance
    if monthly_balance is None: return None
    
    address = get_user_input("Enter your address: ")
    if address == 'M' or address == 'P': return address
    if address is None: return None

    print("\nOur Bank Branches:")
    for i, branch in enumerate(OUR_BRANCHES, 1):
        print(f"{i}. {branch}")
    branch_choice = get_user_input("Select your bank branch: ", int)
    if branch_choice == 'M' or branch_choice == 'P': return branch_choice
    if branch_choice is None: return None
    while not 1 <= branch_choice <= len(OUR_BRANCHES):
        print(f"{RED_X} Invalid branch choice. Please select from the list.")
        branch_choice = get_user_input("Select your bank branch: ", int)
        if branch_choice == 'M' or branch_choice == 'P': break
        if branch_choice is None: return None
    if branch_choice == 'M' or branch_choice == 'P': return branch_choice
    my_branch = OUR_BRANCHES[branch_choice - 1]

    # OTP verification
    generated_otp = generate_otp() # Generate OTP here
    if not send_otp(email, generated_otp): # Send OTP email
        print(f"{RED_X} Failed to send OTP email. Account creation aborted.")
        return False # Indicate failure
    
    entered_otp = get_user_input("Enter the OTP you received: ")
    if entered_otp == 'M' or entered_otp == 'P': return entered_otp
    if entered_otp is None: return None

    if entered_otp == generated_otp: # Compare with generated_otp
        print(f"{GREEN_CHECKMARK} Your details have been successfully verified and saved!")
        # Initial balance for a new account
        initial_balance = 0.0
        while True:
            try:
                balance_input = get_user_input("Enter initial deposit amount (e.g., 100.00, minimum 0): ", float)
                if balance_input == 'M' or balance_input == 'P': return balance_input
                if balance_input is None: return None
                initial_balance = float(balance_input)
                if initial_balance < 0:
                    print(f"{RED_X} Initial deposit cannot be negative. Please enter a positive number.")
                else:
                    break
            except ValueError:
                print(f"{RED_X} Invalid amount. Please enter a valid number.")

        # Assign a random account number
        account_number = "ACC" + ''.join(random.choices('0123456789', k=10))
        
        # Store all user data in the 'details' sub-dictionary
        user_details = {
            "name": name,
            "nationality": nationality,
            "phone_number": country_code + phone_number,
            "email": email,
            "kra_pin": kra_pin,
            "reason": reason,
            "occupation": occupation,
            "source_of_income": source_of_income,
            "monthly_deposits": monthly_deposits,
            "monthly_withdrawals": monthly_withdrawals,
            "monthly_balance": monthly_balance,
            "application_date": datetime.date.today().isoformat(), # Store date as ISO format string
            "address": address,
            "branch": my_branch,
            "account_number": account_number, # Store the generated account number
            "account_type_name": "N/A", # Will be set if they choose an account type
            "loan_limit": 0.0,
            "active_loans": 0.0,
            "cards": [],
            "card_pins": [],
            "payment_methods": [],
            "beneficiaries": [],
            "statements": []
        }

        accounts_data[new_username] = {
            "password": new_password,
            "balance": initial_balance,
            "details": user_details
        }
        save_accounts(accounts_data)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_transaction(timestamp, new_username, "initial_deposit", initial_balance)
        
        send_welcome_email(new_username, email, account_number) # Send welcome email

        print(f"\n{GREEN_CHECKMARK} Account for '{new_username}' successfully created with initial balance ${initial_balance:.2f}!")
        print(f"{BLUE_INFO} Your new account number is: {account_number}")
        print(f"{BLUE_INFO} Please remember your username and password for login.")
        return True # Indicate successful account creation
    else:
        print(f"{RED_X} Incorrect OTP. Account creation failed. Please try again.")
        return False # Indicate failed account creation

# --- Main Application Loop ---

def run_banking_app():
    """Manages the main flow of the banking application."""
    current_username = None # Stores the username of the currently logged-in user

    while True: # Outer loop for login/registration
        display_main_menu(current_username is not None)
        choice = get_user_input("Enter your choice: ", int)
        
        if choice is None: # EOFError or other critical input issue
            print("Exiting Application.")
            break
        if choice == 'M': # Should not happen from main menu, but good for consistency
            continue

        if current_username is None: # Not logged in
            if choice == 1: # Open a bank account
                result = handle_account_opening_flow()
                if result is None: break # Exit program
                if result == 'M': continue # Go back to main menu
                continue # Go back to main menu after account opening attempt
            elif choice == 2: # Explore our offers
                result = handle_offers_flow()
                if result is None: break # Exit program
                if result == 'M': continue
                continue
            elif choice == 3: # Login
                username = get_user_input("Enter your username: ").strip()
                if username == 'M' or username == 'P': continue
                if username is None: break

                password = get_user_input("Enter your password: ").strip()
                if password == 'M' or password == 'P': continue
                if password is None: break
                
                accounts_data = read_accounts()
                if username in accounts_data and accounts_data[username]["password"] == password:
                    print(f"\n{GREEN_CHECKMARK} Login successful! Welcome, {username}!")
                    current_username = username
                    # No need to load all user_data into a global, access via accounts_data[current_username]["details"]
                else:
                    print(f"\n{RED_X} Invalid username or password. Please try again.")
                input("Press Enter to continue...")
            elif choice == 4: # Exit program
                print("\nThank you for using the Python Bank Simulation. Goodbye!")
                break
            else:
                print(f"{RED_X} Invalid choice. Please enter 1, 2, 3, or 4.")
                input("Press Enter to continue...")
        else: # Logged in
            if choice == 1: # Open a bank account (re-direct to account services if logged in)
                print(f"{BLUE_INFO} You are already logged in. Redirecting to Account Services.")
                input("Press Enter to continue...")
                result = handle_account_services_flow(current_username)
                if result == "logout":
                    current_username = None
                elif result is None:
                    break
            elif choice == 2: # Explore our offers
                result = handle_offers_flow()
                if result is None: break
                if result == 'M': continue
            elif choice == 3: # Account Services
                result = handle_account_services_flow(current_username)
                if result == "logout":
                    current_username = None
                elif result is None:
                    break
            elif choice == 4: # Logout
                print(f"\nLogging out {current_username}. Returning to main menu.")
                current_username = None # Set to None to exit this loop and re-enter login loop
                input("Press Enter to continue...")
            else:
                print(f"{RED_X} Invalid choice. Please enter 1, 2, 3, or 4.")
                input("Press Enter to continue...")

def handle_account_opening_flow():
    """Handles the flow for opening a bank account."""
    while True:
        display_account_opening_menu()
        account_choice = get_user_input("Enter your choice: ", int)
        if account_choice == 'M': return 'M'
        if account_choice == 'P': return 'P'
        if account_choice is None: return None

        if account_choice == 1: # Open a bank account online
            email = get_user_input("Enter your email address: ")
            if email == 'M' or email == 'P': continue
            if email is None: return None
            while not is_valid_email(email):
                print(f"{RED_X} Invalid email address.")
                email = get_user_input("Enter your email address: ")
                if email == 'M' or email == 'P': break # Allow breaking from validation loop
                if email is None: return None
            if email == 'M' or email == 'P': continue # If loop broke due to M/P

            print(f"{BLUE_INFO} Dear customer, we appreciate your interest in starting a financial journey with us. Attached to this is your application form. Please download it and fill it carefully, then scan the copy back to us.")
            download_choice = get_user_input("Enter Y (yes to download), M (to go back to main menu), or P (to go back to the previous menu): ")
            if download_choice.upper() == 'Y':
                if send_application_form_email(email): # Send the simulated email
                    print(f"{GREEN_CHECKMARK} Application form sent to your email (check {EMAIL_INBOX_FILE}).")
                else:
                    print(f"{RED_X} Failed to send application form email.")
                input("Press Enter to continue...")
            elif download_choice.upper() == 'M':
                return 'M'
            elif download_choice.upper() == 'P':
                continue # Stay in account opening menu
            elif download_choice is None:
                return None
            else:
                print(f"{RED_X} Invalid choice. Returning to the account opening menu.")
                input("Press Enter to continue...")
            return True # Successfully handled online account opening path
        elif account_choice == 2: # Visit the nearest Bank branch
            while True: # Loop for token machine services
                display_token_machine_menu()
                service_choice = get_user_input("Select a service: ", int)
                if service_choice == 'M': return 'M'
                if service_choice == 'P': break # Go back to account opening menu
                if service_choice is None: return None
                
                display_token(service_choice)

                if service_choice == 1: # Open New Account (in-branch flow)
                    has_requirements = get_user_input("Do you have all the requirements listed on your token? (yes/no): ").lower()
                    if has_requirements == 'M' or has_requirements == 'P': continue
                    if has_requirements is None: return None
                    if has_requirements == 'yes':
                        result = create_account() # Call the detailed account creation function
                        if result is True: # Account successfully created
                            return 'M' # Go to main menu after successful creation
                        elif result is None: # EOFError during creation
                            return None
                        # If result is False (OTP incorrect or email failed), stay in token machine menu
                    else:
                        print(f"{BLUE_INFO} Please gather all requirements and visit us again.")
                        input("Press Enter to continue...")
                else: # Other token machine services (placeholder)
                    print(f"{BLUE_INFO} Service '{get_service_name(service_choice)}' will be handled by a bank representative.")
                    input("Press Enter to continue...")
            continue # After breaking from token machine loop, go back to account opening menu
        else:
            print(f"{RED_X} Invalid choice. Please enter 1 or 2.")
            input("Press Enter to continue...")

def handle_offers_flow():
    """Handles the flow for exploring bank offers."""
    while True:
        display_offers_menu()
        offer_choice = get_user_input("Enter your choice: ", int)
        if offer_choice == 'M': return 'M'
        if offer_choice == 'P': return 'P'
        if offer_choice is None: return None

        if offer_choice == 1: # Bank accounts
            while True:
                display_bank_accounts_menu()
                account_type_choice = get_user_input("Select an account type to view details: ", int)
                if account_type_choice == 'M': return 'M'
                if account_type_choice == 'P': break # Go back to offers menu
                if account_type_choice is None: return None
                
                details = display_account_details_info(account_type_choice)
                if details:
                    input("Press Enter to continue...")
            continue # After breaking from bank accounts loop, go back to offers menu
        elif offer_choice == 2: # Our Cards
            while True:
                display_cards_menu()
                card_category_choice = get_user_input("Select a card category: ", int)
                if card_category_choice == 'M': return 'M'
                if card_category_choice == 'P': break # Go back to offers menu
                if card_category_choice is None: return None

                if card_category_choice == 1: # Debit Cards
                    while True:
                        display_debit_cards()
                        debit_card_choice = get_user_input("Select a debit card to view details: ", int)
                        if debit_card_choice == 'M': return 'M'
                        if debit_card_choice == 'P': break # Go back to cards menu
                        if debit_card_choice is None: return None
                        display_card_details_info(1, debit_card_choice)
                        input("Press Enter to continue...")
                    continue
                elif card_category_choice == 2: # Prepaid Cards
                    while True:
                        display_prepaid_cards()
                        prepaid_card_choice = get_user_input("Select a prepaid card to view details: ", int)
                        if prepaid_card_choice == 'M': return 'M'
                        if prepaid_card_choice == 'P': break # Go back to cards menu
                        if prepaid_card_choice is None: return None
                        display_card_details_info(2, prepaid_card_choice)
                        input("Press Enter to continue...")
                    continue
                elif card_category_choice == 3: # Credit Cards
                    while True:
                        display_credit_cards()
                        credit_card_choice = get_user_input("Select a credit card to view details: ", int)
                        if credit_card_choice == 'M': return 'M'
                        if credit_card_choice == 'P': break # Go back to cards menu
                        if credit_card_choice is None: return None
                        display_card_details_info(3, credit_card_choice)
                        input("Press Enter to continue...")
                    continue
                else:
                    print(f"{RED_X} Invalid card category choice.")
                    input("Press Enter to continue...")
            continue # After breaking from cards category loop, go back to offers menu
        elif offer_choice == 3: # ATM locator
            result = display_atm_locations() # This function handles its own loop and returns 'M'/'P'
            if result == 'M': return 'M'
            if result == 'P': continue # Stay in offers menu after ATM locator
            if result is None: return None
        else:
            print(f"{RED_X} Invalid choice. Please enter 1, 2, or 3.")
            input("Press Enter to continue...")

def handle_account_services_flow(current_username):
    """Handles the flow for logged-in account services."""
    while True:
        display_account_services_menu()
        service_choice = get_user_input("Enter your choice: ", int)
        if service_choice == 'M': return 'M'
        if service_choice == 'P': return 'P' # Return to main menu (or previous if nested)
        if service_choice is None: return None

        if service_choice == 1: # View Account Details
            accounts_data = read_accounts()
            user_details = accounts_data[current_username]["details"]
            print(f"\n--- Your Account Details ({current_username}) ---")
            print(f"Account Number: {user_details.get('account_number', 'N/A')}")
            print(f"Account Type: {user_details.get('account_type_name', 'Not Set')}")
            print(f"Current Balance: ${accounts_data[current_username]['balance']:.2f}")
            for key, value in user_details.items():
                if key not in ['account_number', 'account_type_name']: # Avoid re-printing
                    print(f"{key.replace('_', ' ').title()}: {value}")
            input("Press Enter to continue...")
        elif service_choice == 2: # Make a Deposit
            result = deposit(current_username)
            if result == 'M': return 'M'
            if result == 'P': continue
            if result is None: return None
        elif service_choice == 3: # Make a Withdrawal
            result = withdraw(current_username)
            if result == 'M': return 'M'
            if result == 'P': continue
            if result is None: return None
        elif service_choice == 4: # View Transaction History
            view_transaction_history(current_username)
        elif service_choice == 5: # Manage Cards (placeholder for now)
            print(f"{BLUE_INFO} Card management features are under development.")
            input("Press Enter to continue...")
        elif service_choice == 6: # Request Services (placeholder for now)
            print(f"{BLUE_INFO} Request services features are under development.")
            input("Press Enter to continue...")
        elif service_choice == 7: # Make Payments (placeholder for now)
            print(f"{BLUE_INFO} Payment features are under development.")
            input("Press Enter to continue...")
        elif service_choice == 8: # Check Loan Balance/Limit (placeholder for now)
            accounts_data = read_accounts()
            user_details = accounts_data[current_username]["details"]
            loan_limit = user_details.get("loan_limit", 0.0)
            active_loans = user_details.get("active_loans", 0.0)
            print(f"\n--- Loan Information ---")
            print(f"Your Loan Limit: ${loan_limit:.2f}")
            print(f"Active Loans: ${active_loans:.2f}")
            input("Press Enter to continue...")
        elif service_choice == 9: # Logout
            return "logout" # Signal to the calling function to log out
        else:
            print(f"{RED_X} Invalid choice. Please enter a number between 1 and 9.")
            input("Press Enter to continue...")

# --- Main Execution Block ---

if __name__ == "__main__":
    random.seed() # Seed the random number generator
    run_banking_app()
