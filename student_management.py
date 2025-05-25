import json
from datetime import datetime, timedelta
import math
import random # Added for dummy grade generation

# --- Configuration Data ---

DATA_FILE = "students_data.json" # The text file to store student data

# Define course blocks (assuming 2-month blocks)
# Key: Block Name, Value: (Start Month (int), End Month (int))
BLOCK_SCHEDULE = {
    "Block A": (1, 2),  # Jan-Feb
    "Block B": (3, 4),  # Mar-Apr
    "Block C": (5, 6),  # May-Jun
    "Block D": (7, 8),  # Jul-Aug
    "Block E": (9, 10), # Sep-Oct
    "Block F": (11, 12) # Nov-Dec
}

# Define available courses and their details
# Key: Course Name, Value: {tuition_fee, block_offered, credits, software_and_materials, career_paths}
AVAILABLE_COURSES = {
    "Computer Science I": {
        "tuition_fee": 1200,
        "block_offered": "Block C",
        "credits": 3,
        "software_and_materials": {
            "Required Software": ["Python 3.x Interpreter", "VS Code (or equivalent IDE)", "Git"],
            "Study Materials": ["Introduction to Python Programming (PDF)", "Algorithms & Data Structures Fundamentals (Textbook)"]
        },
        "career_paths": [
            "Junior Software Developer", "IT Support Specialist", "Data Entry Analyst",
            "Technical Writer (Software)", "Quality Assurance Tester"
        ]
    },
    "Calculus II": {
        "tuition_fee": 1000,
        "block_offered": "Block D",
        "credits": 3,
        "software_and_materials": {
            "Required Software": ["Wolfram Alpha (online)", "Desmos Graphing Calculator"],
            "Study Materials": ["Calculus: Early Transcendentals (Textbook)", "Practice Problem Sets (PDF)"]
        },
        "career_paths": [
            "Actuarial Assistant", "Research Assistant (Mathematics)", "Financial Analyst (Entry-Level)",
            "Data Analyst Trainee", "Statistician Assistant"
        ]
    },
    "Introduction to Psychology": {
        "tuition_fee": 900,
        "block_offered": "Block E",
        "credits": 3,
        "software_and_materials": {
            "Required Software": ["No specific software"],
            "Study Materials": ["Psychology: The Core (Textbook)", "Case Studies in Psychology (PDF)"]
        },
        "career_paths": [
            "Social Work Assistant", "Human Resources Assistant", "Market Research Associate",
            "Community Outreach Coordinator", "Entry-Level Counselor Assistant"
        ]
    },
    "Database Management": {
        "tuition_fee": 1500,
        "block_offered": "Block F",
        "credits": 4,
        "software_and_materials": {
            "Required Software": ["MySQL Workbench", "PostgreSQL", "DBeaver (Database Tool)"],
            "Study Materials": ["Database Systems: Design, Implementation, & Management (Textbook)", "SQL Practice Guide (PDF)"]
        },
        "career_paths": [
            "Junior Database Administrator", "Data Modeler", "Business Intelligence Analyst (Entry-Level)",
            "SQL Developer Assistant", "Database Support Specialist"
        ]
    },
    "Web Development Basics": {
        "tuition_fee": 1300,
        "block_offered": "Block A",
        "credits": 3,
        "software_and_materials": {
            "Required Software": ["VS Code", "Web Browser (Chrome/Firefox)", "Git"],
            "Study Materials": ["HTML & CSS: Design and Build Websites (Textbook)", "JavaScript Fundamentals (Online Resource)"]
        },
        "career_paths": [
            "Front-End Web Developer (Junior)", "UI/UX Assistant", "Web Content Editor",
            "Digital Marketing Assistant (Web Focus)", "Freelance Web Designer (Entry-Level)"
        ]
    },
    "Data Structures": {
        "tuition_fee": 1400,
        "block_offered": "Block B",
        "credits": 4,
        "software_and_materials": {
            "Required Software": ["Java Development Kit (JDK)", "IntelliJ IDEA (or Eclipse)"],
            "Study Materials": ["Data Structures and Algorithms in Java (Textbook)", "Algorithm Analysis Handout (PDF)"]
        },
        "career_paths": [
            "Software Development Engineer (Entry-Level)", "Algorithm Developer Assistant", "Systems Analyst Trainee",
            "Backend Developer (Junior)", "Computational Research Assistant"
        ]
    },
}

# --- Data Persistence Functions ---

