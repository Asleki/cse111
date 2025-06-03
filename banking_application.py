import random
import re
import datetime
import time
import os

# --- Global Variables and Constants ---
# Constants for inbox files
EMAIL_INBOX_FILE = "email_inbox.txt"
MESSAGE_INBOX_FILE = "message_inbox.txt"

# Global user session data (will be managed more cleanly in a class in a larger app)
user_data = {}
account_number = None
user_password = None
logged_in = False
account_balance = 0.0
account_type_name = "N/A" # Default account type name
account_details = {} # To store details like currency for the active account
my_cards = [] # List to hold card details
my_card_pins = {} # Dictionary to store card_number: pin
my_payment_methods = [] # List to hold payment methods (e.g., mobile money, PayPal)
my_beneficiaries = [] # List to hold beneficiaries
statements = [] # List to hold transaction statements
loan_limit = 0.0
active_loans = 0 # Number of active loans

# Branch information with mock ATM locations
our_branches = {
    1: {"name": "La Familia Mombasa Road Branch", "atms": ["ATM-MOM-001 (Ground Floor)", "ATM-MOM-002 (First Floor)"]},
    2: {"name": "La Familia Nairobi CBD Branch", "atms": ["ATM-CBD-001 (Main Entrance)", "ATM-CBD-002 (Kenyatta Avenue Exit)"]},
    3: {"name": "La Familia Nairobi Moi Avenue Branch", "atms": ["ATM-MOI-001 (Outside)", "ATM-MOI-002 (Inside Branch)"]},
    4: {"name": "La Familia Nairobi Afya Centre", "atms": ["ATM-AFYA-001 (Street Level)", "ATM-AFYA-002 (Mezzanine Floor)"]},
    5: {"name": "La Familia Kisumu Branch", "atms": ["ATM-KIS-001 (Ojijo Road)", "ATM-KIS-002 (Mega City Mall)"]}
}

# --- Helper Functions ---

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input(prompt, input_type=str):
    """
    Gets user input, handles 'M' for main menu, 'P' for previous menu,
    and 'X' or empty for exit.
    Returns None if user chooses to exit, or 'M'/'P' for navigation,
    otherwise returns the input cast to the specified type.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input.upper() == 'M':
                return 'M'
            elif user_input.upper() == 'P':
                return 'P'
            elif user_input.upper() in ('X', ''): # X or empty input to exit
                return None
            return input_type(user_input)
        except ValueError:
            print("Invalid input. Please try again.")

def is_valid_email(email):
    """Basic email validation."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_kra_pin(kra_pin):
    """Basic KRA PIN validation (e.g., A123456789B)."""
    return re.match(r"^[A-Z]\d{9}[A-Z]$", kra_pin) is not None

def generate_otp():
    """Generates a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def send_otp(email):
    """
    Sends an OTP to the provided email address (simulated by writing to file).

    Args:
        email (str): The email address to send the OTP to.

    Returns:
        str: The generated OTP.
    """
    otp = generate_otp()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write OTP to message_inbox.txt
    try:
        with open(MESSAGE_INBOX_FILE, "a") as f: # 'a' for append mode
            f.write(f"[{timestamp}] To: {email} - Your La Familia Bank OTP is: {otp}\n")
        print(f"OTP sent to {email} (check {MESSAGE_INBOX_FILE})")
    except IOError as e:
        print(f"Error writing OTP to inbox file: {e}")
        print(f"Your OTP is: {otp}") # Fallback to display if file write fails

    return otp

def validate_password(password):
    """
    Validates password complexity:
    - At least 8 characters
    - At least one special character
    - At least one lowercase and one uppercase character
    - No spaces
    """
    special_char_regex = r"[!@#$%^&*(),.?\":{}|<>]"
    lower_case_regex = r"[a-z]"
    upper_case_regex = r"[A-Z]"

    if (len(password) >= 8 and
        re.search(special_char_regex, password) and
        re.search(lower_case_regex, password) and
        re.search(upper_case_regex, password) and
        " " not in password):
        return True
    return False

def add_transaction_statement(type, amount, current_balance, currency="Ksh"):
    """Adds a transaction record to the statements list."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    statement = f"[{timestamp}] {type}: {currency} {amount:.2f}. New Balance: {currency} {current_balance:.2f}"
    statements.append(statement)

# --- Menu Display Functions ---

def display_main_menu():
    """Displays the main menu options."""
    clear_screen()
    print("--- Welcome to La Familia Bank ---")
    print("1. Open a Bank Account")
    print("2. Explore Our Offers")
    if logged_in:
        print("3. Account Services")
        print("4. Logout")
    print("X. Exit")
    print("-----------------------------------")

def display_account_opening_menu():
    """Displays account opening options."""
    print("\n--- Open a Bank Account ---")
    print("1. Apply for Online Account Opening")
    print("2. Get a Token to Visit a Branch")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("---------------------------")

def display_offers_menu():
    """Displays the offers menu."""
    print("\n--- Explore Our Offers ---")
    print("1. Bank Accounts")
    print("2. Cards")
    print("3. ATM Locator")
    print("4. Apply for a Loan") # New option for loans
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("--------------------------")

def display_bank_accounts_menu():
    """Displays available bank account types."""
    print("\n--- Available Bank Account Types ---")
    print("1. Current Account (Ksh 0 Opening Balance)")
    print("2. Savings Account (Ksh 500 Opening Balance)")
    print("3. Fixed Deposit Account (Ksh 10,000 Opening Balance)")
    print("4. Junior Savers Account (Ksh 0 Opening Balance)")
    print("5. Business Account (Ksh 2,000 Opening Balance)")
    print("6. USD Account (USD 10 Opening Balance)")
    print("7. EURO Account (EURO 10 Opening Balance)")
    print("8. GBP Account (GBP 10 Opening Balance)")
    print("9. YEN Account (YEN 1000 Opening Balance)")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("------------------------------------")

def display_cards_menu():
    """Displays general card options."""
    print("\n--- Cards ---")
    print("1. Debit Cards")
    print("2. Prepaid Cards")
    print("3. Credit Cards")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("-------------")

def display_debit_cards():
    """Displays types of debit cards."""
    print("\n--- Debit Cards ---")
    print("1. Visa Classic Debit Card")
    print("2. Mastercard Standard Debit Card")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("-------------------")

def display_prepaid_cards():
    """Displays types of prepaid cards."""
    print("\n--- Prepaid Cards ---")
    print("1. Travel Prepaid Card")
    print("2. Gift Prepaid Card")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("---------------------")

def display_credit_cards():
    """Displays types of credit cards."""
    print("\n--- Credit Cards ---")
    print("1. Visa Gold Credit Card")
    print("2. Mastercard Platinum Credit Card")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("--------------------")

