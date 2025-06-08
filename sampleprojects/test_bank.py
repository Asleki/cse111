import time
import os
import re # Import regex module for stripping ANSI codes
import random # For generating random numbers
from datetime import datetime, timedelta # For generating random dates

# --- ANSI Escape Codes for Terminal Styling ---
RESET = "\033[0m"

# Font Styles
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
INVERSE = "\033[7m"
STRIKETHROUGH = "\033[9m"

# Text Colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

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
# --- End of ANSI Escape Codes ---

# Global symbols for checkmark and cross
GREEN_CHECK = f"{BRIGHT_GREEN}\u2714{RESET}"
RED_X = f"{BRIGHT_RED}\u2718{RESET}"

# --- Utility Function to Clear Screen ---
def clear_screen():
    """Clears the terminal screen."""
    if os.name == 'nt': # For Windows
        _ = os.system('cls')
    else: # For macOS and Linux
        _ = os.system('clear')

# Regex to strip ANSI escape codes for accurate length calculation
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def get_visible_length(s):
    """Returns the visible length of a string, stripping ANSI escape codes."""
    return len(ANSI_ESCAPE.sub('', s))

# --- Provided Card Details Library Function ---
def display_card_details_info(card_type, specific_card=None):
    """
    Retrieves the details of a selected card type or a specific card.
    Note: This function is adapted to *return* details for specific cards,
          and relies on external display functions if specific_card is None.
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
            # If specific_card is None, this implies we need to show the list
            # We'll handle showing the list in the calling function, not here.
            pass
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
            pass
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
            pass
    else:
        # print(f"{RED_X} Invalid card type.") # This will be handled by the caller
        pass
    return details

# --- Helper Functions to display specific card lists ---
def display_available_debit_cards():
    clear_screen()
    print(f"\n{BOLD}{BG_BLUE}{BRIGHT_WHITE}--- Available Debit Cards ---{RESET}")
    print(f"{BRIGHT_CYAN}1. {BOLD}Club Debit MasterCard{RESET} (KES)")
    print(f"{BRIGHT_CYAN}2. {BOLD}Debit Visa{RESET} (KES)")
    print(f"{BRIGHT_CYAN}3. {BOLD}Gold MasterCard{RESET} (KES)")
    print(f"{BOLD}{BG_BLUE}{BRIGHT_WHITE}----------------------------{RESET}")

def display_available_prepaid_cards():
    clear_screen()
    print(f"\n{BOLD}{BG_BLUE}{BRIGHT_WHITE}--- Available Prepaid Cards ---{RESET}")
    print(f"{BRIGHT_CYAN}1. {BOLD}Multi Currency Prepaid MasterCard{RESET} (USD, GBP, EURO, YEN)")
    print(f"{BRIGHT_CYAN}2. {BOLD}Sapphire Prepaid Visa{RESET} (KES)")
    print(f"{BRIGHT_CYAN}3. {BOLD}Safari Prepaid Visa{RESET} (KES)")
    print(f"{BOLD}{BG_BLUE}{BRIGHT_WHITE}------------------------------{RESET}")

def display_available_credit_cards():
    clear_screen()
    print(f"\n{BOLD}{BG_BLUE}{BRIGHT_WHITE}--- Available Credit Cards ---{RESET}")
    print(f"{BRIGHT_CYAN}1. {BOLD}Gold Visa Credit Card{RESET} (KES)")
    print(f"{BRIGHT_CYAN}2. {BOLD}Bronze Credit MasterCard{RESET} (KES)")
    print(f"{BRIGHT_CYAN}3. {BOLD}Diamond Credit Card{RESET} (KES)")
    print(f"{BOLD}{BG_BLUE}{BRIGHT_WHITE}-----------------------------{RESET}")


def display_bank_card(card_holder_name, bank_name, card_number, exp_date, cvv, card_type_name="Generic Card", currency_symbol="CUR"):
    """
    Displays a stylized ASCII art representation of a bank card with details,
    matching the provided image structure and adding new rows.
    """
    clear_screen()
    print(f"\n{BOLD}{BG_MAGENTA}{BRIGHT_WHITE}--- Your New {card_type_name} ---{RESET}\n")

    # Define card dimensions
    card_width = 46 # Adjusted for the specific screenshot layout
    card_inner_width = card_width - 2 # Space between '|' borders

    # Drawing characters for the frame (from user's previous request)
    BORDER_CHAR = '*'
    DIVIDER_CHAR = '-'
    DETAILS_LINE_CHAR = ';' # Used for internal patterns/texture

    # Colors for text content
    text_color = BRIGHT_WHITE
    label_color = BRIGHT_BLACK # For "VALID THRU" label

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

    # Simplified Mastercard Logo for embedding (using ANSI colors for blocks)
    mc_logo_red = BG_RED + " "
    mc_logo_yellow = BG_YELLOW + " "
    mc_logo_overlap = BG_BRIGHT_YELLOW + " "
    mc_logo_string = f"{mc_logo_red}{mc_logo_overlap}{mc_logo_yellow}{RESET}"
    mc_logo_visible_width = get_visible_length(mc_logo_string) # Should be 3 characters

    # --- Card Construction ---

    # Top Border
    print(f"{BORDER_CHAR * card_width}{RESET}")

    # Line 1: Bank Name
    bank_name_indent = 2 # Indent from left border
    bank_name_max_len = card_inner_width - bank_name_indent - 1 # 1 char for right border
    
    bank_name_display = styled_bank_name
    if get_visible_length(bank_name_display) > bank_name_max_len:
        bank_name_display = bank_name_display[:bank_name_max_len - 3] + "..." + RESET # Truncate if too long
    
    bank_name_fill_len = card_inner_width - get_visible_length(bank_name_display) - bank_name_indent
    
    print(
        f"{BORDER_CHAR}"
        f"{' ' * bank_name_indent}" # Left indent
        f"{bank_name_display}"
        f"{DETAILS_LINE_CHAR * max(0, bank_name_fill_len)}" # Fill with ';'
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

    # Line 4: Blank line for vertical spacing (or another divider)
    print(f"{BORDER_CHAR}{DIVIDER_CHAR * card_inner_width}{BORDER_CHAR}{RESET}")

    # Line 5: VALID THRU and Expiration Date (Right-aligned, as in image)
    valid_thru_content = f"{valid_thru_label_styled} {styled_exp_date}"
    valid_thru_indent = 2 # Indent from right border
    content_len = get_visible_length(valid_thru_content)
    padding = card_inner_width - content_len - valid_thru_indent
    print(f"{BORDER_CHAR}{' ' * padding}{valid_thru_content}{' ' * valid_thru_indent}{BORDER_CHAR}{RESET}")

    # Line 6: Card Holder Name (Left-aligned, as in image)
    name_indent = 2
    content_len = get_visible_length(styled_name)
    padding = card_inner_width - content_len - name_indent
    print(f"{BORDER_CHAR}{' ' * name_indent}{styled_name}{' ' * padding}{BORDER_CHAR}{RESET}")

    # Line 7: Divider Line (as in image)
    print(f"{BORDER_CHAR}{DIVIDER_CHAR * card_inner_width}{BORDER_CHAR}{RESET}")

    # Line 8: CVV (left) and Mastercard Logo (right, as in image)
    cvv_indent = 2
    cvv_content_len = get_visible_length(styled_cvv)
    logo_indent = 2 # Indent for logo from right border

    space_between_cvv_logo = card_inner_width - cvv_indent - cvv_content_len - mc_logo_visible_width - logo_indent
    space_between_cvv_logo = max(0, space_between_cvv_logo) # Ensure no negative padding

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
    input(f"\n{BOLD}{CYAN}Press Enter to return to main menu...{RESET}")


def generate_random_card_details():
    """Generates random 16-digit card number, 3-digit CVV, and MM/YY expiry."""
    # Generate 16-digit number (simple random for demo, not actual card logic)
    card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])

    # Generate 3-digit CVV
    cvv = f"{random.randint(100, 999)}"

    # Generate expiry date (MM/YY) - between 1 to 5 years from current month
    current_date = datetime.now()
    
    # Pick a random number of months to add (e.g., 12 to 60 months)
    months_to_add = random.randint(12, 60)
    
    # Calculate approximate expiry date
    expiry_date_obj = current_date + timedelta(days=30 * months_to_add) # Approximate calculation
    
    # Ensure it's the last day of the month for proper expiry
    if expiry_date_obj.month == 12:
        expiry_date_obj = expiry_date_obj.replace(day=31)
    else:
        # Move to the first day of next month, then subtract one day
        expiry_date_obj = expiry_date_obj.replace(month=expiry_date_obj.month + 1, day=1) - timedelta(days=1)

    exp_month = expiry_date_obj.month
    exp_year = expiry_date_obj.year

    # Format as MM/YY
    exp_date = f"{exp_month:02d}/{str(exp_year)[-2:]}"

    return card_number, cvv, exp_date

def apply_for_card_process():
    """Handles the interactive card application process."""
    clear_screen()
    print(f"\n{BOLD}{BG_BLUE}{BRIGHT_WHITE}--- Apply for a New Card ---{RESET}")

    user_full_name = input(f"{YELLOW}Please enter your full name for the card: {RESET}").strip()
    if not user_full_name:
        print(f"{RED_X} Error: Full name cannot be empty. Please try again.{RESET}")
        input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")
        return

    # Step 1: Select Card Type (Debit, Prepaid, Credit)
    selected_card_type_num = None
    while selected_card_type_num is None:
        clear_screen()
        print(f"\n{BOLD}{BG_BLUE}{BRIGHT_WHITE}--- Select Card Category ---{RESET}")
        print(f"{BRIGHT_CYAN}1. {BOLD}Debit Cards{RESET}")
        print(f"{BRIGHT_CYAN}2. {BOLD}Prepaid Cards{RESET}")
        print(f"{BRIGHT_CYAN}3. {BOLD}Credit Cards{RESET}")
        print(f"{BOLD}{BG_BLUE}{BRIGHT_WHITE}--------------------------{RESET}")
        choice_type = input(f"{YELLOW}Enter the number for the card category: {RESET}")

        try:
            choice_type_int = int(choice_type)
            if 1 <= choice_type_int <= 3:
                selected_card_type_num = choice_type_int
            else:
                print(f"{RED_X} Invalid choice. Please enter 1, 2, or 3.{RESET}")
                input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")
        except ValueError:
            print(f"{RED_X} Invalid input. Please enter a number.{RESET}")
            input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")

    # Step 2: Select Specific Card within the chosen category
    selected_specific_card_details = None
    while selected_specific_card_details is None:
        if selected_card_type_num == 1:
            display_available_debit_cards()
        elif selected_card_type_num == 2:
            display_available_prepaid_cards()
        elif selected_card_type_num == 3:
            display_available_credit_cards()

        choice_specific_card = input(f"{YELLOW}Enter the number of the specific card to apply for: {RESET}")

        try:
            choice_specific_card_int = int(choice_specific_card)
            # Use display_card_details_info to retrieve the actual details
            card_details = display_card_details_info(selected_card_type_num, choice_specific_card_int)
            
            if card_details:
                selected_specific_card_details = card_details
            else:
                print(f"{RED_X} Invalid selection for this card category. Please try again.{RESET}")
                input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")
        except ValueError:
            print(f"{RED_X} Invalid input. Please enter a number.{RESET}")
            input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")

    # Step 3: Generate details and display card
    if selected_specific_card_details:
        card_name_to_display = selected_specific_card_details["Card Name"]
        currency_to_display = selected_specific_card_details["Currency"]

        print(f"\n{GREEN_CHECK} You have selected the {BOLD}{card_name_to_display}{RESET}.")
        print(f"{CYAN}Generating your new card details...{RESET}")
        time.sleep(2) # Simulate processing

        random_card_number, random_cvv, random_exp_date = generate_random_card_details()

        display_bank_card(
            card_holder_name=user_full_name,
            bank_name="LA FAMILIA BANK", # Maintaining the bank name
            card_number=random_card_number,
            exp_date=random_exp_date,
            cvv=random_cvv,
            card_type_name=card_name_to_display, # Pass the selected card name
            currency_symbol=currency_to_display # Pass the currency symbol
        )
        # This return allows the user to see the card, then choose to exit or apply again
        return 

# --- Main Application Loop ---
def main():
    while True:
        clear_screen()
        print(f"\n{BOLD}{BG_CYAN}{WHITE}--- Banking Terminal Demo ---{RESET}")
        print(f"{BRIGHT_CYAN}1. {WHITE}Apply for a New Card{RESET}")
        print(f"{BRIGHT_CYAN}2. {WHITE}Exit{RESET}")
        print(f"{BOLD}{BG_CYAN}{WHITE}---------------------------{RESET}")

        choice = input(f"{YELLOW}Enter your choice: {RESET}")

        if choice == '1':
            apply_for_card_process()
        elif choice == '2':
            clear_screen()
            print(f"{BOLD}{MAGENTA}Exiting Banking Terminal Demo. Goodbye!{RESET}")
            break
        else:
            print(f"{RED_X} Invalid choice. Please try again.{RESET}")
            input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main()