def load_students_data():
    """Loads student data from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Convert enrollment_date strings back to datetime objects
            for student_id, details in data.items():
                if 'enrollment_date' in details and isinstance(details['enrollment_date'], str):
                    try:
                        details['enrollment_date'] = datetime.strptime(details['enrollment_date'], '%Y-%m-%d')
                    except ValueError:
                        details['enrollment_date'] = None # Handle invalid date string
            return data
    except FileNotFoundError:
        print(f"'{DATA_FILE}' not found. Starting with empty student data.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from '{DATA_FILE}'. Starting with empty student data.")
        return {}

def save_students_data(data):
    """Saves student data to the JSON file."""
    # Convert datetime objects to string format for JSON serialization
    data_to_save = {}
    for student_id, details in data.items():
        temp_details = details.copy() # Create a shallow copy to modify
        if 'enrollment_date' in temp_details and isinstance(temp_details['enrollment_date'], datetime):
            temp_details['enrollment_date'] = temp_details['enrollment_date'].strftime('%Y-%m-%d')
        data_to_save[student_id] = temp_details

    with open(DATA_FILE, 'w') as f:
        json.dump(data_to_save, f, indent=4)
    print(f"Student data saved to '{DATA_FILE}'.")

# --- Functions for Student Operations (administrative) ---

def display_all_students(data):
    """Displays a list of all student IDs and names."""
    if not data:
        print("No student data available.")
        return

    print("\n--- Student List ---")
    for student_id, details in data.items():
        print(f"ID: {student_id}, Name: {details.get('full_name', 'N/A')}")
    print("-" * 20)

def add_new_student(data):
    """Adds a new student to the system."""
    new_student_id = input("Enter ID for new student (e.g., S005): ").strip().upper()
    if new_student_id in data:
        print(f"\nStudent with ID '{new_student_id}' already exists.")
        return

    full_name = input(f"Enter full name for {new_student_id}: ")
    email = input(f"Enter email for {new_student_id}: ")
    mentor = input(f"Enter mentor for {new_student_id}: ")
    instructor = input(f"Enter instructor for {new_student_id}: ")
    address = input(f"Enter address for {new_student_id}: ")
    phone_number = input(f"Enter phone number for {new_student_id}: ")

    current_course = "Not yet registered" # Initial state
    total_credits_earned = 0 # Initial state
    enrollment_date_str = input(f"Enter enrollment date for {new_student_id} (YYYY-MM-DD, press Enter for today): ")
    try:
        if enrollment_date_str:
            enrollment_date = datetime.strptime(enrollment_date_str, '%Y-%m-%d')
        else:
            enrollment_date = datetime.now() # Default to today
    except ValueError:
        print("Invalid date format. Using current date as enrollment date.")
        enrollment_date = datetime.now()

    # Collect initial degree/certificate info
    degrees = []
    certs = []
    print("\nEnter initial Degrees (type 'done' when finished):")
    while True:
        degree_name = input("Degree Name (e.g., Associate Degree in Software Development): ").strip()
        if degree_name.lower() == 'done':
            break
        degrees.append({"name": degree_name})

    print("\nEnter initial Certificates (type 'done' when finished):")
    while True:
        cert_name = input("Certificate Name (e.g., Web Development): ").strip()
        if cert_name.lower() == 'done':
            break
        certs.append({"name": cert_name})


    data[new_student_id] = {
        "full_name": full_name,
        "email": email,
        "mentor": mentor,
        "instructor": instructor,
        "address": address, # Added
        "phone_number": phone_number, # Added
        "current_course": current_course,
        "enrollment_date": enrollment_date,
        "total_credits_earned": total_credits_earned,
        "payment_method_details": {}, # Last payment
        "payment_history": [], # To store multiple payments
        "linked_payment_methods": [], # Can be populated later or during registration
        "degrees": degrees,
        "certificates": certs,
        "endorsement_status": "Not Submitted", # New field
        "courses_completed": [] # New field for transcript
    }
    print(f"\nStudent '{new_student_id}' added successfully!")
    save_students_data(data) # Save after adding

def delete_student(data):
    """Deletes a student from the system."""
    student_id_to_delete = input("Enter student ID to delete: ").strip().upper()
    if student_id_to_delete in data:
        confirm = input(f"Are you sure you want to delete student '{student_id_to_delete}'? (yes/no): ").lower()
        if confirm == 'yes':
            del data[student_id_to_delete]
            print(f"Student '{student_id_to_delete}' deleted successfully.")
            save_students_data(data) # Save after deleting
        else:
            print("Deletion cancelled.")
    else:
        print(f"Student with ID '{student_id_to_delete}' not found.")

# --- Student Portal "My Profile" Functionalities ---

def display_my_information(student_id, student_info):
    """Displays detailed student personal information."""
    print("\n--- My Information ---")
    print(f"Full Name: {student_info.get('full_name', 'N/A')}")
    print(f"Student ID: {student_id}")
    print(f"Address: {student_info.get('address', 'N/A')}")
    print(f"Phone Number: {student_info.get('phone_number', 'N/A')}")

    print("\nLinked Payment Methods:")
    if student_info.get('linked_payment_methods'):
        for i, method in enumerate(student_info['linked_payment_methods']):
            details = method.get('account') or method.get('number') # PayPal account or M-Pesa number
            print(f"  {i+1}. Method: {method.get('method')}, Details: {details}")
    else:
        print("  No linked payment methods.")
    print("-" * 30)

    update_choice = input("Do you want to update any personal information or manage linked payment methods? (yes/no): ").lower()
    if update_choice == 'yes':
        update_student_information(students_data, student_id)

def update_student_information(data, student_id):
    """Allows updating personal information and linked payment methods."""
    student = data[student_id]
    print("\nWhich information would you like to update?")
    print("1. Full Name")
    print("2. Address")
    print("3. Phone Number")
    print("4. Manage Linked Payment Methods")
    print("5. Go Back")

    choice = input("Enter choice (1-5): ").strip()
    if choice == '1':
        new_value = input(f"Enter new full name: ")
        student["full_name"] = new_value
        print("Full Name updated.")
    elif choice == '2':
        new_value = input(f"Enter new address: ")
        student["address"] = new_value
        print("Address updated.")
    elif choice == '3':
        new_value = input(f"Enter new phone number: ")
        student["phone_number"] = new_value
        print("Phone Number updated.")
    elif choice == '4':
        _manage_linked_payment_methods(student)
    elif choice == '5':
        return
    else:
        print("Invalid choice.")
    save_students_data(data)

def _manage_linked_payment_methods(student):
    """Allows adding/removing linked payment methods."""
    print("\n--- Manage Linked Payment Methods ---")
    while True:
        print("Current Linked Methods:")
        if student.get('linked_payment_methods'):
            for i, method in enumerate(student['linked_payment_methods']):
                details = method.get('account') or method.get('number') # PayPal account or M-Pesa number
                print(f"  {i+1}. Method: {method.get('method')}, Details: {details}")
        else:
            print("  No linked methods currently.")
        print("\nOptions:")
        print("1. Add a new linked payment method")
        print("2. Remove an existing method (by number)")
        print("3. Done managing methods")
        method_choice = input("Enter choice: ").strip()

        if method_choice == '1':
            method_type = input("Enter method type (PayPal/M-Pesa): ").strip().lower()
            if method_type == 'paypal':
                account_detail = input("Enter PayPal account email: ").strip()
                student.setdefault('linked_payment_methods', []).append({"method": "PayPal", "account": account_detail})
                print("PayPal method added.")
            elif method_type == 'm-pesa':
                account_detail = input("Enter M-Pesa number: ").strip()
                student.setdefault('linked_payment_methods', []).append({"method": "M-Pesa", "number": account_detail})
                print("M-Pesa method added.")
            else:
                print("Unsupported payment method type.")
        elif method_choice == '2':
            try:
                idx_to_remove = int(input("Enter number of method to remove: ")) - 1
                if 0 <= idx_to_remove < len(student.get('linked_payment_methods', [])):
                    removed_method = student['linked_payment_methods'].pop(idx_to_remove)
                    print(f"{removed_method.get('method')} method removed.")
                else:
                    print("Invalid method number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif method_choice == '3':
            break
        else:
            print("Invalid option.")


def display_username_emails(student_info):
    """Displays and allows updating email (username is implicit via student ID)."""
    print("\n--- Username & Emails ---")
    print(f"Your Student ID (Username): {student_info['id']}")
    print(f"Current Email: {student_info.get('email', 'N/A')}")
    print("-" * 30)
    update_email_choice = input("Do you want to update your email? (yes/no): ").lower()
    if update_email_choice == 'yes':
        new_email = input("Enter new email address: ")
        student_info['email'] = new_email
        save_students_data(students_data)
        print("Email updated successfully.")
    print("-" * 30)

def display_message_center():
    """Placeholder for Message Center."""
    print("\n--- Message Center ---")
    print("No new messages. Check back later for important announcements and communications.")
    print("-" * 30)

def display_privacy_settings():
    """Placeholder for Privacy Settings."""
    print("\n--- Privacy Settings ---")
    print("Manage your privacy preferences here. (Not implemented yet)")
    print("-" * 30)

def display_my_profile_menu(student_id, student_info):
    """
    Displays the "My Profile" sub-menu from the image.
    """
    while True:
        print("\n--- My Profile Menu ---")
        print("  1. Message Center")
        print("  2. My Information")
        print("  3. Privacy Settings")
        print("  4. Username & Emails")
        print("  5. Go Back to Main Portal Menu")
        print("-" * 30)

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_message_center()
        elif choice == '2':
            display_my_information(student_id, student_info)
        elif choice == '3':
            display_privacy_settings()
        elif choice == '4':
            display_username_emails(student_info)
        elif choice == '5':
            print("Returning to main portal menu.")
            break
        else:
            print("Invalid choice. Please try again.")

# --- Academics Submenu ---

def display_student_program(student_info):
    """Displays the student's registered courses and academic progress."""
    print("\n--- My Program (Registered Courses) ---")
    print(f"Current Registered Course: {student_info.get('current_course', 'N/A')}")
    print(f"Total Credits Earned: {student_info.get('total_credits_earned', 0)}")

    TARGET_CREDITS_FOR_GRADUATION = 120
    AVG_CREDITS_PER_BLOCK = 3

    remaining_credits = TARGET_CREDITS_FOR_GRADUATION - student_info.get('total_credits_earned', 0)

    if remaining_credits <= 0:
        print("Expected Graduation Status: GRADUATED!")
    else:
        blocks_remaining = math.ceil(remaining_credits / AVG_CREDITS_PER_BLOCK)
        months_remaining = blocks_remaining * 2

        enrollment_date = student_info.get('enrollment_date')
        if isinstance(enrollment_date, datetime):
            expected_grad_date = enrollment_date + timedelta(days=months_remaining * 30.44)
            print(f"Expected Graduation Date: {expected_grad_date.strftime('%B %Y')}")
        else:
            print("Expected Graduation Date: N/A (Enrollment date not valid or not set)")
    print("-" * 30)

