import datetime
import random
import json
import os
import hashlib

# --- Constants (Assuming these are defined elsewhere in your project) ---
GREEN_CHECKMARK = "✅"
RED_X = "❌"
BANK_NAME = "Python Bank"
BANK_TAGLINE = "Your trusted financial partner"
MESSAGES_INBOX_FILE = "messages_inbox.txt"
ACCOUNTS_FILE = "accounts.json"

# ANSI escape codes for colors
DARK_BLUE = "\033[38;5;20m" # A dark blue that stands out
BLUE = "\033[34m"
RESET_COLOR = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

# --- Helper Functions (Assuming these are defined elsewhere or will be added) ---

def get_user_input(prompt, input_type=str):
    """
    Gets user input with a prompt and handles potential EOFError.
    Allows 'M' for main menu or 'P' for previous menu.
    """
    try:
        user_input = input(prompt)
        if user_input.strip().upper() == 'M':
            return 'M'
        if user_input.strip().upper() == 'P':
            return 'P'
        if input_type == int:
            return int(user_input)
        return user_input
    except ValueError:
        print(f"{RED_X} Invalid input. Please enter a valid {input_type.__name__}.")
        return get_user_input(prompt, input_type) # Recursive call for valid input
    except EOFError:
        return None # Indicate program should exit

def read_accounts():
    """Reads account data from a JSON file."""
    if not os.path.exists(ACCOUNTS_FILE):
        return {}
    with open(ACCOUNTS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {} # Return empty dict if file is empty or corrupted

def save_accounts(accounts_data):
    """Saves account data to a JSON file."""
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts_data, f, indent=4)

def display_main_menu(is_logged_in):
    """Displays the main menu based on login status."""
    print("\n--- Main Menu ---")
    if not is_logged_in:
        print("1. Open a Bank Account")
        print("2. Explore Our Offers")
        print("3. Login")
        print("4. Exit Program")
    else:
        print("1. Account Services")
        print("2. Explore Our Offers")
        print("3. Logout")
        print("4. Exit Application")

def handle_account_opening_flow():
    """Handles the account opening process."""
    print("\n--- Open a Bank Account ---")
    username = get_user_input("Enter desired username: ").strip()
    if username is None: return None
    if username == 'M': return 'M'

    accounts_data = read_accounts()
    if username in accounts_data:
        print(f"{RED_X} Username already exists. Please choose a different one.")
        input("Press Enter to continue...")
        return 'M'

    password = get_user_input("Enter desired password: ").strip()
    if password is None: return None
    if password == 'M': return 'M'

    # Simple password hashing
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    account_type_features = {
        "Savings": {"Opening balance": 100, "Interest rate": 0.02, "monthly_maintenance_fee": 5},
        "Current": {"Opening balance": 500, "Overdraft limit": 1000, "monthly_maintenance_fee": 10},
        "Fixed Deposit": {"Opening balance": 1000, "Interest rate": 0.05, "Term (months)": 12, "monthly_maintenance_fee": 0}
    }
    print("\nAvailable Account Types:")
    for i, (acc_type, features) in enumerate(account_type_features.items(), 1):
        print(f"{i}. {acc_type} (Opening Balance: ${features['Opening balance']})")

    account_type_choice = get_user_input("Select an account type (1, 2, or 3): ", int)
    if account_type_choice is None: return None
    if account_type_choice == 'M': return 'M'

    selected_account_type = None
    if account_type_choice == 1:
        selected_account_type = "Savings"
    elif account_type_choice == 2:
        selected_account_type = "Current"
    elif account_type_choice == 3:
        selected_account_type = "Fixed Deposit"
    else:
        print(f"{RED_X} Invalid account type choice.")
        input("Press Enter to continue...")
        return 'M'

    initial_balance = account_type_features[selected_account_type]["Opening balance"]
    account_number = ''.join(random.choices('0123456789', k=10)) # Generate a 10-digit account number

    accounts_data[username] = {
        "password": hashed_password,
        "balance": initial_balance,
        "available_balance": initial_balance, # Initially same as balance
        "account_number": account_number,
        "account_type": selected_account_type,
        "activated": initial_balance > 0, # Activated if opening balance > 0
        "account_creation_date": datetime.date.today().isoformat(), # Store as ISO format string
        "transactions": [],
        "payment_methods": [],
        "payment_passcode": None, # Will store hashed passcode
        "loans_active": 0, # Initial loans active
        "details": {
            "account_type_features": account_type_features[selected_account_type]
        }
    }
    save_accounts(accounts_data)
    print(f"\n{GREEN_CHECKMARK} Account created successfully for {username}!")
    print(f"Your Account Number: {account_number}")
    print(f"Initial Balance: ${initial_balance:.2f}")
    input("Press Enter to continue...")
    return True # Indicate success

