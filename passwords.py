
# Enhancement: Provides detailed feedback on password strength,
#              including a breakdown of character types present,
#              suggestions for improvement, and a pass ✅/fail ❌ status
#              for individual password requirements (length, lowercase,
#              uppercase, digits, special characters).
# Enhancement: Allows the user to choose whether to show or hide the password
#              input using asterisks. This feature utilizes the 'getpass'
#              module (imported from the standard Python library) to securely
#              handle password input when hiding is selected, preventing
#              the password from being displayed on the console.
# Enhancement: Shows the entered password and a security reminder if all
#              requirements are met or the strength score is 5 or higher.

# Constants for character types
LOWER = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
UPPER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
SPECIAL = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", "|", ";", ":", '"', "'", ",", ".", "<", ">", "?", "/", "`", "~"]


PASS_MARK = "✅" # Constant representing the checkmark symbol for a passed requirement.
FAIL_MARK = "❌" # Constant representing the cross symbol for a failed requirement.
MIN_LENGTH_THRESHOLD = 10 # Constant defining the minimum acceptable length for a password.

def word_in_file(word, filename, case_sensitive=False):
    """
    Reads a file and checks if the given word exists in it.

    Args:
        word (str): The word to search for.
        filename (str): The path to the file.
        case_sensitive (bool, optional): Whether the match should be case-sensitive. Defaults to False.

    Returns:
        bool: True if the word is found in the file, False otherwise.
    """
    
    
    """
try:
    # Attempt to open the file specified by 'filename' in read mode ('r')
    # using UTF-8 encoding to handle various character sets.
    with open(filename, "r", encoding="utf-8") as file:
        # Iterate through each line in the opened file.
        for line in file:
            # Remove leading/trailing whitespace (including newline characters)
            # from the current line and store it in 'file_word'.
            file_word = line.strip()
            # Check if the comparison should be case-sensitive.
            if case_sensitive:
                # If case-sensitive, compare the input 'word' directly with
                # the 'file_word'. If they are an exact match, return True.
                if word == file_word:
                    return True
            else:
                # If not case-sensitive, convert both the input 'word' and
                # the 'file_word' to lowercase before comparison. If they match
                # (ignoring case), return True.
                if word.lower() == file_word.lower():
                    return True
        # If the loop completes without finding a match, return False
        # indicating the 'word' was not found in the file.
        return False
except FileNotFoundError:
    # If the file specified by 'filename' cannot be found, this block is executed.
    # Print an error message to the console indicating the missing file.
    print(f"Error: File '{filename}' not found.")
    # Return False to signal that the word could not be found due to the missing file.
    return False
"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                file_word = line.strip()
                if case_sensitive:
                    if word == file_word:
                        return True
                else:
                    if word.lower() == file_word.lower():
                        return True
        return False
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return False

def word_has_character(word, character_list):
    """
    Checks if any character in the word is present in the given character list.

    Args:
        word (str): The word to check.
        character_list (list): A list of characters to look for.

    Returns:
        bool: True if any character in the word is in the list, False otherwise.
    """
    for char in word:
        if char in character_list:
            return True
    return False

def word_complexity(word):
    """
    Calculates the complexity of a word based on the types of characters it contains.

    Args:
        word (str): The word to analyze.

    Returns:
        int: The complexity score (0-4).
    """
    complexity = 0
    if word_has_character(word, LOWER):
        complexity += 1
    if word_has_character(word, UPPER):
        complexity += 1
    if word_has_character(word, DIGITS):
        complexity += 1
    if word_has_character(word, SPECIAL):
        complexity += 1
    return complexity

def check_password_requirements(password):
    """
    Checks if the password meets basic strength requirements and provides feedback.

    Args:
        password (str): The password to check.

    Returns:
        dict: A dictionary of requirement checks (length, lower, upper, digits, special).
    """
    requirements = {
        "length": len(password) >= MIN_LENGTH_THRESHOLD,
        "lower": word_has_character(password, LOWER),
        "upper": word_has_character(password, UPPER),
        "digits": word_has_character(password, DIGITS),
        "special": word_has_character(password, SPECIAL),
    }
    all_met = all(requirements.values())
    return requirements, all_met

def password_strength(password, min_length=10, strong_length=16):
    """
    Checks password strength based on dictionary words, common passwords, length, and complexity.

    Args:
        password (str): The password to evaluate.
        min_length (int, optional): The minimum required password length. Defaults to 10.
        strong_length (int, optional): The length at which a password is considered strong. Defaults to 16.

    Returns:
        int: The strength of the password (0-5).
    """
    if word_in_file(password, "wordlist.txt"):
        print("Password is a dictionary word and is not secure.")
        requirements_status, all_requirements_met = check_password_requirements(password)
        print_requirements_feedback(requirements_status)
        return 0
    if word_in_file(password, "toppasswords.txt", case_sensitive=True):
        print("Password is a commonly used password and is not secure.")
        requirements_status, all_requirements_met = check_password_requirements(password)
        print_requirements_feedback(requirements_status)
        return 0

    requirements_status, all_requirements_met = check_password_requirements(password)
    print_requirements_feedback(requirements_status)

    strength = 0
    if len(password) < min_length:
        print("Password is too short and is not secure.")
        strength = 1 # Base strength for being too short
    elif len(password) > strong_length:
        print("Password is long, length trumps complexity this is a good password.")
        strength = 5
    else:
        complexity = word_complexity(password)
        strength = 1 + complexity
        if strength < 4:
            suggestions = []
            if not requirements_status['lower']:
                suggestions.append("Add lowercase letters.")
            if not requirements_status['upper']:
                suggestions.append("Add uppercase letters.")
            if not requirements_status['digits']:
                suggestions.append("Add numeric digits.")
            if not requirements_status['special']:
                suggestions.append("Add special symbols.")
            if suggestions:
                print("Suggestions to improve strength:", " ".join(suggestions))

    return strength, all_requirements_met

def print_requirements_feedback(requirements):
    """
    Prints the password strength requirements with pass/fail indicators.

    Args:
        requirements (dict): A dictionary of requirement checks.
    """
    print("Password Strength Requirements:")
    print(f"  Minimum Length ({MIN_LENGTH_THRESHOLD}): {PASS_MARK if requirements['length'] else FAIL_MARK}")
    print(f"  Contains Lowercase: {PASS_MARK if requirements['lower'] else FAIL_MARK}")
    print(f"  Contains Uppercase: {PASS_MARK if requirements['upper'] else FAIL_MARK}")
    print(f"  Contains Digits: {PASS_MARK if requirements['digits'] else FAIL_MARK}")
    print(f"  Contains Special Characters: {PASS_MARK if requirements['special'] else FAIL_MARK}")
    print("-" * 30)

def main():
    """
    Provides the user input loop for the password strength checker.
    """
    while True:
        show_password_choice = input("Show password while typing? (yes/no): ").lower()
        if show_password_choice == 'yes':
            password = input("Enter a password to check (or 'q' to quit): ")
        elif show_password_choice == 'no':
            import getpass
            password = getpass.getpass("Enter a password to check (or 'q' to quit): ")
        elif show_password_choice == 'q':
            break
        else:
            print("Invalid choice. Assuming hide password.")
            import getpass
            password = getpass.getpass("Enter a password to check (or 'q' to quit): ")

        if password.lower() == 'q':
            break

        strength, all_requirements_met = password_strength(password)
        print(f"Password strength: {strength}")
        if strength == 0:
            print("Very weak.")
        elif strength == 1:
            print("Weak.")
        elif strength == 2:
            print("Fair.")
        elif strength == 3:
            print("Good.")
        elif strength == 4:
            print("Strong.")
        elif strength == 5:
            print("Very strong.")

        if all_requirements_met or strength >= 5:
            print(f"Your password is: {password}")
            print("Please write your password somewhere secure.")

        print("-" * 30)

if __name__ == "__main__":
    main()
    
# Copyright 2025, Alex Malunda. All rights reserved.