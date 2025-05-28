# random_numbers.py

import random

def append_random_numbers(numbers_list, quantity=1):
    """
    Appends a specified quantity of random numbers to the end of a list.

    Parameters:
        numbers_list (list): The list to which random numbers will be appended.
        quantity (int, optional): The number of random numbers to append.
                                   Defaults to 1.
    """
    for _ in range(quantity):
        # Generate a random float between 0 and 100 (adjust range as desired)
        random_number = random.uniform(0, 100)
        numbers_list.append(round(random_number, 2)) # Round to 2 decimal places for neatness

def append_random_words(words_list, quantity=1):
    """
    Randomly selects and appends a specified quantity of words
    from a predefined list to the end of another list.

    Parameters:
        words_list (list): The list to which random words will be appended.
        quantity (int, optional): The number of random words to append.
                                  Defaults to 1.
    """
    # Predefined list of words
    possible_words = ["apple", "banana", "cherry", "date", "elderberry",
                      "fig", "grape", "honeydew", "kiwi", "lemon", "mango",
                      "orange", "pear", "quince", "raspberry", "strawberry"] # Added more words

    for _ in range(quantity):
        # Randomly select a word from the possible_words list
        random_word = random.choice(possible_words)
        words_list.append(random_word)

def main():
    """
    The main function to demonstrate list manipulation with default parameters
    and pass by reference, with a creative enhancement for user interaction.
    """
    print("--- Demonstrating Random Numbers ---")
    numbers = [16.2, 12.8, 9.3]
    print(f"Original numbers list: {numbers}")

    # Call append_random_numbers with one argument (quantity defaults to 1)
    append_random_numbers(numbers)
    print(f"Numbers list after 1 default append: {numbers}")

    # Creative Enhancement: User input for quantity of numbers
    try:
        num_to_append_numbers = int(input("\nEnter how many more random numbers to append: "))
        if num_to_append_numbers < 0:
            print("Quantity cannot be negative. Appending 0 numbers.")
            num_to_append_numbers = 0
    except ValueError:
        print("Invalid input. Appending 1 random number.")
        num_to_append_numbers = 1 # Fallback to default if input is not an integer

    # Call append_random_numbers with user-specified quantity
    append_random_numbers(numbers, num_to_append_numbers)
    print(f"Numbers list after user-specified appends: {numbers}")
    print("-" * 30)


    print("\n--- Demonstrating Random Words ---")
    words = ["hello", "world"]
    print(f"Original words list: {words}")

    # Call append_random_words with one argument (quantity defaults to 1)
    append_random_words(words)
    print(f"Words list after 1 default append: {words}")

    # Creative Enhancement: User input for quantity of words
    try:
        num_to_append_words = int(input("\nEnter how many more random words to append: "))
        if num_to_append_words < 0:
            print("Quantity cannot be negative. Appending 0 words.")
            num_to_append_words = 0
    except ValueError:
        print("Invalid input. Appending 1 random word.")
        num_to_append_words = 1 # Fallback to default if input is not an integer

    # Call append_random_words with user-specified quantity
    append_random_words(words, num_to_append_words)
    print(f"Words list after user-specified appends: {words}")
    print("-" * 30)

    # Optional: Another creative touch - a concluding message
    print("\nThank you for exploring random list manipulation!")
    print("Run the program again to try different quantities.")


# Call main to start the program
if __name__ == "__main__":
    main()