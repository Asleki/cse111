import random
import re  # For email and KRA PIN validation
import datetime  # For handling dates
import time # For OTP

# Global variables (used for storing user data and bank information)
user_data = {}
account_number = None  # Will be generated upon successful account opening
loan_limit = 0
active_loans = 0
my_cards = []
my_card_pins = []
my_payment_methods = []
my_beneficiaries = []
statements = []
my_branch = ""  # Will store the user's selected branch
our_branches = [
    "La Familia Mombasa Road Branch",
    "La Familia Nairobi CBD Branch",
    "La Familia Nairobi Moi Avenue Branch",
    "La Familia Nairobi Afya Centre Branch",
    "La Familia Kisumu Branch"
]
logged_in = False # Flag to track if a user is logged in
user_password = None # To store the user's password
account_balance = 0.0 # initialize account balance.
account_type_name = "" # Store the name of the account type
# Function to validate email format
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

# Function to validate KRA PIN format
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

# Function to display the main menu
def display_main_menu():
    """Displays the main menu options to the user."""
    print("\nMAIN MENU")
    print("1. Open A bank account")
    print("2. Explore our offers")
    if logged_in:
        print("3. Account Services")
        print("4. Logout")

# Function to display the account opening menu
def display_account_opening_menu():
    """Displays the menu for opening a bank account."""
    print("\nOpen a Bank Account")
    print("1. Open a bank account online")
    print("2. Visit the nearest Bank branch")

# Function to display the offers menu
def display_offers_menu():
    """Displays the menu for exploring bank offers."""
    print("\nExplore Our Offers")
    print("1. Bank accounts")
    print("2. Our Cards")
    print("3. ATM locator")
    print("4. Go back to previous menu")
    print("M. Go to main menu")

# Function to display the bank accounts menu
def display_bank_accounts_menu():
    """Displays the menu for available bank accounts."""
    print("\nAvailable Bank Accounts")
    print("1. Current Bank account")
    print("2. Club Account")
    print("3. PayGo account")
    print("4. Sapphire Multi currency account")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

# Function to display the cards menu
def display_cards_menu():
    """Displays the menu for available cards."""
    print("\nOur Cards")
    print("1. Debit Cards")
    print("2. Prepaid Cards")
    print("3. Credit Cards")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

# Function to display debit cards menu
def display_debit_cards():
    print("\nDebit Cards")
    print("1. Club Debit MasterCard")
    print("2. Debit Visa")
    print("3. Gold MasterCard")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

# Function to display prepaid cards menu
def display_prepaid_cards():
    print("\nPrepaid Cards")
    print("1. Multi Currency Prepaid MasterCard")
    print("2. Sapphire Prepaid Visa")
    print("3. Safari prepaid Visa")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

# Function to display credit cards menu
def display_credit_cards():
    print("\nCredit Cards")
    print("1. Gold Visa Credit Card")
    print("2. Bronze Credit MasterCard")
    print("3. Diamond Credit Card")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

# Function to display the token machine menu
def display_token_machine_menu():
    """Displays the menu for the token machine services."""
    print("\nSelect Service")
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

# Function to display account details

