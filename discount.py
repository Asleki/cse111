import datetime

# Let's see what day of the week it is right now. Monday is 0, and it goes up to Sunday as 6.
#(Monday=0, Tuesday=1, ..., Sunday=6)
today = datetime.datetime.now().weekday()

# Gotta start our order total at zero.
subtotal = 0

# Alright, time to get the stuff the customer wants! We'll keep asking for items
# until they tell us they're done by entering '0' for the quantity.
print("Okay, let's ring up your order. Enter the quantity of each item (type '0' when finished):")
while True:
    # I'm gonna try to get the info for each item here...
    # ...but if they type something that's not a number, I need to catch that!by using a try-except block.
    try:
        quantity = int(input("Quantity: "))
        if quantity == 0:
            # Looks like they're all done adding items. Let's move on to the total.
            break
        price = float(input("Price per item: "))
        # Add the cost of these items to our running total.
        subtotal += quantity * price
    
    except ValueError:
        print("Hold on! Please enter a number for both the quantity and the price.")

discount_rate = 0.10  # We're giving a 10% discount.
sales_tax_rate = 0.06  # And the sales tax is 6%.
discount_amount = 0
total_due = 0

# Let's check if it's Tuesday or Wednesday AND if their order is $50 or more.
# That's when they get the special discount!
if (today == 1 or today == 2) and subtotal >= 50:
    # They get the discount! Let's calculate how much they save.
    discount_amount = subtotal * discount_rate
    # This is what's left after we take off the discount.
    subtotal_after_discount = subtotal - discount_amount
    # Now, let's figure out the sales tax on that discounted price.
    sales_tax_amount = subtotal_after_discount * sales_tax_rate
    # And finally, the grand total they owe.
    total_due = subtotal_after_discount + sales_tax_amount
    print(f"\nAwesome! You got a discount of ${discount_amount:.2f}!")
    print(f"Subtotal after discount: ${subtotal_after_discount:.2f}")
    print(f"Sales tax (6%): ${sales_tax_amount:.2f}")
    print(f"Total amount due: ${total_due:.2f}")
# What if it's Tuesday or Wednesday, but their order isn't quite $50 yet?
elif today == 1 or today == 2:
    amount_needed = 50 - subtotal
    print(f"\nAlmost there for the Tuesday/Wednesday discount!")
    print(f"You need to spend ${amount_needed:.2f} more to get 10% off.")
    # Still gotta calculate the sales tax on what they have so far.
    sales_tax_amount = subtotal * sales_tax_rate
    total_due = subtotal + sales_tax_amount
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Sales tax (6%): ${sales_tax_amount:.2f}")
    print(f"Total amount due: ${total_due:.2f}")
# If it's any other day, no discount today.
else:
    sales_tax_amount = subtotal * sales_tax_rate
    total_due = subtotal + sales_tax_amount
    print(f"\nOkay, here's the total for today:")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Sales tax (6%): ${sales_tax_amount:.2f}")
    print(f"Total amount due: ${total_due:.2f}")
# Copyright 2025, Alex Malunda. All rights reserved.