def display_certificates_and_degrees_portal():
    """Placeholder for Certificates and Degrees."""
    print("\n--- Certificates and Degrees ---")
    print("This section shows your earned certificates and degrees.")
    print("For details, please refer to 'My Profile' section.")
    print("-" * 30)

def display_degree_progress_audit():
    """Placeholder for Degree Progress Audit."""
    print("\n--- Degree Progress Audit ---")
    print("This section would show your detailed progress towards your degree requirements.")
    print("Please consult your academic advisor for a full audit.")
    print("-" * 30)

def display_class_schedule():
    """Placeholder for Class Schedule."""
    print("\n--- Class Schedule ---")
    print("Your current class schedule will be displayed here.")
    print("-" * 30)

def display_academics_menu(student_id, student_info):
    """
    Displays the Academics sub-menu and handles navigation within it.
    """
    while True:
        print("\n--- Academics Menu ---")
        print("  1. My Program (Registered Courses)")
        print("  2. Register for Next Block's Course") # Moved registration here
        print("  3. Certificates and Degrees")
        print("  4. Degree Progress Audit")
        print("  5. Class Schedule")
        print("  6. Go Back to Main Portal Menu")
        print("-" * 30)

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_student_program(student_info)
        elif choice == '2':
            _handle_course_registration(student_id, student_info)
        elif choice == '3':
            display_certificates_and_degrees_portal()
        elif choice == '4':
            display_degree_progress_audit()
        elif choice == '5':
            display_class_schedule()
        elif choice == '6':
            print("Returning to main portal menu.")
            break
        else:
            print("Invalid choice. Please try again.")