def handle_offers_flow():
    """Handles displaying bank offers."""
    print("\n--- Explore Our Offers ---")
    print("Check out our exciting offers:")
    print("- Low-interest personal loans")
    print("- High-yield savings accounts")
    print("- Exclusive credit card deals")
    print("- Mortgage solutions at competitive rates")
    print("\nContact us for more details!")
    input("Press Enter to continue...")
    return 'M'

def handle_account_services_flow(username):
    """Handles account services for a logged-in user."""
    accounts_data = read_accounts()
    user_account = accounts_data.get(username)

    if not user_account:
        print(f"{RED_X} Account data not found for {username}.")
        return "logout" # Force logout if account data is missing

    while True:
        print("\n--- Account Services ---")
        print("1. View Balance")
        print("2. Deposit Funds")
        print("3. Withdraw Funds")
        print("4. View Transaction History")
        print("5. Back to Home Screen")

        choice = get_user_input("Enter your choice: ", int)
        if choice is None:
            return None # Exit program
        if choice == 'M':
            return 'M' # Go back to main menu (user home screen)

        if choice == 1:
            print(f"\nYour current balance: ${user_account['balance']:.2f}")
            input("Press Enter to continue...")
        elif choice == 2:
            amount = get_user_input("Enter amount to deposit: ", float)
            if amount is None: return None
            if amount == 'M': continue
            if amount <= 0:
                print(f"{RED_X} Deposit amount must be positive.")
                input("Press Enter to continue...")
                continue
            user_account['balance'] += amount
            user_account['available_balance'] += amount
            user_account['transactions'].append({"type": "deposit", "amount": amount, "date": datetime.datetime.now().isoformat()})
            save_accounts(accounts_data)
            print(f"{GREEN_CHECKMARK} Deposited ${amount:.2f} successfully. New balance: ${user_account['balance']:.2f}")
            input("Press Enter to continue...")
        elif choice == 3:
            amount = get_user_input("Enter amount to withdraw: ", float)
            if amount is None: return None
            if amount == 'M': continue
            if amount <= 0:
                print(f"{RED_X} Withdrawal amount must be positive.")
                input("Press Enter to continue...")
                continue
            if user_account['balance'] < amount:
                print(f"{RED_X} Insufficient funds.")
                input("Press Enter to continue...")
                continue
            user_account['balance'] -= amount
            user_account['available_balance'] -= amount
            user_account['transactions'].append({"type": "withdrawal", "amount": amount, "date": datetime.datetime.now().isoformat()})
            save_accounts(accounts_data)
            print(f"{GREEN_CHECKMARK} Withdrew ${amount:.2f} successfully. New balance: ${user_account['balance']:.2f}")
            input("Press Enter to continue...")
        elif choice == 4:
            print("\n--- Transaction History ---")
            if not user_account['transactions']:
                print("No transactions yet.")
            else:
                for transaction in user_account['transactions']:
                    print(f"Type: {transaction['type'].capitalize()}, Amount: ${transaction['amount']:.2f}, Date: {transaction['date']}")
            input("Press Enter to continue...")
        elif choice == 5:
            return 'M' # Go back to user home screen
        else:
            print(f"{RED_X} Invalid choice. Please enter 1, 2, 3, 4, or 5.")
            input("Press Enter to continue...")

def write_to_inbox(username, message):
    """Writes a message to the user's inbox file."""
    with open(MESSAGES_INBOX_FILE, 'a') as f:
        f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] To {username}: {message}\n")

# --- New Functions for User Home Screen and Features ---

def calculate_ledger_amount(username):
    """Calculates the ledger amount based on transactions (placeholder logic)."""
    accounts_data = read_accounts()
    user_account = accounts_data.get(username)
    if not user_account:
        return 0

    ledger_fee = 0
    # Example: A simple ledger fee could be based on the number of transactions
    # For demonstration, let's assume a fixed ledger fee if there are any transactions
    if user_account['transactions']:
        ledger_fee = 2.50 # Example fixed ledger fee
    return ledger_fee

