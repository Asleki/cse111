import csv

def main():
    # Open the provinces.txt file for reading.
    # Read the contents of the file into a list where each line of text in the file
    # is stored in a separate element in the list.
    provinces_list = read_text_file_into_list("provinces.txt")

    # Print the entire list.
    print(provinces_list)

    # Remove the first element from the list.
    if len(provinces_list) > 0:
        provinces_list.pop(0)

    # Remove the last element from the list.
    if len(provinces_list) > 0:
        provinces_list.pop()

    # Replace all occurrences of "AB" in the list with "Alberta".
    for i in range(len(provinces_list)):
        if provinces_list[i] == "AB":
            provinces_list[i] = "Alberta"

    # Count the number of elements that are "Alberta" and print that number.
    alberta_count = provinces_list.count("Alberta")
    print(f"\nAlberta occurs {alberta_count} times in the modified list.")

def read_text_file_into_list(filename):
    """
    Reads the contents of a text file into a list.
    Each line of text in the file is stored as a separate element in the list.

    Parameter filename: The name of the text file to read.
    Return: A list of strings, where each string is a line from the file
            with leading/trailing whitespace removed.
    """
    text_list = []
    try:
        with open(filename, "rt") as text_file:
            for line in text_file:
                clean_line = line.strip()
                if clean_line:  # Only add non-empty lines
                    text_list.append(clean_line)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    return text_list

if __name__ == "__main__":
    main()

# Copyright 2025, Alex Malunda. All rights reserved.