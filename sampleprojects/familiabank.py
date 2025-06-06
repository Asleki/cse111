import os
import json
import datetime
import random
import re
import time # For simulating delays

# --- Global Constants and Configuration ---
BANK_NAME = "Python Bank"
BANK_TAGLINE = "Your Trusted Digital Financial Partner"
DATA_DIR = "bank_data"
ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")
EMAIL_INBOX_FILE = os.path.join(DATA_DIR, "email_inbox.txt")
SMS_LOG_FILE = os.path.join(DATA_DIR, "sms_log.txt")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

OUR_BRANCHES = [
    "Head Office Branch (Nairobi)",
    "Mombasa Branch",
    "Kisumu Branch",
    "Nakuru Branch",
    "Eldoret Branch",
    "Thika Branch"
]

SECURITY_QUESTIONS = {
    1: "What is your mother's maiden name?",
    2: "What was the name of your first pet?",
    3: "What is your favorite book?",
    4: "What high school did you attend?",
    5: "What is your favorite movie?",
    6: "In what city were you born?"
}

# --- Exchange Rates (Simplified for simulation) ---
# All rates are relative to KES (Kenyan Shilling)
# To convert from A to B: amount_in_B = amount_in_A * (EXCHANGE_RATES['A']['KES'] / EXCHANGE_RATES['B']['KES'])
# Or simply: amount_in_target = amount_in_source * EXCHANGE_RATES[source_currency][target_currency]
EXCHANGE_RATES = {
    "KES": {
        "USD": 0.0076, "GBP": 0.0060, "EURO": 0.0070, "JPY": 1.18, # KES to Foreign
        "KES": 1.0 # KES to KES
    },
    "USD": {
        "KES": 131.00, "GBP": 0.79, "EURO": 0.92, "JPY": 155.00, # USD to Others
        "USD": 1.0
    },
    "GBP": {
        "KES": 165.00, "USD": 1.27, "EURO": 1.17, "JPY": 196.00, # GBP to Others
        "GBP": 1.0
    },
    "EURO": {
        "KES": 142.00, "USD": 1.09, "GBP": 0.85, "JPY": 168.00, # EURO to Others
        "EURO": 1.0
    },
    "JPY": {
        "KES": 0.85, "USD": 0.0064, "GBP": 0.0051, "EURO": 0.0059, # JPY to Others
        "JPY": 1.0
    },
    # Crypto rates are relative to USD (simplified for simulation)
    "BTC": {"USD": 60000.00, "KES": 60000.00 * 131.00},
    "ETH": {"USD": 3000.00, "KES": 3000.00 * 131.00},
    "SOL": {"USD": 150.00, "KES": 150.00 * 131.00},
}


# --- Color Codes for Terminal Output ---
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

GREEN_CHECKMARK = f"{GREEN}\u2713{RESET}" # Green checkmark
RED_X = f"{RED}\u2717{RESET}"             # Red X
BLUE_INFO = f"{BLUE}i{RESET}"             # Blue info icon

# --- File Operations ---

def read_accounts():
    """Reads account data from the JSON file."""
    if not os.path.exists(ACCOUNTS_FILE) or os.stat(ACCOUNTS_FILE).st_size == 0:
        return {}
    with open(ACCOUNTS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_accounts(accounts_data):
    """Saves account data to the JSON file."""
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts_data, f, indent=4)