def calculate_lien_amount(username):
    """
    Calculates and applies the lien amount based on monthly maintenance fee
    and account age.
    """
    accounts_data = read_accounts()
    user_account = accounts_data.get(username)

    if not user_account:
        return 0, 0 # Return lien_amount, remaining_lien

    account_creation_date_str = user_account.get("account_creation_date")
    if not account_creation_date_str:
        return 0, 0 # No creation date, no lien

    try:
        account_creation_date = datetime.date.fromisoformat(account_creation_date_str)
    except ValueError:
        print(f"{RED_X} Error parsing account creation date for {username}.")
        return 0, 0

    today = datetime.date.today()
    age_in_months = (today.year - account_creation_date.year) * 12 + (today.month - account_creation_date.month)

    monthly_maintenance_fee = user_account.get("details", {}).get("account_type_features", {}).get("monthly_maintenance_fee", 0)

    lien_amount_due = 0
    if age_in_months >= 1:
        # A simple model: if account is one month or older, charge the fee
        lien_amount_due = monthly_maintenance_fee

    # Check for previous remaining lien (if any) and add to current due
    # This requires a new field in accounts_data: 'remaining_lien'
    remaining_lien = user_account.get("remaining_lien", 0)
    total_lien_to_process = lien_amount_due + remaining_lien

    actual_deducted = 0
    new_remaining_lien = 0

    if total_lien_to_process > 0:
        if user_account['balance'] >= total_lien_to_process:
            user_account['balance'] -= total_lien_to_process
            user_account['available_balance'] -= total_lien_to_process
            actual_deducted = total_lien_to_process
            user_account['transactions'].append({
                "type": "lien_deduction",
                "amount": total_lien_to_process,
                "date": datetime.datetime.now().isoformat(),
                "description": f"Monthly maintenance fee deduction for {today.strftime('%Y-%m')}"
            })
            new_remaining_lien = 0 # Fully paid
        else:
            actual_deducted = user_account['balance']
            new_remaining_lien = total_lien_to_process - user_account['balance']
            user_account['balance'] = 0
            user_account['available_balance'] = 0 # Balance becomes 0
            user_account['transactions'].append({
                "type": "lien_deduction",
                "amount": actual_deducted,
                "date": datetime.datetime.now().isoformat(),
                "description": f"Partial monthly maintenance fee deduction for {today.strftime('%Y-%m')}"
            })

    user_account['remaining_lien'] = new_remaining_lien
    save_accounts(accounts_data)

    return actual_deducted, new_remaining_lien

def display_user_home_screen(username):
    """
    Displays the user's personalized home screen with account details and options.
    """
    accounts_data = read_accounts()
    user_account = accounts_data.get(username)

    if not user_account:
        print(f"{RED_X} Account data not found for {username}.")
        return "logout"

    # Get current time for greeting
    current_hour = datetime.datetime.now().hour
    greeting = ""
    if 5 <= current_hour < 12:
        greeting = "Good morning"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    # Calculate ledger and lien
    ledger_amount = calculate_ledger_amount(username)
    deducted_lien, remaining_lien = calculate_lien_amount(username) # This also applies the deduction

    # Re-read account data after lien deduction for up-to-date balance
    accounts_data = read_accounts()
    user_account = accounts_data.get(username)

    print(f"\n{DARK_BLUE}{BOLD}{' ' * ((80 - len(BANK_NAME)) // 2)}{BANK_NAME}{RESET_COLOR}")
    print(f"{BLUE}{BOLD}{greeting}, {username}!{RESET_COLOR}")
    print(f"{datetime.date.today().strftime('%A, %B %d, %Y')}")
    print(f"Account Number: {user_account.get('account_number', 'N/A')}")

    print("-" * 40)
    print(f"{'Available Balance:':<20} ${user_account.get('available_balance', 0.00):>15.2f}")
    print(f"{'Balance:':<20} ${user_account.get('balance', 0.00):>15.2f}")
    print(f"{'Loans Active:':<20} {user_account.get('loans_active', 0):>15}")
    print(f"{'Ledger Amount:':<20} ${ledger_amount:>15.2f}")
    print(f"{'Lien Amount:':<20} ${deducted_lien:>15.2f}") # Display the amount deducted or due for this period
    if remaining_lien > 0:
        print(f"{'Remaining Lien:':<20} ${remaining_lien:>15.2f} (will be deducted from future deposits)")
    print("-" * 40)

    print("\n--- Your Services ---")
    print("1. Account Services (Deposit, Withdraw, History)")
    print("2. Add Payment Method")
    print("3. Set Payment Passcode")
    print("4. Transfer Funds")
    print("5. Currency Conversion")
    print("6. Explore Our Offers")
    print("7. Logout")
    print("8. Exit Application")

    while True:
        choice = get_user_input("Enter your choice: ", int)
        if choice is None:
            return None # Exit program
        if choice == 'M' or choice == 'P': # 'M' or 'P' should go back to main menu loop, which is handled outside
            continue # Stay in this loop until valid choice or exit

        if choice == 1:
            result = handle_account_services_flow(username)
            if result == "logout":
                return "logout"
            elif result is None:
                return None
            elif result == 'M': # Back to user home screen
                break # Exit the inner loop to redisplay home screen
        elif choice == 2:
            result = handle_payment_method_flow(username)
            if result is None: return None
            if result == 'M': continue
            break # Redisplay home screen
        elif choice == 3:
            result = handle_set_passcode_flow(username)
            if result is None: return None
            if result == 'M': continue
            break # Redisplay home screen
        elif choice == 4:
            result = handle_transfer_funds_flow(username)
            if result is None: return None
            if result == 'M': continue
            break # Redisplay home screen
        elif choice == 5:
            result = handle_currency_conversion_flow(username)
            if result is None: return None
            if result == 'M': continue
            break # Redisplay home screen
        elif choice == 6:
            result = handle_offers_flow()
            if result is None: return None
            if result == 'M': continue
            break # Redisplay home screen
        elif choice == 7:
            return "logout"
        elif choice == 8:
            return None # Exit application
        else:
            print(f"{RED_X} Invalid choice. Please enter a valid option.")
            input("Press Enter to continue...")
            break # Redisplay home screen after invalid choice