def display_token_machine_menu():
    """Displays token machine service options."""
    print("\n--- Token Machine Services ---")
    print("1. Open a New Bank Account")
    print("2. Close a Bank Account")
    print("3. Reactivate A Bank Account")
    print("4. Statement Enquiry")
    print("5. Cheque Book Request")
    print("6. Cheque Deposit")
    print("7. Cash Withdrawal")
    print("8. Cash Deposit")
    print("9. Currency Conversion")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("------------------------------")

def get_service_name(service_number):
    """
    Returns the name of the service based on the service number.
    """
    services = {
        1: "Open a New Bank Account",
        2: "Close a Bank Account",
        3: "Reactivate A Bank Account",
        4: "Statement Enquiry",
        5: "Cheque Book",
        6: "Cheque Deposit",
        7: "Cash Withdrawal",
        8: "Cash Deposit",
        9: "Currency Conversion"
    }
    return services.get(service_number, "Unknown Service")

def display_token(service):
    """Displays a simulated token and requirements for a service."""
    service_name = get_service_name(service)
    print(f"\nYour token number for '{service_name}' is: {random.randint(100, 999)}")
    print("Please wait for your number to be called.")
    print("Requirements:")
    if service == 1:
        print("Have an original ID")
        print("Have a valid KRA PIN")
        print("Download the online banking app") # This applies to online app
        print("Have a functional email")
    elif service == 2:
        print("Have your Bank account details")
        print("Have original ID")
        print("2 recent passport photos")
    elif service == 3:
        print("Have original ID")
        print("Download the online banking app")
        print("Have your old account Bank details")
    elif service == 4:
        print("Have access to your email address used")
        print("To register the bank account")
        print("Have the online banking app")
    elif service == 5:
        print("Have an existing active Bank Account")
    elif 6 <= service <= 9:
        print("Proceed to the Customer Care desk for further assistance.")
    time.sleep(2) # Simulate delay


def display_account_details(account_type_choice):
    """
    Displays details for a selected bank account type.
    Returns a dictionary of account details or None if invalid choice.
    """
    global account_type_name # To update the global variable
    account_types = {
        1: {"name": "Current Account", "Opening balance": 0, "Currency": "Ksh"},
        2: {"name": "Savings Account", "Opening balance": 500, "Currency": "Ksh"},
        3: {"name": "Fixed Deposit Account", "Opening balance": 10000, "Currency": "Ksh"},
        4: {"name": "Junior Savers Account", "Opening balance": 0, "Currency": "Ksh"},
        5: {"name": "Business Account", "Opening balance": 2000, "Currency": "Ksh"},
        6: {"name": "USD Account", "Opening balance": 10, "Currency": "USD"},
        7: {"name": "EURO Account", "Opening balance": 10, "Currency": "EURO"},
        8: {"name": "GBP Account", "Opening balance": 10, "Currency": "GBP"},
        9: {"name": "YEN Account", "Opening balance": 1000, "Currency": "YEN"}
    }

    details = account_types.get(account_type_choice)
    if details:
        account_type_name = details["name"] # Update global
        print(f"\n--- {details['name']} Details ---")
        print(f"Opening Balance: {details['Currency']} {details['Opening balance']}")
        print(f"Currency: {details['Currency']}")
        # Add more details relevant to each account type
        if details["name"] == "Current Account":
            print("Features: Daily transactions, unlimited withdrawals.")
        elif details["name"] == "Savings Account":
            print("Features: Earn interest, limited withdrawals per month.")
        elif details["name"] == "Fixed Deposit Account":
            print("Features: Higher interest rates, funds locked for a period.")
        elif details["name"] == "Junior Savers Account":
            print("Features: For minors, parental supervision, educational benefits.")
        elif details["name"] == "Business Account":
            print("Features: For businesses, multiple signatories, transaction limits.")
        return details
    else:
        print("Invalid account type choice.")
        return None

def display_card_details(card_type, card_choice):
    """
    Displays details for a selected card type.
    card_type: 1 for Debit, 2 for Prepaid, 3 for Credit
    """
    if card_type == 1: # Debit Cards
        cards = {
            1: {"name": "Visa Classic Debit Card", "features": "Worldwide acceptance, ATM withdrawals, online purchases."},
            2: {"name": "Mastercard Standard Debit Card", "features": "Global acceptance, contactless payments, secure transactions."}
        }
    elif card_type == 2: # Prepaid Cards
        cards = {
            1: {"name": "Travel Prepaid Card", "features": "Load multiple currencies, ideal for international travel, secure."},
            2: {"name": "Gift Prepaid Card", "features": "Perfect for gifts, one-time load, versatile spending."}
        }
    elif card_type == 3: # Credit Cards
        cards = {
            1: {"name": "Visa Gold Credit Card", "features": "Higher credit limit, rewards points, travel insurance."},
            2: {"name": "Mastercard Platinum Credit Card", "features": "Premium benefits, exclusive offers, concierge service."}
        }
    else:
        print("Invalid card type.")
        return

    details = cards.get(card_choice)
    if details:
        print(f"\n--- {details['name']} Details ---")
        print(f"Features: {details['features']}")
        # Add more details like fees, limits etc.
    else:
        print("Invalid card choice.")

def display_atm_locations(branch_number):
    """Displays ATM locations for a selected branch."""
    branch_info = our_branches.get(branch_number)
    if branch_info:
        print(f"\n--- ATMs for {branch_info['name']} ---")
        if branch_info['atms']:
            for atm in branch_info['atms']:
                print(f"- {atm}")
        else:
            print("No ATMs listed for this branch.")
    else:
        print("Invalid branch choice.")
    time.sleep(2) # Allow user to read

def display_request_services_menu():
    """Displays the menu for request services."""
    print("\n--- Request Services ---")
    print("1. Cards")
    print("2. Edit My Profile")
    print("3. ATM locator")
    print("4. Add Beneficiary")
    print("5. Add a payment method")
    print("6. Contact Customer Care")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("------------------------")

def display_cards_request_menu():
    """Displays the menu for card-related requests."""
    print("\n--- Card Requests ---")
    print("1. Request for a new card")
    print("2. Activate My Card")
    print("3. Add funds to my Card")
    print("4. Check My Card Details")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("---------------------")

def display_payment_methods_menu():
    """Displays the menu for adding payment methods."""
    print("\n--- Add a Payment Method ---")
    print("1. Mobile money")
    print("2. PayPal")
    print("3. Crypto Currency")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("----------------------------")

def display_mobile_money_menu():
    """Displays the menu for Mobile Money Options."""
    print("\n--- Mobile Money Options ---")
    print("1. Airtel Money")
    print("2. M-pesa")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("----------------------------")

def display_crypto_platforms():
    """Displays the menu for Crypto Currency Platforms."""
    print("\n--- Available Crypto Currency Platforms ---")
    print("1. Binance")
    print("2. Bybit")
    print("3. Bitget")
    print("4. OKX")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("-----------------------------------------")