def read_transactions():
    """Reads transaction data from the JSON file."""
    if not os.path.exists(TRANSACTIONS_FILE) or os.stat(TRANSACTIONS_FILE).st_size == 0:
        return []
    with open(TRANSACTIONS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_transaction(timestamp, username, type, amount, currency, reference_num, description, running_balance):
    """Saves a single transaction to the transactions file."""
    transactions = read_transactions()
    transactions.append({
        "timestamp": timestamp,
        "username": username,
        "type": type,
        "amount": amount,
        "currency": currency,
        "reference_number": reference_num,
        "description": description,
        "running_balance": running_balance
    })
    with open(TRANSACTIONS_FILE, 'w') as f:
        json.dump(transactions, f, indent=4)

def delete_all_data():
    """Deletes all data files (accounts, transactions, emails, sms)."""
    if os.path.exists(ACCOUNTS_FILE):
        os.remove(ACCOUNTS_FILE)
    if os.path.exists(TRANSACTIONS_FILE):
        os.remove(TRANSACTIONS_FILE)
    if os.path.exists(EMAIL_INBOX_FILE):
        os.remove(EMAIL_INBOX_FILE)
    if os.path.exists(SMS_LOG_FILE):
        os.remove(SMS_LOG_FILE)
    print(f"{YELLOW}All application data has been deleted.{RESET}")

# --- Input/Output and Utility Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input(prompt, type=str):
    """
    Gets input from the user with options to go back to previous or main menu.
    Args:
        prompt (str): The message to display to the user.
        type (callable): The type to convert the input to (e.g., int, float, str).
    Returns:
        The converted input, or 'P' for previous, 'M' for main, or None on EOF/error.
    """
    while True:
        try:
            user_input = input(f"{CYAN}{prompt}{RESET}").strip()
            if user_input.upper() == 'P':
                return 'P'
            if user_input.upper() == 'M':
                return 'M'
            if not user_input: # Handle empty input for optional fields or re-prompt
                if type == str: # Allow empty string for string types if not critical
                    return ""
                print(f"{RED_X} Input cannot be empty. Please try again.")
                continue
            return type(user_input)
        except ValueError:
            print(f"{RED_X} Invalid input. Please enter data of type {type.__name__}.")
        except EOFError:
            print(f"{RED_X} End of input reached. Exiting gracefully.")
            return None
        except Exception as e:
            print(f"{RED_X} An unexpected error occurred: {e}")
            return None

def is_valid_email(email):
    """Basic validation for email format."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def generate_otp(length=6):
    """Generates a random numeric OTP."""
    return ''.join(random.choices('0123456789', k=length))

def generate_reference_number():
    """Generates a unique transaction reference number."""
    return f"TRX-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"

def convert_currency(amount, from_currency, to_currency):
    """
    Converts an amount from one currency to another using predefined rates.
    Handles KES, USD, GBP, EURO, JPY, BTC, ETH, SOL.
    """
    if from_currency == to_currency:
        return amount

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    try:
        # Direct conversion if available
        if from_currency in EXCHANGE_RATES and to_currency in EXCHANGE_RATES[from_currency]:
            return amount * EXCHANGE_RATES[from_currency][to_currency]

        # Convert via USD as an intermediary if direct path not found
        # This assumes all currencies can be converted to/from USD.
        # This logic should be more robust in a real system.
        if from_currency in ["BTC", "ETH", "SOL"]:
            # Convert crypto to USD first
            amount_in_usd = amount * EXCHANGE_RATES[from_currency]["USD"]
            if to_currency == "USD":
                return amount_in_usd
            else:
                # Then convert from USD to target fiat
                return amount_in_usd * EXCHANGE_RATES["USD"][to_currency]
        
        if to_currency in ["BTC", "ETH", "SOL"]:
            # Convert source fiat to USD first
            amount_in_usd = amount * EXCHANGE_RATES[from_currency]["USD"]
            # Then convert from USD to target crypto
            return amount_in_usd / EXCHANGE_RATES[to_currency]["USD"] # Inverted for USD to Crypto

        # For fiat-to-fiat, if direct path not found, go via USD
        if from_currency != "USD" and to_currency != "USD":
            amount_in_usd = amount * EXCHANGE_RATES[from_currency]["USD"]
            return amount_in_usd * EXCHANGE_RATES["USD"][to_currency]

        raise ValueError("Conversion path not found.")

    except KeyError:
        print(f"{RED_X} Error: Exchange rate not found for {from_currency} to {to_currency}.")
        return None
    except Exception as e:
        print(f"{RED_X} An error occurred during currency conversion: {e}")
        return None


# --- Email and SMS Simulation ---

def _log_communication(log_file, sender, recipient, subject, body):
    """Helper to log emails/SMS to a file."""
    with open(log_file, 'a') as f:
        f.write(f"--- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        f.write(f"From: {sender}\n")
        f.write(f"To: {recipient}\n")
        if subject:
            f.write(f"Subject: {subject}\n")
        f.write(f"Body:\n{body}\n")
        f.write("-" * 30 + "\n\n")

def send_otp_email(name, email, otp, expiry_time):
    """Simulates sending an OTP email."""
    sender = f"noreply@{BANK_NAME.lower().replace(' ', '')}.com"
    subject = f"{BANK_NAME} OTP Verification"
    body = (
        f"Dear {name},\n\n"
        f"Your One-Time Passcode (OTP) for {BANK_NAME} is: {BOLD}{otp}{RESET}\n\n"
        f"This OTP is valid for 5 minutes and will expire at {expiry_time.strftime('%H:%M:%S')}.\n"
        f"Please do not share this code with anyone.\n\n"
        f"Thank you,\n"
        f"The {BANK_NAME} Team."
    )
    _log_communication(EMAIL_INBOX_FILE, sender, email, subject, body)
    print(f"{GREEN_CHECKMARK} OTP email sent to {email}. Check your simulated inbox ({EMAIL_INBOX_FILE}).")
    return True

def send_payment_otp_sms(phone_number, otp):
    """Simulates sending an OTP SMS for payment passcode."""
    sender = BANK_NAME.replace(' ', '') # Sender ID
    recipient = phone_number
    body = (
        f"Your {BANK_NAME} payment OTP is: {otp}. "
        f"Do not share this code. Valid for 5 mins."
    )
    _log_communication(SMS_LOG_FILE, sender, recipient, None, body)
    print(f"{GREEN_CHECKMARK} Payment OTP SMS sent to {phone_number}. Check your simulated SMS log ({SMS_LOG_FILE}).")
    return True

def send_application_form_email(email):
    """Simulates sending an account application form."""
    sender = f"support@{BANK_NAME.lower().replace(' ', '')}.com"
    subject = f"{BANK_NAME} Account Application Form"
    body = (
        f"Dear Applicant,\n\n"
        f"Thank you for your interest in opening an account with {BANK_NAME}.\n"
        f"Attached to this email is your application form. Please download, fill it carefully, "
        f"and scan the completed form back to us via email or visit your nearest branch.\n\n"
        f"Required documents typically include:\n"
        f"- Copy of National ID/Passport\n"
        f"- KRA PIN Certificate\n"
        f"- Proof of Address (e.g., utility bill)\n"
        f"- Passport size photo\n\n"
        f"We look forward to serving you!\n\n"
        f"Sincerely,\n"
        f"The {BANK_NAME} Team."
    )
    _log_communication(EMAIL_INBOX_FILE, sender, email, subject, body)
    return True

def send_security_questions_email(name, email, questions):
    """Simulates sending a confirmation email for security questions."""
    sender = f"security@{BANK_NAME.lower().replace(' ', '')}.com"
    subject = f"{BANK_NAME} Security Questions Setup Confirmation"
    body = (
        f"Dear {name},\n\n"
        f"This email confirms that you have successfully set up your security questions for your {BANK_NAME} account.\n"
        f"Your chosen questions and answers (for your reference, do not share):\n"
    )
    for q, a in questions.items():
        body += f"- Question: {q}\n"
        body += f"  Answer: {a}\n" # In a real system, answers would be hashed.
    body += (
        f"\nThese questions will be used to verify your identity if you ever need to reset your password or "
        f"perform sensitive account operations.\n\n"
        f"If you did not make these changes, please contact us immediately.\n\n"
        f"Sincerely,\n"
        f"The {BANK_NAME} Security Team."
    )
    _log_communication(EMAIL_INBOX_FILE, sender, email, subject, body)
    return True

def send_account_activation_email(username, email, account_number, account_type_details, branch_name):
    """Simulates sending an account activation confirmation email."""
    sender = f"accounts@{BANK_NAME.lower().replace(' ', '')}.com"
    subject = f"{BANK_NAME} Account Activated: Welcome!"
    body = (
        f"Dear {username},\n\n"
        f"Congratulations! Your {BANK_NAME} account has been successfully created and activated.\n\n"
        f"Account Details:\n"
        f"  Account Number: {account_number}\n"
        f"  Account Type: {account_type_details.get('Account Name', 'N/A')}\n"
        f"  Currency: {account_type_details.get('Currency', 'N/A')}\n"
        f"  Branch: {branch_name}\n\n"
        f"You can now log in to your online banking portal to manage your finances, "
        f"view statements, and explore our services.\n\n"
        f"Welcome to the {BANK_NAME} family!\n\n"
        f"Sincerely,\n"
        f"The {BANK_NAME} Team."
    )
    _log_communication(EMAIL_INBOX_FILE, sender, email, subject, body)
    return True

def send_activation_sms(phone_number, account_number):
    """Simulates sending an SMS confirmation for account activation."""
    sender = BANK_NAME.replace(' ', '')
    body = (
        f"Congrats! Your {BANK_NAME} account {account_number} is now active. "
        f"Welcome to the family!"
    )
    _log_communication(SMS_LOG_FILE, sender, phone_number, None, body)
    return True

def send_transaction_notification(username, email, phone_number, transaction_type, amount, currency, ref_num, description, new_balance):
    """Simulates sending email and SMS for a transaction."""
    sender_email = f"transactions@{BANK_NAME.lower().replace(' ', '')}.com"
    sender_sms = BANK_NAME.replace(' ', '')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    email_subject = f"{BANK_NAME} Transaction Alert: {transaction_type.title()}"
    email_body = (
        f"Dear {username},\n\n"
        f"A {transaction_type.lower()} of {amount:,.2f} {currency} has occurred on your account.\n\n"
        f"Date/Time: {timestamp}\n"
        f"Reference: {ref_num}\n"
        f"Description: {description}\n"
        f"New Balance: {new_balance:,.2f} {currency}\n\n"
        f"Thank you for banking with {BANK_NAME}.\n"
    )
    _log_communication(EMAIL_INBOX_FILE, sender_email, email, email_subject, email_body)

    sms_body = (
        f"Alert! Your {BANK_NAME} account: {transaction_type.title()} {amount:,.2f} {currency}. "
        f"Ref: {ref_num}. New Balance: {new_balance:,.2f} {currency}. {timestamp}"
    )
    _log_communication(SMS_LOG_FILE, sender_sms, phone_number, None, sms_body)
    print(f"{GREEN_CHECKMARK} Transaction notification sent to {email} and {phone_number}.")

def send_loan_disbursement_notification(username, email, phone_number, loan_amount, interest, repayment_date, disbursed_to, account_currency, ref_num):
    """Simulates sending email and SMS for loan disbursement."""
    sender_email = f"loans@{BANK_NAME.lower().replace(' ', '')}.com"
    sender_sms = BANK_NAME.replace(' ', '')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    email_subject = f"{BANK_NAME} Loan Disbursed Confirmation"
    email_body = (
        f"Dear {username},\n\n"
        f"Your loan request has been approved and disbursed!\n\n"
        f"Loan Amount: {loan_amount:,.2f} {account_currency}\n"
        f"Interest (15% monthly): {interest:,.2f} {account_currency}\n"
        f"Total Repayable: {(loan_amount + interest):,.2f} {account_currency}\n"
        f"Repayment Due Date: {repayment_date.strftime('%Y-%m-%d')}\n"
        f"Disbursed To: {disbursed_to}\n"
        f"Reference: {ref_num}\n"
        f"Date/Time: {timestamp}\n\n"
        f"Please ensure timely repayment to maintain a good credit score.\n\n"
        f"Thank you for banking with {BANK_NAME}.\n"
    )
    _log_communication(EMAIL_INBOX_FILE, sender_email, email, email_subject, email_body)

    sms_body = (
        f"Loan of {loan_amount:,.2f} {account_currency} disbursed to {disbursed_to}. "
        f"Total repayable: {(loan_amount + interest):,.2f} by {repayment_date.strftime('%Y-%m-%d')}. "
        f"Ref: {ref_num}. {BANK_NAME}"
    )
    _log_communication(SMS_LOG_FILE, sender_sms, phone_number, None, sms_body)
    print(f"{GREEN_CHECKMARK} Loan disbursement notification sent to {email} and {phone_number}.")


# --- Display Menus ---

def display_main_menu(logged_in):
    """Displays the main menu based on login status."""
    clear_screen()
    print("\n" + "=" * 50)
    print(f"{BANK_NAME} - {BANK_TAGLINE}".center(50))
    print("=" * 50)
    if logged_in:
        print("1. Account Services")
        print("2. Explore Our Offers")
        print("3. Logout")
        print("4. Exit Application")
    else:
        print("1. Open a Bank Account")
        print("2. Explore Our Offers")
        print("3. Login")
        print("4. Exit Application")
    print("-" * 50)

def display_account_opening_menu():
    """Displays the menu for account opening options."""
    clear_screen()
    print("\n" + "=" * 50)
    print("Open a Bank Account".center(50))
    print("=" * 50)
    print("1. Apply Online (Receive application form via email)")
    print("2. Visit Nearest Bank Branch (Get a token for in-person service)")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_offers_menu():
    """Displays the menu for exploring bank offers."""
    clear_screen()
    print("\n" + "=" * 50)
    print("Explore Our Offers".center(50))
    print("=" * 50)
    print("1. Bank Accounts")
    print("2. Our Cards")
    print("3. ATM Locator")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_bank_accounts_menu():
    """Displays the types of bank accounts offered."""
    clear_screen()
    print("\n" + "=" * 50)
    print("Bank Accounts".center(50))
    print("=" * 50)
    print("1. Current Bank Account")
    print("2. Club Account")
    print("3. PayGo Account")
    print("4. Sapphire Multi Currency Account")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_cards_menu():
    """Displays the categories of cards offered."""
    clear_screen()
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
    clear_screen()
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
    clear_screen()
    print("\n" + "=" * 50)
    print("Prepaid Cards".center(50))
    print("=" * 50)
    print("1. Multi Currency Prepaid MasterCard")
    print("2. Sapphire Prepaid Visa")
    print("3. Safari Prepaid Visa")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_credit_cards():
    clear_screen()
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
    clear_screen()
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

def display_atm_locations_menu():
    """Displays the ATM locations menu for a selected bank branch."""
    clear_screen()
    print("\n" + "=" * 50)
    print("ATM Locations".center(50))
    print("=" * 50)
    for i, branch_name in enumerate(OUR_BRANCHES, 1):
        print(f"{i}. {branch_name}")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

def display_account_services_menu():
    """Displays the menu for account services."""
    clear_screen()
    print("\n" + "=" * 50)
    print("Account Services".center(50))
    print("=" * 50)
    print("1. View Account Details")
    print("2. Make a Deposit")
    print("3. Make a Withdrawal")
    print("4. View Transaction History")
    print("5. My Statements")
    print("6. Add/Manage Payment Methods")
    print("7. Manage Cards")
    print("8. Request Services") # General placeholder for new services
    print("9. Make Payments (Transfers to external methods)")
    print("10. Check Loan Balance/Limit & Request Loan")
    print("11. Logout")
    print("-" * 50)

def display_payment_methods_menu():
    """Displays the menu for managing payment methods."""
    clear_screen()
    print("\n" + "=" * 50)
    print("Add/Manage Payment Methods".center(50))
    print("=" * 50)
    print("1. Add M-Pesa")
    print("2. Add Airtel Money")
    print("3. Add Bank Transfer")
    print("4. Add PayPal")
    print("5. Add Crypto Wallet (Bitcoin, Ethereum, Solana, incl. exchanges)")
    print("6. Set/Change Payment Passcode")
    print("7. View My Payment Methods")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

# --- Token Machine Simulation ---
def display_token(service_choice):
    """Simulates a token machine printing a token."""
    clear_screen()
    service_name = get_service_name(service_choice)
    token_number = random.randint(100, 999)
    print(f"\n{BOLD}{CYAN}----------------------------------------{RESET}")
    print(f"{BOLD}{CYAN}|         {BANK_NAME} Token          |{RESET}")
    print(f"{BOLD}{CYAN}----------------------------------------{RESET}")
    print(f"Service: {service_name}")
    print(f"Token Number: {token_number}")
    print(f"Date: {datetime.date.today().strftime('%Y-%m-%d')}")
    print(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"\n{BLUE_INFO} Please wait for your turn. Requirements for {service_name}:\n")
    if service_choice == 1:
        print("- National ID/Passport")
        print("- KRA PIN Certificate")
        print("- Recent Utility Bill (Proof of Address)")
    elif service_choice in [2, 3]: # Close/Reactivate Account
        print("- National ID/Passport")
        print("- Account details/documents")
    elif service_choice in [4, 5, 6, 7, 8, 9]: # Other services
        print("- National ID/Passport")
        print("- Relevant account information")
    print(f"{BOLD}{CYAN}----------------------------------------{RESET}")
    input("\nPress Enter to take your token...")

def get_service_name(choice):
    """Returns the name of the service based on choice."""
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
    return services.get(choice, "Unknown Service")


# --- Account & Card Details Functions ---

def get_account_type_details(account_type_choice):
    """
    Returns the details of a selected bank account type.
    Args:
        account_type_choice (int): The account type selected by the user.
    Returns:
        dict: A dictionary of account details, or None if invalid type.
    """
    if account_type_choice == 1:
        return {"Account Name": "Current Bank account", "Currency": "KES", "Opening balance": 0, "Monthly maintenance fee": 0,
                        "Minimum balance": 0, "Bank Transfers fees": 0.5, "ATM withdrawal charges": 0.3,
                        "Free monthly e-statements": True, "Debit card": "5"}
    elif account_type_choice == 2:
        return {"Account Name": "Club Account", "Currency": "KES", "Opening balance": 59, "Monthly maintenance fee": 12,
                        "Minimum balance": 0, "Bank Transfers fees": 0.5, "ATM withdrawal charges": 0.3,
                        "Free monthly e-statements": True, "Free Debit MasterCard": True, "Free Cheque book": True}
    elif account_type_choice == 3:
        return {"Account Name": "PayGo account", "Currency": "KES", "Opening balance": 0, "Monthly maintenance fee": 0,
                        "Minimum balance": 0, "Bank Transfers fees": 0.5, "ATM withdrawal charges": 0.3,
                        "Free monthly e-statements": True, "Free Debit MasterCard": True, "Free Cheque book": True}
    elif account_type_choice == 4:
        # Currency will be set during account creation for this type
        return {"Account Name": "Sapphire Multi currency account", "Currency": "N/A", "Opening balance": 100,
                        "Monthly maintenance fee": 0, "Minimum balance": 0, "Bank Transfers fees": 0.5,
                        "ATM withdrawal charges": 0.3, "Free monthly e-statements": True, "Free Debit MasterCard": True,
                        "Free Cheque book": True}
    else:
        return None

def display_account_details_info(account_type_choice):
    """
    Displays the details of a selected bank account type.
    Args:
        account_type_choice (int): The account type selected by the user.
    Returns:
        dict: A dictionary of account details, or None if invalid type.
    """
    details = get_account_type_details(account_type_choice)

    if details:
        print(f"\n--- {details['Account Name']} Overview ---")
        for key, value in details.items():
            if key != "Account Name":
                print(f"{key.replace('_', ' ').title()}: {value}")
    else:
        print(f"{RED_X} Invalid account type.")
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
                       "Currency": "KES", "Card issuance fee": 5, "Card annual fee": 0, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 2:
            details = {"Card Name": "Debit Visa", "Overview": "This card can be issued to all bank account holders",
                       "Currency": "KES", "Card issuance fee": 5, "Card annual fee": 0, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 3:
            details = {"Card Name": "Gold MasterCard", "Overview": "This card can be issued to all bank account holders",
                       "Currency": "KES", "Card issuance fee": 10, "Card annual fee": 1, "Card replacement fee": 10,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        else:
            display_debit_cards()
            return None
    elif card_type == 2: # Prepaid Cards
        if specific_card == 1:
            details = {"Card Name": "Multi Currency Prepaid MasterCard", "Overview": "This card is issued to only Sapphire Multi Currency Account Holders",
                       "Currency": "USD, GBP, EURO, YEN", "Card issuance fee": 12, "Card annual fee": 1, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 2:
            details = {"Card Name": "Sapphire Prepaid Visa", "Overview": "This card can be issued to all bank account holders",
                       "Currency": "KES", "Card issuance fee": 5, "Card annual fee": 0, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 3:
            details = {"Card Name": "Safari Prepaid Visa", "Overview": "This card can be issued to all bank account holders",
                       "Currency": "KES", "Card issuance fee": 5, "Card annual fee": 0, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        else:
            display_prepaid_cards()
            return None
    elif card_type == 3: # Credit Cards
        if specific_card == 1:
            details = {"Card Name": "Gold Visa Credit Card", "Overview": "This card can be issued to all bank account holders with loan limits.",
                       "Currency": "KES", "Card issuance fee": 5, "Card annual fee": 0, "Card replacement fee": 5,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 2:
            details = {"Card Name": "Bronze Credit MasterCard", "Overview": "This card can be issued to only Multi Currency bank account holders with loan limits.",
                       "Currency": "KES", "Card issuance fee": 10, "Card annual fee": 20, "Card replacement fee": 10,
                       "Card purchases": 0.5, "ATM withdrawals": 0.3, "Check balance": 0.3}
        elif specific_card == 3:
            details = {"Card Name": "Diamond Credit Card", "Overview": "This card is only issued to Multi Currency Bank account holders with good transaction history and have an accumulative loan limit.",
                       "Currency": "KES", "Card issuance fee": 100, "Card annual fee": 10, "Card replacement fee": 199,
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


# --- Account Creation Function ---
def create_account():
    """
    Guides the user through the account creation process,
    collects personal details, performs OTP verification,
    handles security questions, and account activation.
    """
    accounts_data = read_accounts() # Load existing accounts

    # --- Collect User Account Details ---
    while True:
        new_username = get_user_input("Enter a new username: ")
        if new_username == 'M' or new_username == 'P': return new_username
        if new_username is None: return None
        if new_username in accounts_data:
            print(f"{RED_X} Username already exists. Please choose a different one.")
        else:
            break

    while True:
        new_password = get_user_input("Enter a new password: ")
        if new_password == 'M' or new_password == 'P': return new_password
        if new_password is None: return None
        confirm_password = get_user_input("Confirm your password: ")
        if confirm_password == 'M' or confirm_password == 'P': return confirm_password
        if confirm_password is None: return None
        if new_password == confirm_password:
            break
        else:
            print(f"{RED_X} Passwords do not match. Please try again.")
    
    # --- Set Security Questions ---
    print("\n--- Set Up Security Questions (Choose Two) ---")
    selected_questions = {}
    available_q_indices = list(SECURITY_QUESTIONS.keys())

    for i in range(2):
        while True:
            print("\nAvailable Security Questions:")
            for idx in available_q_indices:
                print(f"{idx}. {SECURITY_QUESTIONS[idx]}")
            
            q_choice = get_user_input(f"Select question {i+1} (number): ", int)
            if q_choice == 'M' or q_choice == 'P': return q_choice
            if q_choice is None: return None
            
            if q_choice in available_q_indices:
                answer = get_user_input(f"Your answer to '{SECURITY_QUESTIONS[q_choice]}': ")
                if answer == 'M' or answer == 'P': return answer
                if answer is None: return None
                
                selected_questions[SECURITY_QUESTIONS[q_choice]] = answer
                available_q_indices.remove(q_choice) # Remove selected question
                break
            else:
                print(f"{RED_X} Invalid question choice or question already selected. Please choose from the available list.")
    
    # --- Collect Personal Details ---
    name = get_user_input("Enter your full name: ")
    if name == 'M' or name == 'P': return name
    if name is None: return None

    nationality = get_user_input("Enter your nationality: ")
    if nationality == 'M' or nationality == 'P': return nationality
    if nationality is None: return None

    country_code = get_user_input("Enter your country code (e.g., +254 for Kenya): ")
    if country_code == 'M' or country_code == 'P': return country_code
    if country_code is None: return None
    
    phone_number = get_user_input("Enter your phone number (e.g., 712345678): ")
    if phone_number == 'M' or phone_number == 'P': return phone_number
    if phone_number is None: return None
    # Basic phone number validation
    if not (phone_number.isdigit() and len(phone_number) >= 9):
        print(f"{RED_X} Invalid phone number format.")
        input("Press Enter to continue...")
        return False
    full_phone_number = country_code + phone_number # Combine for use

    email = get_user_input("Enter your email address: ")
    if email == 'M' or email == 'P': return email
    if email is None: return None
    while not is_valid_email(email):
        print(f"{RED_X} Invalid email address.")
        email = get_user_input("Enter your email address: ")
        if email == 'M' or email == 'P': break # Allow breaking from validation loop
        if email is None: return None
    if email == 'M' or email == 'P': return email # If loop broke due to M/P

    kra_pin = get_user_input("Enter your KRA PIN: ")
    if kra_pin == 'M' or kra_pin == 'P': return kra_pin
    if kra_pin is None: return None

    reason = get_user_input("Reason for opening account: ")
    if reason == 'M' or reason == 'P': return reason
    if reason is None: return None

    occupation = get_user_input("Enter your occupation: ")
    if occupation == 'M' or occupation == 'P': return occupation
    if occupation is None: return None

    source_of_income = get_user_input("Enter your source of income: ")
    if source_of_income == 'M' or source_of_income == 'P': return source_of_income
    if source_of_income is None: return None

    monthly_deposits = get_user_input("Enter approximate number of monthly deposits: ", int)
    if monthly_deposits == 'M' or monthly_deposits == 'P': return monthly_deposits
    if monthly_deposits is None: return None

    monthly_withdrawals = get_user_input("Enter approximate number of monthly withdrawals: ", int)
    if monthly_withdrawals == 'M' or monthly_withdrawals == 'P': return monthly_withdrawals
    if monthly_withdrawals is None: return None
    while monthly_withdrawals > monthly_deposits:
        print(f"{RED_X} Withdrawals should not be more than deposits. Please enter again.")
        monthly_withdrawals = get_user_input("Enter approximate number of monthly withdrawals: ", int)
        if monthly_withdrawals == 'M' or monthly_withdrawals == 'P': return monthly_withdrawals
        if monthly_withdrawals is None: return None
    
    monthly_balance = get_user_input("Enter monthly balance you intend to maintain (e.g., 50000.00): ", float)
    if monthly_balance == 'M' or monthly_balance == 'P': return monthly_balance
    if monthly_balance is None: return None
    
    address = get_user_input("Enter your address: ")
    if address == 'M' or address == 'P': return address
    if address is None: return None

    print("\nOur Bank Branches:")
    for i, branch in enumerate(OUR_BRANCHES, 1):
        print(f"{i}. {branch}")
    branch_choice = get_user_input(f"Select your bank branch (1-{len(OUR_BRANCHES)}): ", int)
    if branch_choice == 'M' or branch_choice == 'P': return branch_choice
    if branch_choice is None: return None
    while not 1 <= branch_choice <= len(OUR_BRANCHES):
        print(f"{RED_X} Invalid branch choice. Please select from the list.")
        branch_choice = get_user_input(f"Select your bank branch (1-{len(OUR_BRANCHES)}): ", int)
        if branch_choice == 'M' or branch_choice == 'P': return branch_choice
        if branch_choice is None: return None
    my_branch = OUR_BRANCHES[branch_choice - 1]

    # --- Bank Account Type Selection ---
    account_type_details = None
    while True:
        display_bank_accounts_menu()
        acc_type_choice = get_user_input("Select an account type to open: ", int)
        if acc_type_choice == 'M' or acc_type_choice == 'P': return acc_type_choice
        if acc_type_choice is None: return None

        account_type_details = get_account_type_details(acc_type_choice)
        if account_type_details:
            # Handle multi-currency selection for Sapphire Multi Currency Account
            if account_type_details.get("Account Name") == "Sapphire Multi currency account":
                print("\n--- Select Your Preferred Base Currency for Sapphire Multi Currency Account ---")
                print("1. USD (United States Dollar)")
                print("2. GBP (Great British Pound)")
                print("3. EURO (Euro)")
                print("4. JPY (Japanese Yen)")
                
                currency_map = {
                    1: "USD",
                    2: "GBP",
                    3: "EURO",
                    4: "JPY"
                }
                
                while True:
                    currency_choice = get_user_input("Enter your choice (1-4): ", int)
                    if currency_choice == 'M': return 'M'
                    if currency_choice == 'P': return 'P'
                    if currency_choice is None: return None
                    
                    if currency_choice in currency_map:
                        account_type_details["Currency"] = currency_map[currency_choice]
                        print(f"{GREEN_CHECKMARK} You have selected {account_type_details['Currency']} as your account's base currency.")
                        break
                    else:
                        print(f"{RED_X} Invalid currency choice.")
                        input("Press Enter to continue...")

            display_account_details_info(acc_type_choice)
            confirm_account = get_user_input("Do you want to open this account type? (yes/no): ").lower()
            if confirm_account == 'yes':
                break
            elif confirm_account == 'M' or confirm_account == 'P':
                return confirm_account
            elif confirm_account is None:
                return None
            else:
                print(f"{RED_X} Invalid confirmation. Please enter 'yes' or 'no'.")
        else:
            print(f"{RED_X} Invalid account type selection.")
            input("Press Enter to continue...")
    
    # --- OTP verification ---
    generated_otp = generate_otp()
    otp_sent_time = datetime.datetime.now()
    otp_expiration_time = otp_sent_time + datetime.timedelta(minutes=5)

    if not send_otp_email(name, email, generated_otp, otp_expiration_time):
        print(f"{RED_X} Failed to send OTP email. Account creation aborted.")
        return False # Indicate failure
    
    entered_otp = get_user_input("Enter the OTP you received (expires in 5 minutes): ")
    if entered_otp == 'M' or entered_otp == 'P': return entered_otp
    if entered_otp is None: return None

    current_time = datetime.datetime.now()

    if entered_otp == generated_otp and current_time < otp_expiration_time:
        print(f"\n{GREEN_CHECKMARK} Your details have been successfully verified and saved!")
        
        # --- Account Activation Logic ---
        initial_balance_needed = account_type_details.get("Opening balance", 0.0)
        actual_initial_deposit = 0.0 # Account starts with 0 balance for now
        account_activated = False

        if initial_balance_needed > 0:
            # Convert initial_balance_needed to account's currency if it's not KES
            initial_balance_in_account_currency = convert_currency(initial_balance_needed, "KES", account_type_details["Currency"])
            if initial_balance_in_account_currency is None:
                print(f"{RED_X} Error: Could not determine initial balance in chosen currency. Account creation aborted.")
                return False
            
            print(f"{BLUE_INFO} This account type requires an opening balance of {initial_balance_in_account_currency:,.2f} {account_type_details['Currency']}.")
            print(f"{BLUE_INFO} You will need to deposit this amount to fully activate your account.")
            print(f"{BLUE_INFO} Your account will be created. Please note that you must deposit {initial_balance_in_account_currency:,.2f} {account_type_details['Currency']} to fully activate it.")
            print(f"{BLUE_INFO} You can do this from 'Account Services' -> 'Make a Deposit' after logging in.")
            input("Press Enter to continue...") # Pause for user to read

        else: # Opening balance is 0
            account_activated = True
            print(f"{GREEN_CHECKMARK} Account activated immediately (no opening balance required).")

        # Assign a random account number
        account_number = "ACC" + ''.join(random.choices('0123456789', k=10))
        
        # Store all user data in the 'details' sub-dictionary
        user_details = {
            "name": name,
            "nationality": nationality,
            "phone_number": full_phone_number, # Storing the full number
            "email": email,
            "kra_pin": kra_pin,
            "reason": reason,
            "occupation": occupation,
            "source_of_income": source_of_income,
            "monthly_deposits_expected": monthly_deposits, # Store expected number of deposits
            "monthly_withdrawals_expected": monthly_withdrawals, # Store expected number of withdrawals
            "monthly_balance_expected": monthly_balance, # Store expected monthly balance
            "application_date": datetime.date.today().isoformat(),
            "address": address,
            "branch": my_branch,
            "account_number": account_number,
            "account_type_name": account_type_details.get('Account Name', 'N/A'),
            "account_type_features": account_type_details, # Store all features
            "account_currency": account_type_details["Currency"], # Explicitly store chosen currency
            "security_questions": selected_questions,
            "loan_limit": 0.0, # Initial loan limit
            "active_loans": 0.0, # Current active loan amount
            "last_loan_limit_update": datetime.date.today().isoformat(), # Track last update for 30-day rule
            "cards": [],
            "card_pins": [],
            "payment_methods": [], # Initialize empty payment methods list
            "payment_passcode": None, # Initialize payment passcode
            "beneficiaries": [], # For future transfer functionality
            "statements": [] # Initialize empty statements list
        }
        
        # Add a default payment method with 150 USD balance for the user, as discussed
        # This allows them to immediately test deposit functionality
        default_test_wallet_balance_usd = 150.0
        user_details["payment_methods"].append({
            "name": "Default Test Wallet",
            "identifier": "Virtual Wallet",
            "currency": "USD",
            "balance": default_test_wallet_balance_usd
        })

        accounts_data[new_username] = {
            "password": new_password,
            "balance": actual_initial_deposit, # This will likely be 0 initially
            "details": user_details
        }
        save_accounts(accounts_data)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if actual_initial_deposit > 0:
            # This path is currently not taken for new accounts, but if it were, this would log.
            pass # Transaction will be logged when user makes the actual deposit

        # Send security questions confirmation email
        send_security_questions_email(name, email, selected_questions)
        
        # Send comprehensive activation email and SMS if activated
        if account_activated:
            send_account_activation_email(new_username, email, account_number, account_type_details, my_branch)
            send_activation_sms(full_phone_number, account_number)
            print(f"\n{GREEN_CHECKMARK} Account for '{new_username}' successfully created and activated!")
        else:
            print(f"\n{GREEN_CHECKMARK} Account for '{new_username}' successfully created. It needs an initial deposit to be fully activated.")
            print(f"{BLUE_INFO} Your new account number is: {account_number}")
            print(f"{BLUE_INFO} Please remember your username and password for login.")
            print(f"{BLUE_INFO} Log in and navigate to 'Account Services' -> 'Make a Deposit' to activate your account.")

        return True # Indicate successful account creation
    elif current_time >= otp_expiration_time:
        print(f"{RED_X} OTP expired. Account creation failed. Please try again.")
        return False
    else:
        print(f"{RED_X} Incorrect OTP. Account creation failed. Please try again.")
        return False

# --- Core Bank Operations ---

def deposit(username):
    """Allows a user to deposit funds into their account."""
    accounts_data = read_accounts()
    user_account = accounts_data[username]
    user_details = user_account["details"]
    account_currency = user_details["account_currency"]
    
    payment_methods = user_details.get("payment_methods", [])

    if not payment_methods:
        print(f"{RED_X} You have no payment methods linked to make a deposit.")
        print(f"{BLUE_INFO} Please go to 'Add/Manage Payment Methods' to link one.")
        input("Press Enter to continue...")
        return 'P'

    print("\n--- Select a Payment Method for Deposit ---")
    for i, method in enumerate(payment_methods, 1):
        identifier_display = method.get("identifier", "N/A")
        if method["name"] == "Bank Transfer":
            identifier_display = f"Bank: {method.get('bank_name', 'N/A')}, Acc: {method.get('identifier', 'N/A')}"
        elif method["name"] == "Crypto Wallet":
            identifier_display = f"Type: {method.get('crypto_type', 'N/A')}, Exch: {method.get('exchange', 'N/A')}, Addr: {method.get('identifier', 'N/A')}"
        print(f"{i}. {method['name']} - {identifier_display} (Balance: {method['balance']:.2f} {method['currency']})")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

    method_choice = get_user_input("Enter your choice: ", int)
    if method_choice == 'M': return 'M'
    if method_choice == 'P': return 'P'
    if method_choice is None: return None

    if not (1 <= method_choice <= len(payment_methods)):
        print(f"{RED_X} Invalid payment method choice.")
        input("Press Enter to continue...")
        return 'P'

    selected_method = payment_methods[method_choice - 1]
    
    while True:
        amount_to_deposit = get_user_input(f"Enter amount to deposit from {selected_method['name']} ({selected_method['currency']}): ", float)
        if amount_to_deposit == 'M': return 'M'
        if amount_to_deposit == 'P': return 'P'
        if amount_to_deposit is None: return None

        if amount_to_deposit <= 0:
            print(f"{RED_X} Deposit amount must be positive.")
        elif amount_to_deposit > selected_method['balance']:
            print(f"{RED_X} Insufficient funds in your {selected_method['name']} ({selected_method['currency']}) account. Available: {selected_method['balance']:.2f} {selected_method['currency']}.")
        else:
            break

    # Convert amount to account's currency
    converted_amount = convert_currency(amount_to_deposit, selected_method['currency'], account_currency)
    if converted_amount is None:
        print(f"{RED_X} Failed to convert currency for deposit. Please try again.")
        input("Press Enter to continue...")
        return 'P'

    # Check for account activation requirement
    account_opening_balance = user_details["account_type_features"].get("Opening balance", 0.0)
    if not user_account.get("activated", True) and account_opening_balance > 0:
        required_activation_amount = convert_currency(account_opening_balance, "KES", account_currency)
        if converted_amount < required_activation_amount:
            print(f"{RED_X} This is your first deposit and it must be at least the opening balance of {required_activation_amount:,.2f} {account_currency} to activate your account.")
            input("Press Enter to continue...")
            return 'P'
        else:
            user_account["activated"] = True
            print(f"{GREEN_CHECKMARK} Your account has been successfully activated!")

    # Process deposit
    user_account["balance"] += converted_amount
    selected_method['balance'] -= amount_to_deposit
    
    accounts_data[username] = user_account
    save_accounts(accounts_data)

    ref_num = generate_reference_number()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    description = f"Deposit from {selected_method['name']}"
    
    # Store statement
    user_details["statements"].append({
        "timestamp": timestamp,
        "type": "Deposit",
        "amount": converted_amount,
        "currency": account_currency,
        "reference_number": ref_num,
        "description": description,
        "running_balance": user_account["balance"]
    })
    save_accounts(accounts_data) # Save updated statements

    # Update loan limit (after deposit)
    update_loan_limit(username)

    print(f"\n{GREEN_CHECKMARK} Successfully deposited {amount_to_deposit:,.2f} {selected_method['currency']} "
          f"({converted_amount:,.2f} {account_currency}) to your account.")
    print(f"Your new account balance is {user_account['balance']:.2f} {account_currency}.")
    send_transaction_notification(user_details['name'], user_details['email'], user_details['phone_number'],
                                  "Deposit", converted_amount, account_currency, ref_num, description, user_account['balance'])
    input("Press Enter to continue...")
    return True

def withdraw(username):
    """Allows a user to withdraw funds from their account."""
    accounts_data = read_accounts()
    user_account = accounts_data[username]
    user_details = user_account["details"]
    account_currency = user_details["account_currency"]
    
    # Check if account is activated
    if not user_account.get("activated", True):
        print(f"{RED_X} Your account is not yet activated. Please make the required initial deposit to activate it.")
        input("Press Enter to continue...")
        return 'P'

    if user_account["balance"] <= 0:
        print(f"{RED_X} Your account balance is zero or insufficient for withdrawal.")
        input("Press Enter to continue...")
        return 'P'
    
    print("\n--- Withdrawal Options ---")
    print(f"Your current balance: {user_account['balance']:.2f} {account_currency}")
    print("1. Withdraw to Bank Account (same currency as your current bank account)")
    print("2. Withdraw to Mobile Money (KES only, if linked)")
    print("3. Withdraw to PayPal (USD only, if linked)")
    print("4. Withdraw to Crypto Wallet (specific crypto, if linked)")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

    withdrawal_choice = get_user_input("Select withdrawal destination: ", int)
    if withdrawal_choice == 'M': return 'M'
    if withdrawal_choice == 'P': return 'P'
    if withdrawal_choice is None: return None

    destination_method = None
    destination_currency = account_currency # Default to account currency
    
    if withdrawal_choice == 1:
        destination_name = "Bank Account"
        destination_currency = account_currency # No conversion needed if same currency
    elif withdrawal_choice in [2, 3, 4]:
        payment_methods = user_details.get("payment_methods", [])
        if not payment_methods:
            print(f"{RED_X} No payment methods linked for this type of withdrawal. Please add one.")
            input("Press Enter to continue...")
            return 'P'

        eligible_methods = []
        if withdrawal_choice == 2: # Mobile Money
            eligible_methods = [m for m in payment_methods if m['name'] in ["M-Pesa", "Airtel Money"]]
            expected_currency = "KES"
        elif withdrawal_choice == 3: # PayPal
            eligible_methods = [m for m in payment_methods if m['name'] == "PayPal"]
            expected_currency = "USD"
        elif withdrawal_choice == 4: # Crypto Wallet
            eligible_methods = [m for m in payment_methods if m['name'] == "Crypto Wallet"]
            # For crypto, destination currency is its symbol (BTC, ETH, SOL)
            expected_currency = None 

        if not eligible_methods:
            print(f"{RED_X} No eligible linked payment methods found for your selection.")
            input("Press Enter to continue...")
            return 'P'
        
        print(f"\n--- Select a Destination {['','Mobile Money','PayPal','Crypto Wallet'][withdrawal_choice]} ---")
        for i, method in enumerate(eligible_methods, 1):
            identifier_display = method.get("identifier", "N/A")
            if method["name"] == "Crypto Wallet":
                identifier_display = f"Type: {method.get('crypto_type', 'N/A')}, Exch: {method.get('exchange', 'N/A')}, Addr: {method.get('identifier', 'N/A')}"
            print(f"{i}. {method['name']} - {identifier_display} (Current Balance: {method['balance']:.2f} {method['currency']})")
        
        dest_choice = get_user_input("Enter your choice: ", int)
        if dest_choice == 'M': return 'M'
        if dest_choice == 'P': return 'P'
        if dest_choice is None: return None

        if not (1 <= dest_choice <= len(eligible_methods)):
            print(f"{RED_X} Invalid destination choice.")
            input("Press Enter to continue...")
            return 'P'
        
        destination_method = eligible_methods[dest_choice - 1]
        destination_name = destination_method['name']
        destination_currency = destination_method['currency']
        
    else:
        print(f"{RED_X} Invalid withdrawal option.")
        input("Press Enter to continue...")
        return 'P'

    while True:
        amount_to_withdraw = get_user_input(f"Enter amount to withdraw ({account_currency}): ", float)
        if amount_to_withdraw == 'M': return 'M'
        if amount_to_withdraw == 'P': return 'P'
        if amount_to_withdraw is None: return None

        if amount_to_withdraw <= 0:
            print(f"{RED_X} Withdrawal amount must be positive.")
        elif amount_to_withdraw > user_account["balance"]:
            print(f"{RED_X} Insufficient funds. Your current balance is {user_account['balance']:.2f} {account_currency}.")
        else:
            break
            
    # Verify payment passcode for external transfers
    if withdrawal_choice in [2, 3, 4]: # Mobile Money, PayPal, Crypto
        if not user_details.get("payment_passcode"):
            print(f"{RED_X} You must set a Payment Authorization Passcode to make external transfers.")
            input("Press Enter to continue...")
            return 'P'
        
        entered_passcode = get_user_input("Enter your 6-digit Payment Authorization Passcode: ")
        if entered_passcode == 'M': return 'M'
        if entered_passcode == 'P': return 'P'
        if entered_passcode is None: return None

        if entered_passcode != user_details["payment_passcode"]:
            print(f"{RED_X} Incorrect Payment Authorization Passcode. Withdrawal failed.")
            input("Press Enter to continue...")
            return 'P'

    # Convert amount from account's currency to destination currency
    converted_amount = convert_currency(amount_to_withdraw, account_currency, destination_currency)
    if converted_amount is None:
        print(f"{RED_X} Failed to convert currency for withdrawal. Please try again.")
        input("Press Enter to continue...")
        return 'P'

    # Process withdrawal
    user_account["balance"] -= amount_to_withdraw
    
    if destination_method:
        # Find the actual method in the list and update its balance
        for i, method in enumerate(user_details['payment_methods']):
            if method == destination_method: # Assuming direct object comparison works or use identifier
                user_details['payment_methods'][i]['balance'] += converted_amount
                break
    
    accounts_data[username] = user_account
    save_accounts(accounts_data)

    ref_num = generate_reference_number()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    description = f"Withdrawal to {destination_name}"
    if destination_method:
        description += f" ({destination_method.get('identifier', '')})"
    
    # Store statement
    user_details["statements"].append({
        "timestamp": timestamp,
        "type": "Withdrawal",
        "amount": amount_to_withdraw,
        "currency": account_currency,
        "reference_number": ref_num,
        "description": description,
        "running_balance": user_account["balance"]
    })
    save_accounts(accounts_data) # Save updated statements

    print(f"\n{GREEN_CHECKMARK} Successfully withdrew {amount_to_withdraw:,.2f} {account_currency}.")
    print(f"Funds transferred to {destination_name}: {converted_amount:,.2f} {destination_currency}.")
    print(f"Your new account balance is {user_account['balance']:.2f} {account_currency}.")
    send_transaction_notification(user_details['name'], user_details['email'], user_details['phone_number'],
                                  "Withdrawal", amount_to_withdraw, account_currency, ref_num, description, user_account['balance'])
    input("Press Enter to continue...")
    return True

def view_transaction_history(username):
    """Displays simplified transaction history for the user."""
    transactions = read_transactions()
    user_transactions = [t for t in transactions if t["username"] == username]

    if not user_transactions:
        print(f"{BLUE_INFO} No transaction history found for {username}.")
        input("Press Enter to continue...")
        return

    print("\n--- Your Transaction History ---")
    print(f"{'Date':<19} {'Type':<15} {'Amount':<15} {'Currency':<10} {'Ref No.':<20}")
    print("-" * 80)
    for t in user_transactions:
        print(f"{t['timestamp']:<19} {t['type']:<15} {t['amount']:.2f}{t['currency']:<15} {t['reference_number']:<20}")
    print("-" * 80)
    input("Press Enter to continue...")

def view_my_statements(username):
    """Displays detailed statement entries for the user."""
    accounts_data = read_accounts()
    user_details = accounts_data[username]["details"]
    statements = user_details.get("statements", [])

    if not statements:
        print(f"{BLUE_INFO} No statements available for your account yet.")
    else:
        print("\n--- Your Account Statements ---")
        print(f"{'Date/Time':<19} {'Type':<15} {'Amount':<15} {'Currency':<10} {'Running Balance':<20} {'Description':<30}")
        print("-" * 120)
        for s in statements:
            print(f"{s['timestamp']:<19} {s['type']:<15} {s['amount']:<15.2f} {s['currency']:<10} {s['running_balance']:<20.2f} {s['description']:<30}")
        print("-" * 120)
    input("Press Enter to continue...")


# --- Payment Methods ---

def set_payment_passcode(username):
    """Allows a user to set or change their 6-digit payment passcode."""
    accounts_data = read_accounts()
    user_details = accounts_data[username]["details"]
    phone_number = user_details.get("phone_number")

    if not phone_number:
        print(f"{RED_X} Please ensure your phone number is registered to set a passcode.")
        input("Press Enter to continue...")
        return False

    while True:
        new_passcode = get_user_input("Enter a new 6-digit Payment Authorization Passcode: ")
        if new_passcode == 'M': return 'M'
        if new_passcode == 'P': return 'P'
        if new_passcode is None: return None

        if not (new_passcode.isdigit() and len(new_passcode) == 6):
            print(f"{RED_X} Passcode must be a 6-digit number.")
            continue
        
        confirm_passcode = get_user_input("Confirm your 6-digit Payment Authorization Passcode: ")
        if confirm_passcode == 'M': return 'M'
        if confirm_passcode == 'P': return 'P'
        if confirm_passcode is None: return None

        if new_passcode == confirm_passcode:
            # Send OTP to verify
            generated_otp = generate_otp(6) # Using main generate_otp
            if not send_payment_otp_sms(phone_number, generated_otp):
                print(f"{RED_X} Failed to send OTP. Passcode not set.")
                input("Press Enter to continue...")
                return False

            entered_otp = get_user_input("Enter the OTP received on your phone to verify passcode: ")
            if entered_otp == 'M': return 'M'
            if entered_otp == 'P': return 'P'
            if entered_otp is None: return None

            if entered_otp == generated_otp:
                user_details["payment_passcode"] = new_passcode
                accounts_data[username]["details"] = user_details # Update in the main dict
                save_accounts(accounts_data)
                print(f"{GREEN_CHECKMARK} Payment Authorization Passcode successfully set/updated!")
                input("Press Enter to continue...")
                return True
            else:
                print(f"{RED_X} Incorrect OTP. Passcode not set.")
                input("Press Enter to continue...")
                return False
        else:
            print(f"{RED_X} Passcodes do not match. Please try again.")

def add_payment_method(username, method_type):
    """Adds a payment method to the user's account with a default balance."""
    accounts_data = read_accounts()
    user_details = accounts_data[username]["details"]
    payment_methods = user_details.setdefault("payment_methods", [])

    method_name = ""
    currency = "KES" # Default currency for most KES-based methods
    default_balance_usd = 150.0 # Default balance value in USD, will be converted

    if method_type == 1: # M-Pesa
        method_name = "M-Pesa"
        phone_number = get_user_input("Enter M-Pesa phone number (e.g., 254712345678): ")
        if phone_number == 'M': return 'M'
        if phone_number == 'P': return 'P'
        if phone_number is None: return None
        if not (phone_number.isdigit() and len(phone_number) >= 9):
            print(f"{RED_X} Invalid phone number format.")
            input("Press Enter to continue...")
            return False
        
        if any(pm['name'] == method_name and pm['identifier'] == phone_number for pm in payment_methods):
            print(f"{BLUE_INFO} This M-Pesa account is already linked.")
            input("Press Enter to continue...")
            return False
        
        default_balance_kes = convert_currency(default_balance_usd, "USD", "KES")
        payment_methods.append({
            "name": method_name,
            "identifier": phone_number,
            "currency": currency,
            "balance": default_balance_kes
        })
    elif method_type == 2: # Airtel Money
        method_name = "Airtel Money"
        phone_number = get_user_input("Enter Airtel Money phone number (e.g., 254712345678): ")
        if phone_number == 'M': return 'M'
        if phone_number == 'P': return 'P'
        if phone_number is None: return None
        if not (phone_number.isdigit() and len(phone_number) >= 9):
            print(f"{RED_X} Invalid phone number format.")
            input("Press Enter to continue...")
            return False
        
        if any(pm['name'] == method_name and pm['identifier'] == phone_number for pm in payment_methods):
            print(f"{BLUE_INFO} This Airtel Money account is already linked.")
            input("Press Enter to continue...")
            return False

        default_balance_kes = convert_currency(default_balance_usd, "USD", "KES")
        payment_methods.append({
            "name": method_name,
            "identifier": phone_number,
            "currency": currency,
            "balance": default_balance_kes
        })
    elif method_type == 3: # Bank Transfer
        method_name = "Bank Transfer"
        bank_name = get_user_input("Enter Sending Bank Name: ")
        if bank_name == 'M': return 'M'
        if bank_name == 'P': return 'P'
        if bank_name is None: return None
        account_no = get_user_input("Enter Sending Account Number: ")
        if account_no == 'M': return 'M'
        if account_no == 'P': return 'P'
        if account_no is None: return None
        if not account_no.isdigit():
            print(f"{RED_X} Account number must be digits.")
            input("Press Enter to continue...")
            return False

        if any(pm['name'] == method_name and pm['identifier'] == account_no and pm['bank_name'] == bank_name for pm in payment_methods):
            print(f"{BLUE_INFO} This Bank Transfer account is already linked.")
            input("Press Enter to continue...")
            return False
        
        default_balance_kes = convert_currency(default_balance_usd, "USD", "KES")
        payment_methods.append({
            "name": method_name,
            "bank_name": bank_name,
            "identifier": account_no,
            "currency": currency,
            "balance": default_balance_kes
        })
    elif method_type == 4: # PayPal
        method_name = "PayPal"
        paypal_email = get_user_input("Enter PayPal email: ")
        if paypal_email == 'M': return 'M'
        if paypal_email == 'P': return 'P'
        if paypal_email is None: return None
        if not is_valid_email(paypal_email):
            print(f"{RED_X} Invalid PayPal email address.")
            input("Press Enter to continue...")
            return False
        
        if any(pm['name'] == method_name and pm['identifier'] == paypal_email for pm in payment_methods):
            print(f"{BLUE_INFO} This PayPal account is already linked.")
            input("Press Enter to continue...")
            return False

        payment_methods.append({
            "name": method_name,
            "identifier": paypal_email,
            "currency": "USD", # PayPal assumed to hold USD
            "balance": default_balance_usd
        })
    elif method_type == 5: # Crypto Wallet
        method_name = "Crypto Wallet"
        print("\n--- Choose Cryptocurrency and Exchange ---")
        print("1. Bitcoin (BTC) - General Wallet")
        print("2. Ethereum (ETH) - General Wallet")
        print("3. Solana (SOL) - General Wallet")
        print("4. Bitcoin (BTC) - Binance")
        print("5. Ethereum (ETH) - Bybit")
        print("6. Solana (SOL) - OKX")
        
        crypto_options = {
            1: {"type": "Bitcoin", "exchange": "General Wallet", "currency": "BTC"},
            2: {"type": "Ethereum", "exchange": "General Wallet", "currency": "ETH"},
            3: {"type": "Solana", "exchange": "General Wallet", "currency": "SOL"},
            4: {"type": "Bitcoin", "exchange": "Binance", "currency": "BTC"},
            5: {"type": "Ethereum", "exchange": "Bybit", "currency": "ETH"},
            6: {"type": "Solana", "exchange": "OKX", "currency": "SOL"},
        }

        while True:
            crypto_choice_idx = get_user_input("Select crypto option (1-6): ", int)
            if crypto_choice_idx == 'M': return 'M'
            if crypto_choice_idx == 'P': return 'P'
            if crypto_choice_idx is None: return None

            if crypto_choice_idx in crypto_options:
                selected_crypto = crypto_options[crypto_choice_idx]
                crypto_type = selected_crypto['type']
                crypto_exchange = selected_crypto['exchange']
                crypto_currency_symbol = selected_crypto['currency']
                break
            else:
                print(f"{RED_X} Invalid crypto choice.")
                input("Press Enter to continue...")
                return False # Go back to prev menu if invalid crypto choice

        wallet_address = get_user_input(f"Enter {crypto_type} wallet address ({crypto_exchange}): ")
        if wallet_address == 'M': return 'M'
        if wallet_address == 'P': return 'P'
        if wallet_address is None: return None

        if any(pm['name'] == method_name and pm['crypto_type'] == crypto_type and 
               pm.get('exchange') == crypto_exchange and pm['identifier'] == wallet_address 
               for pm in payment_methods):
            print(f"{BLUE_INFO} This Crypto Wallet ({crypto_type} on {crypto_exchange}) is already linked.")
            input("Press Enter to continue...")
            return False
        
        # Convert default USD balance to the selected crypto's equivalent value
        default_balance_crypto = convert_currency(default_balance_usd, "USD", crypto_currency_symbol)
        if default_balance_crypto is None:
            print(f"{RED_X} Error converting default balance to crypto. Cannot add wallet.")
            input("Press Enter to continue...")
            return False

        payment_methods.append({
            "name": method_name,
            "crypto_type": crypto_type,
            "exchange": crypto_exchange,
            "identifier": wallet_address,
            "currency": crypto_currency_symbol,
            "balance": default_balance_crypto
        })
    else:
        print(f"{RED_X} Invalid payment method choice.")
        input("Press Enter to continue...")
        return False

    accounts_data[username]["details"]["payment_methods"] = payment_methods
    save_accounts(accounts_data)
    print(f"{GREEN_CHECKMARK} {method_name} added successfully!")
    input("Press Enter to continue...")
    return True

def view_payment_methods(username):
    """Displays the user's currently added payment methods."""
    accounts_data = read_accounts()
    user_details = accounts_data[username]["details"]
    payment_methods = user_details.get("payment_methods", [])

    if not payment_methods:
        print(f"{BLUE_INFO} You have not added any payment methods yet.")
    else:
        print("\n--- Your Linked Payment Methods ---")
        for i, method in enumerate(payment_methods, 1):
            identifier_display = method.get("identifier", "N/A")
            if method["name"] == "Bank Transfer":
                identifier_display = f"Bank: {method.get('bank_name', 'N/A')}, Acc: {method.get('identifier', 'N/A')}"
            elif method["name"] == "Crypto Wallet":
                identifier_display = f"Type: {method.get('crypto_type', 'N/A')}, Exch: {method.get('exchange', 'N/A')}, Addr: {method.get('identifier', 'N/A')}"

            print(f"{i}. {method['name']} - {identifier_display} (Balance: {method['balance']:.2f} {method['currency']})")
    input("Press Enter to continue...")

def make_payment(username):
    """Facilitates fund transfers from bank account to linked payment methods."""
    accounts_data = read_accounts()
    user_account = accounts_data[username]
    user_details = user_account["details"]
    account_currency = user_details["account_currency"]
    
    if user_account["balance"] <= 0:
        print(f"{RED_X} Your account balance is zero or insufficient for transfer.")
        input("Press Enter to continue...")
        return 'P'

    payment_methods = user_details.get("payment_methods", [])
    if not payment_methods:
        print(f"{RED_X} You have no external payment methods linked to make a transfer.")
        print(f"{BLUE_INFO} Please go to 'Add/Manage Payment Methods' to link one.")
        input("Press Enter to continue...")
        return 'P'

    print("\n--- Select Destination for Payment/Transfer ---")
    print(f"Your current bank balance: {user_account['balance']:.2f} {account_currency}")
    for i, method in enumerate(payment_methods, 1):
        identifier_display = method.get("identifier", "N/A")
        if method["name"] == "Bank Transfer":
            identifier_display = f"Bank: {method.get('bank_name', 'N/A')}, Acc: {method.get('identifier', 'N/A')}"
        elif method["name"] == "Crypto Wallet":
            identifier_display = f"Type: {method.get('crypto_type', 'N/A')}, Exch: {method.get('exchange', 'N/A')}, Addr: {method.get('identifier', 'N/A')}"
        print(f"{i}. {method['name']} - {identifier_display} (Current Balance: {method['balance']:.2f} {method['currency']})")
    print("P. Go back to previous menu")
    print("M. Go to main menu")

    method_choice = get_user_input("Enter your choice: ", int)
    if method_choice == 'M': return 'M'
    if method_choice == 'P': return 'P'
    if method_choice is None: return None

    if not (1 <= method_choice <= len(payment_methods)):
        print(f"{RED_X} Invalid payment method choice.")
        input("Press Enter to continue...")
        return 'P'

    selected_destination = payment_methods[method_choice - 1]
    destination_name = selected_destination['name']
    destination_currency = selected_destination['currency']

    while True:
        amount_to_transfer = get_user_input(f"Enter amount to transfer from your bank account ({account_currency}): ", float)
        if amount_to_transfer == 'M': return 'M'
        if amount_to_transfer == 'P': return 'P'
        if amount_to_transfer is None: return None

        if amount_to_transfer <= 0:
            print(f"{RED_X} Transfer amount must be positive.")
        elif amount_to_transfer > user_account["balance"]:
            print(f"{RED_X} Insufficient funds in your bank account. Available: {user_account['balance']:.2f} {account_currency}.")
        else:
            break
            
    # Verify payment passcode for external transfers
    if not user_details.get("payment_passcode"):
        print(f"{RED_X} You must set a Payment Authorization Passcode to make external transfers.")
        input("Press Enter to continue...")
        return 'P'
    
    entered_passcode = get_user_input("Enter your 6-digit Payment Authorization Passcode: ")
    if entered_passcode == 'M': return 'M'
    if entered_passcode == 'P': return 'P'
    if entered_passcode is None: return None

    if entered_passcode != user_details["payment_passcode"]:
        print(f"{RED_X} Incorrect Payment Authorization Passcode. Transfer failed.")
        input("Press Enter to continue...")
        return 'P'

    # Convert amount from account's currency to destination currency
    converted_amount = convert_currency(amount_to_transfer, account_currency, destination_currency)
    if converted_amount is None:
        print(f"{RED_X} Failed to convert currency for transfer. Please try again.")
        input("Press Enter to continue...")
        return 'P'

    # Process transfer
    user_account["balance"] -= amount_to_transfer
    
    # Find the actual method in the list and update its balance
    for i, method in enumerate(user_details['payment_methods']):
        if method == selected_destination:
            user_details['payment_methods'][i]['balance'] += converted_amount
            break
    
    accounts_data[username] = user_account
    save_accounts(accounts_data)

    ref_num = generate_reference_number()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    description = f"Transfer to {destination_name}"
    if selected_destination.get('identifier'):
        description += f" ({selected_destination['identifier']})"
    
    # Store statement
    user_details["statements"].append({
        "timestamp": timestamp,
        "type": "Transfer Out",
        "amount": amount_to_transfer,
        "currency": account_currency,
        "reference_number": ref_num,
        "description": description,
        "running_balance": user_account["balance"]
    })
    save_accounts(accounts_data) # Save updated statements

    print(f"\n{GREEN_CHECKMARK} Successfully transferred {amount_to_transfer:,.2f} {account_currency} "
          f"to {destination_name}.")
    print(f"Recipient received {converted_amount:,.2f} {destination_currency}.")
    print(f"Your new bank balance is {user_account['balance']:.2f} {account_currency}.")
    send_transaction_notification(user_details['name'], user_details['email'], user_details['phone_number'],
                                  "Transfer Out", amount_to_transfer, account_currency, ref_num, description, user_account['balance'])
    input("Press Enter to continue...")
    return True


# --- Loan Management ---

def update_loan_limit(username):
    """
    Dynamically updates the user's loan limit based on transaction history and account age.
    Updates are applied to the user's account data.
    """
    accounts_data = read_accounts()
    user_account = accounts_data[username]
    user_details = user_account["details"]
    account_currency = user_details["account_currency"]
    
    # Ensure all date fields are datetime.date objects for comparison
    app_date = datetime.date.fromisoformat(user_details.get("application_date", datetime.date.today().isoformat()))
    last_update_date = datetime.date.fromisoformat(user_details.get("last_loan_limit_update", datetime.date.today().isoformat()))
    current_date = datetime.date.today()

    loan_limit_increase = 0.0
    
    # Condition 1: Monthly Balance vs. Transaction Total
    # For simplicity, let's consider total deposits in the current month vs. expected monthly balance
    statements = user_details.get("statements", [])
    
    # Calculate total deposits and number of deposits in the current month
    current_month_deposits_total = 0.0
    current_month_deposits_count = 0
    
    for s in statements:
        try:
            transaction_date = datetime.datetime.strptime(s["timestamp"], "%Y-%m-%d %H:%M:%S").date()
            if transaction_date.year == current_date.year and transaction_date.month == current_date.month:
                if s["type"] == "Deposit":
                    # Convert deposit amount to KES to compare with monthly_balance_expected (which is in KES)
                    deposit_in_kes = convert_currency(s["amount"], s["currency"], "KES")
                    if deposit_in_kes is not None:
                        current_month_deposits_total += deposit_in_kes
                        current_month_deposits_count += 1
        except ValueError:
            # Handle cases where timestamp format might be off (e.g., old data)
            pass

    expected_monthly_balance_kes = user_details.get("monthly_balance_expected", 0.0) # Assumed to be in KES
    expected_monthly_deposits_count = user_details.get("monthly_deposits_expected", 0)

    # Convert expected_monthly_balance to account's currency for better comparison
    expected_monthly_balance_account_currency = convert_currency(expected_monthly_balance_kes, "KES", account_currency)

    # Increase 1: Transaction total above expected monthly balance
    if current_month_deposits_total > expected_monthly_balance_kes: # Compare in KES
        increase_amount_usd_1 = 150.0
        increase_amount_converted_1 = convert_currency(increase_amount_usd_1, "USD", account_currency)
        if increase_amount_converted_1 is not None:
            loan_limit_increase += increase_amount_converted_1
            # print(f"DEBUG: Loan limit +{increase_amount_converted_1:.2f} ({account_currency}) for monthly balance.") # Debug
            
    # Increase 2: Fulfilled monthly deposit count
    if current_month_deposits_count >= expected_monthly_deposits_count and expected_monthly_deposits_count > 0:
        increase_amount_usd_2 = 100.0
        increase_amount_converted_2 = convert_currency(increase_amount_usd_2, "USD", account_currency)
        if increase_amount_converted_2 is not None:
            loan_limit_increase += increase_amount_converted_2
            # print(f"DEBUG: Loan limit +{increase_amount_converted_2:.2f} ({account_currency}) for monthly deposits.") # Debug

    # Increase 3: Account active for 30 days (one-time boost, or monthly check)
    # To make it a one-time boost, ensure it's not applied if already received or applied within the last 30 days.
    thirty_days_passed = (current_date - app_date).days >= 30
    if thirty_days_passed and (current_date - last_update_date).days >= 30: # Check if 30 days since last update
        increase_amount_usd_3 = 80.0
        increase_amount_converted_3 = convert_currency(increase_amount_usd_3, "USD", account_currency)
        if increase_amount_converted_3 is not None:
            loan_limit_increase += increase_amount_converted_3
            user_details["last_loan_limit_update"] = current_date.isoformat() # Update last check date
            # print(f"DEBUG: Loan limit +{increase_amount_converted_3:.2f} ({account_currency}) for 30-day active.") # Debug

    # Apply increase if any
    if loan_limit_increase > 0:
        user_details["loan_limit"] += loan_limit_increase
        print(f"\n{BLUE_INFO} Your loan limit has been reviewed and increased by {loan_limit_increase:,.2f} {account_currency}.")
        print(f"{BLUE_INFO} New loan limit: {user_details['loan_limit']:.2f} {account_currency}.")
        save_accounts(accounts_data) # Save updated loan limit
        input("Press Enter to continue...")


def request_loan(username):
    """Allows a user to request a loan and choose disbursement method."""
    accounts_data = read_accounts()
    user_account = accounts_data[username]
    user_details = user_account["details"]
    account_currency = user_details["account_currency"]

    current_loan_limit = user_details.get("loan_limit", 0.0)
    active_loans = user_details.get("active_loans", 0.0)
    available_loan_amount = current_loan_limit - active_loans

    if available_loan_amount <= 0:
        print(f"{RED_X} You currently have no available loan limit. Your current limit is {current_loan_limit:,.2f} {account_currency} and active loans are {active_loans:,.2f} {account_currency}.")
        input("Press Enter to continue...")
        return 'P'

    print(f"\n--- Request Loan ---")
    print(f"Your available loan limit: {available_loan_amount:,.2f} {account_currency}")

    while True:
        loan_amount = get_user_input(f"Enter loan amount ({account_currency}) to request: ", float)
        if loan_amount == 'M': return 'M'
        if loan_amount == 'P': return 'P'
        if loan_amount is None: return None

        if loan_amount <= 0:
            print(f"{RED_X} Loan amount must be positive.")
        elif loan_amount > available_loan_amount:
            print(f"{RED_X} Requested amount exceeds your available loan limit. Max: {available_loan_amount:,.2f} {account_currency}.")
        else:
            break
    
    # Choose disbursement method
    print("\n--- Choose Where to Receive Loan Funds ---")
    print("1. To My Bank Account")
    
    payment_methods = user_details.get("payment_methods", [])
    mobile_money_methods = [m for m in payment_methods if m['name'] in ["M-Pesa", "Airtel Money"]]
    paypal_methods = [m for m in payment_methods if m['name'] == "PayPal"]
    crypto_methods = [m for m in payment_methods if m['name'] == "Crypto Wallet"]

    option_counter = 2
    disbursement_options_map = {}
    
    if mobile_money_methods:
        print(f"\n--- Mobile Money ---")
        for i, method in enumerate(mobile_money_methods, 1):
            print(f"{option_counter}. {method['name']} - {method['identifier']}")
            disbursement_options_map[str(option_counter)] = {"type": "mobile_money", "method_obj": method, "index": payment_methods.index(method)}
            option_counter += 1
    
    if paypal_methods:
        print(f"\n--- PayPal ---")
        for i, method in enumerate(paypal_methods, 1):
            print(f"{option_counter}. {method['name']} - {method['identifier']}")
            disbursement_options_map[str(option_counter)] = {"type": "paypal", "method_obj": method, "index": payment_methods.index(method)}
            option_counter += 1

    if crypto_methods:
        print(f"\n--- Crypto Wallets/Exchanges ---")
        for i, method in enumerate(crypto_methods, 1):
            id_display = f"{method['crypto_type']} ({method['exchange']}) - {method['identifier']}"
            print(f"{option_counter}. {method['name']} - {id_display}")
            disbursement_options_map[str(option_counter)] = {"type": "crypto", "method_obj": method, "index": payment_methods.index(method)}
            option_counter += 1

    print("P. Go back to previous menu")
    print("M. Go to main menu")

    disbursement_choice = get_user_input("Enter your choice: ") # Keep as string for map lookup
    if disbursement_choice == 'M': return 'M'
    if disbursement_choice == 'P': return 'P'
    if disbursement_choice is None: return None

    disbursed_to_display = "My Bank Account"
    destination_currency = account_currency
    target_payment_method = None # This will store the actual payment method object if external

    if disbursement_choice == '1': # To My Bank Account
        disbursed_to_display = "Your Bank Account"
        # No currency conversion needed as it's added directly to bank balance in account_currency
        final_disbursement_amount = loan_amount
    elif disbursement_choice in disbursement_options_map:
        selected_option = disbursement_options_map[disbursement_choice]
        target_payment_method = payment_methods[selected_option['index']]
        disbursed_to_display = f"{target_payment_method['name']} ({target_payment_method.get('identifier', '')})"
        destination_currency = target_payment_method['currency']

        # Convert loan amount from account currency to destination currency
        final_disbursement_amount = convert_currency(loan_amount, account_currency, destination_currency)
        if final_disbursement_amount is None:
            print(f"{RED_X} Failed to convert currency for loan disbursement. Loan not issued.")
            input("Press Enter to continue...")
            return 'P'
    else:
        print(f"{RED_X} Invalid disbursement choice.")
        input("Press Enter to continue...")
        return 'P'

    # Calculate interest (15% per month)
    interest_rate = 0.15
    interest_amount = loan_amount * interest_rate
    total_repayable = loan_amount + interest_amount
    
    # Due date: 30 days from now
    repayment_date = datetime.date.today() + datetime.timedelta(days=30)

    # Update user's loan details
    user_details["active_loans"] += loan_amount # Track principal loan amount
    accounts_data[username] = user_account # Save updated details first to prevent partial updates

    # Disburse funds
    if disbursement_choice == '1': # To Bank Account
        user_account["balance"] += final_disbursement_amount
    else: # To external payment method
        target_payment_method['balance'] += final_disbursement_amount
        # Update in the main payment_methods list within user_details
        user_details['payment_methods'][selected_option['index']] = target_payment_method 

    save_accounts(accounts_data)

    ref_num = generate_reference_number()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    description = f"Loan Disbursed - Rec'd via {disbursed_to_display}"
    
    # Add statement entry for loan disbursement
    user_details["statements"].append({
        "timestamp": timestamp,
        "type": "Loan Disbursed",
        "amount": loan_amount, # Log original loan amount in account currency
        "currency": account_currency,
        "reference_number": ref_num,
        "description": description,
        "running_balance": user_account["balance"] # Reflects bank balance if disbursed to bank
    })
    save_accounts(accounts_data)

    send_loan_disbursement_notification(user_details['name'], user_details['email'], user_details['phone_number'],
                                        loan_amount, interest_amount, repayment_date, disbursed_to_display, account_currency, ref_num)
    
    print(f"\n{GREEN_CHECKMARK} Loan of {loan_amount:,.2f} {account_currency} successfully disbursed to {disbursed_to_display}.")
    print(f"You will need to repay {total_repayable:,.2f} {account_currency} by {repayment_date.strftime('%Y-%m-%d')}.")
    input("Press Enter to continue...")
    return True


# --- Main Application Flow Handlers ---

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
            return 'P' # Successfully handled online account opening path, go back to previous menu
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

def display_atm_locations():
    """Displays ATM locations and handles user interaction."""
    while True:
        display_atm_locations_menu()
        branch_choice = get_user_input(f"Enter branch number (1-{len(OUR_BRANCHES)}): ", int)
        if branch_choice == 'M': return 'M'
        if branch_choice == 'P': return 'P'
        if branch_choice is None: return None

        if 1 <= branch_choice <= len(OUR_BRANCHES):
            selected_branch = OUR_BRANCHES[branch_choice - 1]
            print(f"\n--- ATMs at {selected_branch} ---")
            print("1. Main Branch ATM (Lobby)")
            print("2. Drive-Thru ATM")
            print("3. Shopping Mall Kiosk ATM")
            print(f"{BLUE_INFO} For exact coordinates, please visit our website.")
            input("Press Enter to continue...")
        else:
            print(f"{RED_X} Invalid branch choice. Please select from the list.")
            input("Press Enter to continue...")


def handle_account_services_flow(current_username):
    """Handles the flow for logged-in account services."""
    while True:
        display_account_services_menu()
        service_choice = get_user_input("Enter your choice: ", int)
        if service_choice == 'M': return 'M'
        if service_choice == 'P': return 'P' # Return to main menu (or previous if nested)
        if service_choice is None: return None

        # Always update loan limit when user enters account services
        # Or you can do it on specific actions like deposit, withdrawal, or upon request.
        # Let's do it on request for simplicity for now to avoid frequent updates.
        # update_loan_limit(current_username) 

        if service_choice == 1: # View Account Details
            accounts_data = read_accounts()
            user_account = accounts_data[current_username]
            user_details = user_account["details"]
            print(f"\n--- Your Account Details ({current_username}) ---")
            print(f"Account Number: {user_details.get('account_number', 'N/A')}")
            print(f"Account Type: {user_details.get('account_type_name', 'Not Set')}")
            print(f"Account Currency: {user_details.get('account_currency', 'N/A')}")
            print(f"Current Balance: {user_account['balance']:.2f} {user_details.get('account_currency', 'N/A')}")
            
            # Display other details
            for key, value in user_details.items():
                if key not in ['account_number', 'account_type_name', 'account_type_features', 'security_questions',
                               'payment_methods', 'payment_passcode', 'statements', 'cards', 'card_pins',
                               'beneficiaries', 'loan_limit', 'active_loans', 'account_currency',
                               'monthly_deposits_expected', 'monthly_withdrawals_expected', 'monthly_balance_expected',
                               'last_loan_limit_update']: # Avoid re-printing nested dicts or already displayed info
                    print(f"{key.replace('_', ' ').title()}: {value}")
            
            # Display account features if available
            if 'account_type_features' in user_details and user_details['account_type_features']:
                print("\n--- Account Features ---")
                for key, value in user_details['account_type_features'].items():
                    if key not in ["Account Name", "Currency"]: # Already displayed
                        print(f"  - {key.replace('_', ' ').title()}: {value}")
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
        elif service_choice == 5: # My Statements
            view_my_statements(current_username)
        elif service_choice == 6: # Add/Manage Payment Methods
            while True: # Loop for managing payment methods
                display_payment_methods_menu()
                payment_method_choice = get_user_input("Enter your choice: ", int)
                if payment_method_choice == 'M': return 'M'
                if payment_method_choice == 'P': break # Go back to account services
                if payment_method_choice is None: return None

                if 1 <= payment_method_choice <= 5: # Add payment method
                    result = add_payment_method(current_username, payment_method_choice)
                    if result is None: return None # Critical exit
                elif payment_method_choice == 6: # Set/Change Payment Passcode
                    result = set_payment_passcode(current_username)
                    if result is None: return None # Critical exit
                elif payment_method_choice == 7: # View My Payment Methods
                    view_payment_methods(current_username)
                else:
                    print(f"{RED_X} Invalid choice for payment methods.")
                    input("Press Enter to continue...")
            continue # Stay in account services after managing payment methods
        elif service_choice == 7: # Manage Cards (placeholder for now)
            print(f"{BLUE_INFO} Card management features are under development.")
            input("Press Enter to continue...")
        elif service_choice == 8: # Request Services (placeholder for now)
            print(f"{BLUE_INFO} General service requests are under development.")
            input("Press Enter to continue...")
        elif service_choice == 9: # Make Payments (Transfers to external methods)
            result = make_payment(current_username)
            if result == 'M': return 'M'
            if result == 'P': continue
            if result is None: return None
        elif service_choice == 10: # Check Loan Balance/Limit & Request Loan
            update_loan_limit(current_username) # Update loan limit before displaying
            accounts_data = read_accounts()
            user_details = accounts_data[current_username]["details"]
            loan_limit = user_details.get("loan_limit", 0.0)
            active_loans = user_details.get("active_loans", 0.0)
            account_currency = user_details["account_currency"]

            print(f"\n--- Loan Information ---")
            print(f"Your Loan Limit: {loan_limit:,.2f} {account_currency}")
            print(f"Active Loans: {active_loans:,.2f} {account_currency}")
            print(f"Available Loan: {(loan_limit - active_loans):,.2f} {account_currency}")
            
            loan_action = get_user_input("Do you want to request a loan? (yes/no): ").lower()
            if loan_action == 'M': return 'M'
            if loan_action == 'P': continue
            if loan_action is None: return None
            
            if loan_action == 'yes':
                result = request_loan(current_username)
                if result == 'M': return 'M'
                if result == 'P': continue
                if result is None: return None
            else:
                input("Press Enter to continue...")

        elif service_choice == 11: # Logout
            return "logout" # Signal to the calling function to log out
        else:
            print(f"{RED_X} Invalid choice. Please enter a number between 1 and 11.")
            input("Press Enter to continue...")

# --- Main Application Loop ---

def run_banking_app():
    """Manages the main flow of the banking application."""
    current_username = None # Stores the username of the currently logged-in user

    print(f"{GREEN_CHECKMARK} Welcome to {BANK_NAME} - {BANK_TAGLINE} {GREEN_CHECKMARK}")

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
                    # Ensure account is marked activated if it had 0 opening balance
                    if not accounts_data[username]["details"].get("account_type_features", {}).get("Opening balance", 0) > 0:
                        accounts_data[username]["activated"] = True
                        save_accounts(accounts_data)

                else:
                    print(f"{RED_X} Invalid username or password. Please try again.")
                input("Press Enter to continue...")
            elif choice == 4: # Exit program
                print("\nThank you for using the Python Bank Simulation. Goodbye!")
                break
            else:
                print(f"{RED_X} Invalid choice. Please enter 1, 2, 3, or 4.")
                input("Press Enter to continue...")
        else: # Logged in
            if choice == 1: # Account Services
                result = handle_account_services_flow(current_username)
                if result == "logout":
                    current_username = None
                elif result is None:
                    break
            elif choice == 2: # Explore our offers
                result = handle_offers_flow()
                if result is None: break
                if result == 'M': continue
            elif choice == 3: # Logout
                print(f"\nLogging out {current_username}. Returning to main menu.")
                current_username = None # Set to None to exit this loop and re-enter login loop
                input("Press Enter to continue...")
            elif choice == 4: # Exit Application
                print("\nThank you for using the Python Bank Simulation. Goodbye!")
                break
            else:
                print(f"{RED_X} Invalid choice. Please enter 1, 2, 3, or 4.")
                input("Press Enter to continue...")

# --- Main Execution Block ---

if __name__ == "__main__":
    random.seed() # Seed the random number generator
    # Optional: uncomment to delete all data on each run for fresh start
    # delete_all_data() 
    run_banking_app()