def handle_payment_method_flow(username):
    """Allows the user to add a payment method."""
    accounts_data = read_accounts()
    user_account = accounts_data.get(username)
    if not user_account:
        print(f"{RED_X} Account data not found.")
        return 'M'

    print("\n--- Add Payment Method ---")
    print("1. M-Pesa")
    print("2. Bank Card")
    print("3. Back to Home Screen")

    choice = get_user_input("Enter your choice: ", int)
    if choice is None: return None
    if choice == 'M': return 'M'

    if choice == 1: # M-Pesa
        mpesa_number = get_user_input("Enter M-Pesa number (e.g., 07XXXXXXXX): ").strip()
        if mpesa_number is None: return None
        if mpesa_number == 'M': return 'M'
        if not (mpesa_number.startswith('07') and len(mpesa_number) == 10 and mpesa_number.isdigit()):
            print(f"{RED_X} Invalid M-Pesa number format.")
            input("Press Enter to continue...")
            return 'M'

        user_account['payment_methods'].append({"type": "M-Pesa", "number": mpesa_number})
        save_accounts(accounts_data)
        print(f"{GREEN_CHECKMARK} M-Pesa number {mpesa_number} added successfully!")
        input("Press Enter to continue...")
    elif choice == 2: # Bank Card
        card_number = get_user_input("Enter card number (16 digits): ").strip()
        if card_number is None: return None
        if card_number == 'M': return 'M'
        if not (len(card_number) == 16 and card_number.isdigit()):
            print(f"{RED_X} Invalid card number format. Must be 16 digits.")
            input("Press Enter to continue...")
            return 'M'

        expiry_date = get_user_input("Enter expiry date (MM/YY): ").strip()
        if expiry_date is None: return None
        if expiry_date == 'M': return 'M'
        # Basic format validation
        if not (len(expiry_date) == 5 and expiry_date[2] == '/' and expiry_date[:2].isdigit() and expiry_date[3:].isdigit()):
            print(f"{RED_X} Invalid expiry date format. Use MM/YY.")
            input("Press Enter to continue...")
            return 'M'

        cvv = get_user_input("Enter CVV (3 or 4 digits): ").strip()
        if cvv is None: return None
        if cvv == 'M': return 'M'
        if not ((len(cvv) == 3 or len(cvv) == 4) and cvv.isdigit()):
            print(f"{RED_X} Invalid CVV format. Must be 3 or 4 digits.")
            input("Press Enter to continue...")
            return 'M'

        user_account['payment_methods'].append({
            "type": "Card",
            "number": card_number,
            "expiry": expiry_date,
            "cvv": cvv # In a real app, this would be highly sensitive and handled with extreme care
        })
        save_accounts(accounts_data)
        print(f"{GREEN_CHECKMARK} Bank card added successfully!")
        input("Press Enter to continue...")
    elif choice == 3:
        return 'M'
    else:
        print(f"{RED_X} Invalid choice.")
        input("Press Enter to continue...")
    return 'M'

def is_predictable_sequence(passcode):
    """Checks if a 6-digit passcode is in a predictable sequence."""
    if not passcode.isdigit() or len(passcode) != 6:
        return True # Not a 6-digit number

    # Check for all same digits (e.g., 111111)
    if len(set(passcode)) == 1:
        return True

    # Check for ascending sequence (e.g., 123456)
    if all(int(passcode[i]) + 1 == int(passcode[i+1]) for i in range(5)):
        return True

    # Check for descending sequence (e.g., 654321)
    if all(int(passcode[i]) - 1 == int(passcode[i+1]) for i in range(5)):
        return True

    return False

