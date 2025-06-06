import random
import datetime
import re
import os
import time

# --- Constants and Global Variables ---
BANK_NAME = "Python Bank Bank"
BANK_TAGLINE = "Your Future, Our Priority"
RED_X = "❌"
GREEN_CHECKMARK = "✅"
BLUE_INFO = "ℹ️"
OUR_BRANCHES = ["La Familia Nairobi Main", "La Familia Mombasa Branch", "La Familia Kisumu Lakeside", "Nakuru Downtown"]
EMAIL_INBOX_FILE = "email_inbox.txt"
MESSAGES_INBOX_FILE = "messages_inbox.txt"
ACCOUNTS_FILE = "bank_accounts.csv"
TRANSACTIONS_FILE = "transactions.csv"
USD_TO_KES_RATE = 135.0 # Example exchange rate for currency conversion

# Ensure inbox files exist
if not os.path.exists(EMAIL_INBOX_FILE):
    with open(EMAIL_INBOX_FILE, 'w') as f:
        pass
if not os.path.exists(MESSAGES_INBOX_FILE):
    with open(MESSAGES_INBOX_FILE, 'w') as f:
        pass

SECURITY_QUESTIONS = {
    1: "What was your first pet's name?",
    2: "What was your best sport in primary school?",
    3: "What was the first city you travelled to?",
}

# --- Helper Functions ---

def get_user_input(prompt, input_type=str):
    """
    Prompts the user for input and handles special commands 'M' and 'P'.
    Also handles ValueError for type conversion.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input.upper() == 'M':
                return 'M'
            if user_input.upper() == 'P':
                return 'P'
            if input_type == int:
                return int(user_input)
            if input_type == float:
                return float(user_input)
            return user_input
        except ValueError:
            print(f"{RED_X} Invalid input. Please enter a valid {input_type.__name__}.")
        except EOFError:
            print(f"{RED_X} End of input detected. Exiting.")
            return None # Indicate a critical exit

def is_valid_email(email):
    """Checks if the email is valid using a simple regex."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def generate_otp():
    """Generates a simple 6-digit OTP."""
    return ''.join(random.choices('0123456789', k=6))

def generate_payment_passcode_otp():
    """Generates a simple 6-digit OTP for payment passcode verification."""
    return ''.join(random.choices('0123456789', k=6))

def generate_reference_number():
    """Generates a reference number in the format KESU-(6digits ending with a letter)."""
    digits = ''.join(random.choices('0123456789', k=5))
    letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return f"KESU-{digits}{letter}"

