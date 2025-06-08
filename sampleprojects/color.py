import time
import os
import re # Import regex module for stripping ANSI codes

# --- Color Codes for Terminal Output ---
RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"         # Added for tagline
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BRIGHT_BLACK = "\033[90m"  # For "other faint color" input prompt

# Backgrounds (specifically for faint background)
BG_BRIGHT_BLACK = "\033[100m" # Often appears as a faint/dark grey background

GREEN_CHECKMARK = f"{GREEN}\u2713{RESET}" # Green checkmark
RED_X = f"{RED}\u2717{RESET}"             # Red X
BLUE_INFO = f"{BLUE}i{RESET}"             # Blue info icon
# --- End of Color Codes ---

# --- Bank Details (Constants) ---
BANK_NAME = "La Familia Bank"
BANK_TAGLINE = "Your Trusted Digital Financial Partner"

# --- Utility Function to Clear Screen ---
def clear_screen():
    """Clears the terminal screen."""
    if os.name == 'nt': # For Windows
        _ = os.system('cls')
    else: # For macOS and Linux
        _ = os.system('clear')

# --- Utility Function for User Input ---
def get_user_input(prompt, return_type=str):
    """Gets user input with a prompt, optionally converting its type."""
    while True:
        user_input = input(prompt).strip()
        if return_type == int:
            try:
                return int(user_input)
            except ValueError:
                print(f"{RED_X} {RED}Invalid input. Please enter a number.{RESET}")
        else:
            return user_input

# --- Main Application Loop ---
def main():
    while True:
        clear_screen()
        # Yellow '=========='
        print(f"{YELLOW}======================================================={RESET}")
        # Bank Name: Blue Bold with Faint Background
        print(f"{BG_BRIGHT_BLACK}{BLUE}{BOLD}{BANK_NAME}{RESET}")
        # Tag Line: Blue Italic with Faint Background
        print(f"{BG_BRIGHT_BLACK}{BLUE}{ITALIC}{BANK_TAGLINE}{RESET}\n")
        print(f"{YELLOW}======================================================={RESET}")

        # Choices: Blue text
        print(f"{BLUE}1. Open a Bank Account{RESET}")
        print(f"{BLUE}2. Explore Our Offers{RESET}")
        print(f"{BLUE}3. Login{RESET}")
        print(f"{BLUE}4. Exit Application{RESET}")
        print(f"{YELLOW}-------------------------------------------------------{RESET}")

        # Input prompt: Other faint color (BRIGHT_BLACK)
        choice = get_user_input(f"{BRIGHT_BLACK}Enter your choice: {RESET}", int)

        # --- Example of handling choices (you would expand this) ---
        if choice == 1:
            print(f"{GREEN_CHECKMARK} Navigating to Open Bank Account...")
            # Call a function for opening an account
            time.sleep(2)
        elif choice == 2:
            print(f"{BLUE_INFO} Displaying offers...")
            # Call a function for exploring offers
            time.sleep(2)
        elif choice == 3:
            print(f"{BLUE_INFO} Login functionality is not yet implemented.")
            time.sleep(2)
        elif choice == 4:
            clear_screen()
            print(f"{BOLD}{CYAN}Thank you for banking with {BANK_NAME}. Goodbye!{RESET}")
            break
        else:
            print(f"{RED_X} {RED}Invalid choice. Please select a number from the menu.{RESET}")
            time.sleep(2)

if __name__ == "__main__":
    main()