def handle_set_passcode_flow(username):
    """Allows the user to set a 6-digit payment passcode."""
    accounts_data = read_accounts()
    user_account = accounts_data.get(username)
    if not user_account:
        print(f"{RED_X} Account data not found.")
        return 'M'

    print("\n--- Set Payment Passcode (6-digits) ---")
    print("Your passcode cannot be in a predictable sequence (e.g., 123456, 111111).")

    while True:
        passcode = get_user_input("Enter your new 6-digit passcode: ").strip()
        if passcode is None: return None
        if passcode == 'M': return 'M'

        if not (passcode.isdigit() and len(passcode) == 6):
            print(f"{RED_X} Passcode must be exactly 6 digits.")
            input("Press Enter to continue...")
            continue

        if is_predictable_sequence(passcode):
            print(f"{RED_X} Passcode is in a predictable sequence. Please choose a stronger one.")
            input("Press Enter to continue...")
            continue

        confirm_passcode = get_user_input("Confirm your 6-digit passcode: ").strip()
        if confirm_passcode is None: return None
        if confirm_passcode == 'M': return 'M'

        if passcode != confirm_passcode:
            print(f"{RED_X} Passcodes do not match. Please try again.")
            input("Press Enter to continue...")
            continue
        break # Passcode is valid and confirmed

    # Generate OTP
    otp = ''.join(random.choices('0123456789', k=6))
    write_to_inbox(username, f"Your OTP for passcode verification is: {otp}")
    print(f"{GREEN_CHECKMARK} An OTP has been sent to your messages_inbox.txt for verification.")

    entered_otp = get_user_input("Enter the OTP received to verify your passcode: ").strip()
    if entered_otp is None: return None
    if entered_otp == 'M': return 'M'

    if entered_otp == otp:
        user_account['payment_passcode'] = hashlib.sha256(passcode.encode()).hexdigest()
        save_accounts(accounts_data)
        print(f"{GREEN_CHECKMARK} Payment passcode set successfully!")
    else:
        print(f"{RED_X} Incorrect OTP. Passcode not set.")
    input("Press Enter to continue...")
    return 'M'

def handle_transfer_funds_flow(username):
    """Handles transferring funds between accounts."""
    accounts_data = read_accounts()
    sender_account = accounts_data.get(username)

    if not sender_account:
        print(f"{RED_X} Your account data not found.")
        return 'M'
    if not sender_account.get("payment_passcode"):
        print(f"{RED_X} You must set a payment passcode before transferring funds. Please go to 'Set Payment Passcode'.")
        input("Press Enter to continue...")
        return 'M'

    print("\n--- Transfer Funds ---")
    recipient_account_number = get_user_input("Enter recipient's account number: ").strip()
    if recipient_account_number is None: return None
    if recipient_account_number == 'M': return 'M'

    recipient_username = None
    for acc_user, acc_details in accounts_data.items():
        if acc_details.get("account_number") == recipient_account_number:
            recipient_username = acc_user
            break

    if not recipient_username:
        print(f"{RED_X} Recipient account not found.")
        input("Press Enter to continue...")
        return 'M'

    recipient_account = accounts_data.get(recipient_username)
    if not recipient_account:
        print(f"{RED_X} Recipient account data could not be loaded.") # Should not happen if recipient_username is found
        input("Press Enter to continue...")
        return 'M'

    amount = get_user_input("Enter amount to transfer: ", float)
    if amount is None: return None
    if amount == 'M': return 'M'

    if amount <= 0:
        print(f"{RED_X} Transfer amount must be positive.")
        input("Press Enter to continue...")
        return 'M'

    if sender_account['available_balance'] < amount:
        print(f"{RED_X} Insufficient funds for transfer.")
        input("Press Enter to continue...")
        return 'M'

    # Passcode verification
    entered_passcode = get_user_input("Enter your payment passcode to confirm: ").strip()
    if entered_passcode is None: return None
    if entered_passcode == 'M': return 'M'

    if hashlib.sha256(entered_passcode.encode()).hexdigest() != sender_account['payment_passcode']:
        print(f"{RED_X} Incorrect payment passcode. Transfer failed.")
        input("Press Enter to continue...")
        return 'M'

    # Perform transfer
    sender_account['balance'] -= amount
    sender_account['available_balance'] -= amount
    recipient_account['balance'] += amount
    recipient_account['available_balance'] += amount

    sender_account['transactions'].append({
        "type": "transfer_out",
        "amount": amount,
        "recipient": recipient_account_number,
        "date": datetime.datetime.now().isoformat()
    })
    recipient_account['transactions'].append({
        "type": "transfer_in",
        "amount": amount,
        "sender": sender_account['account_number'],
        "date": datetime.datetime.now().isoformat()
    })

    save_accounts(accounts_data)
    print(f"{GREEN_CHECKMARK} Transferred ${amount:.2f} to account {recipient_account_number} successfully!")
    input("Press Enter to continue...")
    return 'M'

