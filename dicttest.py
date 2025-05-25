def main():
    print("--- Example 1 & 2: Simple vs. Compound Values ---")
    # Example 1: Dictionary with simple values
    simple_students_dict = {
        "ID_001": "John Doe",
        "ID_002": "Jane Smith"
    }
    print(f"Dictionary with simple values: {simple_students_dict}")
    print("Each key and value are single strings.")

    # Example 2: Dictionary with compound values (lists)
    compound_students_dict = {
        # student_ID: [given_name, surname, email_address, credits]
        "42-039-4736": ["Clint", "Huish", "hui20001@byui.edu", 16],
        "61-315-0160": ["Amelia", "Davis", "dav21012@byui.edu", 3],
        "10-450-1203": ["Ana", "Soares", "soa22005@byui.edu", 15],
        "75-421-2310": ["Abdul", "Ali", "ali20003@byui.edu", 5],
        "07-103-5621": ["Amelia", "Davis", "dav19008@byui.edu", 0]
    }
    print(f"\nDictionary with compound values: {compound_students_dict}")
    print("Each value is a list, containing multiple pieces of student data.")

    print("\n" + "="*50 + "\n")

    print("--- Example 3 & 4: Finding One Item ---")
    # These are the indexes of the elements in the value lists.
    GIVEN_NAME_INDEX = 0
    SURNAME_INDEX = 1
    # EMAIL_INDEX = 2
    # CREDITS_INDEX = 3

    # Get a student ID from the user.
    student_id_to_find = input("Enter a student ID to find (e.g., 61-315-0160): ")

    # Example 3 (BAD WAY): Using a loop to find an item
    # This is inefficient and should be avoided for dictionary lookups.
    found_student_bad_way = None
    for key, value in compound_students_dict.items():
        if key == student_id_to_find:
            found_student_bad_way = value
            break
    if found_student_bad_way:
        print(f"\n(Bad way) Found student: {found_student_bad_way[GIVEN_NAME_INDEX]} {found_student_bad_way[SURNAME_INDEX]}")
    else:
        print(f"\n(Bad way) No student found with ID: {student_id_to_find}")

    # Example 4 (GOOD WAY): Directly accessing an item in a dictionary
    if student_id_to_find in compound_students_dict:
        student_data_good_way = compound_students_dict[student_id_to_find]
        given_name = student_data_good_way[GIVEN_NAME_INDEX]
        surname = student_data_good_way[SURNAME_INDEX]
        print(f"(Good way) Found student: {given_name} {surname}")
    else:
        print(f"(Good way) No student found with ID: {student_id_to_find}")

    print("\n" + "="*50 + "\n")

    print("--- Example 5 & 6: Processing All Items ---")
    students_for_processing = {
        "42-039-4736": ["Clint", "Huish", "hui20001@byui.edu", 16],
        "61-315-0160": ["Amelia", "Davis", "dav21012@byui.edu", 3],
        "10-450-1203": ["Ana", "Soares", "soa22005@byui.edu", 15],
        "75-421-2310": ["Abdul", "Ali", "ali20003@byui.edu", 5],
        "07-103-5621": ["Amelia", "Davis", "dav19008@byui.edu", 0],
        "81-298-9238": ["Sama", "Patel", "pat21004@byui.edu", 8]
    }
    CREDITS_INDEX = 3
    total_credits = 0

    print("Processing all students to calculate total credits:")
    # Example 5 & 6: Processing all items using a for loop with unpacking
    for student_id, student_info in students_for_processing.items():
        credits = student_info[CREDITS_INDEX]
        total_credits += credits
        print(f"  Student {student_id} has {credits} credits.")

    print(f"Total credits earned by all students: {total_credits}")

    print("\n" + "="*50 + "\n")

    print("--- Example 7: Converting Between Lists and Dictionaries ---")

    # Create a list that contains five student numbers.
    numbers_list = ["42-039-4736", "61-315-0160",
                    "10-450-1203", "75-421-2310", "07-103-5621"]
    # Create a list that contains five student names.
    names_list = ["Clint Huish", "Amelia Davis",
                  "Ana Soares", "Abdul Ali", "Amelia Davis"]

    print(f"Original numbers list: {numbers_list}")
    print(f"Original names list: {names_list}")

    # Convert the numbers and names lists into a dictionary.
    student_names_dict = dict(zip(numbers_list, names_list))
    # Print the entire student dictionary.
    print(f"\nConverted Dictionary: {student_names_dict}")

    # Convert the student dictionary into two lists named keys and values.
    keys_list = list(student_names_dict.keys())
    values_list = list(student_names_dict.values())

    # Print both lists.
    print(f"\nConverted Keys List: {keys_list}")
    print(f"Converted Values List: {values_list}")

if __name__ == "__main__":
    main()
    
# Copyright 2025. Alex Malunda. All rights reserved.  