def display_payments_menu():
    """Displays the menu for Payments."""
    print("\n--- Payments ---")
    print("1. Withdraw Funds")
    print("2. Add Funds")
    print("3. Send Money")
    print("4. My Payment Methods")
    print("5. My Beneficiaries")
    print("6. Withdraw at ATM")
    print("7. Make Purchases")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("----------------")

def display_withdraw_options():
    """Displays the menu for Withdraw Options."""
    print("\n--- Withdraw Funds ---")
    print("1. Withdraw to M-pesa")
    print("2. Withdraw to Airtel Money")
    print("3. Withdraw to PayPal")
    print("4. Withdraw to Crypto Wallet")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("----------------------")

def display_add_funds_options():
    """Displays the menu for Add Funds Options."""
    print("\n--- Add Funds ---")
    print("1. Add from M-pesa")
    print("2. Add from PayPal")
    print("3. Add from Airtel Money")
    print("4. Add from Crypto Wallet")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("-----------------")

def display_send_money_options():
    """Displays the menu for Send Money Options."""
    print("\n--- Send Money ---")
    print("1. Send to Beneficiary")
    print("2. Send to Mobile Money")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("X. Exit")
    print("------------------")

def display_account_services_menu():
    """Displays the menu for account services for logged-in users."""
    print("\n--- Account Services ---")
    print("1. View Account Details")
    print("2. Make a Deposit")
    print("3. Make a Withdrawal")
    print("4. View Transaction History")
    print("5. Manage Cards")
    print("6. Request Services")
    print("7. Make Payments")
    print("8. Check Loan Balance/Limit")
    print("9. Go back to main menu") # Changed from P/M for simplicity in this menu
    print("X. Exit")
    print("------------------------")

def display_home_screen():
    """Displays the user's logged-in home screen with dynamic data."""
    clear_screen()
    print("\n--- Welcome to La Familia Bank, " + user_data.get('name', 'Customer') + "!---")
    print(f"Bank Account Number: {account_number}")
    print(f"Bank Account Name: {account_type_name}")
    
    currency_symbol = ""
    if "USD" in account_details.get("Currency", "Ksh"):
        currency_symbol = "$"
    elif "GBP" in account_details.get("Currency", "Ksh"):
        currency_symbol = "£"
    elif "EURO" in account_details.get("Currency", "Ksh"):
        currency_symbol = "€"
    elif "YEN" in account_details.get("Currency", "Ksh"):
        currency_symbol = "¥"
    else:
        currency_symbol = "Ksh "

    print(f"Current Balance: {currency_symbol}{account_balance:.2f}")

    print(f"My Cards: You have {len(my_cards)} cards. Go to 'Manage Cards' to view/request.")
    print(f"My Statements: {len(statements)} transactions recorded. Go to 'View Transaction History'.")
    print(f"Loans: Your loan limit is {currency_symbol}{loan_limit:.2f}. You have {active_loans} active loans.")
    print("\nSelect an option from 'Account Services' to proceed.")
    time.sleep(2) # Give user time to read home screen

# --- Main Application Logic (Refactored) ---