# --- Currency Conversion Data (Example data, replace with real-time if needed) ---
CURRENCY_RATES = {
    "USD": {"name": "US Dollar", "sign": "$", "buy": 1.0, "sell": 1.0}, # Base
    "EUR": {"name": "Euro", "sign": "€", "buy": 1.08, "sell": 1.10},
    "GBP": {"name": "British Pound", "sign": "£", "buy": 1.25, "sell": 1.28},
    "JPY": {"name": "Japanese Yen", "sign": "¥", "buy": 0.0068, "sell": 0.0070},
    "KES": {"name": "Kenyan Shilling", "sign": "KSh", "buy": 0.0076, "sell": 0.0078} # Assuming KES is base
}

def display_currency_table():
    """Displays the currency conversion table with styling."""
    print(f"\n{DARK_BLUE}{BOLD}{' ' * 20}CURRENCY CONVERSION TABLE{' ' * 20}{RESET_COLOR}")
    print(f"{BLUE}{UNDERLINE}{'Currency':<15}{'Abbr':<8}{'Sign':<8}{'Buying':>10}{'Selling':>10}{RESET_COLOR}")
    print("-" * 55)
    for abbr, data in CURRENCY_RATES.items():
        print(f"{data['name']:<15}{abbr:<8}{data['sign']:<8}{data['buy']:>10.4f}{data['sell']:>10.4f}")
    print("-" * 55)
    input("Press Enter to continue...")