def display_account_details(account_type):
    """
    Displays the details of a selected bank account type.

    Args:
        account_type (int): The account type selected by the user.
    """
    global account_type_name
    if account_type == 1:
        account_type_name = "Current Bank account"
        print("\nAccount Name: Current Bank account")
        print("Account Overview.")
        print("Currency: Ksh")
        print("Opening balance $0")
        print("Monthly maintenance fee $0")
        print("Minimum balance $0")
        print("Bank Transfers fees $0.5")
        print("ATM withdrawal charges $0.3")
        print("Free monthly e-statements")
        print("Debit card $5")
        return {"Currency": "Ksh", "Opening balance": 0, "Monthly maintenance fee": 0,
                "Minimum balance": 0, "Bank Transfers fees": 0.5,
                "ATM withdrawal charges": 0.3, "Free monthly e-statements": True,
                "Debit card": 5}
    elif account_type == 2:
        account_type_name = "Club Account"
        print("\nAccount Name: Club Account")
        print("Account Overview.")
        print("Currency: Ksh")
        print("Opening balance $59")
        print("Monthly maintenance fee $12")
        print("Minimum balance $0")
        print("Bank Transfers fees $0.5")
        print("ATM withdrawal charges $0.3")
        print("Free monthly e-statements")
        print("Free Debit MasterCard")
        print("Free Cheque book")
        return {"Currency": "Ksh", "Opening balance": 59, "Monthly maintenance fee": 12,
                "Minimum balance": 0, "Bank Transfers fees": 0.5,
                "ATM withdrawal charges": 0.3, "Free monthly e-statements": True,
                "Free Debit MasterCard": True, "Free Cheque book": True}
    elif account_type == 3:
        account_type_name = "PayGo account"
        print("\nAccount Name: PayGo account")
        print("Account Overview.")
        print("Currency: Ksh")
        print("Opening balance $0")
        print("Monthly maintenance fee $0")
        print("Minimum balance $0")
        print("Bank Transfers fees $0.5")
        print("ATM withdrawal charges $0.3")
        print("Free monthly e-statements")
        print("Free Debit MasterCard")
        print("Free Cheque book")
        return {"Currency": "Ksh", "Opening balance": 0, "Monthly maintenance fee": 0,
                "Minimum balance": 0, "Bank Transfers fees": 0.5,
                "ATM withdrawal charges": 0.3, "Free monthly e-statements": True,
                "Free Debit MasterCard": True, "Free Cheque book": True}
    elif account_type == 4:
        account_type_name = "Sapphire Multi Currency Account"
        print("\nAccount Name: Sapphire Multi Currency Account")
        print("Account Overview.")
        print("Currency: USD,GBP,EURO,YEN")
        print("Opening balance $100")
        print("Monthly maintenance fee $0")
        print("Minimum balance $0")
        print("Bank Transfers fees $0.5")
        print("ATM withdrawal charges $0.3")
        print("Free monthly e-statements")
        print("Free Debit MasterCard")
        print("Free Cheque book")
        return {"Currency": "USD,GBP,EURO,YEN", "Opening balance": 100,
                "Monthly maintenance fee": 0, "Minimum balance": 0,
                "Bank Transfers fees": 0.5, "ATM withdrawal charges": 0.3,
                "Free monthly e-statements": True, "Free Debit MasterCard": True,
                "Free Cheque book": True}
    else:
        print("Invalid account type.")
        return None