def handle_account_opening_menu():
    """Handles the 'Open a Bank Account' menu logic."""
    global user_data, account_number, user_password, logged_in, account_balance, account_type_name, account_details
    while True:
        display_account_opening_menu()
        account_choice = get_user_input("Enter your choice: ", int)

        if account_choice == 'M': return 'M'
        if account_choice == 'P': return 'P'
        if account_choice is None: return None

        if account_choice == 1: # Apply for Online Account Opening
            print("\n--- Online Account Application ---")
            email = get_user_input("Enter your email address: ")
            while not is_valid_email(email):
                print("Invalid email address.")
                email = get_user_input("Enter your email address: ")

            print("Dear customer, we appreciate your interest in starting a financial journey with us. Attached to this is your application form. Please download it and fill it carefully, then scan the copy back to us.")
            download_choice = get_user_input("Enter Y (yes to download), M (to go back to main menu), or P (to go back to the previous menu): ")
            if download_choice.upper() == 'Y':
                print("Form downloaded successfully")
                print("Please complete the form and email it back for review.")
                time.sleep(1)
            elif download_choice.upper() == 'M':
                return 'M'
            elif download_choice.upper() == 'P':
                continue # Stay in current menu
            elif download_choice is None:
                return None
            else:
                print("Invalid choice. Returning to the account opening menu.")

        elif account_choice == 2: # Get a Token to Visit a Branch
            print("\n--- Branch Visit Token ---")
            display_token_machine_menu()
            service_choice = get_user_input("Select a service: ", int)

            if service_choice == 'M': return 'M'
            if service_choice == 'P': continue # Stay in account opening menu
            if service_choice is None: return None

            display_token(service_choice) # Displays token and requirements

            if service_choice == 1: # Open New Account (Branch Flow)
                has_requirements = get_user_input("Do you have all the requirements listed on your token? (yes/no): ").lower()
                if has_requirements == 'yes':
                    print("\n--- Provide Your Details ---")
                    name = get_user_input("Enter your full name: ")
                    nationality = get_user_input("Enter your nationality (Kenyan, Ugandan, Tanzanian): ").capitalize()
                    while nationality not in ["Kenyan", "Ugandan", "Tanzanian"]:
                        print("Invalid nationality. Please enter Kenyan, Ugandan, or Tanzanian.")
                        nationality = get_user_input("Enter your nationality (Kenyan, Ugandan, Tanzanian): ").capitalize()

                    country_code = "+254" if nationality == "Kenyan" else "+256" if nationality == "Ugandan" else "+255"
                    phone_number = get_user_input(f"Enter your phone number (e.g., {country_code}7XXXXXXXX): ")
                    email = get_user_input("Enter your email address: ")
                    while not is_valid_email(email):
                        print("Invalid email address. Please enter a valid email.")
                        email = get_user_input("Enter your email address: ")
                    kra_pin = get_user_input("Enter your KRA PIN: ")
                    while not is_valid_kra_pin(kra_pin):
                        print("Invalid KRA PIN. Please enter a valid KRA PIN (e.g., A12345B).")
                        kra_pin = get_user_input("Enter your KRA PIN: ")
                    reason = get_user_input("Enter the reason for opening a bank account (Regular transactions, Savings, For Business, Oversea Bank Transactions): ")
                    while reason not in ["Regular transactions", "Savings", "For Business", "Oversea Bank Transactions"]:
                        print("Invalid reason. Please select from the list.")
                        reason = get_user_input("Enter the reason for opening a bank account (Regular transactions, Savings, For Business, Oversea Bank Transactions): ")

                    occupation = get_user_input("Enter your occupation (Student, Employed, Self-employed): ")
                    while occupation not in ["Student", "Employed", "Self-employed"]:
                        print("Invalid occupation. Please select from the list.")
                        occupation = get_user_input("Enter your occupation (Student, Employed, Self-employed): ")
                    source_of_income = get_user_input("Enter your source of income (Salary, Savings, Business, Sponsorship, Family and Relatives): ")
                    while source_of_income not in ["Salary", "Savings", "Business", "Sponsorship", "Family and Relatives"]:
                        print("Invalid source of income. Please select from the list.")
                        source_of_income = get_user_input("Enter your source of income (Salary, Savings, Business, Sponsorship, Family and Relatives): ")
                    monthly_deposits = get_user_input("Enter number of monthly deposits: ", int)
                    monthly_withdrawals = get_user_input("Enter number of monthly withdrawals: ", int)
                    while monthly_withdrawals > monthly_deposits:
                        print("Withdrawals should not be more than deposits. Please enter again.")
                        monthly_withdrawals = get_user_input("Enter number of monthly withdrawals: ", int)
                    monthly_balance = get_user_input("Enter monthly balance you intend to maintain: ", float)
                    address = get_user_input("Enter your address: ")

                    print("\nOur Bank Branches:")
                    for i, branch_data in our_branches.items():
                        print(f"{i}. {branch_data['name']}")
                    branch_choice = get_user_input("Select your bank branch: ", int)
                    while not 1 <= branch_choice <= len(our_branches):
                        print("Invalid branch choice. Please select from the list.")
                        branch_choice = get_user_input("Select your bank branch: ", int)
                    my_branch_name = our_branches[branch_choice]["name"] # Store branch name

                    # Store user data
                    user_data = {
                        "name": name,
                        "nationality": nationality,
                        "phone_number": phone_number,
                        "email": email,
                        "kra_pin": kra_pin,
                        "reason": reason,
                        "occupation": occupation,
                        "source_of_income": source_of_income,
                        "monthly_deposits": monthly_deposits,
                        "monthly_withdrawals": monthly_withdrawals,
                        "monthly_balance": monthly_balance,
                        "application_date": datetime.date.today(),
                        "address": address,
                        "branch": my_branch_name
                    }

                    # OTP verification
                    otp = send_otp(email)
                    entered_otp = get_user_input("Enter the OTP you received: ")
                    if entered_otp == otp:
                        print("Your details have been successfully verified and saved!")
                    else:
                        print("Incorrect OTP. Returning to account opening menu.")
                        continue

                    # Bank account registration
                    display_bank_accounts_menu()
                    account_type_choice = get_user_input("Select the type of bank account you want to open: ", int)
                    if account_type_choice == 'M': return 'M'
                    if account_type_choice == 'P': continue
                    if account_type_choice is None: return None

                    global account_details # Ensure we update the global account_details
                    account_details = display_account_details(account_type_choice) # Get the account details.
                    if account_details: # proceed only if a valid account type was selected
                        proceed_choice = get_user_input("Do you want to proceed with registration? (yes/no): ").lower()
                        if proceed_choice == 'yes':
                            print("Prepare for KYC verification.")
                            camera_access = get_user_input("Allow the app to access your camera, SMS, Location and Calls? (yes/no): ").lower()
                            while camera_access != 'yes':
                                print("Please allow access to proceed with KYC.")
                                camera_access = get_user_input("Allow the app to access your camera, SMS, Location and Calls? (yes/no): ").lower()

                            is_well_lit = get_user_input("Is the room well lit and the camera clean? (yes/no): ").lower()
                            while is_well_lit != 'yes':
                                print("Please clean the camera and move to a well-lit environment.")
                                is_well_lit = get_user_input("Is the room well lit and the camera clean? (yes/no): ").lower()

                            print("You have successfully passed the KYC verification.")
                            # Account Number Generation
                            account_number = random.randint(1000000000000, 9999999999999)
                            print("Your account has been successfully opened.")

                            # Password setup
                            print("\n--- Set up a password for your account ---")
                            print("The password is case sensitive and should have:")
                            print("- At least 8 characters")
                            print("- At least one special character (!@#$%^&*)")
                            print("- At least one lowercase and one uppercase character")
                            print("- No spaces")
                            print("Remember this password because three wrong attempts will block your account.")
                            password = get_user_input("Enter your password: ")
                            while not validate_password(password):
                                print("Invalid password. Please ensure it meets all requirements.")
                                password = get_user_input("Enter your password: ")
                            user_password = password # store the password
                            print("Your account is now password protected.")

                            # Simulate login after setup
                            attempts = 3
                            while attempts > 0:
                                login_password = get_user_input("Enter your password to log in: ")
                                if login_password == user_password:
                                    print("You have successfully logged in to your account.")
                                    logged_in = True
                                    break
                                else:
                                    attempts -= 1
                                    if attempts == 0:
                                        print("Account blocked due to too many incorrect attempts. Please reset your password.")
                                        new_password_reset = get_user_input("Enter your new password to reset: ")
                                        while not validate_password(new_password_reset):
                                            print("Invalid new password. Please ensure it meets all requirements.")
                                            new_password_reset = get_user_input("Enter your new password to reset: ")
                                        user_password = new_password_reset # Update the password
                                        attempts = 3 # Reset attempts for next login
                                        print("Password reset successful. Please try logging in again.")
                                        return 'M' # Go to main menu for new login
                                    print(f"Password incorrect. You have {attempts} attempts left.")
                            if not logged_in: # If still not logged in after reset
                                return 'M' # Go to main menu

                            # Account activation
                            if account_details["Opening balance"] == 0:
                                print("Account Activation Complete (No opening balance required).")
                                account_balance = 0.0 # Set balance to 0 if no opening balance required
                            else:
                                print(f"Account Activation Pending. To activate, please deposit at least {account_details['Currency']} {account_details['Opening balance']}.")
                                deposit_amount = get_user_input("Enter the amount you want to deposit: ", float)
                                if deposit_amount >= account_details["Opening balance"]:
                                    account_balance = deposit_amount
                                    add_transaction_statement("Initial Deposit", deposit_amount, account_balance, account_details['Currency'])
                                    print("Account Activation Complete!")
                                else:
                                    print("Insufficient funds. Account activation pending. Please deposit more.")
                                    return 'M' # Go back to main menu
                            display_home_screen() # Show home screen immediately after successful activation/login
                            return '3' # Simulate going to Account Services after login

                        elif proceed_choice == 'no':
                            print("Account registration cancelled.")
                            return 'M'
                        elif proceed_choice is None:
                            return None
                        else:
                            print("Invalid choice. Returning to the main menu.")
                            return 'M'
                    else:
                        print("No account type selected. Returning to account opening menu.")
                        continue
                else:
                    print("You do not have all the requirements. Please gather them and try again.")
                    continue # Stay in token menu
            else:
                print(f"Thank you for requesting '{get_service_name(service_choice)}'. Please proceed to the counter when your token is called.")
                time.sleep(2)
        else:
            print("Invalid choice. Please select a valid option.")
            time.sleep(1)


