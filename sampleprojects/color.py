import os
import json
import datetime
import random
import re
import time # For simulating delays

# --- Global Constants and Configuration ---
BANK_NAME = "La Familia Bank"
BANK_TAGLINE = "Your Trusted Digital Financial Partner"
DATA_DIR = "bank_data"
ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")
EMAIL_INBOX_FILE = os.path.join(DATA_DIR, "email_inbox.txt")
SMS_LOG_FILE = os.path.join(DATA_DIR, "sms_log.txt")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Ensure inbox files exist inside the DATA_DIR
if not os.path.exists(EMAIL_INBOX_FILE):
    with open(EMAIL_INBOX_FILE, 'w') as f:
        pass # Create an empty email inbox file
if not os.path.exists(SMS_LOG_FILE):
    with open(SMS_LOG_FILE, 'w') as f:
        pass # Create an empty SMS log file

OUR_BRANCHES = [
    "La Familia Bank Head Office Branch (Nairobi)",
    "La Familia Bank Mombasa Branch",
    "La Familia Bank Kisumu Branch",
    "La Familia Bank Nakuru Branch",
    "La Familia BankEldoret Branch",
    "La Familia Bank Thika Branch"
]

SECURITY_QUESTIONS = {
    1: "What is your mother's maiden name?",
    2: "What was the name of your first pet?",
    3: "What is your favorite book?",
    4: "What high school did you attend?",
    5: "What is your favorite movie?",
    6: "In what city were you born?"
}

# Choices for various inputs
NATIONALITY_CHOICES = {
    1: "Kenyan",
    2: "Ugandan",
    3: "Tanzanian",
    4: "USA",
    5: "England",
    6: "Germany",
    7: "Other"
}

REASON_CHOICES = {
    1: "Savings",
    2: "Personal Transactions",
    3: "Business Transactions",
    4: "Overseas Transactions",
    5: "Other"
}

OCCUPATION_CHOICES = {
    1: "Student",
    2: "Employed",
    3: "Self-Employed",
    4: "Unemployed",
    5: "Retired",
    6: "Other"
}

