import datetime

# Get the current day of the week (Monday is 0, Sunday is 6)
today = datetime.datetime.now().weekday()

# Initialize subtotal
subtotal = 0
discount_applied = False  # Flag to track if a discount was applied

# Loop to get price and quantity until quantity is 0
print("Enter items for the order (enter quantity '0' when done):")
while True:
    # Attempt to get item input, handle non-numeric entries.
    try:
        quantity = int(input("Enter quantity: "))
        if quantity == 0:
            break
        price = float(input("Enter price per item: "))
        subtotal += quantity * price
    except ValueError:
        print("Invalid input. Please enter a number for quantity and price.")

discount_rate = 0.10  # 10% discount
sales_tax_rate = 0.06  # 6% sales tax
discount_amount = 0
total_due = 0

# Check for Tuesday (1) or Wednesday (2) and if subtotal is $50 or greater
if (today == 1 or today == 2) and subtotal >= 50:
    discount_amount = subtotal * discount_rate
    subtotal_after_discount = subtotal - discount_amount
    sales_tax_amount = subtotal_after_discount * sales_tax_rate
    total_due = subtotal_after_discount + sales_tax_amount
    print(f"\nDiscount applied: ${discount_amount:.2f}")
    print(f"Subtotal after discount: ${subtotal_after_discount:.2f}")
    print(f"Sales tax (6%): ${sales_tax_amount:.2f}")
    print(f"Total amount due: ${total_due:.2f}")
    discount_applied = True  # Set the flag to True
elif today == 1 or today == 2:
    amount_needed = 50 - subtotal
    print(f"\nTo receive a 10% discount on Tuesday or Wednesday,")
    print(f"you need to spend ${amount_needed:.2f} more.")
    sales_tax_amount = subtotal * sales_tax_rate
    total_due = subtotal + sales_tax_amount
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Sales tax (6%): ${sales_tax_amount:.2f}")
    print(f"Total amount due: ${total_due:.2f}")
else:
    sales_tax_amount = subtotal * sales_tax_rate
    total_due = subtotal + sales_tax_amount
    print(f"\nSubtotal: ${subtotal:.2f}")
    print(f"Sales tax (6%): ${sales_tax_amount:.2f}")
    print(f"Total amount due: ${total_due:.2f}")

# Message about whether a discount was applied
print("\n---")
if discount_applied:
    print("A 10% discount was applied to your order today!")
else:
    print("No discount was applied to your order today.")
    print("Remember, you can get a 10% discount on orders of $50 or more on Tuesdays and Wednesdays.")
    
    
# Promotion message for future purchases
print("\n---")
print("Did you know? You can get a 10% discount on your order when your subtotal is $50 or more on Tuesdays and Wednesdays!")
print("Come back and save on those days!")
# Copyright 2025, Alex Malunda. All rights reserved.