def handle_explore_offers_menu():
    """Handles the 'Explore Our Offers' menu logic."""
    while True:
        display_offers_menu()
        offers_choice = get_user_input("Enter your choice: ", int)

        if offers_choice == 'M': return 'M'
        if offers_choice == 'P': return 'P'
        if offers_choice is None: return None

        if offers_choice == 1: # Bank Accounts
            while True:
                display_bank_accounts_menu()
                bank_account_choice = get_user_input("Enter your choice: ", int)
                if bank_account_choice == 'M': return 'M'
                if bank_account_choice == 'P': break # Go back to offers menu
                if bank_account_choice is None: return None
                display_account_details(bank_account_choice)
                time.sleep(2) # Allow user to read details

        elif offers_choice == 2: # Cards
            while True:
                display_cards_menu()
                cards_choice = get_user_input("Enter your choice: ", int)
                if cards_choice == 'M': return 'M'
                if cards_choice == 'P': break # Go back to offers menu
                if cards_choice is None: return None

                if cards_choice == 1: # Debit Cards
                    while True:
                        display_debit_cards()
                        debit_card_choice = get_user_input("Enter your choice: ", int)
                        if debit_card_choice == 'M': return 'M'
                        if debit_card_choice == 'P': break # Go back to cards menu
                        if debit_card_choice is None: return None
                        display_card_details(1, debit_card_choice)
                        time.sleep(2)

                elif cards_choice == 2: # Prepaid Cards
                    while True:
                        display_prepaid_cards()
                        prepaid_card_choice = get_user_input("Enter your choice: ", int)
                        if prepaid_card_choice == 'M': return 'M'
                        if prepaid_card_choice == 'P': break
                        if prepaid_card_choice is None: return None
                        display_card_details(2, prepaid_card_choice)
                        time.sleep(2)

                elif cards_choice == 3: # Credit Cards
                    while True:
                        display_credit_cards()
                        credit_card_choice = get_user_input("Enter your choice: ", int)
                        if credit_card_choice == 'M': return 'M'
                        if credit_card_choice == 'P': break
                        if credit_card_choice is None: return None
                        display_card_details(3, credit_card_choice)
                        time.sleep(2)
                else:
                    print("Invalid choice.")
                    time.sleep(1)

        elif offers_choice == 3: # ATM Locator
            print("\n--- Our Branches ---")
            for i, branch_data in our_branches.items():
                print(f"{i}. {branch_data['name']}")
            branch_choice = get_user_input("Select a branch to view ATM locations: ", int)
            if branch_choice == 'M': return 'M'
            if branch_choice == 'P': continue # Stay in offers menu
            if branch_choice is None: return None
            display_atm_locations(branch_choice)
            time.sleep(2)

        elif offers_choice == 4: # Apply for a Loan (New Option)
            print("\n--- Apply for a Loan ---")
            print("Our loans are subject to credit approval and current interest rates.")
            print("Please visit any of our branches for more information on loan products.")
            time.sleep(2)

        else:
            print("Invalid choice. Please select a valid option.")
            time.sleep(1)

