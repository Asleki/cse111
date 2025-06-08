name = "Alex"
mobile = "0707176595"
address = "00519"
details = name + " " + mobile 
place = address


# --- Color Codes for Terminal Output ---
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

def display_main_menu(logged_in):
    """Displays the main menu based on login status."""
    
print(f"{YELLOW}\n" + "=" * 60)
print(f"{BLUE}{" "}{">>>"}La Familia Bank - Your Best of the Best".center(50))
print(f"{YELLOW}" + "=" * 60)

print("1. Account Services")
print("2. Explore Our Offers")
print("3. Logout")
print("4. Exit Application")
    
print("1. Open a Bank Account")
print("2. Explore Our Offers")
print("3. Login")
print("4. Exit Application")
print("-" * 50)