def send_otp_email(customer_name, email, otp, expiration_time):
    """Sends an OTP email to the given email, including expiry."""
    try:
        with open(EMAIL_INBOX_FILE, 'a') as f:
            f.write(f"\n--- New Email ---\n")
            f.write(f"Date: {datetime.date.today().isoformat()}\n")
            f.write(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n")
            f.write(f"From: noreply@{BANK_NAME.lower().replace(' ', '')}.com\n")
            f.write(f"To: {email}\n")
            f.write(f"Subject: Your {BANK_NAME} OTP for Account Registration\n")
            f.write(f"\nDear {customer_name},\n\n")
            f.write(f"Your One-Time Password (OTP) for {BANK_NAME} account registration is: {otp}\n")
            f.write(f"This OTP is valid for 5 minutes and will expire at {expiration_time.strftime('%H:%M:%S')}.\n")
            f.write(f"Please do not share this OTP with anyone.\n\n")
            f.write(f"Thank you for choosing {BANK_NAME} - {BANK_TAGLINE}\n")
            f.write(f"-------------------\n")
        print(f"{GREEN_CHECKMARK} OTP sent to {email}. Please check your email inbox.")
        return True
    except IOError:
        print(f"{RED_X} Error: Could not write to email inbox file.")
        return False

def send_application_form_email(email):
    """Simulates sending an application form to the given email."""
    try:
        with open(EMAIL_INBOX_FILE, 'a') as f:
            f.write(f"\n--- New Email ---\n")
            f.write(f"Date: {datetime.date.today().isoformat()}\n")
            f.write(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n")
            f.write(f"From: noreply@{BANK_NAME.lower().replace(' ', '')}.com\n")
            f.write(f"To: {email}\n")
            f.write(f"Subject: {BANK_NAME} Account Application Form\n")
            f.write(f"\nDear Customer,\n\n")
            f.write(f"We appreciate your interest in starting a financial journey with us.\n")
            f.write(f"Attached to this email is your application form. Please download it, fill it carefully, \n")
            f.write(f"and then scan the signed copy back to us.\n\n")
            f.write(f"Thank you for choosing {BANK_NAME} - {BANK_TAGLINE}\n")
            f.write(f"-------------------\n")
        return True
    except IOError:
        return False

def send_security_questions_email(customer_name, email, security_q_a):
    """Sends an email confirming security questions setup."""
    try:
        with open(EMAIL_INBOX_FILE, 'a') as f:
            f.write(f"\n--- New Email ---\n")
            f.write(f"Date: {datetime.date.today().isoformat()}\n")
            f.write(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n")
            f.write(f"From: noreply@{BANK_NAME.lower().replace(' ', '')}.com\n")
            f.write(f"To: {email}\n")
            f.write(f"Subject: {BANK_NAME} Security Questions Setup Confirmation\n")
            f.write(f"\nDear {customer_name},\n\n")
            f.write(f"This is to confirm that your security questions have been successfully set up for your {BANK_NAME} account.\n")
            f.write(f"These questions will help you reset your password or username if needed.\n\n")
            f.write(f"Your selected security questions are:\n")
            for q, a in security_q_a.items():
                f.write(f"- {q}\n") # Only display the question, not the answer
            f.write(f"\nThank you for enhancing the security of your account with {BANK_NAME} - {BANK_TAGLINE}\n")
            f.write(f"-------------------\n")
        print(f"{GREEN_CHECKMARK} Security questions setup confirmation email sent to {email}.")
        return True
    except IOError:
        print(f"{RED_X} Error: Could not write security questions confirmation email.")
        return False

def send_account_activation_email(username, email, account_number, account_type_details, branch):
    """Sends a detailed welcome email upon account activation."""
    try:
        with open(EMAIL_INBOX_FILE, 'a') as f:
            f.write(f"\n--- New Email ---\n")
            f.write(f"Date: {datetime.date.today().isoformat()}\n")
            f.write(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n")
            f.write(f"From: noreply@{BANK_NAME.lower().replace(' ', '')}.com\n")
            f.write(f"To: {email}\n")
            f.write(f"Subject: Your {BANK_NAME} Account is Now Active! - Welcome!\n")
            f.write(f"\nDear {username},\n\n")
            f.write(f"Congratulations! Your {BANK_NAME} account has been successfully activated.\n\n")
            f.write(f"Here are your account details:\n")
            f.write(f"  Account Holder: {username}\n")
            f.write(f"  Account Number: {account_number}\n")
            f.write(f"  Account Type: {account_type_details.get('Account Name', 'N/A')}\n")
            f.write(f"  Branch: {branch}\n\n")
            
            f.write(f"Features of your {account_type_details.get('Account Name', 'N/A')}:\n")
            for key, value in account_type_details.items():
                if key not in ["Account Name"]: # Avoid re-printing
                    f.write(f"  - {key.replace('_', ' ').title()}: {value}\n")
            
            f.write(f"\nWe are thrilled to have you as part of the {BANK_NAME} family. Enjoy seamless banking with us!\n")
            f.write(f"For any queries, please do not reply to this email. Contact our customer support directly.\n\n")
            f.write(f"Thank you for choosing {BANK_NAME} - {BANK_TAGLINE}\n")
            f.write(f"-------------------\n")
        print(f"{GREEN_CHECKMARK} Account activation confirmation email sent to {email}.")
        return True
    except IOError:
        print(f"{RED_X} Error: Could not write account activation email.")
        return False

def send_activation_sms(phone_number, account_number):
    """Sends an SMS notification upon account activation."""
    try:
        with open(MESSAGES_INBOX_FILE, 'a') as f:
            f.write(f"\n--- New SMS ---\n")
            f.write(f"Date: {datetime.date.today().isoformat()}\n")
            f.write(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n")
            f.write(f"To: {phone_number}\n")
            f.write(f"From: {BANK_NAME}\n")
            f.write(f"Message: Your {BANK_NAME} account ({account_number}) is active! To deposit, use Paybill 234765, Acc No: {account_number}. We are excited to serve you!\n")
            f.write(f"-------------------\n")
        print(f"{GREEN_CHECKMARK} Account activation SMS sent to your phone number.")
        return True
    except IOError:
        print(f"{RED_X} Error: Could not write SMS to inbox file.")
        return False

def send_payment_otp_sms(phone_number, otp):
    """Sends an OTP SMS for payment passcode verification."""
    try:
        with open(MESSAGES_INBOX_FILE, 'a') as f:
            f.write(f"\n--- New SMS ---\n")
            f.write(f"Date: {datetime.date.today().isoformat()}\n")
            f.write(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n")
            f.write(f"To: {phone_number}\n")
            f.write(f"From: {BANK_NAME}\n")
            f.write(f"Message: Your {BANK_NAME} Payment Passcode verification OTP is: {otp}. Do not share this code.\n")
            f.write(f"-------------------\n")
        print(f"{GREEN_CHECKMARK} Payment verification OTP sent to your phone number (check {MESSAGES_INBOX_FILE}).")
        return True
    except IOError:
        print(f"{RED_X} Error: Could not write payment OTP SMS to inbox file.")
        return False

def send_deposit_email_statement(username, email, bank_account_number, amount, payment_method, reference_number, balance_after_deposit):
    """Generates and 'sends' a detailed e-statement email after a deposit, also returning its content for storage."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    statement_content = f"""
--- New Email (E-Statement) ---
Date: {datetime.date.today().isoformat()}
Time: {datetime.datetime.now().strftime('%H:%M:%S')}
From: noreply@{BANK_NAME.lower().replace(' ', '')}.com
To: {email}
Subject: {BANK_NAME} Deposit Confirmation - Reference: {reference_number}

Dear {username},

This is to confirm a successful deposit into your {BANK_NAME} account.

Transaction Details:
  Reference Number: {reference_number}
  Date & Time: {timestamp}
  Bank Account Number: {bank_account_number}
  Amount Deposited: KES {amount:,.2f}
  Payment Method: {payment_method}
  Current Bank Account Balance: KES {balance_after_deposit:,.2f}

Thank you for banking with {BANK_NAME} - {BANK_TAGLINE}
-------------------------------
"""
    try:
        with open(EMAIL_INBOX_FILE, 'a') as f:
            f.write(statement_content)
        print(f"{GREEN_CHECKMARK} Deposit confirmation email (e-statement) sent to {email}.")
        return statement_content # Return content to store in user's statements
    except IOError:
        print(f"{RED_X} Error: Could not write deposit confirmation email statement.")
        return None

def send_deposit_sms(phone_number, amount, bank_account_number):
    """Sends an SMS notification after a deposit."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(MESSAGES_INBOX_FILE, 'a') as f:
            f.write(f"\n--- New SMS ---\n")
            f.write(f"Date: {datetime.date.today().isoformat()}\n")
            f.write(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n")
            f.write(f"To: {phone_number}\n")
            f.write(f"From: {BANK_NAME}\n")
            f.write(f"Message: KES {amount:,.2f} deposited to Acc {bank_account_number} at {timestamp}. Thank you for choosing {BANK_NAME}!\n")
            f.write(f"-------------------\n")
        print(f"{GREEN_CHECKMARK} Deposit confirmation SMS sent to your phone number.")
        return True
    except IOError:
        print(f"{RED_X} Error: Could not write deposit SMS to inbox file.")
        return False

def read_accounts():
    """Reads user accounts from the CSV file."""
    accounts = {}
    if not os.path.exists(ACCOUNTS_FILE):
        return accounts
    with open(ACCOUNTS_FILE, 'r') as f:
        for line in f:
            try:
                username, data_str = line.strip().split(',', 1)
                data = eval(data_str) # Safely parse the dictionary string
                accounts[username] = data
            except (SyntaxError, ValueError, IndexError) as e:
                print(f"{RED_X} Error parsing account data in {ACCOUNTS_FILE}: {e} for line: {line.strip()}")
                continue # Skip corrupted line and try next
    return accounts

def save_accounts(accounts_data):
    """Saves user accounts to the CSV file."""
    try:
        with open(ACCOUNTS_FILE, 'w') as f:
            for username, data in accounts_data.items():
                f.write(f"{username},{data}\n")
    except IOError:
        print(f"{RED_X} Error: Could not save accounts data.")

def save_transaction(timestamp, username, type, amount, description=""):
    """Saves a transaction record to the transactions CSV file."""
    try:
        with open(TRANSACTIONS_FILE, 'a') as f:
            f.write(f"{timestamp},{username},{type},{amount},{description}\n")
    except IOError:
        print(f"{RED_X} Error: Could not save transaction.")

def display_token(service_choice):
    """Displays a simulated token for the selected service."""
    service_name = get_service_name(service_choice)
    token_number = random.randint(100, 999)
    wait_time = random.randint(2, 10) # Simulate random wait time
    print("\n" + "=" * 50)
    print(f"YOUR TOKEN".center(50))
    print("=" * 50)
    print(f"Service: {service_name}".center(50))
    print(f"Token Number: {token_number}".center(50))
    print(f"Estimated Wait: {wait_time} minutes".center(50))
    print("=" * 50)
    if service_choice == 1: # Special requirements for opening new account
        print(f"{BLUE_INFO} Please ensure you have your original ID/Passport, KRA PIN, and a recent utility bill.")
    input("Press Enter to continue...")

def get_service_name(service_choice):
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
    return services.get(service_choice, "Unknown Service")

def currency_converter(amount, from_currency, to_currency):
    """Simple currency converter between USD and KES."""
    if from_currency == to_currency:
        return amount

    if from_currency == "USD" and to_currency == "KES":
        return amount * USD_TO_KES_RATE
    elif from_currency == "KES" and to_currency == "USD":
        return amount / USD_TO_KES_RATE
    else:
        print(f"{RED_X} Unsupported currency conversion: {from_currency} to {to_currency}")
        return None

def deposit(username):
    """Handles the deposit process for a given user using payment methods, including passcode and currency conversion."""
    accounts_data = read_accounts()
    if username not in accounts_data:
        print(f"{RED_X} Account not found.")
        return 'P' # Go back to previous menu
    
    user_details = accounts_data[username]["details"]
    payment_methods = user_details.get("payment_methods", [])

    if not payment_methods:
        print(f"{RED_X} No payment methods added. Please add one first from 'Add/Manage Payment Methods' menu.")
        input("Press Enter to continue...")
        return 'P'

    # --- Verify Payment Passcode First ---
    if "payment_passcode" not in user_details or not user_details["payment_passcode"]:
        print(f"{RED_X} You need to set a 6-digit Payment Authorization Passcode before making a deposit.")
        print(f"{BLUE_INFO} Go to 'Add/Manage Payment Methods' -> 'Set/Change Payment Passcode' to set it up.")
        input("Press Enter to continue...")
        return 'P'

    tries = 3
    while tries > 0:
        entered_passcode = get_user_input("Enter your 6-digit Payment Authorization Passcode: ")
        if entered_passcode == 'M': return 'M'
        if entered_passcode == 'P': return 'P'
        if entered_passcode is None: return None

        if entered_passcode == user_details["payment_passcode"]:
            print(f"{GREEN_CHECKMARK} Passcode verified.")
            break
        else:
            tries -= 1
            print(f"{RED_X} Incorrect passcode. {tries} attempts remaining.")
            if tries == 0:
                print(f"{RED_X} Too many incorrect attempts. Returning to previous menu.")
                input("Press Enter to continue...")
                return 'P' # Return to previous menu after failed attempts

    # --- Select Payment Method ---
    print("\n--- Select Payment Method for Deposit ---")
    for i, method in enumerate(payment_methods, 1):
        print(f"{i}. {method['name']} (Balance: {method['balance']:.2f} {method['currency']})")
    
    while True:
        method_choice = get_user_input(f"Select a payment method (1-{len(payment_methods)}): ", int)
        if method_choice == 'M': return 'M'
        if method_choice == 'P': return 'P'
        if method_choice is None: return None

        if 1 <= method_choice <= len(payment_methods):
            selected_method = payment_methods[method_choice - 1]
            break
        else:
            print(f"{RED_X} Invalid choice. Please select a valid number.")

    while True:
        amount_to_deposit = get_user_input("Enter amount to deposit from selected payment method: ", float)
        if amount_to_deposit == 'M': return 'M'
        if amount_to_deposit == 'P': return 'P'
        if amount_to_deposit is None: return None

        if amount_to_deposit <= 0:
            print(f"{RED_X} Deposit amount must be positive.")
            continue

        if amount_to_deposit > selected_method['balance']:
            print(f"{RED_X} Insufficient balance in {selected_method['name']}. Available: {selected_method['balance']:.2f} {selected_method['currency']}")
            continue
        
        # Currency Conversion if needed
        converted_amount = amount_to_deposit
        bank_account_currency = user_details.get('account_type_features', {}).get('Currency', 'KES') # Default to KES
        
        if selected_method['currency'] != bank_account_currency:
            print(f"{BLUE_INFO} Converting {amount_to_deposit:.2f} {selected_method['currency']} to {bank_account_currency}...")
            converted_amount = currency_converter(amount_to_deposit, selected_method['currency'], bank_account_currency)
            if converted_amount is None:
                print(f"{RED_X} Currency conversion failed. Aborting deposit.")
                return 'P'
            print(f"{BLUE_INFO} Converted amount: {bank_account_currency} {converted_amount:,.2f}")

        # Proceed with deposit
        selected_method['balance'] -= amount_to_deposit # Deduct from payment method
        accounts_data[username]["balance"] += converted_amount # Add to bank account
        
        save_accounts(accounts_data) # Save updated payment method balance and bank account balance
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_transaction(timestamp, username, "deposit", converted_amount, f"Deposit of {bank_account_currency} {converted_amount:.2f} from {selected_method['name']}")
        
        # Send Notifications and store statement
        reference_number = generate_reference_number()
        email_statement_content = send_deposit_email_statement(
            username, 
            user_details['email'], 
            user_details['account_number'], 
            converted_amount, # Amount in KES after conversion
            selected_method['name'], 
            reference_number, 
            accounts_data[username]['balance'] # New bank account balance
        )
        
        if email_statement_content:
            # Ensure 'statements' list exists and append
            accounts_data[username]["details"].setdefault("statements", []).append(email_statement_content)
            save_accounts(accounts_data) # Save accounts again to persist the statement
        
        send_deposit_sms(user_details['phone_number'], converted_amount, user_details['account_number'])

        print(f"{GREEN_CHECKMARK} Successfully deposited {bank_account_currency} {converted_amount:.2f} from {selected_method['name']}.")
        print(f"New bank account balance: {bank_account_currency} {accounts_data[username]['balance']:.2f}")
        input("Press Enter to continue...")
        return True # Indicate success

def withdraw(username):
    """Handles the withdrawal process for a given user."""
    accounts_data = read_accounts()
    if username not in accounts_data:
        print(f"{RED_X} Account not found.")
        return 'P' # Go back to previous menu
    
    while True:
        amount = get_user_input("Enter amount to withdraw: ", float)
        if amount == 'M': return 'M'
        if amount == 'P': return 'P'
        if amount is None: return None

        if amount <= 0:
            print(f"{RED_X} Withdrawal amount must be positive.")
        elif amount > accounts_data[username]["balance"]:
            print(f"{RED_X} Insufficient balance. Current balance: KES {accounts_data[username]['balance']:.2f}")
        else:
            accounts_data[username]["balance"] -= amount
            save_accounts(accounts_data)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_transaction(timestamp, username, "withdrawal", -amount, f"Withdrawal of KES {amount:.2f}") # Negative for withdrawal
            print(f"{GREEN_CHECKMARK} Successfully withdrew KES {amount:.2f}. New balance: KES {accounts_data[username]['balance']:.2f}")
            input("Press Enter to continue...")
            return True # Indicate success

def view_transaction_history(username):
    """Displays the transaction history for a given user."""
    transactions = []
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 4 and parts[1] == username:
                    transactions.append(parts)
    
    if not transactions:
        print(f"{BLUE_INFO} No transaction history available for {username}.")
    else:
        print("\n--- Your Transaction History ---")
        for tx in transactions:
            print(f"Timestamp: {tx[0]}, Type: {tx[2]}, Amount: {float(tx[3]):.2f}, Description: {tx[4] if len(tx) > 4 else 'N/A'}")
    input("Press Enter to continue...")

def view_my_statements(username):
    """Displays stored e-statements for a given user."""
    accounts_data = read_accounts()
    if username not in accounts_data:
        print(f"{RED_X} Account not found.")
        return 'P'

    user_details = accounts_data[username]["details"]
    statements = user_details.get("statements", [])

    if not statements:
        print(f"{BLUE_INFO} No e-statements available for your account yet.")
    else:
        print("\n--- Your E-Statements ---")
        for i, statement in enumerate(statements, 1):
            print(f"\n----- Statement {i} -----")
            print(statement)
            print(f"------------------------")
    input("Press Enter to continue...")

def display_atm_locations():
    """Handles the display of ATM locations."""
    while True:
        display_atm_locations_menu()
        branch_choice = get_user_input(f"Select a branch to see ATMs (1-{len(OUR_BRANCHES)}): ", int)
        if branch_choice == 'M': return 'M'
        if branch_choice == 'P': return 'P'
        if branch_choice is None: return None

        if 1 <= branch_choice <= len(OUR_BRANCHES):
            selected_branch = OUR_BRANCHES[branch_choice - 1]
            print(f"\n--- ATMs for {selected_branch} ---")
            print(f"{BLUE_INFO} ATMs are available at {selected_branch} branch and nearby locations.")
            print(f"{BLUE_INFO} Visit our website or contact customer care for exact coordinates.")
            input("Press Enter to continue...")
        else:
            print(f"{RED_X} Invalid branch choice.")
            input("Press Enter to continue...")

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
        print("3. Login to your account")
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

def get_account_type_details(account_type_choice):
    """
    Returns the details of a selected bank account type.
    Args:
        account_type_choice (int): The account type selected by the user.
    Returns:
        dict: A dictionary of account details, or None if invalid type.
    """
    if account_type_choice == 1:
        return {"Account Name": "Current Bank account", "Currency": "Ksh", "Opening balance": 0, "Monthly maintenance fee": 0,
                   "Minimum balance": 0, "Bank Transfers fees": 0.5, "ATM withdrawal charges": 0.3,
                   "Free monthly e-statements": True, "Debit card": "5"}
    elif account_type_choice == 2:
        return {"Account Name": "Club Account", "Currency": "Ksh", "Opening balance": 59, "Monthly maintenance fee": 12,
                   "Minimum balance": 0, "Bank Transfers fees": 0.5, "ATM withdrawal charges": 0.3,
                   "Free monthly e-statements": True, "Free Debit MasterCard": True, "Free Cheque book": True}
    elif account_type_choice == 3:
        return {"Account Name": "PayGo account", "Currency": "Ksh", "Opening balance": 0, "Monthly maintenance fee": 0,
                   "Minimum balance": 0, "Bank Transfers fees": 0.5, "ATM withdrawal charges": 0.3,
                   "Free monthly e-statements": True, "Free Debit MasterCard": True, "Free Cheque book": True}
    elif account_type_choice == 4:
        return {"Account Name": "Sapphire Multi currency account", "Currency": "USD", "Opening balance": 100,
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

def display_atm_locations_menu():
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

def display_account_services_menu():
    """Displays the menu for account services."""
    print("\n" + "=" * 50)
    print("Account Services".center(50))
    print("=" * 50)
    print("1. View Account Details")
    print("2. Make a Deposit")
    print("3. Make a Withdrawal")
    print("4. View Transaction History")
    print("5. My Statements") # New
    print("6. Add/Manage Payment Methods") # New
    print("7. Manage Cards")
    print("8. Request Services")
    print("9. Make Payments")
    print("10. Check Loan Balance/Limit")
    print("11. Logout")
    print("-" * 50)

def display_payment_methods_menu():
    """Displays the menu for managing payment methods."""
    print("\n" + "=" * 50)
    print("Add/Manage Payment Methods".center(50))
    print("=" * 50)
    print("1. Add M-Pesa")
    print("2. Add Airtel Money")
    print("3. Add Bank Transfer")
    print("4. Add PayPal")
    print("5. Add Crypto Wallet (Bitcoin, Ethereum, Solana)")
    print("6. Set/Change Payment Passcode")
    print("7. View My Payment Methods")
    print("P. Go back to previous menu")
    print("M. Go to main menu")
    print("-" * 50)

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
            generated_otp = generate_payment_passcode_otp()
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
    currency = "KES"
    default_balance = 150.0 # Default balance for all methods

    if method_type == 1: # M-Pesa
        method_name = "M-Pesa"
        phone_number = get_user_input("Enter M-Pesa phone number (e.g., 254712345678): ")
        if phone_number == 'M': return 'M'
        if phone_number == 'P': return 'P'
        if phone_number is None: return None
        # Basic validation for phone number
        if not (phone_number.isdigit() and len(phone_number) >= 9):
            print(f"{RED_X} Invalid phone number format.")
            input("Press Enter to continue...")
            return False
        
        # Check if already added
        if any(pm['name'] == method_name and pm['identifier'] == phone_number for pm in payment_methods):
            print(f"{BLUE_INFO} This M-Pesa account is already linked.")
            input("Press Enter to continue...")
            return False

        payment_methods.append({
            "name": method_name,
            "identifier": phone_number,
            "currency": currency,
            "balance": default_balance
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

        payment_methods.append({
            "name": method_name,
            "identifier": phone_number,
            "currency": currency,
            "balance": default_balance
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

        payment_methods.append({
            "name": method_name,
            "bank_name": bank_name,
            "identifier": account_no,
            "currency": currency,
            "balance": default_balance
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
            "balance": default_balance
        })
    elif method_type == 5: # Crypto Wallet
        method_name = "Crypto Wallet"
        print("\n--- Choose Cryptocurrency ---")
        print("1. Bitcoin (BTC)")
        print("2. Ethereum (ETH)")
        print("3. Solana (SOL)")
        crypto_choice = get_user_input("Select crypto type: ", int)
        if crypto_choice == 'M': return 'M'
        if crypto_choice == 'P': return 'P'
        if crypto_choice is None: return None

        crypto_type = ""
        if crypto_choice == 1: crypto_type = "Bitcoin"
        elif crypto_choice == 2: crypto_type = "Ethereum"
        elif crypto_choice == 3: crypto_type = "Solana"
        else:
            print(f"{RED_X} Invalid crypto choice.")
            input("Press Enter to continue...")
            return False
        
        wallet_address = get_user_input(f"Enter {crypto_type} wallet address: ")
        if wallet_address == 'M': return 'M'
        if wallet_address == 'P': return 'P'
        if wallet_address is None: return None

        if any(pm['name'] == method_name and pm['crypto_type'] == crypto_type and pm['identifier'] == wallet_address for pm in payment_methods):
            print(f"{BLUE_INFO} This Crypto Wallet is already linked.")
            input("Press Enter to continue...")
            return False

        payment_methods.append({
            "name": method_name,
            "crypto_type": crypto_type,
            "identifier": wallet_address,
            "currency": "USD", # Crypto assumed to be in USD equivalent
            "balance": default_balance
        })
    else:
        print(f"{RED_X} Invalid payment method choice.")
        input("Press Enter to continue...")
        return False

    accounts_data[username]["details"]["payment_methods"] = payment_methods
    save_accounts(accounts_data)
    print(f"{GREEN_CHECKMARK} {method_name} added successfully with a default balance of {default_balance:.2f} {currency}!")
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
                identifier_display = f"Type: {method.get('crypto_type', 'N/A')}, Addr: {method.get('identifier', 'N/A')}"

            print(f"{i}. {method['name']} - {identifier_display} (Balance: {method['balance']:.2f} {method['currency']})")
    input("Press Enter to continue...")

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

    monthly_deposits = get_user_input("Enter number of monthly deposits: ", int)
    if monthly_deposits == 'M' or monthly_deposits == 'P': return monthly_deposits
    if monthly_deposits is None: return None

    monthly_withdrawals = get_user_input("Enter number of monthly withdrawals: ", int)
    if monthly_withdrawals == 'M' or monthly_withdrawals == 'P': return monthly_withdrawals
    if monthly_withdrawals is None: return None
    while monthly_withdrawals > monthly_deposits:
        print(f"{RED_X} Withdrawals should not be more than deposits. Please enter again.")
        monthly_withdrawals = get_user_input("Enter number of monthly withdrawals: ", int)
        if monthly_withdrawals == 'M' or monthly_withdrawals == 'P': return monthly_withdrawals
        if monthly_withdrawals is None: return None
    
    monthly_balance = get_user_input("Enter monthly balance you intend to maintain: ", float)
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

    full_phone_number = country_code + phone_number

    if not send_otp_email(name, email, generated_otp, otp_expiration_time):
        print(f"{RED_X} Failed to send OTP email. Account creation aborted.")
        return False # Indicate failure
    
    entered_otp = get_user_input("Enter the OTP you received (expires in 5 minutes): ")
    if entered_otp == 'M' or entered_otp == 'P': return entered_otp
    if entered_otp is None: return None

    current_time = datetime.datetime.now()

    if entered_otp == generated_otp and current_time < otp_expiration_time:
        print(f"{GREEN_CHECKMARK} Your details have been successfully verified and saved!")
        
        # --- Account Activation Logic ---
        initial_balance_needed = account_type_details.get("Opening balance", 0.0)
        actual_initial_deposit = 0.0
        account_activated = False

        if initial_balance_needed > 0:
            print(f"{BLUE_INFO} This account type requires an opening balance of KES {initial_balance_needed:,.2f}.")
            print(f"{BLUE_INFO} You will need to deposit this amount to fully activate your account.")
            
            # The previous confusing question is replaced by this clear instruction.
            # Account is created, but considered not fully activated until the deposit is made.
            actual_initial_deposit = 0.0 # Account starts with 0 balance for now
            account_activated = False # Will need to activate via deposit later
            print(f"{BLUE_INFO} Your account will be created. Please note that you must deposit KES {initial_balance_needed:,.2f} to fully activate it.")
            print(f"{BLUE_INFO} You can do this from 'Account Services' -> 'Make a Deposit' after logging in.")
            input("Press Enter to continue...") # Pause for user to read

        else: # Opening balance is 0
            actual_initial_deposit = 0.0
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
            "monthly_deposits": monthly_deposits,
            "monthly_withdrawals": monthly_withdrawals,
            "monthly_balance": monthly_balance,
            "application_date": datetime.date.today().isoformat(),
            "address": address,
            "branch": my_branch,
            "account_number": account_number,
            "account_type_name": account_type_details.get('Account Name', 'N/A'),
            "account_type_features": account_type_details, # Store all features
            "security_questions": selected_questions,
            "loan_limit": 0.0,
            "active_loans": 0.0,
            "cards": [],
            "card_pins": [],
            "payment_methods": [], # Initialize empty payment methods list
            "payment_passcode": None, # Initialize payment passcode
            "beneficiaries": [],
            "statements": [] # Initialize empty statements list
        }
        
        # Add a default payment method with 150 USD balance for the user, as discussed
        # This allows them to immediately test deposit functionality
        user_details["payment_methods"].append({
            "name": "Default Test Wallet",
            "identifier": "Virtual Wallet",
            "currency": "USD",
            "balance": 150.0
        })

        accounts_data[new_username] = {
            "password": new_password,
            "balance": actual_initial_deposit, # This will likely be 0 initially
            "details": user_details
        }
        save_accounts(accounts_data)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if actual_initial_deposit > 0: # This path is currently not taken in this version for new accounts
            save_transaction(timestamp, new_username, "initial_deposit", actual_initial_deposit)
        
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
            if choice == 1: # Open a bank account (re-direct to account services if logged in)
                print(f"{BLUE_INFO} You are already logged in. If you wish to open another account, please log out first.")
                input("Press Enter to continue...")
                # Could also offer to go to Account Services directly instead of forcing logout
                # result = handle_account_services_flow(current_username)
                # if result == "logout":
                #     current_username = None
                # elif result is None:
                #     break
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
            print(f"Current Balance: KES {accounts_data[current_username]['balance']:.2f}")
            for key, value in user_details.items():
                if key not in ['account_number', 'account_type_name', 'account_type_features', 'security_questions', 'payment_methods', 'payment_passcode', 'statements', 'cards', 'card_pins', 'beneficiaries']: # Avoid re-printing nested dicts directly
                    print(f"{key.replace('_', ' ').title()}: {value}")
            
            # Display account features if available
            if 'account_type_features' in user_details and user_details['account_type_features']:
                print("\n--- Account Features ---")
                for key, value in user_details['account_type_features'].items():
                    if key != "Account Name": # Already displayed
                        print(f"  - {key.replace('_', ' ').title()}: {value}")
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
        elif service_choice == 5: # My Statements (New)
            view_my_statements(current_username)
        elif service_choice == 6: # Add/Manage Payment Methods (New)
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
            print(f"{BLUE_INFO} Request services features are under development.")
            input("Press Enter to continue...")
        elif service_choice == 9: # Make Payments (placeholder for now, distinct from Deposit)
            print(f"{BLUE_INFO} Payment features (e.g., bill payments, transfers to others) are under development.")
            input("Press Enter to continue...")
        elif service_choice == 10: # Check Loan Balance/Limit (placeholder for now)
            accounts_data = read_accounts()
            user_details = accounts_data[current_username]["details"]
            loan_limit = user_details.get("loan_limit", 0.0)
            active_loans = user_details.get("active_loans", 0.0)
            print(f"\n--- Loan Information ---")
            print(f"Your Loan Limit: KES {loan_limit:.2f}")
            print(f"Active Loans: KES {active_loans:.2f}")
            input("Press Enter to continue...")
        elif service_choice == 11: # Logout
            return "logout" # Signal to the calling function to log out
        else:
            print(f"{RED_X} Invalid choice. Please enter a number between 1 and 11.")
            input("Press Enter to continue...")

# --- Main Execution Block ---

if __name__ == "__main__":
    random.seed() # Seed the random number generator
    run_banking_app()