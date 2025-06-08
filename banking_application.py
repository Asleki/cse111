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

# Ensure inbox files exist inside the DATA_DIR
if not os.path.exists(EMAIL_INBOX_FILE):
    with open(EMAIL_INBOX_FILE, 'w') as f:
        pass # Create an empty email inbox file
if not os.path.exists(SMS_LOG_FILE):
    with open(SMS_LOG_FILE, 'w') as f:
        pass # Create an empty SMS log file

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
EXCHANGE_RATES = {
    "KES": {
        "USD": 0.0076, "GBP": 0.0060, "EURO": 0.0070, "JPY": 1.18,
        "KES": 1.0
    },
    "USD": {
        "KES": 131.00, "GBP": 0.79, "EURO": 0.92, "JPY": 155.00,
        "USD": 1.0
    },
    "GBP": {
        "KES": 165.00, "USD": 1.27, "EURO": 1.17, "JPY": 196.00,
        "GBP": 1.0
    },
    "EURO": {
        "KES": 142.00, "USD": 1.09, "GBP": 0.85, "JPY": 168.00,
        "EURO": 1.0
    },
    "JPY": {
        "KES": 0.85, "USD": 0.0064, "GBP": 0.0051, "EURO": 0.0059,
        "JPY": 1.0
    },
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
DARK_BLUE = "\033[38;5;20m" # A deeper blue for the bank name
GREEN_CHECKMARK = f"{GREEN}\u2713{RESET}"
RED_X = f"{RED}\u2717{RESET}"
BLUE_INFO = f"{BLUE}i{RESET}"

# --- File Operations (unchanged from previous) ---
def read_accounts():
    if not os.path.exists(ACCOUNTS_FILE) or os.stat(ACCOUNTS_FILE).st_size == 0:
        return {}
    with open(ACCOUNTS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_accounts(accounts_data):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts_data, f, indent=4)

def read_transactions():
    if not os.path.exists(TRANSACTIONS_FILE) or os.stat(TRANSACTIONS_FILE).st_size == 0:
        return []
    with open(TRANSACTIONS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_transaction(timestamp, username, type, amount, currency, reference_num, description, running_balance):
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
    if os.path.exists(ACCOUNTS_FILE):
        os.remove(ACCOUNTS_FILE)
    if os.path.exists(TRANSACTIONS_FILE):
        os.remove(TRANSACTIONS_FILE)
    if os.path.exists(EMAIL_INBOX_FILE):
        os.remove(EMAIL_INBOX_FILE)
    if os.path.exists(SMS_LOG_FILE):
        os.remove(SMS_LOG_FILE)
    print(f"{YELLOW}All application data has been deleted.{RESET}")

# --- Input/Output and Utility Functions (unchanged from previous) ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input(prompt, type=str):
    while True:
        try:
            user_input = input(f"{CYAN}{prompt}{RESET}").strip()
            if user_input.upper() == 'P':
                return 'P'
            if user_input.upper() == 'M':
                return 'M'
            if not user_input:
                if type == str:
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
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def generate_otp(length=4):
    return ''.join(random.choices('0123456789', k=length))

def generate_reference_number():
    return f"TRX-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"

def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    try:
        if from_currency in EXCHANGE_RATES and to_currency in EXCHANGE_RATES[from_currency]:
            return amount * EXCHANGE_RATES[from_currency][to_currency]
        if from_currency in ["BTC", "ETH", "SOL"]:
            amount_in_usd = amount * EXCHANGE_RATES[from_currency]["USD"]
            if to_currency == "USD":
                return amount_in_usd
            else:
                return amount_in_usd * EXCHANGE_RATES["USD"][to_currency]
        if to_currency in ["BTC", "ETH", "SOL"]:
            amount_in_usd = amount * EXCHANGE_RATES[from_currency]["USD"]
            return amount_in_usd / EXCHANGE_RATES[to_currency]["USD"]
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

# --- Email and SMS Simulation (unchanged from previous) ---
def _log_communication(log_file, sender, recipient, subject, body):
    try:
        with open(log_file, 'a') as f:
            f.write(f"--- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            f.write(f"From: {sender}\n")
            f.write(f"To: {recipient}\n")
            if subject:
                f.write(f"Subject: {subject}\n")
            f.write(f"Body:\n{body}\n")
            f.write("-" * 30 + "\n\n")
    except IOError as e:
        print(f"{RED_X} ERROR: Could not write to communication log file '{log_file}'. Check permissions or path: {e}")
    except Exception as e:
        print(f"{RED_X} An unexpected error occurred during communication logging: {e}")

def send_otp_email(name, email, otp, expiry_time):
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
    sender = BANK_NAME.replace(' ', '')
    recipient = phone_number
    body = (
        f"Your {BANK_NAME} payment OTP is: {otp}. "
        f"Do not share this code. Valid for 5 mins."
    )
    _log_communication(SMS_LOG_FILE, sender, recipient, None, body)
    print(f"{GREEN_CHECKMARK} Payment OTP SMS sent to {phone_number}. Check your simulated SMS log ({SMS_LOG_FILE}).")
    return True

def send_application_form_email(email):
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
    sender = f"security@{BANK_NAME.lower().replace(' ', '')}.com"
    subject = f"{BANK_NAME} Security Questions Setup Confirmation"
    body = (
        f"Dear {name},\n\n"
        f"This email confirms that you have successfully set up your security questions for your {BANK_NAME} account.\n"
        f"Your chosen questions and answers (for your reference, do not share):\n"
    )
    for q, a in questions.items():
        body += f"- Question: {q}\n"
        body += f"   Answer: {a}\n"
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
    sender = BANK_NAME.replace(' ', '')
    body = (
        f"Congrats! Your {BANK_NAME} account {account_number} is now active. "
        f"Welcome to the family!"
    )
    _log_communication(SMS_LOG_FILE, sender, phone_number, None, body)
    return True

def send_transaction_notification(username, email, phone_number, transaction_type, amount, currency, ref_num, description, new_balance):
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

# --- OTP Verification Function (unchanged from previous) ---
def verify_otp_with_retries(target_name, contact_info, generated_otp, otp_expiry_time, max_retries=3, otp_delivery_method="email"):
    attempts = 0
    while attempts < max_retries:
        if datetime.datetime.now() > otp_expiry_time:
            print(f"{RED_X} OTP has expired. Please request a new OTP.")
            return False

        prompt = f"Enter the {otp_delivery_method} OTP ({max_retries - attempts} attempts left, P/M to go back): "
        user_otp = get_user_input(prompt, type=str)

        if user_otp in ['P', 'M']:
            return user_otp

        if not user_otp.isdigit() or len(user_otp) != len(generated_otp):
            print(f"{RED_X} Invalid OTP format. Please enter a {len(generated_otp)}-digit number.")
            attempts += 1
            continue

        if user_otp == generated_otp:
            print(f"{GREEN_CHECKMARK} OTP verified successfully!")
            return True
        else:
            attempts += 1
            if attempts < max_retries:
                print(f"{RED_X} Incorrect OTP. Please try again.")
            else:
                print(f"{RED_X} Too many incorrect OTP attempts. For security, the verification process has been cancelled.")
                print(f"{BLUE_INFO} Please restart the process or contact support if you need assistance.")
                return False
    return False

# --- Placeholder for a simplified login function (to set current_user) ---
def login_user():
    """Simulates a login process and returns a mock user object."""
    # In a real app, this would verify credentials from accounts.json
    # For demonstration, we just prompt for a username.
    print(f"\n{BOLD}{CYAN}--- User Login ---{RESET}")
    username = get_user_input("Enter your username (P/M to cancel): ")
    if username in ['P', 'M']: return None

    # Simulate fetching user data
    accounts = read_accounts()
    if username not in accounts:
        print(f"{RED_X} Username '{username}' not found. Please register or try again.{RESET}")
        time.sleep(2)
        return None

    # In a real app, you'd check password/security questions here.
    # For now, let's just assume successful login.
    print(f"{GREEN_CHECKMARK} Successfully logged in as {username}!{RESET}")
    time.sleep(1)
    return accounts[username] # Return the user's account dictionary


# --- NEW ACCOUNT HOMESCREEN / MAIN MENU ---
def display_main_menu(logged_in_user=None):
    """
    Displays the main menu options to the user,
    or the account homescreen if logged in.
    """
    clear_screen() # Clear screen for a fresh display

    # Get current time for greeting
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    screen_width = 70 # Adjust as needed for your terminal

    # --- Display Bank Name (Centered, Dark Blue) ---
    print(f"{DARK_BLUE}{BOLD}{BANK_NAME}{RESET}".center(screen_width))
    print(f"{BANK_TAGLINE}".center(screen_width))
    print("=" * screen_width)

    if logged_in_user:
        # --- LOGGED-IN HOMESCREEN ---
        username = logged_in_user.get('username', 'User') # Fallback if username missing
        account_number = logged_in_user.get('account_number', 'N/A')
        balance = logged_in_user.get('balance', 0.0)
        currency = logged_in_user.get('currency', 'KES')

        print(f"{BLUE}{greeting}, {username}!{RESET}".center(screen_width))
        print(f"Current Date: {datetime.date.today().strftime('%Y-%m-%d')}".center(screen_width))
        print(f"Account Number: {account_number}".center(screen_width))
        print("-" * screen_width)

        # Balance Display (Left and Right aligned)
        # Using string formatting for alignment
        balance_str = f"{balance:,.2f} {currency}" # Format balance with commas
        print(f"{GREEN}Available Balance: {RESET}{balance_str.rjust(screen_width - len('Available Balance: '))}")
        print(f"{GREEN}Current Balance:   {RESET}{balance_str.rjust(screen_width - len('Current Balance:   '))}")
        print("-" * screen_width)

        # Logged-in services
        print(f"{CYAN}1. Make a Deposit{RESET}")
        print(f"{CYAN}2. Make a Withdrawal{RESET}")
        print(f"{CYAN}3. Transfer Funds{RESET}")
        print(f"{CYAN}4. View Transaction History{RESET}")
        print(f"{CYAN}5. Apply for a Loan{RESET}")
        print(f"{CYAN}6. Change Password{RESET}")
        print(f"{CYAN}7. Update Contact Info{RESET}")
        print(f"{CYAN}8. Logout{RESET}")
        print("-" * screen_width)
    else:
        # --- GENERAL MAIN MENU (NOT LOGGED IN) ---
        print(f"{BOLD}{CYAN}--- MAIN MENU ---{RESET}".center(screen_width))
        print("=" * screen_width)
        print(f"{CYAN}1. Open A Bank Account{RESET}")
        print(f"{CYAN}2. Explore Our Offers{RESET}")
        print(f"{CYAN}3. Login to Your Account{RESET}")
        print(f"{CYAN}4. Exit Program{RESET}")
        print("-" * screen_width)

# --- Placeholder Function for New Account Registration ---
def register_new_account():
    clear_screen()
    print(f"{BOLD}{BLUE_INFO}--- New Account Registration ---{RESET}")

    customer_name = get_user_input("Enter your full name (P/M to go back): ")
    if customer_name in ['P', 'M']: return customer_name

    customer_email = get_user_input("Enter your email address: ")
    if customer_email in ['P', 'M']: return customer_email
    if not is_valid_email(customer_email):
        print(f"{RED_X} Invalid email format. Please enter a valid email address.")
        time.sleep(2)
        return False

    customer_phone = get_user_input("Enter your phone number (e.g., +254...): ")
    if customer_phone in ['P', 'M']: return customer_phone

    # Simulate OTP generation and sending
    print(f"\n{BLUE_INFO} Sending OTP to {customer_email} for verification...{RESET}")
    otp_code = generate_otp(length=4) # Using the simpler 4-digit OTP
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
        # Here you would actually create the user account in accounts.json
        # For this example, let's create a dummy account entry immediately
        accounts_data = read_accounts()
        new_account_number = f"ACC{random.randint(100000, 999999)}"
        accounts_data[customer_name] = {
            'username': customer_name,
            'email': customer_email,
            'phone': customer_phone,
            'account_number': new_account_number,
            'password': 'password123', # In a real app, hash this!
            'balance': 5000.00,
            'currency': 'KES',
            'account_type': 'Savings',
            'branch': random.choice(OUR_BRANCHES)
        }
        save_accounts(accounts_data)

        # Simulate sending activation emails/SMS
        send_account_activation_email(customer_name, customer_email, new_account_number, accounts_data[customer_name], accounts_data[customer_name]['branch'])
        send_activation_sms(customer_phone, new_account_number)

        print(f"{GREEN_CHECKMARK} Account registration complete! Your account number is {new_account_number}.{RESET}")
        print(f"{BLUE_INFO} You can now log in using '{customer_name}'.{RESET}")
        time.sleep(3)
        return True
    elif otp_verified in ['P', 'M']:
        print(f"{BLUE_INFO} OTP verification cancelled. Returning to previous menu.{RESET}")
        time.sleep(2)
        return otp_verified
    else:
        print(f"{RED_X} Account registration aborted due to OTP verification failure.{RESET}")
        time.sleep(2)
        return False

# --- Main Application Loop ---
def main():
    logged_in_user = None # This will hold the dict of the currently logged-in user

    while True:
        display_main_menu(logged_in_user)
        
        if logged_in_user:
            # Options for logged-in user
            choice = get_user_input("Enter your choice: ", int)
            if choice == 8: # Logout
                logged_in_user = None
                print(f"{BLUE_INFO} You have been logged out.{RESET}")
                time.sleep(1)
            elif choice == 1:
                print(f"{BLUE_INFO} Deposit functionality selected. (Not yet implemented){RESET}")
                get_user_input("Press Enter to continue...")
            elif choice == 2:
                print(f"{BLUE_INFO} Withdrawal functionality selected. (Not yet implemented){RESET}")
                get_user_input("Press Enter to continue...")
            elif choice == 3:
                print(f"{BLUE_INFO} Transfer functionality selected. (Not yet implemented){RESET}")
                get_user_input("Press Enter to continue...")
            elif choice == 4:
                print(f"{BLUE_INFO} Transaction History functionality selected. (Not yet implemented){RESET}")
                get_user_input("Press Enter to continue...")
            elif choice == 5:
                print(f"{BLUE_INFO} Loan Application functionality selected. (Not yet implemented){RESET}")
                get_user_input("Press Enter to continue...")
            elif choice == 6:
                print(f"{BLUE_INFO} Change Password functionality selected. (Not yet implemented){RESET}")
                get_user_input("Press Enter to continue...")
            elif choice == 7:
                print(f"{BLUE_INFO} Update Contact Info functionality selected. (Not yet implemented){RESET}")
                get_user_input("Press Enter to continue...")
            else:
                print(f"{RED_X} Invalid choice. Please enter a valid option.{RESET}")
                time.sleep(1)
        else:
            # Options for not logged-in user
            choice = get_user_input("Enter your choice: ", int)
            if choice == 1: # Open A Bank Account
                reg_status = register_new_account()
                # If registration is successful, automatically log in the user for convenience
                if reg_status == True:
                    accounts = read_accounts()
                    # Find the newly created user (simplistic, in real app you'd get their username/password)
                    # For this example, we'll assume the last registered user is the one to log in
                    # This is NOT robust for a multi-user system, just for this demo.
                    last_username = list(accounts.keys())[-1] if accounts else None
                    if last_username:
                        logged_in_user = accounts[last_username]
                        print(f"{GREEN_CHECKMARK} Automatically logged in as {last_username}.{RESET}")
                        time.sleep(1)
                elif reg_status in ['P', 'M']:
                    # User cancelled registration, remain at general main menu
                    pass
                else: # reg_status is False (OTP failed)
                    pass # Error message already printed by register_new_account
                # get_user_input("\nPress Enter to continue...") # No need, login prompt handles it
                continue # Go back to the top of the loop to display menu again
            elif choice == 2:
                print(f"{BLUE_INFO} Exploring offers... (Not yet implemented){RESET}")
                get_user_input("Press Enter to continue...")
            elif choice == 3: # Login to your account
                logged_in_user = login_user() # Attempt to log in
                if logged_in_user:
                    print(f"{GREEN_CHECKMARK} Login successful! Welcome, {logged_in_user['username']}!{RESET}")
                    time.sleep(1)
                else:
                    print(f"{RED_X} Login failed or cancelled.{RESET}")
                    time.sleep(1)
            elif choice == 4: # Exit program
                print(f"{BLUE_INFO} Thank you for banking with {BANK_NAME}. Goodbye!{RESET}")
                break
            else:
                print(f"{RED_X} Invalid choice. Please enter a number from the menu.{RESET}")
                time.sleep(1)


# --- Run the application ---
if __name__ == "__main__":
    main()