def display_card_details(card_type, specific_card=None):
    """
    Displays the details of a selected card type or a specific card.

    Args:
        card_type (int): The card type (1: Debit, 2: Prepaid, 3: Credit).
        specific_card (int, optional): The specific card selected by the user.
                                      Defaults to None.
    """
    if card_type == 1:
        if specific_card == 1:
            print("\nCard Name: Club Debit MasterCard")
            print("Card Overview")
            print("This card can be issued to all bank account holders")
            print("Currency: Ksh")
            print("Card issuance fee $5")
            print("Card annual fee $0")
            print("Card replacement fee $5")
            print("Card purchases $0.5")
            print("ATM withdrawals $0.3")
            print("Check balance $0.3")
            return {"Card Name": "Club Debit MasterCard", "Currency": "Ksh",
                    "Card issuance fee": 5, "Card annual fee": 0,
                    "Card replacement fee": 5, "Card purchases": 0.5,
                    "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 2:
            print("\nCard Name: Debit Visa")
            print("Card Overview")
            print("This card can be issued to all bank account holders")
            print("Currency :Ksh")
            print("Card issuance fee $5")
            print("Card annual fee $0")
            print("Card replacement fee $5")
            print("Card purchases $0.5")
            print("ATM withdrawals $0.3")
            print("Check balance $0.3")
            return {"Card Name": "Debit Visa", "Currency": "Ksh",
                    "Card issuance fee": 5, "Card annual fee": 0,
                    "Card replacement fee": 5, "Card purchases": 0.5,
                    "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 3:
            print("\nCard Name: Gold MasterCard")
            print("Card Overview")
            return {"Card Name": "Gold MasterCard"}
        else:
            print("\nDebit Cards")
            print("1. Club Debit MasterCard")
            print("2. Debit Visa")
            print("3. Gold MasterCard")
            print("P. Go back to previous menu")
            print("M. Go to main menu")
    elif card_type == 2:
        if specific_card == 1:
            print("\nCard Name: Multi Currency Prepaid MasterCard")
            print("Card Overview")
            print("This card is issued to only Sapphire Multi Currency Account Holders")
            print("Currency: USD, GBP, EURO,YEN")
            print("Card issuance fee $12")
            print("Card annual fee $1")
            print("Card replacement fee $5")
            print("Card purchases $0.5")
            print("ATM withdrawals $0.3")
            print("Check balance $0.3")
            return {"Card Name": "Multi Currency Prepaid MasterCard",
                    "Currency": "USD, GBP, EURO,YEN", "Card issuance fee": 12,
                    "Card annual fee": 1, "Card replacement fee": 5,
                    "Card purchases": 0.5, "ATM withdrawals": 0.3,
                    "Check balance": 0.3}
        elif specific_card == 2:
            print("\nCard Name: Sapphire Prepaid Visa")
            print("Card Overview")
            print("This card can be issued to all bank account holders")
            print("Card issuance fee $5")
            print("Card annual fee $0")
            print("Card replacement fee $5")
            print("Card purchases $0.5")
            print("ATM withdrawals $0.3")
            print("Check balance $0.3")
            return {"Card Name": "Sapphire Prepaid Visa", "Currency": "Ksh", # Assuming default currency
                    "Card issuance fee": 5, "Card annual fee": 0,
                    "Card replacement fee": 5, "Card purchases": 0.5,
                    "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 3:
            print("\nCard Name: Safari prepaid Visa")
            print("Card Overview")
            print("This card can be issued to all bank account holders")
            print("Card issuance fee $5")
            print("Card annual fee $0")
            print("Card replacement fee $5")
            print("Card purchases $0.5")
            print("ATM withdrawals $0.3")
            print("Check balance $0.3")
            return {"Card Name": "Safari prepaid Visa", "Currency": "Ksh", # Assuming default currency
                    "Card issuance fee": 5, "Card annual fee": 0,
                    "Card replacement fee": 5, "Card purchases": 0.5,
                    "ATM withdrawals": 0.3, "Check balance": 0.3}
        else:
            print("\nPrepaid Cards")
            print("1. Multi Currency Prepaid MasterCard")
            print("2. Sapphire Prepaid Visa")
            print("3. Safari prepaid Visa")
            print("P. Go back to previous menu")
            print("M. Go to main menu")
    elif card_type == 3:
        if specific_card == 1:
            print("\nCard Name: Gold Visa Credit Card")
            print("Card Overview")
            print("This card can be issued to all bank account holders with loan limits.")
            print("Card issuance fee $5")
            print("Card annual fee $0")
            print("Card replacement fee $5")
            print("Card purchases $0.5")
            print("ATM withdrawals $0.3")
            print("Check balance $0.3")
            return {"Card Name": "Gold Visa Credit Card", "Currency": "Ksh", # Assuming default currency
                    "Card issuance fee": 5, "Card annual fee": 0,
                    "Card replacement fee": 5, "Card purchases": 0.5,
                    "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 2:
            print("\nCard Name: Bronze Credit MasterCard")
            print("Card Overview")
            print("This card can be issued to only Multi Currency bank account holders with loan limits.")
            print("Card issuance fee $10")
            print("Card annual fee $20")
            print("Card replacement fee $10")
            print("Card purchases $0.5")
            print("ATM withdrawals $0.3")
            print("Check balance $0.3")
            return {"Card Name": "Bronze Credit MasterCard", "Currency": "Ksh",  # Assuming default currency
                    "Card issuance fee": 10, "Card annual fee": 20,
                    "Card replacement fee": 10, "Card purchases": 0.5,
                    "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 3:
            print("\nCard Name: Diamond Credit Card")
            print("Card Overview")
            print(
                "This card is only issued to Multi Currency Bank account holders with good transaction history and have an accumulative loan limit.")
            print("Card issuance fee $100")
            print("Card annual fee $10")
            print("Card replacement fee $199")
            print("Card purchases $0.5")
            print("ATM withdrawals $0.3")
            print("Check balance $0.3")
            return {"Card Name": "Diamond Credit Card", "Currency": "Ksh", # Assuming default currency
                    "Card issuance fee": 100, "Card annual fee": 10,
                    "Card replacement fee": 199, "Card purchases": 0.5,
                    "ATM withdrawals": 0.3, "Check balance": 0.3}
        else:
            print("\nCredit Cards")
            print("1. Gold Visa Credit Card")
            print("2. Bronze Credit MasterCard")
            print("3. Diamond Credit Card")
            print("P. Go back to previous menu")
            print("M. Go to main menu")
    else:
        print("Invalid card type.")
        return None

# Function to display ATM locations
def display_atm_locations(branch):
    """
    Displays the ATM locations for a selected bank branch.

    Args:
        branch (int): The branch selected by the user.
    """
    if branch == 1:
        print("\nATM Locations for La Familia Mombasa Road Branch")
        print("Cabanas ATM")
        print("Airtel ATM")
        print("Syokimau ATM")
        print("Signature Mall ATM")
    elif branch == 2:
        print("\nATM Locations for La Familia Nairobi CBD Branch")
        print("La Familia Bank ATM")
        print("LC Waikiki ATM")
        print("Carrefour ATM")
        print("Naivas ATM")
    elif branch == 3:
        print("\nATM Locations for La Familia Nairobi Moi Avenue Branch")
        print("Nyayo House ATM")
        print("GPU ATM")
    elif branch == 4:
        print("\nATM Locations for La Familia Nairobi Afya Centre Branch")
        print("Afya Centre ATM")
        print("Mfangano street ATM")
        print("Hakati Road ATM")
    elif branch == 5:
        print("\nATM Locations for La Familia Kisumu Branch")
        print("La Familia Bank ATM")
        print("Bondo Carrefour ATM")
    else:
        print("Invalid branch selection.")

def get_user_input(prompt, input_type=str):
    """
    Gets user input with a specified prompt and input type.  Handles potential errors.

    Args:
        prompt (str): The prompt to display to the user.
        input_type (type, optional): The expected input type (e.g., str, int, float).
            Defaults to str.

    Returns:
        The user's input, converted to the specified input type.  Returns None on error.
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
            print("Invalid input. Please enter the correct type of value.")
        except EOFError:
            print("No input received.  Exiting.")
            return None  # Or some other sentinel value to indicate termination

def generate_otp():
    """Generates a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def send_otp(email):
    """
    Sends an OTP to the provided email address (simulated).

    Args:
        email (str): The email address to send the OTP to.

    Returns:
        str: The generated OTP.
    """
    otp = generate_otp()
    print(f"Sending OTP {otp} to {email}")  # Simulate sending
    return otp

def display_token(service):
    """
    Displays a token with service details.

    Args:
        service (int): The selected service.
    """
    token_number = random.randint(1, 30)
    service_desk = random.randint(1, 30)
    customers_ahead = token_number - 1 if token_number > 1 else 0

    print("\nYour Token")
    print(f"Service: {get_service_name(service)}")
    if 6 <= service <= 9:  # Services 6 to 9 don't have token numbers, desk numbers, or customers ahead.
        print("Token Number: N/A")
        print("Service Desk: N/A")
        print("Customers Ahead: N/A")
    else:
        print(f"Token Number: {token_number}")
        print(f"Service Desk: {service_desk}")
        print(f"Customers Ahead: {customers_ahead}")

    print("\nAdditional Information:")
    if service == 1:
        print("Requirements:")
        print("Have an original ID")
        print("Have a valid KRA PIN")
        print("Download the online banking app")
        print("Have a functional email")
    elif service == 2:
        print("Requirements:")
        print("Have your Bank account details")
        print("Have original ID")
        print("2 recent passport photos")
    elif service == 3:
        print("Requirements:")
        print("Have original ID")
        print("Download the online banking app")
        print("Have your old account Bank details")
    elif service == 4:
        print("Requirements:")
        print("Have access to your email address used")
        print("To register the bank account")
        print("Have the online banking app")
    elif service == 5:
        print("Requirements:")
        print("Have an existing active Bank Account")
    elif 6 <= service <= 9:
        print("Proceed to the Customer Care desk for further assistance.")

def get_service_name(service_number):
    """
    Returns the name of the service based on the service number.

    Args:
        service_number (int): The number of the service.

    Returns:
        str: The name of the service.
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

def get_branch_name(branch_number):
    """
    Returns the name of the branch based on the branch number.

    Args:
        branch_number (int): The number of the branch.

    Returns:
        str: The name of the branch.
    """
    branches = {
        1: "La Familia Mombasa Road Branch",
        2: "La Familia Nairobi CBD Branch",
        3: "La Familia Nairobi Moi Avenue Branch",
        4: "La Familia Nairobi Afya Centre",
        5: "La Familia Kisumu Branch"
    }
    return branches.get(branch_number, "Unknown Branch")

def display_request_services_menu():
    """Displays the menu for request services."""
    print("\nRequest Services")
    print("1. Cards")
    print("2. Edit My Profile")
    print("3. ATM locator")
    print("4. Add Beneficiary")
    print("5. Add a payment method")
    print("6. Contact Customer Care")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

def display_cards_request_menu():
    """
    Displays the menu for card-related requests.
    """
    print("\nCards")
    print("1. Request for a new card")
    print("2. Activate My Card")
    print("3. Add funds to my Card")
    print("4. Check My Card Details")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

def display_payment_methods_menu():
    """
    Displays the menu for adding payment methods
    """
    print("\nAdd a payment method")
    print("1. Mobile money")
    print("2. PayPal")
    print("3. Crypto Currency")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

def display_mobile_money_menu():
    """
Displays the menu for Mobile Money Options
    """
    print("\nMobile Money Options")
    print("1. Airtel Money")
    print("2. M-pesa")

def display_crypto_platforms():
    """
    Displays the menu for Crypto Currency Platforms
    """
    print("\nAvailable Crypto Currency platforms")
    print("1. Binance")
    print("2. Bybit")
    print("3. Bitget")
    print("4. OKX")

def display_payments_menu():
    """
    Displays the menu for Payments
    """
    print("\nPayments")
    print("1.Withdraw")
    print("2. Add Funds")
    print("3. Send money")
    print("4. My Payment methods")
    print("5. My Beneficiaries")
    print("6. Withdraw at ATM")
    print("7. Make Purchases")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

def display_withdraw_options():
    """
    Displays the menu for Withdraw Options
    """
    print("\nWithdraw")
    print("1. Withdraw to M-pesa")
    print("2. Withdraw to Airtel Money")
    print("3. Withdraw to PayPal")
    print("4. Withdraw to Crypto Wallet")

def display_add_funds_options():
    """
    Displays the menu for Add Funds Options
    """
    print("\nAdd Funds")
    print("1. Add from M-pesa")
    print("2. Add from PayPal")
    print("3. Add from Airtel Money")
    print("4. Add from Crypto Wallet")

def display_send_money_options():
    """
    Displays the menu for Send Money Options
    """
    print("\nSend money")
    print("1. Send to Beneficiary")
    print("2. Send to Mobile Money")

def display_account_services_menu():
    """Displays the menu for account services."""
    print("\nAccount Services")
    print("1. View Account Details")
    print("2. Make a Deposit")
    print("3. Make a Withdrawal")
    print("4. View Transaction History")
    print("5. Manage Cards")
    print("6. Request Services")
    print("7. Make Payments")
    print("8. Check Loan Balance/Limit")
    print("9. Go back to main menu")

def main():
    """Main function to run the online banking app."""
    global user_data, account_number, loan_limit, active_loans, my_cards, my_card_pins, my_payment_methods, my_beneficiaries, statements, my_branch, our_branches, logged_in, user_password, account_balance, account_type_name
    # Seed the random number generator for OTP and account numbers.
    random.seed()
    application_date = datetime.date.today() # store the date of application
    while True:
        display_main_menu()
        choice = get_user_input("Enter your choice: ", int)
        if choice == 'M':
            continue
        if choice == None:
            print("Exiting Application")
            break

        if choice == 1:
            display_account_opening_menu()
            account_choice = get_user_input("Enter your choice: ", int)
            if account_choice == 'M':
                continue
            if account_choice == 'P':
                continue
            if account_choice == None:
                print("Exiting Application")
                break

            if account_choice == 1:
                email = get_user_input("Enter your email address: ")
                while not is_valid_email(email):
                    print("Invalid email address.")
                    email = get_user_input("Enter your email address: ")
                # Send the application form (simulated)
                print("Dear customer, we appreciate your interest in starting a financial journey with us, attached to this is your application form, please download it and fill it carefully, then scan the copy back to us.")
                download_choice = get_user_input("Enter Y (yes to download), M (to go back to main menu), or P (to go back to the previous menu): ")
                if download_choice.upper() == 'Y':
                    print("Form downloaded successfully")
                elif download_choice.upper() == 'M':
                    continue
                elif download_choice.upper() == 'P':
                    display_account_opening_menu() # Go back to the previous menu
                elif download_choice == None:
                    print("Exiting Application")
                    break
                else:
                    print("Invalid choice. Returning to the main menu.")

            elif account_choice == 2:
                display_token_machine_menu()
                service_choice = get_user_input("Select a service: ", int)
                if service_choice == 'M':
                    continue
                if service_choice == 'P':
                    display_account_opening_menu()
                    continue
                if service_choice == None:
                    print("Exiting Application")
                    break
                display_token(service_choice)

                if service_choice == 1: # Open New Account.
                    has_requirements = get_user_input("Do you have all the requirements listed on your token? (yes/no): ").lower()
                    if has_requirements == 'yes':
                        # Get user details for the online banking app
                        name = get_user_input("Enter your name: ")
                        nationality = get_user_input("Enter your nationality (Kenyan, Ugandan, Tanzanian): ").capitalize()
                        while nationality not in ["Kenyan", "Ugandan", "Tanzanian"]:
                            print("Invalid nationality. Please enter Kenyan, Ugandan, or Tanzanian.")
                            nationality = get_user_input("Enter your nationality (Kenyan, Ugandan, Tanzanian): ").capitalize()

                        country_code = "+254" if nationality == "Kenyan" else "+256" if nationality == "Ugandan" else "+255"
                        phone_number = get_user_input(f"Enter your phone number (starting with {country_code}): ")
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
                        for i, branch in enumerate(our_branches, 1):
                            print(f"{i}. {branch}")
                        branch_choice = get_user_input("Select your bank branch: ", int)
                        while not 1 <= branch_choice <= len(our_branches):
                            print("Invalid branch choice. Please select from the list.")
                            branch_choice = get_user_input("Select your bank branch: ", int)
                        my_branch = our_branches[branch_choice - 1]

                        # Store user data
                        user_data = {
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
                            "application_date": application_date,
                            "address": address,
                            "branch": my_branch
                        }

                        # OTP verification
                        otp = send_otp(email)
                        entered_otp = get_user_input("Enter the OTP you received: ")
                        if entered_otp == otp:
                            print("Your details have been successfully verified and saved!")
                        else:
                            print("Incorrect OTP. Please try again.")
                            continue  # Go back to the beginning of the main loop

                        # Bank account registration
                        display_bank_accounts_menu()
                        account_type_choice = get_user_input("Select the type of bank account you want to open: ", int)
                        if account_type_choice == 'M':
                            continue
                        if account_type_choice == 'P':
                            continue
                        if account_type_choice == None:
                            print("Exiting Application")
                            break
                        account_details = display_account_details(account_type_choice) # Get the account details.
                        if account_details: # proceed only if a valid account type was selected
                            proceed_choice = get_user_input("Do you want to proceed with registration? (yes/no): ").lower()
                            if proceed_choice == 'yes':
                                print("Prepare for KYC verification.")
                                # Simulate KYC verification
                                camera_access = get_user_input("Allow the app to access your camera, SMS, Location and Calls? (yes/no): ").lower()
                                while camera_access != 'yes':
                                    print("Please allow access.")
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
                                print("\nSet up a password for your account:")
                                print("The password is case sensitive")
                                print("The password should have at least one special Character")
                                print("The password should have at least on lower case character and at least one upper case character")
                                print("No spaces")
                                print("Remember this password Because three wrong attempts will block you account.")
                                password = get_user_input("Enter your password: ")
                                #  Password validation (simplified for demonstration)
                                while True:
                                    special_char_regex = r"[!@#$%^&*(),.?\":{}|<>]"
                                    lower_case_regex = r"[a-z]"
                                    upper_case_regex = r"[A-Z]"
                                    if (len(password) >= 8 and
                                        re.search(special_char_regex, password) and
                                        re.search(lower_case_regex, password) and
                                        re.search(upper_case_regex, password) and
                                        " " not in password):
                                        break;
                                    else:
                                        password = get_user_input("Invalid password. Please enter a valid password: ")
                                user_password = password # store the password
                                print("Your account is now password protected.")

                                # Simulate login
                                attempts = 3
                                while attempts > 0:
                                    login_password = get_user_input("Enter your password to log in: ")
                                    if login_password == user_password:
                                        print("You have successfully logged in to your account.")
                                        logged_in = True # set logged in to true
                                        break
                                    else:
                                        attempts -= 1
                                        if attempts == 0:
                                            print("Account blocked, please reset your password.")
                                            #  password reset
                                            new_password = get_user_input("Enter your new password: ")
                                            while True:
                                                if (len(new_password) >= 8 and
                                                    re.search(special_char_regex, new_password) and
                                                    re.search(lower_case_regex, new_password) and
                                                    re.search(upper_case_regex, new_password) and
                                                    " " not in new_password):
                                                    break;
                                                else:
                                                    new_password = get_user_input("Invalid password. Please enter a valid password: ")
                                            user_password = new_password # update the password
                                            attempts = 3 # give 3 more attempts
                                            continue
                                        print(f"Password incorrect, you have {attempts} attempts left.")
                                if attempts == 0:
                                    continue # Go back to the main menu

                                # Account activation
                                if account_details["Opening balance"] == 0:
                                    print("Account Activation Complete")
                                else:
                                    print("Account Activation Pending.")
                                    print(f"To activate your account, please deposit at least ${account_details['Opening balance']}.")
                                    deposit_amount = get_user_input("Enter the amount you want to deposit: ", float)
                                    if deposit_amount >= account_details["Opening balance"]:
                                        print("Account Activation Complete")
                                        account_balance = deposit_amount # set initial balance
                                    else:
                                        print("Insufficient funds. Account activation pending.")
                                        print("Returning to Main Menu")
                                        continue

                                # Display account details after successful login
                                print("\nWelcome to La Familia Bank")
                                print(f"Bank Account Number: {account_number}")
                                print(f"Date: {application_date}")
                                print(f"Name: {user_data['name']}")
                                print(f"Bank Account Name: {account_type_name}")
                                # Display balance with currency
                                currency = account_details["Currency"]
                                if "USD" in currency:
                                    print(f"Balance: ${account_balance:.2f}")
                                elif "GBP" in currency:
                                    print(f"Balance: £{account_balance:.2f}")
                                elif "EURO" in currency:
                                    print(f"Balance: €{account_balance:.2f}")
                                elif "YEN" in currency:
                                    print(f"Balance: ¥{account_balance:.2f}")
                                else:
                                    print(f"Balance: Ksh {account_balance:.2f}")
                                print("My Cards: You have 0 cards, go to request services to request for a card")
                                print("My statements: No statements yet.")
                                print("Loans: Your loan limit is $0")

                                #Here, the program should go to the "homescreen" or a menu that allows the user to access
                                # the account functionalities.  For now, I'll just break out of the main loop.
                                # break # Exit the main loop after successful account opening and activation.
                                continue # Go to main menu, and since logged_in is true, Account Services will be displayed.

                            elif proceed_choice == 'no':
                                print("Returning to the main menu.")
                            elif proceed_choice == None:
                                print("Exiting Application")
                                break
                            else:
                                print("Invalid choice. Returning to the main menu.")
                    else:
                        print("Returning to token menu")
                elif service_choice == 2: # Close account
                    display_token(service_choice)
                elif service_choice == 3: # Reactivate
                    display_token(service_choice)
                elif service_choice == 4: # statement
                    display_token(service_choice)
                elif service_choice == 5: # Cheque book
                    display_token(service_choice)
                elif service_choice == 6: # cheque deposit
                    display_token(service_choice)
                elif service_choice == 7: # cash withdrawal
                    display_token(service_choice)
                elif service_choice == 8: # cash deposit
                    display_token(service_choice)
                elif service_choice == 9: # currency conversion
                    display_token(service_choice)
                else:
                    print("Invalid service choice.")
            else:
                print("Invalid account choice. Returning to the main menu.")

        elif choice == 2:
            while True:
                display_offers_menu()
                offers_choice = get_user_input("Enter your choice: ", int)
                if offers_choice == 'M':
                    break
                if offers_choice == 'P':
                    break
                if offers_choice == None:
                    print("Exiting Application")
                    break

                if offers_choice == 1:
                    display_bank_accounts_menu()
                    bank_account_choice = get_user_input("Enter your choice: ", int)
                    if bank_account_choice == 'M':
                        break
                    if bank_account_choice == 'P':
                        break
                    if bank_account_choice == None:
                        print("Exiting Application")
                        break
                    display_account_details(bank_account_choice)
                elif offers_choice == 2:
                    while True:
                        display_cards_menu()
                        cards_choice = get_user_input("Enter your choice: ", int)
                        if cards_choice == 'M':
                            break
                        if cards_choice == 'P':
                            break
                        if cards_choice == None:
                            print("Exiting Application")
                            break
                        if cards_choice == 1:
                            while True:
                                display_debit_cards()
                                debit_card_choice = get_user_input("Enter your choice: ", int)
                                if debit_card_choice == 'M':
                                    break
                                if debit_card_choice == 'P':
                                    break
                                if debit_card_choice == None:
                                    print("Exiting Application")
                                    break
                                display_card_details(1, debit_card_choice)
                        elif cards_choice == 2:
                            while True:
                                display_prepaid_cards()
                                prepaid_card_choice = get_user_input("Enter your choice: ", int)
                                if prepaid_card_choice == 'M':
                                    break
                                if prepaid_card_choice == 'P':
                                    break
                                if prepaid_card_choice == None:
                                    print("Exiting Application")
                                    break
                                display_card_details(2, prepaid_card_choice)
                        elif cards_choice == 3:
                            while True:
                                display_credit_cards()
                                credit_card_choice = get_user_input("Enter your choice: ", int)
                                if credit_card_choice == 'M':
                                    break
                                if credit_card_choice == 'P':
                                    break
                                if credit_card_choice == None:
                                    print("Exiting Application")
                                    break
                                display_card_details(3, credit_card_choice)
                        else:
                            print("Invalid choice")
                elif offers_choice == 3:
                    print("\nOur Branches:")
                    for i, branch in enumerate(our_branches, 1):
                        print(f"{i}. {branch}")
                    branch_choice = get_user_input("Select a branch to view ATM locations: ", int)
                    if branch_choice == 'M':
                        break
                    if branch_choice == 'P':
                        break
                    if branch_choice == None:
                        print("Exiting Application")
                        break
                    display_atm_locations(branch_choice)
                elif offers_choice == 4:
                    break
                else:
                    print("Invalid choice. Returning to the main menu.")
        elif choice == 3 and logged_in: # choice 3 is account services
            while True:
                display_account_services_menu()
                account_service_choice = get_user_input("Enter your choice: ", int)
                if account_service_choice == 9:
                    break # Go back to main menu
                if account_service_choice == None:
                    print("Exiting Application")
                    break
                elif account_service_choice == 1:
                    print("\nYour Account Details:")
                    print(f"Bank Account Number: {account_number}")
                    print(f"Name: {user_data['name']}")
                    print(f"Phone Number: {user_data['phone_number']}")
                    print(f"Bank Account Name: {account_type_name}")
                    currency = account_details["Currency"]
                    if "USD" in currency:
                        print(f"Balance: ${account_balance:.2f}")
                    elif "GBP" in currency:
                        print(f"Balance: £{account_balance:.2f}")
                    elif "EURO" in currency:
                        print(f"Balance: €{account_balance:.2f}")
                    elif "YEN" in currency:
                        print(f"Balance: ¥{account_balance:.2f}")
                    else:
                        print(f"Balance: Ksh {account_balance:.2f}")
                    print(f"Date: {user_data['application_date']}")

                elif account_service_choice == 2:
                    deposit_amount = get_user_input("Enter the amount you want to deposit: ", float)
                    if deposit_amount > 0:
                        account_balance += deposit_amount
                        print("Deposit successful.")
                        currency = account_details["Currency"]
                        if "USD" in currency:
                            print(f"Current Balance: ${account_balance:.2f}")
                        elif "GBP" in currency:
                            print(f"Current Balance: £{account_balance:.2f}")
                        elif "EURO" in currency:
                            print(f"Current Balance: €{account_balance:.2f}")
                        elif "YEN" in currency:
                            print(f"Current Balance: ¥{account_balance:.2f}")
                        else:
                            print(f"Current Balance: Ksh {account_balance:.2f}")
                    else:
                        print("Invalid deposit amount.")
                elif account_service_choice == 3:
                    withdraw_amount = get_user_input("Enter the amount you want to withdraw: ", float)
                    if 0 < withdraw_amount <= account_balance:
                        account_balance -= withdraw_amount
                        print("Withdrawal successful.")
                        currency = account_details["Currency"]
                        if "USD" in currency:
                            print(f"Current Balance: ${account_balance:.2f}")
                        elif "GBP" in currency:
                            print(f"Current Balance: £{account_balance:.2f}")
                        elif "EURO" in currency:
                            print(f"Current Balance: €{account_balance:.2f}")
                        elif "YEN" in currency:
                            print(f"Current Balance: ¥{account_balance:.2f}")
                        else:
                            print(f"Current Balance: Ksh {account_balance:.2f}")
                    else:
                        print("Invalid withdrawal amount.")
                elif account_service_choice == 4:
                    print("\nTransaction History:")
                    if not statements:
                        print("No transactions yet.")
                    else:
                        for statement in statements:
                            print(statement) # print the statements
                elif account_service_choice == 5:
                    display_cards_request_menu()
                    cards_request_choice = get_user_input("Enter your choice: ", int)
                elif account_service_choice == 6:
                    display_request_services_menu()
                    request_service_choice = get_user_input("Enter your choice: ", int)
                elif account_service_choice == 7:
                    display_payments_menu()
                    payments_choice = get_user_input("Enter your choice: ", int)
                elif account_service_choice == 8:
                    print(f"Your loan limit is: ${loan_limit}")
                    print(f"You have {active_loans} active loans.")
                else:
                    print("Invalid choice. Please select a valid option.")
        elif choice == 4 and logged_in:
            logged_in = False
            print("You have been logged out.")
        elif choice == 4 and not logged_in:
            print("You are not logged in.")
        else:
            print("Invalid choice. Returning to the main menu.")

if __name__ == "__main__":
    main()
# Copyright 2025. Alex Malunda. All rights reserved.