def handle_currency_conversion_flow(username):
    """Handles currency conversion for the user."""
    accounts_data = read_accounts()
    user_account = accounts_data.get(username)
    if not user_account:
        print(f"{RED_X} Account data not found.")
        return 'M'

    print("\n--- Currency Conversion ---")
    print("1. View Currency Conversion Table")
    print("2. Proceed with Auto Conversion")
    print("3. Back to Home Screen")

    choice = get_user_input("Enter your choice: ", int)
    if choice is None: return None
    if choice == 'M': return 'M'

    if choice == 1:
        display_currency_table()
        return 'M' # Go back to conversion menu or main menu
    elif choice == 2:
        while True:
            from_currency = get_user_input("Enter currency to convert FROM (e.g., KES, USD): ").strip().upper()
            if from_currency is None: return None
            if from_currency == 'M': return 'M'
            if from_currency not in CURRENCY_RATES:
                print(f"{RED_X} Invalid 'from' currency. Please choose from: {', '.join(CURRENCY_RATES.keys())}")
                continue

            to_currency = get_user_input("Enter currency to convert TO (e.g., USD, EUR): ").strip().upper()
            if to_currency is None: return None
            if to_currency == 'M': return 'M'
            if to_currency not in CURRENCY_RATES:
                print(f"{RED_X} Invalid 'to' currency. Please choose from: {', '.join(CURRENCY_RATES.keys())}")
                continue

            if from_currency == to_currency:
                print(f"{RED_X} 'From' and 'To' currencies cannot be the same.")
                continue

            amount = get_user_input(f"Enter amount in {from_currency} to convert: ", float)
            if amount is None: return None
            if amount == 'M': return 'M'
            if amount <= 0:
                print(f"{RED_X} Amount to convert must be positive.")
                continue

            # Assuming the user's account balance is in KES for simplification
            # In a real system, accounts would have specific currencies
            if user_account['available_balance'] < amount: # This check needs to be more robust if account has multiple currencies
                print(f"{RED_X} Insufficient funds in your primary account to cover this conversion.")
                input("Press Enter to continue...")
                return 'M'

            # Convert to base (e.g., KES) then to target
            # Example: KES -> USD (buy USD) means KES / USD_sell_rate
            # USD -> KES (sell USD) means USD * KES_buy_rate
            # The logic here assumes KES is the primary currency of the user's account
            # and that all conversions involve KES as an intermediary or direct.
            # A more robust system would handle multiple currency wallets.

            try:
                # To get target amount: (amount / sell_rate_of_from_currency) * buy_rate_of_to_currency
                # This assumes our rates are against a common base (e.g., KES to X, and X to KES)
                # Let's simplify: if converting from KES, use sell rate. If converting to KES, use buy rate.
                # If neither is KES, convert to KES first, then from KES to target.

                # Convert 'from_currency' amount to 'base' units (e.g., KES)
                # If from_currency is KES, then base_amount = amount
                # If from_currency is USD, and rates are relative to KES, then base_amount = amount * CURRENCY_RATES["USD"]["sell"] (selling USD to get KES)
                # This needs a clear definition of what CURRENCY_RATES "buy" and "sell" refer to.
                # Let's assume "buy" is what the bank buys the foreign currency for (i.e., you get less KES for foreign currency)
                # "sell" is what the bank sells the foreign currency for (i.e., you pay more KES for foreign currency)

                # For simplicity, let's assume rates are relative to USD as a conceptual base for conversion calculations.
                # So to convert FROM_CURRENCY to TO_CURRENCY:
                # 1. Convert FROM_CURRENCY to USD equivalent: amount_in_usd = amount / CURRENCY_RATES[from_currency]["buy"]
                # 2. Convert USD equivalent to TO_CURRENCY: converted_amount = amount_in_usd / CURRENCY_RATES[to_currency]["sell"]

                # A more common bank model:
                # When converting from 'from_currency' to 'to_currency':
                # The bank 'buys' the 'to_currency' from the user, and 'sells' the 'from_currency' to the user.
                # So if converting KES to USD, bank sells USD, user buys USD. So use USD 'sell' rate relative to KES.
                # If converting USD to KES, bank buys USD, user sells USD. So use USD 'buy' rate relative to KES.

                # Let's clarify the CURRENCY_RATES: they represent the KES value of 1 unit of that currency.
                # buy: KES per foreign unit (bank buys foreign currency)
                # sell: KES per foreign unit (bank sells foreign currency)

                # If KES is our base currency, and we're converting from X to Y:
                # 1. Convert X to KES: amount * CURRENCY_RATES[from_currency]["buy"]
                # 2. Convert KES to Y: (amount * CURRENCY_RATES[from_currency]["buy"]) / CURRENCY_RATES[to_currency]["sell"]

                # Simplified example: User has KES and wants USD.
                # User sells KES, Bank sells USD.
                # amount_in_usd = amount_in_kes / CURRENCY_RATES["USD"]["sell"]

                # User has USD and wants KES.
                # User sells USD, Bank buys USD.
                # amount_in_kes = amount_in_usd * CURRENCY_RATES["USD"]["buy"]


                # Let's assume a primary currency for the user's account (e.g., KES).
                # All 'buy' and 'sell' rates are how many KES for 1 unit of foreign currency.

                # To convert 'amount' FROM 'from_currency' TO 'to_currency':
                # First, convert 'from_currency' to KES equivalent:
                amount_in_kes = amount * CURRENCY_RATES[from_currency]["buy"] # Bank buys from_currency from you (or if it's KES, it's just amount)

                # Then, convert KES equivalent to 'to_currency':
                converted_amount = amount_in_kes / CURRENCY_RATES[to_currency]["sell"] # Bank sells to_currency to you

                # This logic is simplified and assumes user account is KES, and rates are KES per unit of foreign.
                # For actual multi-currency accounts, you'd need multiple balance fields.

                # For the purpose of this simulation, we'll assume the 'balance' is in KES
                # and conversions are performed against this KES balance.

                if from_currency == "KES":
                    # User is spending KES to buy 'to_currency'
                    if user_account['available_balance'] < amount:
                        print(f"{RED_X} Insufficient KES balance for this conversion.")
                        input("Press Enter to continue...")
                        continue
                    converted_amount = amount / CURRENCY_RATES[to_currency]["sell"]
                    user_account['balance'] -= amount
                    user_account['available_balance'] -= amount
                    user_account['transactions'].append({
                        "type": "currency_conversion",
                        "from_currency": from_currency,
                        "to_currency": to_currency,
                        "amount_out": amount,
                        "amount_in": converted_amount,
                        "date": datetime.datetime.now().isoformat()
                    })
                    save_accounts(accounts_data)
                    print(f"{GREEN_CHECKMARK} Converted {amount:.2f} {from_currency} to {converted_amount:.2f} {to_currency}.")
                elif to_currency == "KES":
                    # User is selling 'from_currency' to get KES
                    # This implies the user has 'from_currency' elsewhere.
                    # For a single-currency balance, this is tricky.
                    # Let's assume for simulation, they 'convert' their existing KES balance if they wanted to convert
                    # FROM a foreign currency TO KES. This would be a deposit of the foreign currency amount,
                    # converted to KES, and then added to their KES balance.
                    # To keep it simple with one balance: we are converting from their existing KES to another currency.
                    # Or they are adding foreign currency which gets converted to KES and added to balance.

                    # Let's simplify: All transactions are from/to the user's KES balance.
                    # So, if FROM_CURRENCY is not KES, it means the user is *receiving* that currency
                    # and it's being converted to KES for their balance.
                    # If TO_CURRENCY is not KES, it means the user is *sending* KES to buy that currency.

                    print(f"{RED_X} Currently, this simulator only supports converting FROM KES to other currencies, or from other currencies to KES as a deposit.")
                    print("Please specify KES as either the 'from' or 'to' currency for direct balance interaction.")
                    input("Press Enter to continue...")
                    continue
                else:
                    # Conversion between two foreign currencies.
                    # This would involve two steps with KES as intermediary.
                    # e.g., USD -> KES -> EUR
                    # 1. Sell USD to get KES: amount_in_kes = amount * CURRENCY_RATES["USD"]["buy"]
                    # 2. Buy EUR with KES: amount_in_eur = amount_in_kes / CURRENCY_RATES["EUR"]["sell"]

                    # For the current simple model, this is not directly supported without multiple currency wallets.
                    print(f"{RED_X} Direct conversion between two non-KES currencies is not supported in this simulation.")
                    print("Please convert to/from KES.")
                    input("Press Enter to continue...")
                    continue


                print(f"Your new KES balance: ${user_account['balance']:.2f}")

            except Exception as e:
                print(f"{RED_X} An error occurred during conversion: {e}")
                input("Press Enter to continue...")
            input("Press Enter to continue...")
            break # Exit conversion loop after successful or failed attempt
    elif choice == 3:
        return 'M' # Back to home screen
    else:
        print(f"{RED_X} Invalid choice.")
        input("Press Enter to continue...")
    return 'M'