def handle_account_services_menu():
    """Handles the 'Account Services' menu logic for logged-in users."""
    global account_balance, statements, my_cards, my_card_pins, my_payment_methods, my_beneficiaries, loan_limit, active_loans, logged_in

    while True:
        display_account_services_menu()
        account_service_choice = get_user_input("Enter your choice: ", int)

        if account_service_choice == 'M': return 'M' # Should not happen from this menu, but handled by get_user_input
        if account_service_choice == 'P': return 'P' # Should not happen from this menu
        if account_service_choice is None: return None

        if account_service_choice == 9: # Go back to main menu
            return 'M'

        elif account_service_choice == 1: # View Account Details
            print("\n--- Your Account Details ---")
            print(f"Bank Account Number: {account_number}")
            print(f"Name: {user_data.get('name', 'N/A')}")
            print(f"Phone Number: {user_data.get('phone_number', 'N/A')}")
            print(f"Bank Account Name: {account_type_name}")
            
            currency = account_details.get("Currency", "Ksh")
            currency_symbol = ""
            if "USD" in currency: currency_symbol = "$"
            elif "GBP" in currency: currency_symbol = "£"
            elif "EURO" in currency: currency_symbol = "€"
            elif "YEN" in currency: currency_symbol = "¥"
            else: currency_symbol = "Ksh "

            print(f"Balance: {currency_symbol}{account_balance:.2f}")
            print(f"Account Opened Date: {user_data.get('application_date', 'N/A')}")
            print(f"Branch: {user_data.get('branch', 'N/A')}")
            time.sleep(3) # Allow user to read details

        elif account_service_choice == 2: # Make a Deposit
            deposit_amount = get_user_input("Enter the amount you want to deposit: ", float)
            if deposit_amount is None: continue
            if deposit_amount > 0:
                account_balance += deposit_amount
                add_transaction_statement("Deposit", deposit_amount, account_balance, account_details.get("Currency", "Ksh"))
                print(f"Deposit successful. Current Balance: {account_details.get('Currency', 'Ksh')} {account_balance:.2f}")
            else:
                print("Invalid deposit amount. Amount must be positive.")
            time.sleep(1)

        elif account_service_choice == 3: # Make a Withdrawal
            withdraw_amount = get_user_input("Enter the amount you want to withdraw: ", float)
            if withdraw_amount is None: continue
            if 0 < withdraw_amount <= account_balance:
                account_balance -= withdraw_amount
                add_transaction_statement("Withdrawal", withdraw_amount, account_balance, account_details.get("Currency", "Ksh"))
                print(f"Withdrawal successful. Current Balance: {account_details.get('Currency', 'Ksh')} {account_balance:.2f}")
            else:
                print("Invalid withdrawal amount or insufficient funds.")
            time.sleep(1)

        elif account_service_choice == 4: # View Transaction History
            print("\n--- Your Transaction History ---")
            if not statements:
                print("No transactions yet.")
            else:
                for stmt in statements:
                    print(stmt)
            time.sleep(3) # Allow user to read history

        elif account_service_choice == 5: # Manage Cards
            while True:
                display_cards_request_menu()
                cards_request_choice = get_user_input("Enter your choice: ", int)
                if cards_request_choice == 'M': return 'M'
                if cards_request_choice == 'P': break # Go back to account services menu
                if cards_request_choice is None: return None

                if cards_request_choice == 1: # Request for a new card
                    print("\n--- Request a New Card ---")
                    print("Which type of card would you like to request?")
                    print("1. Debit Card")
                    print("2. Prepaid Card")
                    print("3. Credit Card")
                    card_type_request = get_user_input("Enter choice: ", int)
                    if card_type_request == 1:
                        card_name = get_user_input("Enter desired debit card (e.g., Visa Classic Debit Card): ")
                    elif card_type_request == 2:
                        card_name = get_user_input("Enter desired prepaid card (e.g., Travel Prepaid Card): ")
                    elif card_type_request == 3:
                        card_name = get_user_input("Enter desired credit card (e.g., Visa Gold Credit Card): ")
                    else:
                        print("Invalid card type.")
                        continue

                    if card_name:
                        new_card_number = f"**** **** **** {random.randint(1000, 9999)}"
                        new_card_pin = str(random.randint(1000, 9999))
                        my_cards.append({"name": card_name, "number": new_card_number, "status": "Pending Activation"})
                        my_card_pins[new_card_number] = new_card_pin
                        print(f"Your request for a {card_name} has been submitted. Card number: {new_card_number}")
                        print(f"Your PIN is: {new_card_pin}. Keep this safe!")
                        print("You will receive a notification when your physical card is ready for pickup/delivery.")
                    time.sleep(2)

                elif cards_request_choice == 2: # Activate My Card
                    if not my_cards:
                        print("You have no cards to activate yet. Request a new card first.")
                        time.sleep(1)
                        continue
                    print("\n--- Activate My Card ---")
                    print("Your cards:")
                    for idx, card in enumerate(my_cards):
                        print(f"{idx+1}. {card['name']} ({card['number']}) - Status: {card['status']}")
                    card_to_activate_idx = get_user_input("Select card to activate: ", int) - 1
                    if 0 <= card_to_activate_idx < len(my_cards):
                        selected_card = my_cards[card_to_activate_idx]
                        if selected_card['status'] == 'Active':
                            print(f"{selected_card['name']} is already active.")
                        else:
                            pin_attempt = get_user_input("Enter your card PIN to activate: ")
                            if pin_attempt == my_card_pins.get(selected_card['number']):
                                selected_card['status'] = 'Active'
                                print(f"{selected_card['name']} has been successfully activated!")
                            else:
                                print("Incorrect PIN. Card activation failed.")
                    else:
                        print("Invalid card selection.")
                    time.sleep(2)

                elif cards_request_choice == 3: # Add funds to my Card (assuming card is tied to main account)
                    if not my_cards:
                        print("You have no cards. Request one first.")
                        time.sleep(1)
                        continue
                    print("\n--- Add Funds to Card ---")
                    print("Your cards:")
                    for idx, card in enumerate(my_cards):
                        print(f"{idx+1}. {card['name']} ({card['number']}) - Status: {card['status']}")
                    card_to_fund_idx = get_user_input("Select card to add funds to: ", int) - 1
                    if 0 <= card_to_fund_idx < len(my_cards):
                        if my_cards[card_to_fund_idx]['status'] != 'Active':
                            print("This card is not active. Please activate it first.")
                            time.sleep(1)
                            continue
                        fund_amount = get_user_input("Enter amount to add from your main account: ", float)
                        if fund_amount is None: continue
                        if 0 < fund_amount <= account_balance:
                            account_balance -= fund_amount
                            add_transaction_statement(f"Funds Added to Card {my_cards[card_to_fund_idx]['number']}", fund_amount, account_balance, account_details.get("Currency", "Ksh"))
                            print(f"Successfully added {account_details.get('Currency', 'Ksh')} {fund_amount:.2f} to {my_cards[card_to_fund_idx]['name']}.")
                            print(f"Remaining Main Account Balance: {account_details.get('Currency', 'Ksh')} {account_balance:.2f}")
                        else:
                            print("Invalid amount or insufficient funds in main account.")
                    else:
                        print("Invalid card selection.")
                    time.sleep(2)

                elif cards_request_choice == 4: # Check My Card Details
                    if not my_cards:
                        print("You have no cards yet.")
                        time.sleep(1)
                        continue
                    print("\n--- Your Card Details ---")
                    for card in my_cards:
                        print(f"Card Name: {card['name']}")
                        print(f"Card Number: {card['number']}")
                        print(f"Status: {card['status']}")
                        # WARNING: In a real app, never display PIN. This is for simulation only.
                        print(f"PIN: {my_card_pins.get(card['number'], 'N/A')}")
                        print("---")
                    time.sleep(3)
                else:
                    print("Invalid choice.")
                    time.sleep(1)

        elif account_service_choice == 6: # Request Services
            while True:
                display_request_services_menu()
                request_service_choice = get_user_input("Enter your choice: ", int)
                if request_service_choice == 'M': return 'M'
                if request_service_choice == 'P': break # Go back to account services menu
                if request_service_choice is None: return None

                if request_service_choice == 1: # Cards (goes back to cards request menu)
                    while True:
                        display_cards_request_menu()
                        sub_choice = get_user_input("Enter choice: ", int)
                        if sub_choice == 'M': return 'M'
                        if sub_choice == 'P': break # Go back to request services menu
                        if sub_choice is None: return None
                        # This would call the card management logic, similar to account_service_choice == 5
                        print("This is a placeholder for card management logic under Request Services.")
                        time.sleep(1)
                elif request_service_choice == 2: # Edit My Profile
                    print("\n--- Edit My Profile ---")
                    print("Please contact customer care to update your profile details.")
                    time.sleep(2)
                elif request_service_choice == 3: # ATM locator
                    print("\n--- Our Branches ---")
                    for i, branch_data in our_branches.items():
                        print(f"{i}. {branch_data['name']}")
                    branch_choice = get_user_input("Select a branch to view ATM locations: ", int)
                    if branch_choice == 'M': return 'M'
                    if branch_choice == 'P': continue
                    if branch_choice is None: return None
                    display_atm_locations(branch_choice)
                    time.sleep(2)
                elif request_service_choice == 4: # Add Beneficiary
                    print("\n--- Add Beneficiary ---")
                    beneficiary_name = get_user_input("Enter beneficiary name: ")
                    beneficiary_account = get_user_input("Enter beneficiary account number: ")
                    if beneficiary_name and beneficiary_account:
                        my_beneficiaries.append({"name": beneficiary_name, "account": beneficiary_account})
                        print(f"{beneficiary_name} added as a beneficiary.")
                    else:
                        print("Beneficiary details cannot be empty.")
                    time.sleep(2)
                elif request_service_choice == 5: # Add a payment method
                    while True:
                        display_payment_methods_menu()
                        payment_method_choice = get_user_input("Enter choice: ", int)
                        if payment_method_choice == 'M': return 'M'
                        if payment_method_choice == 'P': break
                        if payment_method_choice is None: return None

                        if payment_method_choice == 1: # Mobile money
                            while True:
                                display_mobile_money_menu()
                                mobile_money_type = get_user_input("Select Mobile Money type: ", int)
                                if mobile_money_type == 'M': return 'M'
                                if mobile_money_type == 'P': break
                                if mobile_money_type is None: return None
                                if mobile_money_type in [1, 2]:
                                    phone_num = get_user_input("Enter mobile money phone number: ")
                                    if phone_num:
                                        provider = "Airtel Money" if mobile_money_type == 1 else "M-pesa"
                                        my_payment_methods.append({"type": provider, "number": phone_num})
                                        print(f"{provider} ({phone_num}) added as a payment method.")
                                    else:
                                        print("Phone number cannot be empty.")
                                else:
                                    print("Invalid mobile money type.")
                                time.sleep(2)
                        elif payment_method_choice == 2: # PayPal
                            paypal_email = get_user_input("Enter PayPal email: ")
                            if paypal_email:
                                my_payment_methods.append({"type": "PayPal", "email": paypal_email})
                                print(f"PayPal ({paypal_email}) added as a payment method.")
                            else:
                                print("PayPal email cannot be empty.")
                            time.sleep(2)
                        elif payment_method_choice == 3: # Crypto Currency
                            while True:
                                display_crypto_platforms()
                                crypto_platform_choice = get_user_input("Select crypto platform: ", int)
                                if crypto_platform_choice == 'M': return 'M'
                                if crypto_platform_choice == 'P': break
                                if crypto_platform_choice is None: return None
                                if crypto_platform_choice in [1,2,3,4]:
                                    wallet_address = get_user_input("Enter crypto wallet address: ")
                                    platform_name = {1:"Binance", 2:"Bybit", 3:"Bitget", 4:"OKX"}.get(crypto_platform_choice)
                                    if wallet_address:
                                        my_payment_methods.append({"type": "Crypto", "platform": platform_name, "address": wallet_address})
                                        print(f"Crypto wallet ({platform_name}: {wallet_address}) added as a payment method.")
                                    else:
                                        print("Wallet address cannot be empty.")
                                else:
                                    print("Invalid crypto platform.")
                                time.sleep(2)
                        else:
                            print("Invalid payment method choice.")
                        time.sleep(1)

                elif request_service_choice == 6: # Contact Customer Care
                    print("\n--- Contact Customer Care ---")
                    print("You can reach us via:")
                    print("Phone: +254 7XX XXX XXX")
                    print("Email: customercare@lafamiliabank.com")
                    print("Working Hours: Mon-Fri, 9 AM - 5 PM")
                    time.sleep(2)
                else:
                    print("Invalid choice.")
                    time.sleep(1)

        elif account_service_choice == 7: # Make Payments
            while True:
                display_payments_menu()
                payments_choice = get_user_input("Enter your choice: ", int)
                if payments_choice == 'M': return 'M'
                if payments_choice == 'P': break # Go back to account services menu
                if payments_choice is None: return None

                if payments_choice == 1: # Withdraw Funds
                    while True:
                        display_withdraw_options()
                        withdraw_option = get_user_input("Select withdrawal option: ", int)
                        if withdraw_option == 'M': return 'M'
                        if withdraw_option == 'P': break
                        if withdraw_option is None: return None

                        withdraw_amount = get_user_input("Enter amount to withdraw: ", float)
                        if withdraw_amount is None: continue
                        if 0 < withdraw_amount <= account_balance:
                            account_balance -= withdraw_amount
                            add_transaction_statement(f"Withdrawal to {get_user_input_string(withdraw_option, 'withdraw')}", withdraw_amount, account_balance, account_details.get("Currency", "Ksh"))
                            print(f"Successfully withdrew {account_details.get('Currency', 'Ksh')} {withdraw_amount:.2f}.")
                            print(f"Remaining Balance: {account_details.get('Currency', 'Ksh')} {account_balance:.2f}")
                        else:
                            print("Invalid amount or insufficient funds.")
                        time.sleep(2)

                elif payments_choice == 2: # Add Funds
                    while True:
                        display_add_funds_options()
                        add_fund_option = get_user_input("Select add funds option: ", int)
                        if add_fund_option == 'M': return 'M'
                        if add_fund_option == 'P': break
                        if add_fund_option is None: return None

                        add_amount = get_user_input("Enter amount to add: ", float)
                        if add_amount is None: continue
                        if add_amount > 0:
                            account_balance += add_amount
                            add_transaction_statement(f"Funds Added from {get_user_input_string(add_fund_option, 'add_funds')}", add_amount, account_balance, account_details.get("Currency", "Ksh"))
                            print(f"Successfully added {account_details.get('Currency', 'Ksh')} {add_amount:.2f}.")
                            print(f"Current Balance: {account_details.get('Currency', 'Ksh')} {account_balance:.2f}")
                        else:
                            print("Invalid amount. Amount must be positive.")
                        time.sleep(2)

                elif payments_choice == 3: # Send money
                    while True:
                        display_send_money_options()
                        send_money_option = get_user_input("Select send money option: ", int)
                        if send_money_option == 'M': return 'M'
                        if send_money_option == 'P': break
                        if send_money_option is None: return None

                        if send_money_option == 1: # Send to Beneficiary
                            if not my_beneficiaries:
                                print("No beneficiaries added yet. Add one via 'Request Services' -> 'Add Beneficiary'.")
                                time.sleep(2)
                                continue
                            print("\n--- Send to Beneficiary ---")
                            for idx, beneficiary in enumerate(my_beneficiaries):
                                print(f"{idx+1}. {beneficiary['name']} (Account: {beneficiary['account']})")
                            beneficiary_idx = get_user_input("Select beneficiary: ", int) - 1
                            if 0 <= beneficiary_idx < len(my_beneficiaries):
                                send_amount = get_user_input(f"Enter amount to send to {my_beneficiaries[beneficiary_idx]['name']}: ", float)
                                if send_amount is None: continue
                                if 0 < send_amount <= account_balance:
                                    account_balance -= send_amount
                                    add_transaction_statement(f"Sent to Beneficiary {my_beneficiaries[beneficiary_idx]['name']}", send_amount, account_balance, account_details.get("Currency", "Ksh"))
                                    print(f"Successfully sent {account_details.get('Currency', 'Ksh')} {send_amount:.2f} to {my_beneficiaries[beneficiary_idx]['name']}.")
                                    print(f"Remaining Balance: {account_details.get('Currency', 'Ksh')} {account_balance:.2f}")
                                else:
                                    print("Invalid amount or insufficient funds.")
                            else:
                                print("Invalid beneficiary selection.")
                            time.sleep(2)

                        elif send_money_option == 2: # Send to Mobile Money
                            if not any(pm['type'] in ["Airtel Money", "M-pesa"] for pm in my_payment_methods):
                                print("No mobile money payment methods added yet. Add one via 'Request Services' -> 'Add a payment method'.")
                                time.sleep(2)
                                continue
                            print("\n--- Send to Mobile Money ---")
                            mobile_money_methods = [pm for pm in my_payment_methods if pm['type'] in ["Airtel Money", "M-pesa"]]
                            if not mobile_money_methods:
                                print("No mobile money methods found.")
                                time.sleep(1)
                                continue

                            for idx, pm in enumerate(mobile_money_methods):
                                print(f"{idx+1}. {pm['type']} ({pm['number']})")
                            mm_choice_idx = get_user_input("Select mobile money method: ", int) - 1

                            if 0 <= mm_choice_idx < len(mobile_money_methods):
                                send_amount = get_user_input(f"Enter amount to send to {mobile_money_methods[mm_choice_idx]['type']}: ", float)
                                if send_amount is None: continue
                                if 0 < send_amount <= account_balance:
                                    account_balance -= send_amount
                                    add_transaction_statement(f"Sent to Mobile Money {mobile_money_methods[mm_choice_idx]['type']}", send_amount, account_balance, account_details.get("Currency", "Ksh"))
                                    print(f"Successfully sent {account_details.get('Currency', 'Ksh')} {send_amount:.2f} to {mobile_money_methods[mm_choice_idx]['type']}.")
                                    print(f"Remaining Balance: {account_details.get('Currency', 'Ksh')} {account_balance:.2f}")
                                else:
                                    print("Invalid amount or insufficient funds.")
                            else:
                                print("Invalid mobile money selection.")
                            time.sleep(2)
                        else:
                            print("Invalid send money option.")
                        time.sleep(1)

                elif payments_choice == 4: # My Payment methods
                    print("\n--- Your Payment Methods ---")
                    if not my_payment_methods:
                        print("No payment methods added yet.")
                    else:
                        for pm in my_payment_methods:
                            if pm['type'] == 'Mobile':
                                print(f"Type: {pm['type']}, Number: {pm['number']}")
                            elif pm['type'] == 'PayPal':
                                print(f"Type: {pm['type']}, Email: {pm['email']}")
                            elif pm['type'] == 'Crypto':
                                print(f"Type: {pm['type']}, Platform: {pm['platform']}, Address: {pm['address']}")
                    time.sleep(2)

                elif payments_choice == 5: # My Beneficiaries
                    print("\n--- Your Beneficiaries ---")
                    if not my_beneficiaries:
                        print("No beneficiaries added yet.")
                    else:
                        for b in my_beneficiaries:
                            print(f"Name: {b['name']}, Account: {b['account']}")
                    time.sleep(2)

                elif payments_choice == 6: # Withdraw at ATM
                    print("\n--- Withdraw at ATM ---")
                    print("You can withdraw cash from any La Familia Bank ATM using your activated debit card.")
                    time.sleep(2)

                elif payments_choice == 7: # Make Purchases
                    print("\n--- Make Purchases ---")
                    print("You can make online and in-store purchases using your activated La Familia Bank cards.")
                    time.sleep(2)
                else:
                    print("Invalid choice.")
                    time.sleep(1)

        elif account_service_choice == 8: # Check Loan Balance/Limit
            print(f"\nYour current loan limit is: {account_details.get('Currency', 'Ksh')} {loan_limit:.2f}")
            print(f"You currently have {active_loans} active loans.")
            if active_loans > 0:
                print("Visit 'Explore Our Offers' -> 'Apply for a Loan' or a branch for loan details.")
            time.sleep(2)
        else:
            print("Invalid choice. Please select a valid option.")
            time.sleep(1)