def _handle_course_registration(student_id, student):
    """Handles the actual course registration and payment process."""
    print("\n--- Course Registration ---")

    # Ecclesiastical Endorsement Check
    endorsement_status = student.get('endorsement_status', 'Not Submitted')
    if endorsement_status != "Approved":
        print(f"\nImportant: Your Ecclesiastical Endorsement is currently '{endorsement_status}'.")
        print("You must have an 'Approved' endorsement to register for courses.")
        endorsement_choice = input("Would you like to manage your endorsement now? (yes/no): ").lower()
        if endorsement_choice == 'yes':
            handle_ecclesiastical_endorsement(student_id, student) # Direct to endorsement management
            # After managing, re-check status. If still not approved, prevent registration.
            if student.get('endorsement_status') != "Approved":
                print("Endorsement not approved. Cannot proceed with course registration.")
                return
        else:
            print("Course registration cancelled due to unapproved endorsement.")
            return

    # Continue with course registration if endorsement is approved
    print("Available Course Blocks:")
    for block_name, (start_month, end_month) in BLOCK_SCHEDULE.items():
        print(f"- {block_name}: Months {start_month}-{end_month}")

    selected_block = input("Enter the block you wish to register for (e.g., Block C): ").strip()
    if selected_block not in BLOCK_SCHEDULE:
        print("Invalid block name. Please try again.")
        return

    print(f"\nCourses available in {selected_block}:")
    available_courses_in_block = {}
    for course_name, details in AVAILABLE_COURSES.items():
        if details["block_offered"] == selected_block:
            available_courses_in_block[course_name] = details
            print(f"- {course_name} (Fee: ${details['tuition_fee']}, Credits: {details['credits']})")

    if not available_courses_in_block:
        print(f"No courses available in {selected_block} currently.")
        return

    chosen_course = input("Enter the full name of the course you want to register for: ").strip()
    if chosen_course not in available_courses_in_block:
        print("Invalid course name. Please choose from the list.")
        return

    course_details = available_courses_in_block[chosen_course]
    tuition_fee = course_details["tuition_fee"]
    course_credits = course_details["credits"]

    print(f"\nYou selected '{chosen_course}'. Tuition fee: ${tuition_fee}")

    # Payment
    payment_method = input("Choose payment method (PayPal/M-Pesa): ").strip().lower()
    payment_info = {}

    if payment_method == "paypal":
        paypal_account = input("Enter your PayPal account email: ")
        payment_info = {"method": "PayPal", "account": paypal_account, "amount": tuition_fee, "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        print(f"Processing ${tuition_fee} via PayPal account: {paypal_account}...")
        print("PayPal payment simulation successful!")
    elif payment_method == "m-pesa":
        mpesa_number = input("Enter your M-Pesa number: ")
        payment_info = {"method": "M-Pesa", "number": mpesa_number, "amount": tuition_fee, "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        print(f"Processing KSh. {tuition_fee} via M-Pesa number: {mpesa_number}...")
        print("M-Pesa payment simulation successful!")
    else:
        print("Invalid payment method. Registration failed.")
        return

    # Update student data
    # Before changing current_course, if there was one, move it to completed
    if student.get('current_course') and student['current_course'] != "Not yet registered":
        # For simulation, assign a dummy grade and add to completed courses
        # In a real system, this would happen after a term ends and grades are finalized
        completed_course_name = student['current_course']
        completed_course_credits = AVAILABLE_COURSES.get(completed_course_name, {}).get('credits', 0)
        # Randomly assign a grade for simulation purposes
        grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
        dummy_grade = random.choice(grades)

        student.setdefault('courses_completed', []).append({
            "course_name": completed_course_name,
            "grade": dummy_grade,
            "credits": completed_course_credits
        })
        print(f"'{completed_course_name}' moved to completed courses with grade '{dummy_grade}'.")

    student["current_course"] = chosen_course
    student["total_credits_earned"] = student.get("total_credits_earned", 0) + course_credits
    student["payment_method_details"] = payment_info # Store last payment details
    student.setdefault('payment_history', []).append(payment_info) # Add to payment history

    # Optionally, add this payment method to linked_payment_methods if it's new
    if payment_info.get('method') and (payment_info.get('account') or payment_info.get('number')):
        new_linked_method = {
            "method": payment_info['method'],
            "account": payment_info.get('account'),
            "number": payment_info.get('number')
        }
        # Check if the exact method (type and identifier) is already linked
        if not any(
            lm.get('method') == new_linked_method['method'] and
            (lm.get('account') == new_linked_method.get('account') or lm.get('number') == new_linked_method.get('number'))
            for lm in student.get('linked_payment_methods', [])
        ):
            student.setdefault('linked_payment_methods', []).append(new_linked_method)


    print(f"Successfully registered for '{chosen_course}'!")
    save_students_data(students_data) # Save after registration

# --- Student Portal "Finances" Functionalities ---

def display_account_information(student_info):
    """Displays financial account information, including payment history."""
    print("\n--- Account Information ---")
    print("Last Payment Details:")
    last_payment = student_info.get('payment_method_details')
    if last_payment:
        for key, value in last_payment.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    else:
        print("  No recent payment record.")

    print("\nPayment History:")
    payment_history = student_info.get('payment_history', [])
    if payment_history:
        for i, payment in enumerate(payment_history):
            print(f"  Payment {i+1}:")
            for key, value in payment.items():
                print(f"    {key.replace('_', ' ').title()}: {value}")
            print("-" * 10)
    else:
        print("  No payment history available.")
    print("-" * 30)

def apply_tuition_discount():
    """Placeholder for Tuition Discount."""
    print("\n--- Tuition Discount ---")
    print("Information on eligible tuition discounts will appear here.")
    print("Please contact the financial aid office for details.")
    print("-" * 30)

def pay_tuition(student_id, student_info):
    """Handles direct tuition payment."""
    print("\n--- Pay Tuition ---")
    amount_to_pay = input("Enter the amount you wish to pay: ").strip()
    try:
        amount_to_pay = float(amount_to_pay)
        if amount_to_pay <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    print(f"You wish to pay ${amount_to_pay}.")

    # Offer linked payment methods first
    if student_info.get('linked_payment_methods'):
        print("\nChoose from linked payment methods:")
        for i, method in enumerate(student_info['linked_payment_methods']):
            details = method.get('account') or method.get('number')
            print(f"  {i+1}. {method.get('method')} ({details})")
        print(f"  {len(student_info['linked_payment_methods']) + 1}. Use a new method")

        method_choice = input(f"Enter choice (1-{len(student_info['linked_payment_methods']) + 1}): ").strip()
        try:
            choice_idx = int(method_choice) - 1
            if 0 <= choice_idx < len(student_info['linked_payment_methods']):
                chosen_method = student_info['linked_payment_methods'][choice_idx]
                payment_method_type = chosen_method['method']
                if payment_method_type == "PayPal":
                    account_detail = chosen_method.get('account')
                elif payment_method_type == "M-Pesa":
                    account_detail = chosen_method.get('number')
                else: # Should not happen with current logic
                    print("Error: Unknown linked payment method type.")
                    return
            elif choice_idx == len(student_info['linked_payment_methods']):
                payment_method_type = input("Choose new payment method (PayPal/M-Pesa): ").strip().lower()
                if payment_method_type == "paypal":
                    account_detail = input("Enter your PayPal account email: ").strip()
                elif payment_method_type == "m-pesa":
                    account_detail = input("Enter your M-Pesa number: ").strip()
                else:
                    print("Invalid new payment method.")
                    return
            else:
                print("Invalid choice.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
    else: # No linked methods, ask for new one
        payment_method_type = input("Choose payment method (PayPal/M-Pesa): ").strip().lower()
        if payment_method_type == "paypal":
            account_detail = input("Enter your PayPal account email: ").strip()
        elif payment_method_type == "m-pesa":
            account_detail = input("Enter your M-Pesa number: ").strip()
        else:
            print("Invalid payment method.")
            return

    payment_info = {
        "method": payment_method_type.capitalize(),
        "amount": amount_to_pay,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if payment_method_type == "paypal":
        payment_info["account"] = account_detail
        print(f"Processing ${amount_to_pay} via PayPal account: {account_detail}...")
    elif payment_method_type == "m-pesa":
        payment_info["number"] = account_detail
        print(f"Processing KSh. {amount_to_pay} via M-Pesa number: {account_detail}...")

    print("Payment simulation successful!")

    # Add to payment history
    student_info.setdefault('payment_history', []).append(payment_info)
    student_info['payment_method_details'] = payment_info # Update last payment details

    # Add to linked_payment_methods if it's a new method
    new_linked_method_info = {
        "method": payment_method_type.capitalize(),
        "account": account_detail if payment_method_type == "paypal" else None,
        "number": account_detail if payment_method_type == "m-pesa" else None
    }
    if not any(
        lm.get('method') == new_linked_method_info['method'] and
        (lm.get('account') == new_linked_method_info.get('account') or lm.get('number') == new_linked_method_info.get('number'))
        for lm in student_info.get('linked_payment_methods', [])
    ):
        student_info.setdefault('linked_payment_methods', []).append(new_linked_method_info)

    save_students_data(students_data)
    print(f"Payment of ${amount_to_pay} recorded.")
    print("-" * 30)


def display_finances_menu(student_id, student_info):
    """
    Displays the "Finances" sub-menu from the image.
    """
    while True:
        print("\n--- Finances Menu ---")
        print("  1. Account Information")
        print("  2. Tuition Discount")
        print("  3. Pay Tuition")
        print("  4. Go Back to Main Portal Menu")
        print("-" * 30)

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_account_information(student_info)
        elif choice == '2':
            apply_tuition_discount()
        elif choice == '3':
            pay_tuition(student_id, student_info)
        elif choice == '4':
            print("Returning to main portal menu.")
            break
        else:
            print("Invalid choice. Please try again.")

# --- Student Portal "Documents" Functionalities ---

def display_document_center():
    """Placeholder for Document Center."""
    print("\n--- Document Center ---")
    print("Browse and download general student documents here.")
    print("-" * 30)

def download_fill_endorsement_cert():
    """Simulates downloading an endorsement certificate."""
    print("\n--- Download & Fill Endorsement Certificate ---")
    print("You can download the Ecclesiastical Endorsement Certificate form here:")
    print("  [Link: BYU-Pathway-Endorsement-Form.pdf (simulated download)]")
    print("Please fill out the form, obtain the necessary signatures from your ecclesiastical leader, and upload it.")
    print("Follow the instructions carefully.")
    print("-" * 30)


def handle_ecclesiastical_endorsement(student_id, student_info):
    """Manages the student's ecclesiastical endorsement status."""
    print("\n--- Ecclesiastical Endorsement ---")
    current_status = student_info.get('endorsement_status', 'Not Submitted')
    print(f"Your current endorsement status: {current_status}")

    if current_status == "Not Submitted":
        print("\nTo register for courses, an 'Approved' Ecclesiastical Endorsement is required.")
        print("1. Download and fill the endorsement certificate.")
        print("2. Submit the completed certificate for review.")
        print("3. Go Back")
        endorsement_choice = input("Enter your choice: ").strip()
        if endorsement_choice == '1':
            download_fill_endorsement_cert()
        elif endorsement_choice == '2':
            confirm_submit = input("Simulate submission? (yes/no): ").lower()
            if confirm_submit == 'yes':
                student_info['endorsement_status'] = "Pending"
                print("Endorsement submitted. Status updated to 'Pending'.")
                print("It may take some time for your endorsement to be reviewed and approved.")
                save_students_data(students_data)
            else:
                print("Submission cancelled.")
        elif endorsement_choice == '3':
            pass # Go back
        else:
            print("Invalid choice.")
    elif current_status == "Pending":
        print("Your endorsement is currently under review.")
        print("Please check back later for updates.")
        simulate_approval = input("Simulate approval of endorsement? (yes/no): ").lower()
        if simulate_approval == 'yes':
            student_info['endorsement_status'] = "Approved"
            print("Endorsement status updated to 'Approved'. You can now register for courses!")
            save_students_data(students_data)
    elif current_status == "Approved":
        print("Your Ecclesiastical Endorsement is currently APPROVED. You are cleared for course registration.")
        # Optionally, simulate expiration or renewal
        simulate_expire = input("Simulate endorsement expiration? (yes/no): ").lower()
        if simulate_expire == 'yes':
            student_info['endorsement_status'] = "Expired"
            print("Endorsement status updated to 'Expired'. You will need to renew it soon.")
            save_students_data(students_data)
    elif current_status == "Expired":
        print("Your Ecclesiastical Endorsement has EXPIRED.")
        print("You need to renew it to continue registering for courses.")
        renew_choice = input("Simulate renewal (set status to Approved)? (yes/no): ").lower()
        if renew_choice == 'yes':
            student_info['endorsement_status'] = "Approved"
            print("Endorsement successfully renewed and status is now 'Approved'.")
            save_students_data(students_data)
    print("-" * 30)

def display_transcript(student_info):
    """Displays the student's academic transcript."""
    print("\n--- Academic Transcript ---")
    print(f"Student Name: {student_info.get('full_name', 'N/A')}")
    print(f"Student ID: {student_info['id']}")
    print(f"Enrollment Date: {student_info['enrollment_date'].strftime('%Y-%m-%d') if isinstance(student_info['enrollment_date'], datetime) else 'N/A'}")
    print(f"Total Credits Earned: {student_info.get('total_credits_earned', 0)}")
    print("\nCourses Completed:")
    if student_info.get('courses_completed'):
        for course in student_info['courses_completed']:
            print(f"  - Course: {course.get('course_name', 'N/A')}")
            print(f"    Grade: {course.get('grade', 'N/A')}")
            print(f"    Credits: {course.get('credits', 'N/A')}")
            print("    ---")
    else:
        print("  No courses completed yet.")
    print("-" * 30)


def display_documents_menu(student_id, student_info):
    """
    Displays the "Documents" sub-menu from the image.
    """
    while True:
        print("\n--- Documents Menu ---")
        print("  1. Document Center")
        print("  2. Ecclesiastical Endorsement")
        print("  3. Transcript")
        print("  4. Go Back to Main Portal Menu")
        print("-" * 30)

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_document_center()
        elif choice == '2':
            handle_ecclesiastical_endorsement(student_id, student_info)
        elif choice == '3':
            display_transcript(student_info)
        elif choice == '4':
            print("Returning to main portal menu.")
            break
        else:
            print("Invalid choice. Please try again.")

# --- Student Portal "Resources" Functionalities ---

def display_student_software(student_info):
    """Displays software and study materials for the student's current course."""
    print("\n--- Student Software & Study Materials ---")
    current_course = student_info.get('current_course')
    if current_course and current_course != "Not yet registered":
        course_details = AVAILABLE_COURSES.get(current_course)
        if course_details and "software_and_materials" in course_details:
            materials = course_details["software_and_materials"]
            print(f"For your current course: '{current_course}'")
            for category, items in materials.items():
                print(f"\n{category}:")
                if items:
                    for item in items:
                        print(f"  - {item}")
                else:
                    print("  No items listed.")
        else:
            print(f"No specific software or materials listed for '{current_course}'.")
    else:
        print("You are not currently registered for a course. Please register to view course-specific resources.")
    print("-" * 30)

def display_careers(student_info):
    """Displays potential career paths related to the student's current course or general fields."""
    print("\n--- Career Opportunities ---")
    current_course = student_info.get('current_course')
    if current_course and current_course != "Not yet registered":
        course_details = AVAILABLE_COURSES.get(current_course)
        if course_details and "career_paths" in course_details and course_details["career_paths"]:
            print(f"Potential career paths related to '{current_course}':")
            for path in course_details["career_paths"]:
                print(f"  - {path}")
        else:
            print(f"No specific career paths listed for '{current_course}'.")
    else:
        print("Considering a career in the following fields might be beneficial:")
        # Provide general career advice if no current course is registered
        general_careers = [
            "Technology & Software Development",
            "Business & Management",
            "Healthcare & Wellness",
            "Education & Training",
            "Creative Arts & Design"
        ]
        for career in general_careers:
            print(f"  - {career}")
    print("\nFor more personalized career guidance, please visit the Careers Services office.")
    print("-" * 30)

def display_academic_tools():
    """Placeholder for Academic Tools."""
    print("\n--- Academic Tools ---")
    print("Access useful academic tools like citation generators, plagiarism checkers, and study guides here.")
    print("(Not implemented yet)")
    print("-" * 30)

def display_student_wellness():
    """Placeholder for Student Wellness."""
    print("\n--- Student Wellness ---")
    print("Find resources for mental health, physical well-being, and stress management.")
    print("(Not implemented yet)")
    print("-" * 30)

def display_community():
    """Placeholder for Community."""
    print("\n--- Community ---")
    print("Connect with fellow students, join study groups, and participate in campus events.")
    print("(Not implemented yet)")
    print("-" * 30)

def display_resources_menu(student_id, student_info):
    """
    Displays the "Resources" sub-menu as per the image.
    """
    while True:
        print("\n--- Resources Menu ---")
        print("  1. Student Software")
        print("  2. Careers")
        print("  3. Academic Tools")
        print("  4. Student Wellness")
        print("  5. Community")
        print("  6. Go Back to Main Portal Menu")
        print("-" * 30)

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_student_software(student_info)
        elif choice == '2':
            display_careers(student_info)
        elif choice == '3':
            display_academic_tools()
        elif choice == '4':
            display_student_wellness()
        elif choice == '5':
            display_community()
        elif choice == '6':
            print("Returning to main portal menu.")
            break
        else:
            print("Invalid choice. Please try again.")

# --- Student Portal Main Menu and Login ---

def student_portal_menu(student_id, student_info):
    """
    Displays the main student portal menu and directs to sub-menus.
    """
    while True:
        print(f"\n--- Welcome to BYU-Pathway Worldwide Student Portal, {student_info.get('full_name', student_id)} ---")
        print("1. My Profile")
        print("2. Academics")
        print("3. Finances")
        print("4. Documents")
        print("5. Resources") # Added Resources menu
        print("6. Logout")
        print("-" * 30)

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_my_profile_menu(student_id, student_info)
        elif choice == '2':
            display_academics_menu(student_id, student_info)
        elif choice == '3':
            display_finances_menu(student_id, student_info)
        elif choice == '4':
            display_documents_menu(student_id, student_info)
        elif choice == '5': # New resources option
            display_resources_menu(student_id, student_info)
        elif choice == '6':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def student_login(data):
    """Handles student login and directs to the portal."""
    student_id = input("\nEnter your Student ID to login: ").strip().upper()
    if student_id in data:
        # In a real system, password authentication would happen here
        print(f"Login successful for {data[student_id]['full_name']}!")
        # Add the student_id to student_info for display_username_emails
        student_info_with_id = data[student_id].copy()
        student_info_with_id['id'] = student_id
        student_portal_menu(student_id, student_info_with_id)
    else:
        print(f"Student with ID '{student_id}' not found.")

# --- Main Application Logic ---

def main():
    """Main function to run the student management system."""
    global students_data # Declare students_data as global
    students_data = load_students_data()

    while True:
        print("\n--- Student Management System ---")
        print("1. Admin: Display All Students")
        print("2. Admin: Add New Student")
        print("3. Admin: Delete Student")
        print("4. Student: Login to Portal")
        print("5. Exit")
        print("-" * 30)

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_all_students(students_data)
        elif choice == '2':
            add_new_student(students_data)
        elif choice == '3':
            delete_student(students_data)
        elif choice == '4':
            student_login(students_data)
        elif choice == '5':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()