# --- Main Application Loop ---

def run_banking_app():
    """Manages the main flow of the banking application."""
    current_username = None  # Stores the username of the currently logged-in user

    print(f"{GREEN_CHECKMARK} Welcome to {BANK_NAME} - {BANK_TAGLINE} {GREEN_CHECKMARK}")

    while True:  # Outer loop for login/registration
        if current_username is None: # Not logged in
            display_main_menu(False)
            choice = get_user_input("Enter your choice: ", int)

            if choice is None:  # EOFError or other critical input issue
                print("Exiting Application.")
                break
            if choice == 'M' or choice == 'P':
                continue

            if choice == 1:  # Open a bank account
                result = handle_account_opening_flow()
                if result is None:
                    break  # Exit program
                if result == 'M':
                    continue  # Go back to main menu
                continue  # Go back to main menu after account opening attempt
            elif choice == 2:  # Explore our offers
                result = handle_offers_flow()
                if result is None:
                    break  # Exit program
                if result == 'M':
                    continue
                continue
            elif choice == 3:  # Login
                username = get_user_input("Enter your username: ").strip()
                if username == 'M' or username == 'P':
                    continue
                if username is None:
                    break

                password = get_user_input("Enter your password: ").strip()
                if password == 'M' or password == 'P':
                    continue
                if password is None:
                    break

                accounts_data = read_accounts()
                hashed_password_attempt = hashlib.sha256(password.encode()).hexdigest()

                if username in accounts_data and accounts_data[username]["password"] == hashed_password_attempt:
                    print(f"\n{GREEN_CHECKMARK} Login successful! Welcome, {username}!")
                    current_username = username
                    # Ensure account is marked activated if it had 0 opening balance
                    # This logic should ideally be part of account creation or deposit if 0 initial.
                    # Let's re-evaluate this as it's a bit redundant if opening balance logic is solid.
                    # For now, keeping it as is based on original request.
                    if not accounts_data[username]["activated"]: # If account was created with 0 balance
                        accounts_data[username]["activated"] = True
                        save_accounts(accounts_data)

                else:
                    print(f"{RED_X} Invalid username or password. Please try again.")
                input("Press Enter to continue...")
            elif choice == 4:  # Exit program
                print("\nThank you for using the Python Bank Simulation. Goodbye!")
                break
            else:
                print(f"{RED_X} Invalid choice. Please enter 1, 2, 3, or 4.")
                input("Press Enter to continue...")
        else:  # Logged in
            # Display the user's home screen
            result = display_user_home_screen(current_username)
            if result == "logout":
                current_username = None
                print("\nLogging out. Returning to main menu.")
                input("Press Enter to continue...")
            elif result is None:
                print("\nThank you for using the Python Bank Simulation. Goodbye!")
                break
            # If result is not "logout" or None, it means the user chose an option
            # that led them back to the user home screen loop, so we just continue
            # the outer loop which will re-call display_user_home_screen.


# --- Main Execution Block ---

def delete_all_data():
    """Deletes the accounts.json and messages_inbox.txt files."""
    if os.path.exists(ACCOUNTS_FILE):
        os.remove(ACCOUNTS_FILE)
        print(f"Deleted {ACCOUNTS_FILE}")
    if os.path.exists(MESSAGES_INBOX_FILE):
        os.remove(MESSAGES_INBOX_FILE)
        print(f"Deleted {MESSAGES_INBOX_FILE}")

if __name__ == "__main__":
    random.seed()  # Seed the random number generator
    # Optional: uncomment to delete all data on each run for fresh start
    # delete_all_data()
    run_banking_app()