def get_user_input_string(choice, menu_type):
    """Helper to get string names for transaction types."""
    if menu_type == 'withdraw':
        options = {1: "M-pesa", 2: "Airtel Money", 3: "PayPal", 4: "Crypto Wallet"}
    elif menu_type == 'add_funds':
        options = {1: "M-pesa", 2: "PayPal", 3: "Airtel Money", 4: "Crypto Wallet"}
    elif menu_type == 'send_money':
        options = {1: "Beneficiary", 2: "Mobile Money"}
    else:
        return "Unknown"
    return options.get(choice, "Unknown")


# --- Main Application Loop ---

def main():
    """Main function to run the online banking app with state-based navigation."""
    global logged_in, account_details # Ensure these are accessible globally
    random.seed() # Seed the random number generator for OTP and account numbers.

    current_menu = "main" # Initial state

    while True:
        if current_menu == "main":
            display_main_menu()
            choice = get_user_input("Enter your choice: ", int)
            if choice is None: # Exit
                print("Exiting Application. Goodbye!")
                break
            elif choice == 1:
                current_menu = handle_account_opening_menu() # Transition to account opening flow
            elif choice == 2:
                current_menu = handle_explore_offers_menu() # Transition to offers flow
            elif choice == 3 and logged_in:
                current_menu = handle_account_services_menu() # Transition to account services flow
            elif choice == 4 and logged_in:
                logged_in = False
                user_data.clear() # Clear user data on logout
                global account_number, user_password, account_balance, account_type_name, my_cards, my_card_pins, my_payment_methods, my_beneficiaries, statements, loan_limit, active_loans
                account_number = None
                user_password = None
                account_balance = 0.0
                account_type_name = "N/A"
                my_cards = []
                my_card_pins = {}
                my_payment_methods = []
                my_beneficiaries = []
                statements = []
                loan_limit = 0.0
                active_loans = 0
                account_details = {} # Reset account details on logout
                print("You have been logged out.")
                current_menu = "main" # Go back to main menu
                time.sleep(1)
            elif choice == 4 and not logged_in:
                print("You are not logged in.")
                time.sleep(1)
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)

        # Handle navigation return values from sub-menus
        if current_menu == 'M': # If a sub-menu returned 'M', go back to main menu
            current_menu = "main"
        elif current_menu == 'P': # If a sub-menu returned 'P', it means it wants to go back to its *caller*
            # This 'P' logic is handled within the sub-menu functions themselves (e.g., `break` from inner loops)
            # So, if we receive 'P' here, it implies a navigation error or a need to refine flow.
            # For this simple state machine, 'P' just means 'stay in the current sub-menu' unless explicitly broken.
            # We will rely on explicit returns from the `handle_` functions.
            pass # Keep current_menu as is, loop will continue for the current menu
        elif current_menu is None: # If a sub-menu returned None, exit the application
            print("Exiting Application. Goodbye!")
            break


if __name__ == "__main__":
    # Create empty inbox files if they don't exist
    for filename in [EMAIL_INBOX_FILE, MESSAGE_INBOX_FILE]:
        if not os.path.exists(filename):
            try:
                with open(filename, 'w') as f:
                    pass # Just create an empty file
                print(f"Created empty inbox file: {filename}")
            except IOError as e:
                print(f"Error creating file {filename}: {e}")

    main()

# Copyright 2025. Alex Malunda. All rights reserved.