SOURCE_OF_INCOME_CHOICES = {
    1: "Salary",
    2: "Business Profits",
    3: "Investments",
    4: "Freelance",
    5: "Pension",
    6: "Remittances",
    7: "Other"
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
ITALIC = "\033[3m" # Added for italic tagline
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m" # Added for completeness as it was defined, though not used much
WHITE = "\033[37m" # Added for completeness as it was defined, though not used much

# Bright Text Colors
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Background Colors
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Bright Background Colors
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"


GREEN_CHECKMARK = f"{GREEN}\u2713{RESET}" # Green checkmark
RED_X = f"{RED}\u2717{RESET}"             # Red X
BLUE_INFO = f"{BLUE}i{RESET}"             # Blue info icon

# Regex to strip ANSI escape codes for accurate length calculation
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def get_visible_length(s):
    """Returns the visible length of a string, stripping ANSI escape codes."""
    return len(ANSI_ESCAPE.sub('', s))

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
            # Use BRIGHT_BLACK for faint prompt, CYAN for the prompt itself
            user_input = input(f"{BRIGHT_BLACK}{CYAN}{prompt}{RESET}").strip()
            if user_input.upper() == 'P':
                return 'P'
            if user_input.upper() == 'M':
                return 'M'
            if not user_input: # Handle empty input for optional fields or re-prompt
                if type == str: # Allow empty string for string types if not critical
                    return ""
                print(f"{RED_X} Input cannot be empty. Please try again.{RESET}")
                continue
            return type(user_input)
        except ValueError:
            print(f"{RED_X} Invalid input. Please enter data of type {type.__name__}.{RESET}")
        except EOFError:
            print(f"{RED_X} End of input reached. Exiting gracefully.{RESET}")
            return None
        except Exception as e:
            print(f"{RED_X} An unexpected error occurred: {e}{RESET}")
            return None

def get_choice_input(prompt_header, choices_dict):
    """
    Presents a list of choices to the user and gets their selection.
    Allows for 'Other' option to input custom text.
    Args:
        prompt_header (str): The header/question to display before choices.
        choices_dict (dict): A dictionary mapping numbers to choice strings.
                              Should include an 'Other' option if custom input is desired.
    Returns:
        str: The selected choice string, or custom input, or 'P'/'M' or None.
    """
    while True:
        print(f"\n{BLUE}{prompt_header}{RESET}")
        for key, value in choices_dict.items():
            print(f"{GREEN}{key}. {value}{RESET}")
        print(f"{YELLOW}P. Go back to previous menu{RESET}")
        print(f"{YELLOW}M. Go to main menu{RESET}")

        choice = get_user_input("Enter your choice (number): ", type=str) # Read as string to handle 'Other'
        if choice in ['P', 'M', None]:
            return choice

        try:
            choice_int = int(choice)
            if choice_int in choices_dict:
                selected_value = choices_dict[choice_int]
                if selected_value == "Other":
                    custom_input = get_user_input(f"Please specify your {prompt_header.lower().replace('select your ', '').replace(':', '')}: ")
                    if custom_input in ['P', 'M', None]:
                        return custom_input
                    return custom_input
                return selected_value
            else:
                print(f"{RED_X} Invalid choice. Please select a number from the list.{RESET}")
        except ValueError:
            print(f"{RED_X} Invalid input. Please enter a number.{RESET}")

def is_valid_email(email):
    """Basic validation for email format."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_kra_pin(pin):
    """Validates KRA PIN format: Capital letter, 9 digits, Capital letter."""
    return re.match(r"^[A-Z]\d{9}[A-Z]$", pin)

def generate_otp(length=6): # Changed default length to 6
    """Generates a random numeric OTP of specified length (defaulting to 6)."""
    return ''.join(random.choices('0123456789', k=length))

def generate_reference_number():
    """Generates a unique transaction reference number."""
    return f"TRX-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"

def strip_ansi_codes(s):
    """Strips ANSI escape codes from a string."""
    return re.sub(r'\x1b\[[0-9;]*m', '', s)

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
        if from_currency in ["BTC", "ETH", "SOL"]:
            amount_in_usd = amount * EXCHANGE_RATES[from_currency]["USD"]
            if to_currency == "USD":
                return amount_in_usd
            else:
                return amount_in_usd * EXCHANGE_RATES["USD"][to_currency]
        
        if to_currency in ["BTC", "ETH", "SOL"]:
            amount_in_usd = amount * EXCHANGE_RATES[from_currency]["USD"]
            return amount_in_usd / EXCHANGE_RATES[to_currency]["USD"] # Inverted for USD to Crypto

        # For fiat-to-fiat, if direct path not found, go via USD
        if from_currency != "USD" and to_currency != "USD":
            amount_in_usd = amount * EXCHANGE_RATES[from_currency]["USD"]
            return amount_in_usd * EXCHANGE_RATES["USD"][to_currency]

        raise ValueError("Conversion path not found.")

    except KeyError:
        print(f"{RED_X} Error: Exchange rate not found for {from_currency} to {to_currency}.{RESET}")
        return None
    except Exception as e:
        print(f"{RED_X} An error occurred during currency conversion: {e}{RESET}")
        return None


# --- Email and SMS Simulation ---

def _log_communication(log_file, sender, recipient, subject, body):
    """Helper to log emails/SMS to a file."""
    try:
        with open(log_file, 'a') as f:
            f.write(f"--- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            f.write(f"From: {sender}\n")
            f.write(f"To: {recipient}\n")
            if subject:
                f.write(f"Subject: {subject}\n")
            # Strip ANSI codes for file output
            f.write(f"Body:\n{strip_ansi_codes(body)}\n")
            f.write("-" * 30 + "\n\n")
    except IOError as e:
        print(f"{RED_X} ERROR: Could not write to communication log file '{log_file}'. Check permissions or path: {e}{RESET}")
    except Exception as e:
        print(f"{RED_X} An unexpected error occurred during communication logging: {e}{RESET}")


def send_otp_email(name, email, otp, expiry_time):
    """Simulates sending an OTP email."""
    sender = f"noreply@{BANK_NAME.lower().replace(' ', '')}.com"
    subject = f"{BANK_NAME} OTP Verification"
    # The body string contains ANSI escape codes for terminal output
    body = (
        f"Dear {name},\n\n"
        f"Your One-Time Passcode (OTP) for {BANK_NAME} is: {BOLD}{otp}{RESET}\n\n"
        f"This OTP is valid for 5 minutes and will expire at {expiry_time.strftime('%H:%M:%S')}.\n"
        f"Please do not share this code with anyone.\n\n"
        f"Thank you,\n"
        f"The {BANK_NAME} Team."
    )
    _log_communication(EMAIL_INBOX_FILE, sender, email, subject, body)
    print(f"{GREEN_CHECKMARK} OTP email sent to {email}. Check your simulated inbox ({EMAIL_INBOX_FILE}).{RESET}")
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
    print(f"{GREEN_CHECKMARK} Payment OTP SMS sent to {phone_number}. Check your simulated SMS log ({SMS_LOG_FILE}).{RESET}")
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
        body += f"   Answer: {a}\n" # In a real system, answers would be hashed.
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
        f"   Account Number: {account_number}\n"
        f"   Account Type: {account_type_details.get('Account Name', 'N/A')}\n"
        f"   Currency: {account_type_details.get('Currency', 'N/A')}\n"
        f"   Branch: {branch_name}\n\n"
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
    print(f"{GREEN_CHECKMARK} Transaction notification sent to {email} and {phone_number}.{RESET}")

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
    print(f"{GREEN_CHECKMARK} Loan disbursement notification sent to {email} and {phone_number}.{RESET}")

# --- NEW OTP VERIFICATION FUNCTION ---
def verify_otp_with_retries(target_name, contact_info, generated_otp, otp_expiry_time, max_retries=3, otp_delivery_method="email"):
    """
    Verifies an OTP, allowing a specified number of retries for incorrect input.

    Args:
        target_name (str): The name of the customer/recipient.
        contact_info (str): The email address or phone number the OTP was sent to.
        generated_otp (str): The actual OTP that was sent.
        otp_expiry_time (datetime.datetime): When the OTP expires.
        max_retries (int): Maximum number of attempts allowed.
        otp_delivery_method (str): "email" or "sms" to differentiate messages (optional).

    Returns:
        bool: True if OTP is successfully verified, False otherwise (expired or too many wrong attempts).
        str: 'P' or 'M' if user selects those options.
    """
    attempts = 0
    while attempts < max_retries:
        if datetime.datetime.now() > otp_expiry_time:
            print(f"{RED_X} OTP has expired. Please request a new OTP.{RESET}")
            return False # OTP expired, verification failed

        prompt = f"Enter the {otp_delivery_method} OTP (a {len(generated_otp)}-digit code, {max_retries - attempts} attempts left, P/M to go back): "
        user_otp = get_user_input(prompt, type=str) # OTPs are strings

        if user_otp in ['P', 'M']:
            return user_otp # User wants to go back or to main menu

        # Validate that the user_otp is digits only and has correct length
        if not user_otp.isdigit() or len(user_otp) != len(generated_otp):
            print(f"{RED_X} Invalid OTP format. Please enter a {len(generated_otp)}-digit number.{RESET}")
            attempts += 1 # Count as an attempt even if format is wrong
            continue # Continue to the next loop iteration

        if user_otp == generated_otp:
            print(f"{GREEN_CHECKMARK} OTP verified successfully!{RESET}")
            return True # OTP is correct
        else:
            attempts += 1
            if attempts < max_retries:
                print(f"{RED_X} Incorrect OTP. Please try again.{RESET}")
            else:
                print(f"{RED_X} Too many incorrect OTP attempts. For security, the verification process has been cancelled.{RESET}")
                print(f"{BLUE_INFO} Please restart the process or contact support if you need assistance.{RESET}")
                return False # Too many wrong attempts, verification failed

    return False # Fallback, should ideally be caught by max_retries check


# --- Placeholder Function for New Account Registration ---
def register_new_account():
    clear_screen()
    print(f"{BOLD}{BLUE_INFO}--- New Account Registration ---{RESET}")

    customer_name = get_user_input("Enter your full name (P/M to go back): ")
    if customer_name in ['P', 'M']: return customer_name
    if customer_name is None: return None

    customer_email = get_user_input("Enter your email address: ")
    if customer_email in ['P', 'M']: return customer_email
    if customer_email is None: return None
    if not is_valid_email(customer_email):
        print(f"{RED_X} Invalid email format. Please enter a valid email address.{RESET}")
        time.sleep(2)
        return False # Indicate failure, user can try again from main menu

    customer_phone = get_user_input("Enter your phone number (e.g., +254...): ")
    if customer_phone in ['P', 'M']: return customer_phone
    if customer_phone is None: return None
    # Add phone number validation if needed

    # --- OTP Sending and Verification ---
    print(f"\n{BLUE_INFO} Sending 6-digit OTP to {customer_email} for verification...{RESET}")
    otp_code = generate_otp(length=6) # Changed to 6 digits
    otp_expiry = datetime.datetime.now() + datetime.timedelta(minutes=5)

    # For testing, display the OTP (REMOVE IN REAL APP)
    print(f"{YELLOW}DEBUG: The generated OTP is: {otp_code}{RESET}")
    send_otp_email(customer_name, customer_email, otp_code, otp_expiry)

    otp_verified = verify_otp_with_retries(
        target_name=customer_name,
        contact_info=customer_email,
        generated_otp=otp_code,
        otp_expiry_time=otp_expiry,
        max_retries=3, # User gets 3 attempts
        otp_delivery_method="email"
    )

    if otp_verified == True:
        print(f"\n{GREEN_CHECKMARK} OTP successfully verified. Proceeding with account setup...{RESET}")
        # In a real system, you would now collect more details (password, account type, etc.)
        # and then call send_account_activation_email and send_activation_sms
        # For this example, we'll just simulate completion:
        print(f"{GREEN_CHECKMARK} Account registration process complete! (conceptually){RESET}")
        time.sleep(2)
        return True # Indicate successful registration completion
    elif otp_verified in ['P', 'M']:
        print(f"{BLUE_INFO} OTP verification cancelled. Returning to previous menu.{RESET}")
        time.sleep(2)
        return otp_verified # Propagate 'P' or 'M'
    else: # otp_verified is False (expired or too many failed attempts)
        print(f"{RED_X} Account registration aborted due to OTP verification failure.{RESET}")
        time.sleep(2)
        return False # Indicate failure


# --- Main Application Loop ---
def main():
    while True:
        clear_screen()
        # Changed from \033[33m to YELLOW for consistency
        print(f"{YELLOW}{BOLD}=\033[0m" * 50) # Top border
        # Changed from \033[34m to BLUE for consistency
        print(f"{BOLD}{BLUE}--- {BANK_NAME} Main Menu ---{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
        # Changed from \033[33m to YELLOW for consistency
        print(f"{YELLOW}{BOLD}=\033[0m" * 50) # Bottom border
        # Changed from \033[34m to BLUE for consistency
        print(f"{ITALIC}{BLUE}{BANK_TAGLINE}{RESET}\n") # Italic blue tagline

        # Changed from \033[32m to GREEN for consistency
        print(f"{GREEN}1. Register New Account{RESET}") # Green text
        print(f"{GREEN}2. Login{RESET}") # Green text - Updated to reflect it's functional
        print(f"{GREEN}3. Delete All Data (For Testing){RESET}") # Green text
        print(f"{GREEN}4. Exit{RESET}") # Green text
        # Changed from \033[33m to YELLOW for consistency
        print(f"{YELLOW}-" * 30 + f"{RESET}") # Yellow separator

        # Changed from \033[90m to BRIGHT_BLACK for consistency
        choice = get_user_input(f"{BRIGHT_BLACK}Enter your choice: {RESET}", int) # Faint input prompt

        if choice == 1:
            reg_status = register_new_account()
            # Changed from \033[90m to BRIGHT_BLACK for consistency
            get_user_input(f"\n{BRIGHT_BLACK}Press Enter to continue to Main Menu...{RESET}") # Faint input prompt
            continue
        elif choice == 2:
            # Login functionality:
            username = get_user_input("Enter your username: ").strip()
            if username == 'M' or username == 'P': continue
            if username is None: break # Exit application

            password = get_user_input("Enter your password: ").strip()
            if password == 'M' or password == 'P': continue
            if password is None: break # Exit application
            
            accounts_data = read_accounts()
            if username in accounts_data and accounts_data[username]["password"] == password:
                print(f"\n{GREEN_CHECKMARK} Login successful! Welcome, {username}!{RESET}")
                current_username = username
                # Ensure account is marked activated if it had 0 opening balance and wasn't activated yet
                if not accounts_data[username]["details"].get("account_type_features", {}).get("Opening balance", 0) > 0 and not accounts_data[username].get("activated", False):
                    accounts_data[username]["activated"] = True
                    save_accounts(accounts_data)
                
                # Display logged-in user details
                now = datetime.datetime.now()
                if now.hour < 12:
                    greeting = "Good morning"
                elif 12 <= now.hour < 18:
                    greeting = "Good afternoon"
                else:
                    greeting = "Good evening"
                
                surname = accounts_data[current_username]["details"].get("name", "User").split()[-1]

                clear_screen() # Clear screen before displaying greeting
                print(f"{GREEN}{greeting} {surname},{RESET}")
                
                # Center Bank Name
                bank_name_display = f"{BOLD}{BLUE}{BANK_NAME}{RESET}"
                bank_name_padded = bank_name_display.center(len(bank_name_display) + (50 - len(strip_ansi_codes(bank_name_display))))
                print(bank_name_padded)

                # Center Tagline
                tagline_display = f"{ITALIC}{BLUE}{BANK_TAGLINE}{RESET}"
                tagline_padded = tagline_display.center(len(tagline_display) + (50 - len(strip_ansi_codes(tagline_display))))
                print(tagline_padded)

                user_details = accounts_data[current_username]["details"]
                account_number = user_details.get("account_number", "N/A")
                current_balance = accounts_data[current_username]["balance"]
                account_currency = user_details.get("account_currency", "KES")

                print(f"\n{BLUE}Account Number:{RESET} {account_number}")
                print(f"{BLUE}Available Balance:{RESET} {current_balance:,.2f} {account_currency}".ljust(50))
                print(f"{BLUE}Current Balance:  {RESET} {current_balance:,.2f} {account_currency}".ljust(50)) # For simplicity, current and available are same

                input(f"\n{BRIGHT_BLACK}Press Enter to continue to Account Services...{RESET}")
            else:
                print(f"{RED_X} Invalid username or password. Please try again.{RESET}")
                input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        elif choice == 3:
            # Changed from \033[31m\u2717\033[0m to RED_X for consistency
            print(f"{RED_X} Delete All Data (For Testing)...{RESET}") # Red X symbol
            delete_all_data()
            # Changed from \033[90m to BRIGHT_BLACK for consistency
            get_user_input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}") # Faint input prompt
        elif choice == 4:
            # Changed from \033[34mi\033[0m to BLUE_INFO for consistency
            print(f"{BLUE_INFO} Thank you for choosing {BANK_NAME}. Goodbye!{RESET}") # Blue info symbol
            break
        else:
            # Changed from \033[31m\u2717\033[0m to RED_X for consistency
            print(f"{RED_X} Invalid choice. Please enter 1, 2, 3, or 4.{RESET}") # Red X symbol
            time.sleep(2)


def display_main_menu(logged_in):
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}{BANK_NAME} - {BANK_TAGLINE}{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    if logged_in:
        # Changed from \033[32m to GREEN for consistency
        print(f"{GREEN}1. Account Services{RESET}") # Green text
        print(f"{GREEN}2. Explore Our Offers{RESET}") # Green text
        print(f"{GREEN}3. Logout{RESET}") # Green text
        print(f"{GREEN}4. Exit Application{RESET}") # Green text
    else:
        print(f"{GREEN}1. Open a Bank Account{RESET}") # Green text
        print(f"{GREEN}2. Explore Our Offers{RESET}") # Green text
        print(f"{GREEN}3. Login{RESET}") # Green text
        print(f"{GREEN}4. Exit Application{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_account_opening_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}Open a Bank Account{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[32m to GREEN for consistency
    print(f"{GREEN}1. Apply Online (Receive application form via email){RESET}") # Green text
    print(f"{GREEN}2. Visit Nearest Bank Branch (Get a token for in-person service){RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}P. Go back to previous menu{RESET}") # Yellow text
    print(f"{YELLOW}M. Go to main menu{RESET}") # Yellow text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_offers_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}Explore Our Offers{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[32m to GREEN for consistency
    print(f"{GREEN}1. Bank Accounts{RESET}") # Green text
    print(f"{GREEN}2. Our Cards{RESET}") # Green text
    print(f"{GREEN}3. ATM Locator{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}P. Go back to previous menu{RESET}") # Yellow text
    print(f"{YELLOW}M. Go to main menu{RESET}") # Yellow text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_bank_accounts_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}Bank Accounts{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[32m to GREEN for consistency
    print(f"{GREEN}1. Current Bank Account{RESET}") # Green text
    print(f"{GREEN}2. Club Account{RESET}") # Green text
    print(f"{GREEN}3. PayGo Account{RESET}") # Green text
    print(f"{GREEN}4. Sapphire Multi Currency Account{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}P. Go back to previous menu{RESET}") # Yellow text
    print(f"{YELLOW}M. Go to main menu{RESET}") # Yellow text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_cards_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}Our Cards{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[32m to GREEN for consistency
    print(f"{GREEN}1. Debit Cards{RESET}") # Green text
    print(f"{GREEN}2. Prepaid Cards{RESET}") # Green text
    print(f"{GREEN}3. Credit Cards{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}P. Go back to previous menu{RESET}") # Yellow text
    print(f"{YELLOW}M. Go to main menu{RESET}") # Yellow text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_debit_cards():
    clear_screen()
    # Using BG_BLUE and BRIGHT_WHITE for header consistency with cards.py example
    print(f"\n{BOLD}{BG_BLUE}{BRIGHT_WHITE}--- Debit Cards Available for Inquiry ---{RESET}")
    print(f"{BRIGHT_CYAN}1. {BOLD}Club Debit MasterCard{RESET}")
    print(f"{BRIGHT_CYAN}2. {BOLD}Debit Visa{RESET}")
    print(f"{BRIGHT_CYAN}3. {BOLD}Gold MasterCard{RESET}")
    print(f"{BOLD}{BG_BLUE}{BRIGHT_WHITE}-----------------------------------------{RESET}")

def display_prepaid_cards():
    clear_screen()
    print(f"\n{BOLD}{BG_BLUE}{BRIGHT_WHITE}--- Prepaid Cards Available for Inquiry ---{RESET}")
    print(f"{BRIGHT_CYAN}1. {BOLD}Multi Currency Prepaid MasterCard{RESET}")
    print(f"{BRIGHT_CYAN}2. {BOLD}Sapphire Prepaid Visa{RESET}")
    print(f"{BRIGHT_CYAN}3. {BOLD}Safari Prepaid Visa{RESET}")
    print(f"{BOLD}{BG_BLUE}{BRIGHT_WHITE}-------------------------------------------{RESET}")

def display_credit_cards():
    clear_screen()
    print(f"\n{BOLD}{BG_BLUE}{BRIGHT_WHITE}--- Credit Cards Available for Inquiry ---{RESET}")
    print(f"{BRIGHT_CYAN}1. {BOLD}Gold Visa Credit Card{RESET}")
    print(f"{BRIGHT_CYAN}2. {BOLD}Bronze Credit MasterCard{RESET}")
    print(f"{BRIGHT_CYAN}3. {BOLD}Diamond Credit Card{RESET}")
    print(f"{BOLD}{BG_BLUE}{BRIGHT_WHITE}------------------------------------------{RESET}")

def get_card_details_by_id(card_type, specific_card):
    """
    Retrieves the details of a selected card type or a specific card without displaying.
    Args:
        card_type (int): The card type (1: Debit, 2: Prepaid, 3: Credit).
        specific_card (int, optional): The specific card selected by the user.
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
    return details

def _print_card_details_info_display(details):
    """Helper function to display formatted card details."""
    if details:
        print(f"\n{BOLD}{BLUE}--- {details['Card Name']} Overview ---{RESET}")
        for key, value in details.items():
            if key != "Card Name":
                print(f"{BLUE}{key.replace('_', ' ').title()}:{RESET} {value}")
    else:
        print(f"{RED_X} Card details not found.{RESET}")

def display_card_details_info(card_type, specific_card=None):
    """
    Retrieves and displays the details of a selected card type or a specific card.
    Args:
        card_type (int): The card type (1: Debit, 2: Prepaid, 3: Credit).
        specific_card (int, optional): The specific card selected by the user.
                                        Defaults to None.
    Returns:
        dict: A dictionary of card details, or None if invalid.
    """
    details = get_card_details_by_id(card_type, specific_card)
    _print_card_details_info_display(details)
    return details

def display_token_machine_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}Select Service{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[32m to GREEN for consistency
    print(f"{GREEN}1. Open a New Bank Account{RESET}") # Green text
    print(f"{GREEN}2. Close a Bank Account{RESET}") # Green text
    print(f"{GREEN}3. Reactivate A Bank Account{RESET}") # Green text
    print(f"{GREEN}4. Statement Enquiry{RESET}") # Green text
    print(f"{GREEN}5. Cheque Book{RESET}") # Green text
    print(f"{GREEN}6. Cheque Deposit{RESET}") # Green text
    print(f"{GREEN}7. Cash Withdrawal{RESET}") # Green text
    print(f"{GREEN}8. Cash Deposit{RESET}") # Green text
    print(f"{GREEN}9. Currency Conversion{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}P. Go back to previous menu{RESET}") # Yellow text
    print(f"{YELLOW}M. Go to main menu{RESET}") # Yellow text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_atm_locations_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}ATM Locations{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    for i, branch_name in enumerate(OUR_BRANCHES, 1):
        # Changed from \033[32m to GREEN for consistency
        print(f"{GREEN}{i}. {branch_name}{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}P. Go back to previous menu{RESET}") # Yellow text
    print(f"{YELLOW}M. Go to main menu{RESET}") # Yellow text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_account_services_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}Account Services{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[32m to GREEN for consistency
    print(f"{GREEN}1. View Account Details{RESET}") # Green text
    print(f"{GREEN}2. Make a Deposit{RESET}") # Green text
    print(f"{GREEN}3. Make a Withdrawal{RESET}") # Green text
    print(f"{GREEN}4. View Transaction History{RESET}") # Green text
    print(f"{GREEN}5. My Statements{RESET}") # Green text
    print(f"{GREEN}6. Add/Manage Payment Methods{RESET}") # Green text
    print(f"{GREEN}7. Manage Cards{RESET}") # Green text
    print(f"{GREEN}8. Request Services{RESET}") # Green text
    print(f"{GREEN}9. Make Payments (Transfers to external methods){RESET}") # Green text
    print(f"{GREEN}10. Check Loan Balance/Limit & Request Loan{RESET}") # Green text
    print(f"{GREEN}11. Logout{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_payment_methods_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}Add/Manage Payment Methods{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[32m to GREEN for consistency
    print(f"{GREEN}1. Add M-Pesa{RESET}") # Green text
    print(f"{GREEN}2. Add Airtel Money{RESET}") # Green text
    print(f"{GREEN}3. Add Bank Transfer{RESET}") # Green text
    print(f"{GREEN}4. Add PayPal{RESET}") # Green text
    print(f"{GREEN}5. Add Crypto Wallet (Bitcoin, Ethereum, Solana, incl. exchanges){RESET}") # Green text
    print(f"{GREEN}6. Set/Change Payment Passcode{RESET}") # Green text
    print(f"{GREEN}7. View My Payment Methods{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}P. Go back to previous menu{RESET}") # Yellow text
    print(f"{YELLOW}M. Go to main menu{RESET}") # Yellow text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_token(service_choice):
    clear_screen()
    service_name = get_service_name(service_choice)
    token_number = random.randint(100, 999)
    # Changed from \033[1m\033[36m to BOLD and CYAN for consistency
    print(f"{BOLD}{CYAN}----------------------------------------{RESET}") # Bold Cyan separator
    print(f"{BOLD}{CYAN}|        {BANK_NAME} Token          |{RESET}") # Bold Cyan Bank Name
    print(f"{BOLD}{CYAN}----------------------------------------{RESET}") # Bold Cyan separator
    # Changed from \033[34m to BLUE for consistency
    print(f"{BLUE}Service:{RESET} {service_name}") # Blue label
    print(f"{BLUE}Token Number:{RESET} {token_number}") # Blue label
    print(f"{BLUE}Date:{RESET} {datetime.date.today().strftime('%Y-%m-%d')}") # Blue label
    print(f"{BLUE}Time:{RESET} {datetime.datetime.now().strftime('%H:%M:%S')}") # Blue label
    # Changed from \033[34mi\033[0m to BLUE_INFO for consistency
    print(f"\n{BLUE_INFO} Please wait for your turn. Requirements for {service_name}:\n{RESET}") # Blue info symbol
    if service_choice == 1:
        # Changed from \033[32m to GREEN for consistency
        print(f"{GREEN}- National ID/Passport{RESET}") # Green requirements
        print(f"{GREEN}- KRA PIN Certificate{RESET}")
        print(f"{GREEN}- Recent Utility Bill (Proof of Address){RESET}")
    elif service_choice in [2, 3]:
        print(f"{GREEN}- National ID/Passport{RESET}")
        print(f"{GREEN}- Account details/documents{RESET}")
    elif service_choice in [4, 5, 6, 7, 8, 9]:
        print(f"{GREEN}- National ID/Passport{RESET}")
        print(f"{GREEN}- Relevant account information{RESET}")
    # Changed from \033[1m\033[36m to BOLD and CYAN for consistency
    print(f"{BOLD}{CYAN}----------------------------------------{RESET}") # Bold Cyan separator
    # Changed from \033[90m to BRIGHT_BLACK for consistency
    input(f"\n{BRIGHT_BLACK}Press Enter to take your token...{RESET}") # Faint input prompt

def get_service_name(choice):
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
        # Use BOLD and BLUE for the section header
        print(f"\n{BOLD}{BLUE}--- {details['Account Name']} Overview ---{RESET}")
        for key, value in details.items():
            if key != "Account Name":
                # Use BLUE for keys, default for values
                print(f"{BLUE}{key.replace('_', ' ').title()}:{RESET} {value}")
    else:
        # Use RED_X for error
        print(f"{RED_X} Invalid account type.{RESET}")
    return details

# --- NEW CARD DISPLAY AND GENERATION FUNCTIONS (from cards.py) ---
def display_bank_card(card_holder_name, bank_name, card_number, exp_date, cvv, card_type_name="Generic Card", currency_symbol="CUR", card_status="active"):
    """
    Displays a stylized ASCII art representation of a bank card with details.
    Includes card status.
    """
    clear_screen()
    print(f"\n{BOLD}{BG_MAGENTA}{BRIGHT_WHITE}--- Your {card_type_name} ---{RESET}\n")

    # Define card dimensions
    card_width = 46
    card_inner_width = card_width - 2

    # Drawing characters for the frame
    BORDER_CHAR = '*'
    DIVIDER_CHAR = '-'
    DETAILS_LINE_CHAR = ';'

    # Colors for text content
    text_color = BRIGHT_WHITE
    label_color = BRIGHT_BLACK

    # Prepare card details with styling
    styled_bank_name = f"{BOLD}{text_color}{bank_name.upper()}{RESET}"

    # Card Number: Masked, showing only last 4 digits
    masked_card_number = f"**** **** **** {card_number[-4:]}"
    styled_card_number = f"{BOLD}{text_color}{masked_card_number}{RESET}"

    # Valid Thru styling
    valid_thru_label_styled = f"{ITALIC}{label_color}VALID THRU{RESET}"
    styled_exp_date = f"{BOLD}{text_color}{exp_date}{RESET}"
    
    styled_name = f"{BOLD}{text_color}{card_holder_name.upper()}{RESET}"

    # CVV (always masked for display)
    styled_cvv = f"{BOLD}{text_color}CVV: {RESET}{BOLD}{text_color}***{RESET}"

    # Status display
    status_text = f"Status: {card_status.upper()}"
    status_color = GREEN if card_status.lower() == 'active' else RED
    styled_status = f"{BOLD}{status_color}{status_text}{RESET}"

    # Simplified Mastercard Logo for embedding (using ANSI colors for blocks)
    mc_logo_red = BG_RED + " "
    mc_logo_yellow = BG_YELLOW + " "
    mc_logo_overlap = BG_BRIGHT_YELLOW + " "
    mc_logo_string = f"{mc_logo_red}{mc_logo_overlap}{mc_logo_yellow}{RESET}"
    mc_logo_visible_width = get_visible_length(mc_logo_string)

    # --- Card Construction ---

    # Top Border
    print(f"{BORDER_CHAR * card_width}{RESET}")

    # Line 1: Bank Name
    bank_name_indent = 2
    bank_name_max_len = card_inner_width - bank_name_indent - 1
    bank_name_display = styled_bank_name
    if get_visible_length(bank_name_display) > bank_name_max_len:
        bank_name_display = bank_name_display[:bank_name_max_len - 3] + "..." + RESET
    bank_name_fill_len = card_inner_width - get_visible_length(bank_name_display) - bank_name_indent
    print(
        f"{BORDER_CHAR}"
        f"{' ' * bank_name_indent}"
        f"{bank_name_display}"
        f"{DETAILS_LINE_CHAR * max(0, bank_name_fill_len)}"
        f"{BORDER_CHAR}{RESET}"
    )

    # Line 2: Card Type Name & Currency
    card_type_info = f"{BOLD}{text_color}{card_type_name}{RESET} ({CYAN}{currency_symbol}{RESET})"
    card_type_indent = 2
    card_type_content_len = get_visible_length(card_type_info)
    card_type_padding = card_inner_width - card_type_content_len - card_type_indent
    print(f"{BORDER_CHAR}{' ' * card_type_indent}{card_type_info}{' ' * card_type_padding}{BORDER_CHAR}{RESET}")


    # Line 3: Account Number
    account_num_indent = 2
    account_num_content_len = get_visible_length(styled_card_number)
    account_num_padding = card_inner_width - account_num_content_len - account_num_indent
    print(f"{BORDER_CHAR}{' ' * account_num_indent}{styled_card_number}{' ' * account_num_padding}{BORDER_CHAR}{RESET}")

    # Line 4: Status
    status_indent = 2
    status_content_len = get_visible_length(styled_status)
    status_padding = card_inner_width - status_content_len - status_indent
    print(f"{BORDER_CHAR}{' ' * status_indent}{styled_status}{' ' * status_padding}{BORDER_CHAR}{RESET}")

    # Line 5: Blank line for vertical spacing (or another divider)
    print(f"{BORDER_CHAR}{DIVIDER_CHAR * card_inner_width}{BORDER_CHAR}{RESET}")

    # Line 6: VALID THRU and Expiration Date (Right-aligned)
    valid_thru_content = f"{valid_thru_label_styled} {styled_exp_date}"
    valid_thru_indent = 2
    content_len = get_visible_length(valid_thru_content)
    padding = card_inner_width - content_len - valid_thru_indent
    print(f"{BORDER_CHAR}{' ' * padding}{valid_thru_content}{' ' * valid_thru_indent}{BORDER_CHAR}{RESET}")

    # Line 7: Card Holder Name (Left-aligned)
    name_indent = 2
    content_len = get_visible_length(styled_name)
    padding = card_inner_width - content_len - name_indent
    print(f"{BORDER_CHAR}{' ' * name_indent}{styled_name}{' ' * padding}{BORDER_CHAR}{RESET}")

    # Line 8: Divider Line
    print(f"{BORDER_CHAR}{DIVIDER_CHAR * card_inner_width}{BORDER_CHAR}{RESET}")

    # Line 9: CVV (left) and Mastercard Logo (right)
    cvv_indent = 2
    cvv_content_len = get_visible_length(styled_cvv)
    logo_indent = 2

    space_between_cvv_logo = card_inner_width - cvv_indent - cvv_content_len - mc_logo_visible_width - logo_indent
    space_between_cvv_logo = max(0, space_between_cvv_logo)

    print(
        f"{BORDER_CHAR}"
        f"{' ' * cvv_indent}"
        f"{styled_cvv}"
        f"{' ' * space_between_cvv_logo}"
        f"{mc_logo_string}"
        f"{' ' * logo_indent}"
        f"{BORDER_CHAR}{RESET}"
    )

    # Bottom Border
    print(f"{BORDER_CHAR * card_width}{RESET}")

    print(f"\n{BOLD}{CYAN}This is a demonstration. Do not share real card details!{RESET}")
    input(f"\n{BOLD}{CYAN}Press Enter to return to card management...{RESET}")


def generate_random_card_details():
    """Generates random 16-digit card number, 3-digit CVV, and MM/YY expiry."""
    # Generate 16-digit number (simple random for demo, not actual card logic)
    card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])

    # Generate 3-digit CVV
    cvv = f"{random.randint(100, 999)}"

    # Generate expiry date (MM/YY) - between 1 to 5 years from current month
    current_date = datetime.datetime.now()
    
    # Pick a random number of months to add (e.g., 12 to 60 months)
    months_to_add = random.randint(12, 60)
    
    # Calculate approximate expiry date
    expiry_date_obj = current_date + datetime.timedelta(days=30 * months_to_add) # Approximate calculation
    
    # Ensure it's the last day of the month for proper expiry
    if expiry_date_obj.month == 12:
        expiry_date_obj = expiry_date_obj.replace(day=31)
    else:
        # Move to the first day of next month, then subtract one day
        expiry_date_obj = expiry_date_obj.replace(month=expiry_date_obj.month + 1, day=1) - datetime.timedelta(days=1)

    exp_month = expiry_date_obj.month
    exp_year = expiry_date_obj.year

    # Format as MM/YY
    exp_date = f"{exp_month:02d}/{str(exp_year)[-2:]}"

    return card_number, cvv, exp_date

# --- END NEW CARD DISPLAY AND GENERATION FUNCTIONS ---


def display_token_machine_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}Select Service{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[32m to GREEN for consistency
    print(f"{GREEN}1. Open a New Bank Account{RESET}") # Green text
    print(f"{GREEN}2. Close a Bank Account{RESET}") # Green text
    print(f"{GREEN}3. Reactivate A Bank Account{RESET}") # Green text
    print(f"{GREEN}4. Statement Enquiry{RESET}") # Green text
    print(f"{GREEN}5. Cheque Book{RESET}") # Green text
    print(f"{GREEN}6. Cheque Deposit{RESET}") # Green text
    print(f"{GREEN}7. Cash Withdrawal{RESET}") # Green text
    print(f"{GREEN}8. Cash Deposit{RESET}") # Green text
    print(f"{GREEN}9. Currency Conversion{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}P. Go back to previous menu{RESET}") # Yellow text
    print(f"{YELLOW}M. Go to main menu{RESET}") # Yellow text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_atm_locations_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}ATM Locations{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    for i, branch_name in enumerate(OUR_BRANCHES, 1):
        # Changed from \033[32m to GREEN for consistency
        print(f"{GREEN}{i}. {branch_name}{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}P. Go back to previous menu{RESET}") # Yellow text
    print(f"{YELLOW}M. Go to main menu{RESET}") # Yellow text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_account_services_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}Account Services{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[32m to GREEN for consistency
    print(f"{GREEN}1. View Account Details{RESET}") # Green text
    print(f"{GREEN}2. Make a Deposit{RESET}") # Green text
    print(f"{GREEN}3. Make a Withdrawal{RESET}") # Green text
    print(f"{GREEN}4. View Transaction History{RESET}") # Green text
    print(f"{GREEN}5. My Statements{RESET}") # Green text
    print(f"{GREEN}6. Add/Manage Payment Methods{RESET}") # Green text
    print(f"{GREEN}7. Manage Cards{RESET}") # Green text
    print(f"{GREEN}8. Request Services{RESET}") # Green text
    print(f"{GREEN}9. Make Payments (Transfers to external methods){RESET}") # Green text
    print(f"{GREEN}10. Check Loan Balance/Limit & Request Loan{RESET}") # Green text
    print(f"{GREEN}11. Logout{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_payment_methods_menu():
    clear_screen()
    # Changed from \033[33m to YELLOW for consistency
    print(f"\n{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[34m to BLUE for consistency
    print(f"{BOLD}{BLUE}Add/Manage Payment Methods{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET))) # Centered, bold blue
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'=' * 50}{RESET}") # Yellow border
    # Changed from \033[32m to GREEN for consistency
    print(f"{GREEN}1. Add M-Pesa{RESET}") # Green text
    print(f"{GREEN}2. Add Airtel Money{RESET}") # Green text
    print(f"{GREEN}3. Add Bank Transfer{RESET}") # Green text
    print(f"{GREEN}4. Add PayPal{RESET}") # Green text
    print(f"{GREEN}5. Add Crypto Wallet (Bitcoin, Ethereum, Solana, incl. exchanges){RESET}") # Green text
    print(f"{GREEN}6. Set/Change Payment Passcode{RESET}") # Green text
    print(f"{GREEN}7. View My Payment Methods{RESET}") # Green text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}P. Go back to previous menu{RESET}") # Yellow text
    print(f"{YELLOW}M. Go to main menu{RESET}") # Yellow text
    # Changed from \033[33m to YELLOW for consistency
    print(f"{YELLOW}{'-' * 50}{RESET}") # Yellow separator

def display_token(service_choice):
    clear_screen()
    service_name = get_service_name(service_choice)
    token_number = random.randint(100, 999)
    # Changed from \033[1m\033[36m to BOLD and CYAN for consistency
    print(f"{BOLD}{CYAN}----------------------------------------{RESET}") # Bold Cyan separator
    print(f"{BOLD}{CYAN}|        {BANK_NAME} Token          |{RESET}") # Bold Cyan Bank Name
    print(f"{BOLD}{CYAN}----------------------------------------{RESET}") # Bold Cyan separator
    # Changed from \033[34m to BLUE for consistency
    print(f"{BLUE}Service:{RESET} {service_name}") # Blue label
    print(f"{BLUE}Token Number:{RESET} {token_number}") # Blue label
    print(f"{BLUE}Date:{RESET} {datetime.date.today().strftime('%Y-%m-%d')}") # Blue label
    print(f"{BLUE}Time:{RESET} {datetime.datetime.now().strftime('%H:%M:%S')}") # Blue label
    # Changed from \033[34mi\033[0m to BLUE_INFO for consistency
    print(f"\n{BLUE_INFO} Please wait for your turn. Requirements for {service_name}:\n{RESET}") # Blue info symbol
    if service_choice == 1:
        # Changed from \033[32m to GREEN for consistency
        print(f"{GREEN}- National ID/Passport{RESET}") # Green requirements
        print(f"{GREEN}- KRA PIN Certificate{RESET}")
        print(f"{GREEN}- Recent Utility Bill (Proof of Address){RESET}")
    elif service_choice in [2, 3]:
        print(f"{GREEN}- National ID/Passport{RESET}")
        print(f"{GREEN}- Account details/documents{RESET}")
    elif service_choice in [4, 5, 6, 7, 8, 9]:
        print(f"{GREEN}- National ID/Passport{RESET}")
        print(f"{GREEN}- Relevant account information{RESET}")
    # Changed from \033[1m\033[36m to BOLD and CYAN for consistency
    print(f"{BOLD}{CYAN}----------------------------------------{RESET}") # Bold Cyan separator
    # Changed from \033[90m to BRIGHT_BLACK for consistency
    input(f"\n{BRIGHT_BLACK}Press Enter to take your token...{RESET}") # Faint input prompt

def get_service_name(choice):
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
            print(f"{RED_X} Username already exists. Please choose a different one.{RESET}")
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
            print(f"{RED_X} Passwords do not match. Please try again.{RESET}")
    
    # --- Set Security Questions ---
    # Use BOLD and BLUE for section header
    print(f"\n{BOLD}{BLUE}--- Set Up Security Questions (Choose Two) ---{RESET}")
    selected_questions = {}
    available_q_indices = list(SECURITY_QUESTIONS.keys())

    for i in range(2):
        while True:
            # Use BLUE for section title
            print(f"\n{BLUE}Available Security Questions:{RESET}")
            for idx in available_q_indices:
                # Use GREEN for questions
                print(f"{GREEN}{idx}. {SECURITY_QUESTIONS[idx]}{RESET}")
            
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
                print(f"{RED_X} Invalid question choice or question already selected. Please choose from the available list.{RESET}")
    
    # --- Collect Personal Details ---
    name = get_user_input("Enter your full name: ")
    if name in ['M', 'P', None]: return name

    nationality = get_choice_input("Select your nationality:", NATIONALITY_CHOICES)
    if nationality in ['M', 'P', None]: return nationality

    country_code = get_user_input("Enter your country code (e.g., +254 for Kenya): ")
    if country_code in ['M', 'P', None]: return country_code
    
    phone_number = get_user_input("Enter your phone number (e.g., 712345678): ")
    if phone_number in ['M', 'P', None]: return phone_number
    # Basic phone number validation
    if not (phone_number.isdigit() and len(phone_number) >= 9):
        print(f"{RED_X} Invalid phone number format.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return False
    full_phone_number = country_code + phone_number # Combine for use

    email = get_user_input("Enter your email address: ")
    if email in ['M', 'P', None]: return email
    while not is_valid_email(email):
        print(f"{RED_X} Invalid email address.{RESET}")
        email = get_user_input("Enter your email address: ")
        if email in ['M', 'P', None]: return email
    
    while True:
        kra_pin = get_user_input("Enter your KRA PIN (e.g., A12345678B - Capital letter, 9 digits, Capital letter): ")
        if kra_pin in ['M', 'P', None]: return kra_pin
        if is_valid_kra_pin(kra_pin):
            break
        else:
            print(f"{RED_X} Invalid KRA PIN format. Please follow the format: Capital letter, 9 digits, Capital letter (e.g., A12345678B).{RESET}")

    reason = get_choice_input("Select reason for opening account:", REASON_CHOICES)
    if reason in ['M', 'P', None]: return reason

    occupation = get_choice_input("Select your occupation:", OCCUPATION_CHOICES)
    if occupation in ['M', 'P', None]: return occupation

    source_of_income = get_choice_input("Select your source of income:", SOURCE_OF_INCOME_CHOICES)
    if source_of_income in ['M', 'P', None]: return source_of_income

    monthly_deposits = get_user_input("Enter approximate number of monthly deposits: ", int)
    if monthly_deposits in ['M', 'P', None]: return monthly_deposits

    monthly_withdrawals = get_user_input("Enter approximate number of monthly withdrawals: ", int)
    if monthly_withdrawals in ['M', 'P', None]: return monthly_withdrawals
    while monthly_withdrawals > monthly_deposits:
        print(f"{RED_X} Withdrawals should not be more than deposits. Please enter again.{RESET}")
        monthly_withdrawals = get_user_input("Enter approximate number of monthly withdrawals: ", int)
        if monthly_withdrawals in ['M', 'P', None]: return monthly_withdrawals
    
    monthly_balance = get_user_input("Enter monthly balance you intend to maintain (e.g., 50000.00): ", float)
    if monthly_balance in ['M', 'P', None]: return monthly_balance
    
    address = get_user_input("Enter your address: ")
    if address in ['M', 'P', None]: return address

    # Use BLUE for the section title
    print(f"\n{BLUE}Our Bank Branches:{RESET}")
    for i, branch in enumerate(OUR_BRANCHES, 1):
        # Use GREEN for branch names
        print(f"{GREEN}{i}. {branch}{RESET}")
    branch_choice = get_user_input(f"Select your bank branch (1-{len(OUR_BRANCHES)}): ", int)
    if branch_choice in ['M', 'P', None]: return branch_choice
    while not 1 <= branch_choice <= len(OUR_BRANCHES):
        print(f"{RED_X} Invalid branch choice. Please select from the list.{RESET}")
        branch_choice = get_user_input(f"Select your bank branch (1-{len(OUR_BRANCHES)}): ", int)
        if branch_choice in ['M', 'P', None]: return branch_choice
    my_branch = OUR_BRANCHES[branch_choice - 1]

    # --- Bank Account Type Selection ---
    account_type_details = None
    while True:
        display_bank_accounts_menu()
        acc_type_choice = get_user_input("Select an account type to open: ", int)
        if acc_type_choice in ['M', 'P', None]: return acc_type_choice

        account_type_details = get_account_type_details(acc_type_choice)
        if account_type_details:
            # Handle multi-currency selection for Sapphire Multi Currency Account
            if account_type_details.get("Account Name") == "Sapphire Multi currency account":
                # Use BOLD and BLUE for section title
                print(f"\n{BOLD}{BLUE}--- Select Your Preferred Base Currency for Sapphire Multi Currency Account ---{RESET}")
                # Use GREEN for options
                print(f"{GREEN}1. USD (United States Dollar){RESET}")
                print(f"{GREEN}2. GBP (Great British Pound){RESET}")
                print(f"{GREEN}3. EURO (Euro){RESET}")
                print(f"{GREEN}4. JPY (Japanese Yen){RESET}")
                
                currency_map = {
                    1: "USD",
                    2: "GBP",
                    3: "EURO",
                    4: "JPY"
                }
                
                while True:
                    currency_choice = get_user_input("Enter your choice (1-4): ", int)
                    if currency_choice in ['M', 'P', None]: return currency_choice
                    
                    if currency_choice in currency_map:
                        account_type_details["Currency"] = currency_map[currency_choice]
                        print(f"{GREEN_CHECKMARK} You have selected {account_type_details['Currency']} as your account's base currency.{RESET}")
                        break
                    else:
                        print(f"{RED_X} Invalid currency choice.{RESET}")
                        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")

            _print_card_details_info_display(account_type_details) # Use the new display function
            confirm_account = get_user_input("Do you want to open this account type? (yes/no): ").lower()
            if confirm_account == 'yes':
                break
            elif confirm_account in ['M', 'P', None]:
                return confirm_account
            else:
                print(f"{RED_X} Invalid confirmation. Please enter 'yes' or 'no'.{RESET}")
        else:
            print(f"{RED_X} Invalid account type selection.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
    
    # --- OTP verification ---
    generated_otp = generate_otp(length=6) # Ensure 6 digits
    otp_sent_time = datetime.datetime.now()
    otp_expiration_time = otp_sent_time + datetime.timedelta(minutes=5)

    if not send_otp_email(name, email, generated_otp, otp_expiration_time):
        print(f"{RED_X} Failed to send OTP email. Account creation aborted.{RESET}")
        return False # Indicate failure
    
    otp_verified = verify_otp_with_retries(
        target_name=name,
        contact_info=email,
        generated_otp=generated_otp,
        otp_expiry_time=otp_expiration_time,
        max_retries=3, # User gets 3 attempts
        otp_delivery_method="email"
    )

    if otp_verified == True:
        print(f"\n{GREEN_CHECKMARK} OTP successfully verified. Proceeding with account setup...{RESET}")
        
        # --- Account Activation Logic ---
        initial_balance_needed = account_type_details.get("Opening balance", 0.0)
        actual_initial_deposit = 0.0 # Account starts with 0 balance for now
        account_activated = False

        if initial_balance_needed > 0:
            # Convert initial_balance_needed to account's currency if it's not KES
            initial_balance_in_account_currency = convert_currency(initial_balance_needed, "KES", account_type_details["Currency"])
            if initial_balance_in_account_currency is None:
                print(f"{RED_X} Error: Could not determine initial balance in chosen currency. Account creation aborted.{RESET}")
                return False
            
            # Use BLUE_INFO for information messages
            print(f"{BLUE_INFO} This account type requires an opening balance of {initial_balance_in_account_currency:,.2f} {account_type_details['Currency']}.{RESET}")
            print(f"{BLUE_INFO} You will need to deposit this amount to fully activate your account.{RESET}")
            print(f"{BLUE_INFO} Your account will be created. Please note that you must deposit {initial_balance_in_account_currency:,.2f} {account_type_details['Currency']} to fully activate it.{RESET}")
            print(f"{BLUE_INFO} You can do this from 'Account Services' -> 'Make a Deposit' after logging in.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}") # Pause for user to read

        else: # Opening balance is 0
            account_activated = True
            print(f"{GREEN_CHECKMARK} Account activated immediately (no opening balance required).{RESET}")

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
            "cards": [], # Initialize empty cards list
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
            print(f"\n{GREEN_CHECKMARK} Account for '{new_username}' successfully created and activated!{RESET}")
        else:
            print(f"\n{GREEN_CHECKMARK} Account for '{new_username}' successfully created. It needs an initial deposit to be fully activated.{RESET}")
            print(f"{BLUE_INFO} Your new account number is: {account_number}{RESET}")
            print(f"{BLUE_INFO} Please remember your username and password for login.{RESET}")
            print(f"{BLUE_INFO} Log in and navigate to 'Account Services' -> 'Make a Deposit' to activate your account.{RESET}")

        return True # Indicate successful account creation
    elif otp_verified in ['P', 'M']:
        print(f"{BLUE_INFO} OTP verification cancelled. Returning to previous menu.{RESET}")
        time.sleep(2)
        return otp_verified # Propagate 'P' or 'M'
    else: # otp_verified is False (expired or too many failed attempts)
        print(f"{RED_X} Account registration aborted due to OTP verification failure.{RESET}")
        time.sleep(2)
        return False # Indicate failure

# --- Core Bank Operations ---

def deposit(username):
    """Allows a user to deposit funds into their account."""
    accounts_data = read_accounts()
    user_account = accounts_data[username]
    user_details = user_account["details"]
    account_currency = user_details["account_currency"]
    
    payment_methods = user_details.get("payment_methods", [])

    if not payment_methods:
        print(f"{RED_X} You have no payment methods linked to make a deposit.{RESET}")
        print(f"{BLUE_INFO} Please go to 'Add/Manage Payment Methods' to link one.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    # Use BOLD and BLUE for section title
    print(f"\n{BOLD}{BLUE}--- Select a Payment Method for Deposit ---{RESET}")
    for i, method in enumerate(payment_methods, 1):
        identifier_display = method.get("identifier", "N/A")
        if method["name"] == "Bank Transfer":
            identifier_display = f"Bank: {method.get('bank_name', 'N/A')}, Acc: {method.get('identifier', 'N/A')}"
        elif method["name"] == "Crypto Wallet":
            identifier_display = f"Type: {method.get('crypto_type', 'N/A')}, Exch: {method.get('exchange', 'N/A')}, Addr: {method.get('identifier', 'N/A')}"
        # Use GREEN for options
        print(f"{GREEN}{i}. {method['name']} - {identifier_display} (Balance: {method['balance']:.2f} {method['currency']}){RESET}")
    # Use YELLOW for navigation options
    print(f"{YELLOW}P. Go back to previous menu{RESET}")
    print(f"{YELLOW}M. Go to main menu{RESET}")

    method_choice = get_user_input("Enter your choice: ", int)
    if method_choice == 'M': return 'M'
    if method_choice == 'P': return 'P'
    if method_choice is None: return None

    if not (1 <= method_choice <= len(payment_methods)):
        print(f"{RED_X} Invalid payment method choice.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    selected_method = payment_methods[method_choice - 1]
    
    while True:
        amount_to_deposit = get_user_input(f"Enter amount to deposit from {selected_method['name']} ({selected_method['currency']}): ", float)
        if amount_to_deposit == 'M': return 'M'
        if amount_to_deposit == 'P': return 'P'
        if amount_to_deposit is None: return None

        if amount_to_deposit <= 0:
            print(f"{RED_X} Deposit amount must be positive.{RESET}")
        elif amount_to_deposit > selected_method['balance']:
            print(f"{RED_X} Insufficient funds in your {selected_method['name']} ({selected_method['currency']}) account. Available: {selected_method['balance']:.2f} {selected_method['currency']}.{RESET}")
        else:
            break

    # Convert amount to account's currency
    converted_amount = convert_currency(amount_to_deposit, selected_method['currency'], account_currency)
    if converted_amount is None:
        print(f"{RED_X} Failed to convert currency for deposit. Please try again.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    # Check for account activation requirement
    account_opening_balance = user_details["account_type_features"].get("Opening balance", 0.0)
    if not user_account.get("activated", True) and account_opening_balance > 0:
        required_activation_amount = convert_currency(account_opening_balance, "KES", account_currency)
        if converted_amount < required_activation_amount:
            print(f"{RED_X} This is your first deposit and it must be at least the opening balance of {required_activation_amount:,.2f} {account_currency} to activate your account.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return 'P'
        else:
            print(f"{GREEN_CHECKMARK} Your account has been successfully activated!{RESET}")
            user_account["activated"] = True


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
          f"({converted_amount:,.2f} {account_currency}) to your account.{RESET}")
    print(f"{BLUE_INFO} Your new account balance is {user_account['balance']:.2f} {account_currency}.{RESET}")
    send_transaction_notification(user_details['name'], user_details['email'], user_details['phone_number'],
                                  "Deposit", converted_amount, account_currency, ref_num, description, user_account['balance'])
    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
    return True

def withdraw(username):
    """Allows a user to withdraw funds from their account."""
    accounts_data = read_accounts()
    user_account = accounts_data[username]
    user_details = user_account["details"]
    account_currency = user_details["account_currency"]
    
    # Check if account is activated
    if not user_account.get("activated", True):
        print(f"{RED_X} Your account is not yet activated. Please make the required initial deposit to activate it.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    if user_account["balance"] <= 0:
        print(f"{RED_X} Your account balance is zero or insufficient for withdrawal.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'
    
    # Use BOLD and BLUE for section title
    print(f"\n{BOLD}{BLUE}--- Withdrawal Options ---{RESET}")
    # Use BLUE for current balance info
    print(f"{BLUE}Your current balance:{RESET} {user_account['balance']:.2f} {account_currency}")
    # Use GREEN for options
    print(f"{GREEN}1. Withdraw to Bank Account (same currency as your current bank account){RESET}")
    print(f"{GREEN}2. Withdraw to Mobile Money (KES only, if linked){RESET}")
    print(f"{GREEN}3. Withdraw to PayPal (USD only, if linked){RESET}")
    print(f"{GREEN}4. Withdraw to Crypto Wallet (specific crypto, if linked){RESET}")
    # Use YELLOW for navigation options
    print(f"{YELLOW}P. Go back to previous menu{RESET}")
    print(f"{YELLOW}M. Go to main menu{RESET}")

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
            print(f"{RED_X} No payment methods linked for this type of withdrawal. Please add one.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
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
            print(f"{RED_X} No eligible linked payment methods found for your selection.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return 'P'
        
        # Use BOLD and BLUE for section title
        print(f"\n{BOLD}{BLUE}--- Select a Destination {['','Mobile Money','PayPal','Crypto Wallet'][withdrawal_choice]} ---{RESET}")
        for i, method in enumerate(eligible_methods, 1):
            identifier_display = method.get("identifier", "N/A")
            if method["name"] == "Crypto Wallet":
                identifier_display = f"Type: {method.get('crypto_type', 'N/A')}, Exch: {method.get('exchange', 'N/A')}, Addr: {method.get('identifier', 'N/A')}"
            # Use GREEN for options
            print(f"{GREEN}{i}. {method['name']} - {identifier_display} (Current Balance: {method['balance']:.2f} {method['currency']}){RESET}")
        
        dest_choice = get_user_input("Enter your choice: ", int)
        if dest_choice == 'M': return 'M'
        if dest_choice == 'P': return 'P'
        if dest_choice is None: return None

        if not (1 <= dest_choice <= len(eligible_methods)):
            print(f"{RED_X} Invalid destination choice.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return 'P'
        
        destination_method = eligible_methods[dest_choice - 1]
        destination_name = destination_method['name']
        destination_currency = destination_method['currency']
        
    else:
        print(f"{RED_X} Invalid withdrawal option.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    while True:
        amount_to_withdraw = get_user_input(f"Enter amount to withdraw ({account_currency}): ", float)
        if amount_to_withdraw == 'M': return 'M'
        if amount_to_withdraw == 'P': return 'P'
        if amount_to_withdraw is None: return None

        if amount_to_withdraw <= 0:
            print(f"{RED_X} Withdrawal amount must be positive.{RESET}")
        elif amount_to_withdraw > user_account["balance"]:
            print(f"{RED_X} Insufficient funds. Your current balance is {user_account['balance']:.2f} {account_currency}.{RESET}")
        else:
            break
            
    # Verify payment passcode for external transfers
    if withdrawal_choice in [2, 3, 4]: # Mobile Money, PayPal, Crypto
        if not user_details.get("payment_passcode"):
            print(f"{RED_X} You must set a Payment Authorization Passcode to make external transfers.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return 'P'
        
        entered_passcode = get_user_input("Enter your 6-digit Payment Authorization Passcode: ")
        if entered_passcode in ['M', 'P', None]: return entered_passcode

        if entered_passcode != user_details["payment_passcode"]:
            print(f"{RED_X} Incorrect Payment Authorization Passcode. Withdrawal failed.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return 'P'

    # Convert amount from account's currency to destination currency
    converted_amount = convert_currency(amount_to_withdraw, account_currency, destination_currency)
    if converted_amount is None:
        print(f"{RED_X} Failed to convert currency for withdrawal. Please try again.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
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

    print(f"\n{GREEN_CHECKMARK} Successfully withdrew {amount_to_withdraw:,.2f} {account_currency}.{RESET}")
    print(f"{BLUE_INFO} Funds transferred to {destination_name}: {converted_amount:,.2f} {destination_currency}.{RESET}")
    print(f"{BLUE_INFO} Your new account balance is {user_account['balance']:.2f} {account_currency}.{RESET}")
    send_transaction_notification(user_details['name'], user_details['email'], user_details['phone_number'],
                                  "Withdrawal", amount_to_withdraw, account_currency, ref_num, description, user_account['balance'])
    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
    return True

def view_transaction_history(username):
    """Displays simplified transaction history for the user."""
    transactions = read_transactions()
    user_transactions = [t for t in transactions if t["username"] == username]

    if not user_transactions:
        print(f"{BLUE_INFO} No transaction history found for {username}.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return

    # Use BOLD and BLUE for section title
    print(f"\n{BOLD}{BLUE}--- Your Transaction History ---{RESET}")
    # Use CYAN for headers
    print(f"{CYAN}{'Date':<19} {'Type':<15} {'Amount':<15} {'Currency':<10} {'Ref No.':<20}{RESET}")
    # Use YELLOW for separator
    print(f"{YELLOW}-" * 80 + f"{RESET}")
    for t in user_transactions:
        print(f"{t['timestamp']:<19} {t['type']:<15} {t['amount']:.2f}{t['currency']:<15} {t['reference_number']:<20}")
    print(f"{YELLOW}-" * 80 + f"{RESET}")
    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")

def view_my_statements(username):
    """Displays detailed statement entries for the user."""
    accounts_data = read_accounts()
    user_details = accounts_data[username]["details"]
    statements = user_details.get("statements", [])

    if not statements:
        print(f"{BLUE_INFO} No statements available for your account yet.{RESET}")
    else:
        # Use BOLD and BLUE for section title
        print(f"\n{BOLD}{BLUE}--- Your Account Statements ---{RESET}")
        # Use CYAN for headers
        print(f"{CYAN}{'Date/Time':<19} {'Type':<15} {'Amount':<15} {'Currency':<10} {'Running Balance':<20} {'Description':<30}{RESET}")
        # Use YELLOW for separator
        print(f"{YELLOW}-" * 120 + f"{RESET}")
        for s in statements:
            print(f"{s['timestamp']:<19} {s['type']:<15} {s['amount']:<15.2f} {s['currency']:<10} {s['running_balance']:<20.2f} {s['description']:<30}")
        print(f"{YELLOW}-" * 120 + f"{RESET}")
    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")


# --- Payment Methods ---

def set_payment_passcode(username):
    """Allows a user to set or change their 6-digit payment passcode."""
    accounts_data = read_accounts()
    user_details = accounts_data[username]["details"]
    phone_number = user_details.get("phone_number")

    if not phone_number:
        print(f"{RED_X} Please ensure your phone number is registered to set a passcode.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return False

    while True:
        new_passcode = get_user_input("Enter a new 6-digit Payment Authorization Passcode: ")
        if new_passcode in ['M', 'P', None]: return new_passcode

        if not (new_passcode.isdigit() and len(new_passcode) == 6):
            print(f"{RED_X} Passcode must be a 6-digit number.{RESET}")
            continue
        
        confirm_passcode = get_user_input("Confirm your 6-digit Payment Authorization Passcode: ")
        if confirm_passcode in ['M', 'P', None]: return confirm_passcode

        if new_passcode == confirm_passcode:
            # Send OTP to verify
            generated_otp = generate_otp(6) # Using main generate_otp
            if not send_payment_otp_sms(phone_number, generated_otp):
                print(f"{RED_X} Failed to send OTP. Passcode not set.{RESET}")
                input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                return False

            entered_otp = get_user_input("Enter the OTP received on your phone to verify passcode: ")
            if entered_otp in ['M', 'P', None]: return entered_otp

            if entered_otp == generated_otp:
                user_details["payment_passcode"] = new_passcode
                accounts_data[username]["details"] = user_details # Update in the main dict
                save_accounts(accounts_data)
                print(f"{GREEN_CHECKMARK} Payment Authorization Passcode successfully set/updated!{RESET}")
                input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                return True
            else:
                print(f"{RED_X} Incorrect OTP. Passcode not set.{RESET}")
                input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                return False
        else:
            print(f"{RED_X} Passcodes do not match. Please try again.{RESET}")

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
        if phone_number in ['M', 'P', None]: return phone_number
        if not (phone_number.isdigit() and len(phone_number) >= 9):
            print(f"{RED_X} Invalid phone number format.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return False
        
        if any(pm['name'] == method_name and pm['identifier'] == phone_number for pm in payment_methods):
            print(f"{BLUE_INFO} This M-Pesa account is already linked.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
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
        if phone_number in ['M', 'P', None]: return phone_number
        if not (phone_number.isdigit() and len(phone_number) >= 9):
            print(f"{RED_X} Invalid phone number format.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return False
        
        if any(pm['name'] == method_name and pm['identifier'] == phone_number for pm in payment_methods):
            print(f"{BLUE_INFO} This Airtel Money account is already linked.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
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
        if bank_name in ['M', 'P', None]: return bank_name
        account_no = get_user_input("Enter Sending Account Number: ")
        if account_no in ['M', 'P', None]: return account_no
        if not account_no.isdigit():
            print(f"{RED_X} Account number must be digits.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return False

        if any(pm['name'] == method_name and pm['identifier'] == account_no and pm['bank_name'] == bank_name for pm in payment_methods):
            print(f"{BLUE_INFO} This Bank Transfer account is already linked.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
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
        if paypal_email in ['M', 'P', None]: return paypal_email
        if not is_valid_email(paypal_email):
            print(f"{RED_X} Invalid PayPal email address.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return False
        
        if any(pm['name'] == method_name and pm['identifier'] == paypal_email for pm in payment_methods):
            print(f"{BLUE_INFO} This PayPal account is already linked.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return False

        payment_methods.append({
            "name": method_name,
            "identifier": paypal_email,
            "currency": "USD", # PayPal assumed to hold USD
            "balance": default_balance_usd
        })
    elif method_type == 5: # Crypto Wallet
        method_name = "Crypto Wallet"
        # Use BOLD and BLUE for section title
        print(f"\n{BOLD}{BLUE}--- Choose Cryptocurrency and Exchange ---{RESET}")
        # Use GREEN for options
        print(f"{GREEN}1. Bitcoin (BTC) - General Wallet{RESET}")
        print(f"{GREEN}2. Ethereum (ETH) - General Wallet{RESET}")
        print(f"{GREEN}3. Solana (SOL) - General Wallet{RESET}")
        print(f"{GREEN}4. Bitcoin (BTC) - Binance{RESET}")
        print(f"{GREEN}5. Ethereum (ETH) - Bybit{RESET}")
        print(f"{GREEN}6. Solana (SOL) - OKX{RESET}")
        
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
            if crypto_choice_idx in ['M', 'P', None]: return crypto_choice_idx

            if crypto_choice_idx in crypto_options:
                selected_crypto = crypto_options[crypto_choice_idx]
                crypto_type = selected_crypto['type']
                crypto_exchange = selected_crypto['exchange']
                crypto_currency_symbol = selected_crypto['currency']
                break
            else:
                print(f"{RED_X} Invalid crypto choice.{RESET}")
                input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                return False # Go back to prev menu if invalid crypto choice

        wallet_address = get_user_input(f"Enter {crypto_type} wallet address ({crypto_exchange}): ")
        if wallet_address in ['M', 'P', None]: return wallet_address

        if any(pm['name'] == method_name and pm['crypto_type'] == crypto_type and 
               pm.get('exchange') == crypto_exchange and pm['identifier'] == wallet_address 
               for pm in payment_methods):
            print(f"{BLUE_INFO} This Crypto Wallet ({crypto_type} on {crypto_exchange}) is already linked.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return False
        
        # Convert default USD balance to the selected crypto's equivalent value
        default_balance_crypto = convert_currency(default_balance_usd, "USD", crypto_currency_symbol)
        if default_balance_crypto is None:
            print(f"{RED_X} Error converting default balance to crypto. Cannot add wallet.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
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
        print(f"{RED_X} Invalid payment method choice.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return False

    accounts_data[username]["details"]["payment_methods"] = payment_methods
    save_accounts(accounts_data)
    print(f"{GREEN_CHECKMARK} {method_name} added successfully!{RESET}")
    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
    return True

def view_payment_methods(username):
    """Displays the user's currently added payment methods."""
    accounts_data = read_accounts()
    user_details = accounts_data[username]["details"]
    payment_methods = user_details.get("payment_methods", [])

    if not payment_methods:
        print(f"{BLUE_INFO} You have not added any payment methods yet.{RESET}")
    else:
        # Use BOLD and BLUE for section title
        print(f"\n{BOLD}{BLUE}--- Your Linked Payment Methods ---{RESET}")
        for i, method in enumerate(payment_methods, 1):
            identifier_display = method.get("identifier", "N/A")
            if method["name"] == "Bank Transfer":
                identifier_display = f"Bank: {method.get('bank_name', 'N/A')}, Acc: {method.get('identifier', 'N/A')}"
            elif method["name"] == "Crypto Wallet":
                identifier_display = f"Type: {method.get('crypto_type', 'N/A')}, Exch: {method.get('exchange', 'N/A')}, Addr: {method.get('identifier', 'N/A')}"
            # Use GREEN for method details
            print(f"{GREEN}{i}. {method['name']} - {identifier_display} (Balance: {method['balance']:.2f} {method['currency']}){RESET}")
    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")

def make_payment(username):
    """Facilitates fund transfers from bank account to linked payment methods."""
    accounts_data = read_accounts()
    user_account = accounts_data[username]
    user_details = user_account["details"]
    account_currency = user_details["account_currency"]
    
    if user_account["balance"] <= 0:
        print(f"{RED_X} Your account balance is zero or insufficient for transfer.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    payment_methods = user_details.get("payment_methods", [])
    if not payment_methods:
        print(f"{RED_X} You have no external payment methods linked to make a transfer.{RESET}")
        print(f"{BLUE_INFO} Please go to 'Add/Manage Payment Methods' to link one.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    # Use BOLD and BLUE for section title
    print(f"\n{BOLD}{BLUE}--- Select Destination for Payment/Transfer ---{RESET}")
    # Use BLUE for current balance info
    print(f"{BLUE}Your current bank balance:{RESET} {user_account['balance']:.2f} {account_currency}")
    for i, method in enumerate(payment_methods, 1):
        identifier_display = method.get("identifier", "N/A")
        if method["name"] == "Bank Transfer":
            identifier_display = f"Bank: {method.get('bank_name', 'N/A')}, Acc: {method.get('identifier', 'N/A')}"
        elif method["name"] == "Crypto Wallet":
            identifier_display = f"Type: {method.get('crypto_type', 'N/A')}, Exch: {method.get('exchange', 'N/A')}, Addr: {method.get('identifier', 'N/A')}"
        # Use GREEN for method options
        print(f"{GREEN}{i}. {method['name']} - {identifier_display} (Current Balance: {method['balance']:.2f} {method['currency']}){RESET}")
    # Use YELLOW for navigation options
    print(f"{YELLOW}P. Go back to previous menu{RESET}")
    print(f"{YELLOW}M. Go to main menu{RESET}")

    method_choice = get_user_input("Enter your choice: ", int)
    if method_choice in ['M', 'P', None]: return method_choice

    if not (1 <= method_choice <= len(payment_methods)):
        print(f"{RED_X} Invalid payment method choice.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    selected_destination = payment_methods[method_choice - 1]
    destination_name = selected_destination['name']
    destination_currency = selected_destination['currency']

    while True:
        amount_to_transfer = get_user_input(f"Enter amount to transfer from your bank account ({account_currency}): ", float)
        if amount_to_transfer in ['M', 'P', None]: return amount_to_transfer

        if amount_to_transfer <= 0:
            print(f"{RED_X} Transfer amount must be positive.{RESET}")
        elif amount_to_transfer > user_account["balance"]:
            print(f"{RED_X} Insufficient funds in your bank account. Available: {user_account['balance']:.2f} {account_currency}.{RESET}")
        else:
            break
            
    # Verify payment passcode for external transfers
    if not user_details.get("payment_passcode"):
        print(f"{RED_X} You must set a Payment Authorization Passcode to make external transfers.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'
    
    entered_passcode = get_user_input("Enter your 6-digit Payment Authorization Passcode: ")
    if entered_passcode in ['M', 'P', None]: return entered_passcode

    if entered_passcode != user_details["payment_passcode"]:
        print(f"{RED_X} Incorrect Payment Authorization Passcode. Transfer failed.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    # Convert amount from account's currency to destination currency
    converted_amount = convert_currency(amount_to_transfer, account_currency, destination_currency)
    if converted_amount is None:
        print(f"{RED_X} Failed to convert currency for transfer. Please try again.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
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
          f"to {destination_name}.{RESET}")
    print(f"{BLUE_INFO} Recipient received {converted_amount:,.2f} {destination_currency}.{RESET}")
    print(f"{BLUE_INFO} Your new bank balance is {user_account['balance']:.2f} {account_currency}.{RESET}")
    send_transaction_notification(user_details['name'], user_details['email'], user_details['phone_number'],
                                  "Transfer Out", amount_to_transfer, account_currency, ref_num, description, user_account['balance'])
    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
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
        # Use BLUE_INFO for info messages
        print(f"\n{BLUE_INFO} Your loan limit has been reviewed and increased by {loan_limit_increase:,.2f} {account_currency}.{RESET}")
        print(f"{BLUE_INFO} New loan limit: {user_details['loan_limit']:.2f} {account_currency}.{RESET}")
        save_accounts(accounts_data) # Save updated loan limit
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")


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
        print(f"{RED_X} You currently have no available loan limit. Your current limit is {current_loan_limit:,.2f} {account_currency} and active loans are {active_loans:,.2f} {account_currency}.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    # Use BOLD and BLUE for section title
    print(f"\n{BOLD}{BLUE}--- Request Loan ---{RESET}")
    # Use BLUE for available loan info
    print(f"{BLUE}Your available loan limit:{RESET} {available_loan_amount:,.2f} {account_currency}")

    while True:
        loan_amount = get_user_input(f"Enter loan amount ({account_currency}) to request: ", float)
        if loan_amount in ['M', 'P', None]: return loan_amount

        if loan_amount <= 0:
            print(f"{RED_X} Loan amount must be positive.{RESET}")
        elif loan_amount > available_loan_amount:
            print(f"{RED_X} Requested amount exceeds your available loan limit. Max: {available_loan_amount:,.2f} {account_currency}.{RESET}")
        else:
            break
    
    # Choose disbursement method
    # Use BOLD and BLUE for section title
    print(f"\n{BOLD}{BLUE}--- Choose Where to Receive Loan Funds ---{RESET}")
    # Use GREEN for options
    print(f"{GREEN}1. To My Bank Account{RESET}")
    
    payment_methods = user_details.get("payment_methods", [])
    mobile_money_methods = [m for m in payment_methods if m['name'] in ["M-Pesa", "Airtel Money"]]
    paypal_methods = [m for m in payment_methods if m['name'] == "PayPal"]
    crypto_methods = [m for m in payment_methods if m['name'] == "Crypto Wallet"]

    option_counter = 2
    disbursement_options_map = {}
    
    if mobile_money_methods:
        # Use BLUE for sub-section title
        print(f"\n{BLUE}--- Mobile Money ---{RESET}")
        for i, method in enumerate(mobile_money_methods, 1):
            # Use GREEN for options
            print(f"{GREEN}{option_counter}. {method['name']} - {method['identifier']}{RESET}")
            disbursement_options_map[str(option_counter)] = {"type": "mobile_money", "method_obj": method, "index": payment_methods.index(method)}
            option_counter += 1
    
    if paypal_methods:
        # Use BLUE for sub-section title
        print(f"\n{BLUE}--- PayPal ---{RESET}")
        for i, method in enumerate(paypal_methods, 1):
            # Use GREEN for options
            print(f"{GREEN}{option_counter}. {method['name']} - {method['identifier']}{RESET}")
            disbursement_options_map[str(option_counter)] = {"type": "paypal", "method_obj": method, "index": payment_methods.index(method)}
            option_counter += 1

    if crypto_methods:
        # Use BLUE for sub-section title
        print(f"\n{BLUE}--- Crypto Wallets/Exchanges ---{RESET}")
        for i, method in enumerate(crypto_methods, 1):
            id_display = f"{method['crypto_type']} ({method['exchange']}) - {method['identifier']}"
            # Use GREEN for options
            print(f"{GREEN}{option_counter}. {method['name']} - {id_display}{RESET}")
            disbursement_options_map[str(option_counter)] = {"type": "crypto", "method_obj": method, "index": payment_methods.index(method)}
            option_counter += 1

    # Use YELLOW for navigation options
    print(f"{YELLOW}P. Go back to previous menu{RESET}")
    print(f"{YELLOW}M. Go to main menu{RESET}")

    disbursement_choice = get_user_input("Enter your choice: ") # Keep as string for map lookup
    if disbursement_choice in ['M', 'P', None]: return disbursement_choice

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
            print(f"{RED_X} Failed to convert currency for loan disbursement. Loan not issued.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return 'P'
    else:
        print(f"{RED_X} Invalid disbursement choice.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
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
    # Use GREEN_CHECKMARK for success message
    send_loan_disbursement_notification(user_details['name'], user_details['email'], user_details['phone_number'],
                                        loan_amount, interest_amount, repayment_date, disbursed_to_display, account_currency, ref_num)
    
    print(f"\n{GREEN_CHECKMARK} Loan of {loan_amount:,.2f} {account_currency} successfully disbursed to {disbursed_to_display}.{RESET}")
    print(f"{BLUE_INFO} You will need to repay {total_repayable:,.2f} {account_currency} by {repayment_date.strftime('%Y-%m-%d')}.{RESET}")
    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
    return True

# --- Card Management Functions ---

def view_my_cards(username):
    accounts_data = read_accounts()
    user_details = accounts_data[username]["details"]
    cards = user_details.get("cards", [])

    if not cards:
        print(f"{BLUE_INFO} You currently have no cards linked to your account.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return

    while True:
        clear_screen()
        print(f"\n{BOLD}{BLUE}--- Your Linked Cards ---{RESET}")
        if not cards:
            print(f"{BLUE_INFO} No cards to display.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return 'P'

        for i, card in enumerate(cards, 1):
            masked_card_number = f"**** **** **** {card['card_number'][-4:]}"
            status_color = GREEN if card['status'] == 'active' else RED
            print(f"{GREEN}{i}. {card['card_name']} ({masked_card_number}) - Status: {status_color}{card['status'].upper()}{RESET}")
        
        print(f"{YELLOW}S. Select a card for full details{RESET}")
        print(f"{YELLOW}P. Go back to previous menu{RESET}")
        print(f"{YELLOW}M. Go to main menu{RESET}")

        choice = get_user_input("Enter your choice: ").upper()
        if choice == 'P': return 'P'
        if choice == 'M': return 'M'
        if choice is None: return None

        if choice == 'S':
            while True:
                card_index_str = get_user_input("Enter the number of the card to view full details: ")
                if card_index_str in ['P', 'M', None]: break
                try:
                    card_index = int(card_index_str) - 1
                    if 0 <= card_index < len(cards):
                        selected_card = cards[card_index]
                        display_bank_card(
                            card_holder_name=user_details['name'],
                            bank_name=BANK_NAME,
                            card_number=selected_card['card_number'],
                            exp_date=selected_card['exp_date'],
                            cvv=selected_card['cvv'],
                            card_type_name=selected_card['card_name'],
                            currency_symbol=selected_card['currency'],
                            card_status=selected_card['status']
                        )
                        break # Break from inner loop, return to card list
                    else:
                        print(f"{RED_X} Invalid card number.{RESET}")
                except ValueError:
                    print(f"{RED_X} Invalid input. Please enter a number.{RESET}")
        else:
            print(f"{RED_X} Invalid choice. Please try again.{RESET}")


def request_new_card(username):
    accounts_data = read_accounts()
    user_account = accounts_data[username]
    user_details = user_account["details"]
    
    # Check if user has an account name and currency for card association
    if not user_details.get('account_type_name') or not user_details.get('account_currency'):
        print(f"{RED_X} Your account details are incomplete. Please ensure your bank account type and currency are set before requesting a card.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    user_full_name = user_details.get("name", username) # Use registered name or username

    selected_card_type_num = None
    while selected_card_type_num is None:
        clear_screen()
        print(f"\n{BOLD}{BG_BLUE}{BRIGHT_WHITE}--- Select Card Category ---{RESET}")
        print(f"{BRIGHT_CYAN}1. {BOLD}Debit Cards{RESET}")
        print(f"{BRIGHT_CYAN}2. {BOLD}Prepaid Cards{RESET}")
        print(f"{BRIGHT_CYAN}3. {BOLD}Credit Cards{RESET}")
        print(f"{YELLOW}P. Go back to previous menu{RESET}")
        print(f"{YELLOW}M. Go to main menu{RESET}")
        print(f"{BOLD}{BG_BLUE}{BRIGHT_WHITE}--------------------------{RESET}")
        choice_type_str = get_user_input("Enter the number for the card category: ")

        if choice_type_str in ['P', 'M', None]: return choice_type_str

        try:
            choice_type_int = int(choice_type_str)
            if 1 <= choice_type_int <= 3:
                selected_card_type_num = choice_type_int
            else:
                print(f"{RED_X} Invalid choice. Please enter 1, 2, or 3.{RESET}")
                input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")
        except ValueError:
            print(f"{RED_X} Invalid input. Please enter a number.{RESET}")
            input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")

    selected_specific_card_details = None
    while selected_specific_card_details is None:
        if selected_card_type_num == 1:
            display_debit_cards()
        elif selected_card_type_num == 2:
            display_prepaid_cards()
        elif selected_card_type_num == 3:
            display_credit_cards()
        
        print(f"{YELLOW}P. Go back to previous menu{RESET}")
        print(f"{YELLOW}M. Go to main menu{RESET}")
        choice_specific_card_str = get_user_input("Enter the number of the specific card to apply for: ")

        if choice_specific_card_str in ['P', 'M', None]: return choice_specific_card_str

        try:
            choice_specific_card_int = int(choice_specific_card_str)
            card_details = get_card_details_by_id(selected_card_type_num, choice_specific_card_int)
            
            if card_details:
                # Add validation for card types that might require a specific account type
                if card_details["Card Name"] == "Multi Currency Prepaid MasterCard" and \
                   user_details.get("account_type_name") != "Sapphire Multi currency account":
                    print(f"{RED_X} This card requires a 'Sapphire Multi currency account'. You have a '{user_details.get('account_type_name', 'N/A')}'.{RESET}")
                    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                    continue # Stay in this loop for specific card selection

                selected_specific_card_details = card_details
            else:
                print(f"{RED_X} Invalid selection for this card category. Please try again.{RESET}")
                input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")
        except ValueError:
            print(f"{RED_X} Invalid input. Please enter a number.{RESET}")
            input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")

    # Generate PIN (4 digits)
    while True:
        new_pin_str = get_user_input("Set a 4-digit PIN for your new card: ")
        if new_pin_str in ['P', 'M', None]: return new_pin_str
        if not (new_pin_str.isdigit() and len(new_pin_str) == 4):
            print(f"{RED_X} PIN must be a 4-digit number.{RESET}")
            continue
        confirm_pin_str = get_user_input("Confirm your 4-digit PIN: ")
        if confirm_pin_str in ['P', 'M', None]: return confirm_pin_str
        if new_pin_str == confirm_pin_str:
            new_pin = new_pin_str
            break
        else:
            print(f"{RED_X} PINs do not match. Please try again.{RESET}")

    # Generate card details
    random_card_number, random_cvv, random_exp_date = generate_random_card_details()

    # Store the new card details in the user's account
    new_card = {
        "card_id": f"{random_card_number[-4:]}-{random.randint(100,999)}", # Simple unique ID
        "card_name": selected_specific_card_details["Card Name"],
        "card_number": random_card_number,
        "exp_date": random_exp_date,
        "cvv": random_cvv, # For simulation, storing. In real system, hash or encrypt.
        "currency": selected_specific_card_details["Currency"],
        "pin": new_pin, # Store the PIN
        "status": "active", # Default status
        "issued_date": datetime.date.today().isoformat()
    }
    user_details.setdefault("cards", []).append(new_card)
    accounts_data[username]["details"] = user_details
    save_accounts(accounts_data)

    print(f"\n{GREEN_CHECKMARK} You have selected the {BOLD}{new_card['card_name']}{RESET}.")
    print(f"{CYAN}Generating and linking your new card details...{RESET}")
    time.sleep(2)

    display_bank_card(
        card_holder_name=user_full_name,
        bank_name=BANK_NAME,
        card_number=new_card['card_number'],
        exp_date=new_card['exp_date'],
        cvv=new_card['cvv'],
        card_type_name=new_card['card_name'],
        currency_symbol=new_card['currency'],
        card_status=new_card['status']
    )
    return True # Indicate successful card request

def block_unblock_card(username):
    accounts_data = read_accounts()
    user_details = accounts_data[username]["details"]
    cards = user_details.get("cards", [])

    if not cards:
        print(f"{BLUE_INFO} You have no cards to block or unblock.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    while True:
        clear_screen()
        print(f"\n{BOLD}{BLUE}--- Block/Unblock Card ---{RESET}")
        for i, card in enumerate(cards, 1):
            status_color = GREEN if card['status'] == 'active' else RED
            print(f"{GREEN}{i}. {card['card_name']} (**** **** **** {card['card_number'][-4:]}) - Status: {status_color}{card['status'].upper()}{RESET}")
        
        print(f"{YELLOW}P. Go back to previous menu{RESET}")
        print(f"{YELLOW}M. Go to main menu{RESET}")

        card_choice_str = get_user_input("Select card to modify (number): ")
        if card_choice_str in ['P', 'M', None]: return card_choice_str

        try:
            card_index = int(card_choice_str) - 1
            if 0 <= card_index < len(cards):
                selected_card = cards[card_index]
                current_status = selected_card['status']
                
                action_prompt = f"Current status is '{current_status}'. Do you want to {'block' if current_status == 'active' else 'unblock'} this card? (yes/no): "
                confirm_action = get_user_input(action_prompt).lower()
                
                if confirm_action == 'yes':
                    # Verify with payment passcode before changing status
                    if not user_details.get("payment_passcode"):
                        print(f"{RED_X} You must set a Payment Authorization Passcode to modify card status.{RESET}")
                        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                        return 'P'
                    
                    entered_passcode = get_user_input("Enter your 6-digit Payment Authorization Passcode to confirm: ")
                    if entered_passcode in ['M', 'P', None]: return entered_passcode

                    if entered_passcode != user_details["payment_passcode"]:
                        print(f"{RED_X} Incorrect Payment Authorization Passcode. Card status not changed.{RESET}")
                        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                        return 'P'
                    
                    new_status = 'blocked' if current_status == 'active' else 'active'
                    cards[card_index]['status'] = new_status
                    accounts_data[username]["details"]["cards"] = cards
                    save_accounts(accounts_data)
                    print(f"{GREEN_CHECKMARK} Card '{selected_card['card_name']}' is now {new_status}.{RESET}")
                    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                    return True # Action successful, return to prev menu
                elif confirm_action in ['P', 'M']:
                    return confirm_action
                else:
                    print(f"{BLUE_INFO} Action cancelled.{RESET}")
                    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                    continue # Stay in block/unblock menu
            else:
                print(f"{RED_X} Invalid card number.{RESET}")
                input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        except ValueError:
            print(f"{RED_X} Invalid input. Please enter a number.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")

def change_card_pin(username):
    accounts_data = read_accounts()
    user_details = accounts_data[username]["details"]
    cards = user_details.get("cards", [])

    if not cards:
        print(f"{BLUE_INFO} You have no cards to change PINs for.{RESET}")
        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        return 'P'

    while True:
        clear_screen()
        print(f"\n{BOLD}{BLUE}--- Change Card PIN ---{RESET}")
        for i, card in enumerate(cards, 1):
            print(f"{GREEN}{i}. {card['card_name']} (**** **** **** {card['card_number'][-4:]}){RESET}")
        
        print(f"{YELLOW}P. Go back to previous menu{RESET}")
        print(f"{YELLOW}M. Go to main menu{RESET}")

        card_choice_str = get_user_input("Select card to change PIN for (number): ")
        if card_choice_str in ['P', 'M', None]: return card_choice_str

        try:
            card_index = int(card_choice_str) - 1
            if 0 <= card_index < len(cards):
                selected_card = cards[card_index]

                # Verify with old PIN first
                old_pin_entered = get_user_input("Enter current 4-digit PIN: ")
                if old_pin_entered in ['P', 'M', None]: return old_pin_entered
                
                if old_pin_entered != selected_card['pin']:
                    print(f"{RED_X} Incorrect old PIN. PIN change failed.{RESET}")
                    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                    return 'P' # Return to previous menu

                while True:
                    new_pin_str = get_user_input("Enter new 4-digit PIN: ")
                    if new_pin_str in ['P', 'M', None]: return new_pin_str
                    if not (new_pin_str.isdigit() and len(new_pin_str) == 4):
                        print(f"{RED_X} New PIN must be a 4-digit number.{RESET}")
                        continue
                    confirm_pin_str = get_user_input("Confirm new 4-digit PIN: ")
                    if confirm_pin_str in ['P', 'M', None]: return new_pin_str # Propagate P/M from confirm
                    if new_pin_str == confirm_pin_str:
                        cards[card_index]['pin'] = new_pin_str
                        accounts_data[username]["details"]["cards"] = cards
                        save_accounts(accounts_data)
                        print(f"{GREEN_CHECKMARK} PIN for '{selected_card['card_name']}' successfully changed.{RESET}")
                        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                        return True # PIN change successful, return to prev menu
                    else:
                        print(f"{RED_X} New PINs do not match. Please try again.{RESET}")
            else:
                print(f"{RED_X} Invalid card number.{RESET}")
                input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        except ValueError:
            print(f"{RED_X} Invalid input. Please enter a number.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")


def display_card_management_menu():
    clear_screen()
    print(f"\n{YELLOW}{'=' * 50}{RESET}")
    print(f"{BOLD}{BLUE}Manage Cards{RESET}".center(50 + len(BOLD) + len(BLUE) + len(RESET)))
    print(f"{YELLOW}{'=' * 50}{RESET}")
    print(f"{GREEN}1. View My Cards{RESET}")
    print(f"{GREEN}2. Request New Card{RESET}")
    print(f"{GREEN}3. Block/Unblock Card{RESET}")
    print(f"{GREEN}4. Change Card PIN{RESET}")
    print(f"{YELLOW}P. Go back to previous menu{RESET}")
    print(f"{YELLOW}M. Go to main menu{RESET}")
    print(f"{YELLOW}{'-' * 50}{RESET}")

def handle_card_management_flow(username):
    """Handles the flow for managing cards."""
    while True:
        display_card_management_menu()
        card_manage_choice = get_user_input("Enter your choice: ", int)
        if card_manage_choice in ['M', 'P', None]: return card_manage_choice

        if card_manage_choice == 1:
            result = view_my_cards(username)
            if result in ['M', 'P', None]: return result
        elif card_manage_choice == 2:
            result = request_new_card(username)
            if result in ['M', 'P', None]: return result
        elif card_manage_choice == 3:
            result = block_unblock_card(username)
            if result in ['M', 'P', None]: return result
        elif card_manage_choice == 4:
            result = change_card_pin(username)
            if result in ['M', 'P', None]: return result
        else:
            print(f"{RED_X} Invalid choice. Please enter a number between 1 and 4.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")


# --- Main Application Flow Handlers ---

def handle_account_opening_flow():
    """Handles the flow for opening a bank account."""
    while True:
        display_account_opening_menu()
        account_choice = get_user_input("Enter your choice: ", int)
        if account_choice in ['M', 'P', None]: return account_choice

        if account_choice == 1: # Open a bank account online
            email = get_user_input("Enter your email address: ")
            if email in ['M', 'P', None]: continue
            while not is_valid_email(email):
                print(f"{RED_X} Invalid email address.{RESET}")
                email = get_user_input("Enter your email address: ")
                if email in ['M', 'P', None]: break # Allow breaking from validation loop
            if email in ['M', 'P', None]: continue # If loop broke due to M/P

            # Use BLUE_INFO for info messages
            print(f"{BLUE_INFO} Dear customer, we appreciate your interest in starting a financial journey with us. Attached to this is your application form. Please download it and fill it carefully, then scan the copy back to us.{RESET}")
            download_choice = get_user_input("Enter Y (yes to download), M (to go back to main menu), or P (to go back to the previous menu): ")
            if download_choice.upper() == 'Y':
                if send_application_form_email(email): # Send the simulated email
                    print(f"{GREEN_CHECKMARK} Application form sent to your email (check {EMAIL_INBOX_FILE}).{RESET}")
                else:
                    print(f"{RED_X} Failed to send application form email.{RESET}")
                input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            elif download_choice.upper() == 'M':
                return 'M'
            elif download_choice.upper() == 'P':
                continue # Stay in account opening menu
            elif download_choice is None:
                return None
            else:
                print(f"{RED_X} Invalid choice. Returning to the account opening menu.{RESET}")
                input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            return 'P' # Successfully handled online account opening path, go back to previous menu
        elif account_choice == 2: # Visit the nearest Bank branch
            while True: # Loop for token machine services
                display_token_machine_menu()
                service_choice = get_user_input("Select a service: ", int)
                if service_choice in ['M', 'P', None]: break # Go back to account opening menu
                
                display_token(service_choice)

                if service_choice == 1: # Open New Account (in-branch flow)
                    has_requirements = get_user_input("Do you have all the requirements listed on your token? (yes/no): ").lower()
                    if has_requirements in ['M', 'P', None]: continue
                    if has_requirements == 'yes':
                        result = create_account() # Call the detailed account creation function
                        if result is True: # Account successfully created
                            return 'M' # Go to main menu after successful creation
                        elif result is None: # EOFError during creation
                            return None
                        # If result is False (OTP incorrect or email failed), stay in token machine menu
                    else:
                        print(f"{BLUE_INFO} Please gather all requirements and visit us again.{RESET}")
                        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                else: # Other token machine services (placeholder)
                    print(f"{BLUE_INFO} Service '{get_service_name(service_choice)}' will be handled by a bank representative.{RESET}")
                    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            continue # After breaking from token machine loop, go back to account opening menu
        else:
            print(f"{RED_X} Invalid choice. Please enter 1 or 2.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")

def handle_offers_flow():
    """Handles the flow for exploring bank offers."""
    while True:
        display_offers_menu()
        offer_choice = get_user_input("Enter your choice: ", int)
        if offer_choice in ['M', 'P', None]: return offer_choice

        if offer_choice == 1: # Bank accounts
            while True:
                display_bank_accounts_menu()
                account_type_choice = get_user_input("Select an account type to view details: ", int)
                if account_type_choice in ['M', 'P', None]: break # Go back to offers menu
                
                details = get_account_type_details(account_type_choice) # Get details without auto-display
                _print_card_details_info_display(details) # Use new display helper
                if details:
                    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            continue # After breaking from bank accounts loop, go back to offers menu
        elif offer_choice == 2: # Our Cards
            while True:
                display_cards_menu()
                card_category_choice = get_user_input("Select a card category: ", int)
                if card_category_choice in ['M', 'P', None]: break # Go back to offers menu

                if card_category_choice == 1: # Debit Cards
                    while True:
                        display_debit_cards()
                        debit_card_choice = get_user_input("Select a debit card to view details: ", int)
                        if debit_card_choice in ['M', 'P', None]: break # Go back to cards menu
                        details = get_card_details_by_id(1, debit_card_choice) # Get details without auto-display
                        _print_card_details_info_display(details) # Use new display helper
                        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                    continue
                elif card_category_choice == 2: # Prepaid Cards
                    while True:
                        display_prepaid_cards()
                        prepaid_card_choice = get_user_input("Select a prepaid card to view details: ", int)
                        if prepaid_card_choice in ['M', 'P', None]: break # Go back to cards menu
                        details = get_card_details_by_id(2, prepaid_card_choice) # Get details without auto-display
                        _print_card_details_info_display(details) # Use new display helper
                        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                    continue
                elif card_category_choice == 3: # Credit Cards
                    while True:
                        display_credit_cards()
                        credit_card_choice = get_user_input("Select a credit card to view details: ", int)
                        if credit_card_choice in ['M', 'P', None]: break # Go back to cards menu
                        details = get_card_details_by_id(3, credit_card_choice) # Get details without auto-display
                        _print_card_details_info_display(details) # Use new display helper
                        input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
                    continue
                else:
                    print(f"{RED_X} Invalid card category choice.{RESET}")
                    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            continue # After breaking from cards category loop, go back to offers menu
        elif offer_choice == 3: # ATM locator
            result = display_atm_locations() # This function handles its own loop and returns 'M'/'P'
            if result == 'M': return 'M'
            if result == 'P': continue # Stay in offers menu after ATM locator
            if result is None: return None
        else:
            print(f"{RED_X} Invalid choice. Please enter 1, 2, or 3.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")

def display_atm_locations():
    """Displays ATM locations and handles user interaction."""
    while True:
        display_atm_locations_menu()
        branch_choice = get_user_input(f"Enter branch number (1-{len(OUR_BRANCHES)}): ", int)
        if branch_choice in ['M', 'P', None]: return branch_choice

        if 1 <= branch_choice <= len(OUR_BRANCHES):
            selected_branch = OUR_BRANCHES[branch_choice - 1]
            # Use BOLD and BLUE for section title
            print(f"\n{BOLD}{BLUE}--- ATMs at {selected_branch} ---{RESET}")
            # Use GREEN for ATM types
            print(f"{GREEN}1. Main Branch ATM (Lobby){RESET}")
            print(f"{GREEN}2. Drive-Thru ATM{RESET}")
            print(f"{GREEN}3. Shopping Mall Kiosk ATM{RESET}")
            # Use BLUE_INFO for info message
            print(f"{BLUE_INFO} For exact coordinates, please visit our website.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        else:
            print(f"{RED_X} Invalid branch choice. Please select from the list.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")


def handle_account_services_flow(current_username):
    """Handles the flow for logged-in account services."""
    while True:
        display_account_services_menu()
        service_choice = get_user_input("Enter your choice: ", int)
        if service_choice in ['M', 'P', None]: return service_choice

        # Always update loan limit when user enters account services
        # Or you can do it on specific actions like deposit, withdrawal, or upon request.
        # Let's do it on request for simplicity for now to avoid frequent updates.
        # update_loan_limit(current_username) 

        if service_choice == 1: # View Account Details
            accounts_data = read_accounts()
            user_account = accounts_data[current_username]
            user_details = user_account["details"]
            # Use BOLD and BLUE for section title
            print(f"\n{BOLD}{BLUE}--- Your Account Details ({current_username}) ---{RESET}")
            # Use BLUE for labels, default for values
            print(f"{BLUE}Account Number:{RESET} {user_details.get('account_number', 'N/A')}")
            print(f"{BLUE}Account Type:{RESET} {user_details.get('account_type_name', 'Not Set')}")
            print(f"{BLUE}Account Currency:{RESET} {user_details.get('account_currency', 'N/A')}")
            print(f"{BLUE}Current Balance:{RESET} {user_account['balance']:.2f} {user_details.get('account_currency', 'N/A')}")
            
            # Display other details
            for key, value in user_details.items():
                if key not in ['account_number', 'account_type_name', 'account_type_features', 'security_questions',
                               'payment_methods', 'payment_passcode', 'statements', 'cards', # Exclude 'cards' as it's now handled separately
                               'beneficiaries', 'loan_limit', 'active_loans', 'account_currency',
                               'monthly_deposits_expected', 'monthly_withdrawals_expected', 'monthly_balance_expected',
                               'last_loan_limit_update']: # Avoid re-printing nested dicts or already displayed info
                    print(f"{BLUE}{key.replace('_', ' ').title()}:{RESET} {value}")
            
            # Display account features if available
            if 'account_type_features' in user_details and user_details['account_type_features']:
                # Use BLUE for sub-section title
                print(f"\n{BLUE}--- Account Features ---{RESET}")
                for key, value in user_details['account_type_features'].items():
                    if key not in ["Account Name", "Currency"]: # Already displayed
                        # Use CYAN for feature names
                        print(f"  {CYAN}- {key.replace('_', ' ').title()}:{RESET} {value}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        elif service_choice == 2: # Make a Deposit
            result = deposit(current_username)
            if result in ['M', 'P', None]: return result
        elif service_choice == 3: # Make a Withdrawal
            result = withdraw(current_username)
            if result in ['M', 'P', None]: return result
        elif service_choice == 4: # View Transaction History
            view_transaction_history(current_username)
        elif service_choice == 5: # My Statements
            view_my_statements(current_username)
        elif service_choice == 6: # Add/Manage Payment Methods
            while True: # Loop for managing payment methods
                display_payment_methods_menu()
                payment_method_choice = get_user_input("Enter your choice: ", int)
                if payment_method_choice in ['M', 'P', None]: break # Go back to account services

                if 1 <= payment_method_choice <= 5: # Add payment method
                    result = add_payment_method(current_username, payment_method_choice)
                    if result is None: return None # Critical exit
                elif payment_method_choice == 6: # Set/Change Payment Passcode
                    result = set_payment_passcode(current_username)
                    if result is None: return None # Critical exit
                elif payment_method_choice == 7: # View My Payment Methods
                    view_payment_methods(current_username)
                else:
                    print(f"{RED_X} Invalid choice for payment methods.{RESET}")
                    input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
            continue # Stay in account services after managing payment methods
        elif service_choice == 7: # Manage Cards (Now calls handle_card_management_flow)
            result = handle_card_management_flow(current_username)
            if result in ['M', 'P', None]: return result
        elif service_choice == 8: # Request Services (placeholder for now)
            print(f"{BLUE_INFO} General service requests are under development.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")
        elif service_choice == 9: # Make Payments (Transfers to external methods)
            result = make_payment(current_username)
            if result in ['M', 'P', None]: return result
        elif service_choice == 10: # Check Loan Balance/Limit & Request Loan
            update_loan_limit(current_username) # Update loan limit before displaying
            accounts_data = read_accounts()
            user_details = accounts_data[current_username]["details"]
            loan_limit = user_details.get("loan_limit", 0.0)
            active_loans = user_details.get("active_loans", 0.0)
            account_currency = user_details["account_currency"]

            # Use BOLD and BLUE for section title
            print(f"\n{BOLD}{BLUE}--- Loan Information ---{RESET}")
            # Use BLUE for labels
            print(f"{BLUE}Your Loan Limit:{RESET} {loan_limit:,.2f} {account_currency}")
            print(f"{BLUE}Active Loans:{RESET} {active_loans:,.2f} {account_currency}")
            print(f"{BLUE}Available Loan:{RESET} {(loan_limit - active_loans):,.2f} {account_currency}")
            
            loan_action = get_user_input("Do you want to request a loan? (yes/no): ").lower()
            if loan_action in ['M', 'P', None]: continue
            
            if loan_action == 'yes':
                result = request_loan(current_username)
                if result in ['M', 'P', None]: return result
            else:
                input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")

        elif service_choice == 11: # Logout
            return "logout" # Signal to the calling function to log out
        else:
            print(f"{RED_X} Invalid choice. Please enter a number between 1 and 11.{RESET}")
            input(f"{BRIGHT_BLACK}Press Enter to continue...{RESET}")

# --- Main Application Loop ---

def run_banking_app():
    """Manages the main flow of the banking application."""
    current_username = None # Stores the username of the currently logged-in user

    # Use GREEN_CHECKMARK for welcome message
    print(f"{GREEN_CHECKMARK} Welcome to {BANK_NAME} - {BANK_TAGLINE} {GREEN_CHECKMARK}{RESET}")

    while True: # Outer loop for login/registration
        display_main_menu(current_username is not None)
        choice = get_user_input("Enter your choice: ", int)
        
        if choice is None: # EOFError or other critical input issue
            print(f"{BLUE_INFO}Exiting Application.{RESET}")
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
                    print(f"\n{GREEN_CHECKMARK} Login successful! Welcome, {username}!{RESET}")
                    current_username = username
                    # Ensure account is marked activated if it had 0 opening balance
                    if not accounts_data[username]["details"].get("account_type_features", {}).get("Opening balance", 0) > 0:
                        accounts_data[username]["activated"] = True
                        save_accounts(accounts_data)

                    # Display logged-in user details
                    now = datetime.datetime.now()
                    if now.hour < 12:
                        greeting = "Good morning"
                    elif 12 <= now.hour < 18:
                        greeting = "Good afternoon"
                    else:
                        greeting = "Good evening"
                    
                    user_details = accounts_data[current_username]["details"]
                    # Safely get name, default to username if not found
                    full_name = user_details.get("name", current_username)
                    surname = full_name.split()[-1] if ' ' in full_name else full_name # Get last word as surname

                    clear_screen() # Clear screen before displaying greeting
                    print(f"{GREEN}{greeting} {surname},{RESET}")
                    
                    # Center Bank Name
                    bank_name_display = f"{BOLD}{BLUE}{BANK_NAME}{RESET}"
                    # Calculate padding based on stripped length for centering
                    bank_name_padded = bank_name_display.center(50 + len(bank_name_display) - len(strip_ansi_codes(bank_name_display)))
                    print(bank_name_padded)

                    # Center Tagline
                    tagline_display = f"{ITALIC}{BLUE}{BANK_TAGLINE}{RESET}"
                    tagline_padded = tagline_display.center(50 + len(tagline_display) - len(strip_ansi_codes(tagline_display)))
                    print(tagline_padded)

                    account_number = user_details.get("account_number", "N/A")
                    current_balance = accounts_data[current_username]["balance"]
                    account_currency = user_details.get("account_currency", "KES")

                    # Use string formatting to align left and right
                    print(f"\n{BLUE}Account Number:{RESET} {account_number}")
                    # Using f-strings with alignment for balance display
                    balance_line_len = 50 # Desired total length of the line
                    currency_symbol = "" # Placeholder for currency symbol if needed later
                    
                    # Available Balance line
                    available_balance_label = f"{BLUE}Available Balance:{RESET}"
                    available_balance_value = f"{current_balance:,.2f} {account_currency}"
                    available_balance_padding = balance_line_len - len(strip_ansi_codes(available_balance_label)) - len(available_balan