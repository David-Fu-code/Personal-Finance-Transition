# Write all of the functions here so the main is a bit more clean
from datetime import datetime

date_format = "%d-%m-%Y"
categories = {"I": "Income", "E": "Expense"} # We can add more categories later

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format) # Format to specify the way we want to get the date
    
    try:
        valid_date = datetime.strptime(date_str, date_format) # convert it into a datetime object
        return valid_date.strftime(date_str) # back into string -- cleans date user type in and gives user the format he needs
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format: ")
        return get_date(prompt, allow_default) # Recursive function, it's gonna repeat it until the date is valid

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for Income 'E' for Expense): ").upper()
    if category in categories:
        return categories[category]
    
    print("Invalid category. Please enter 'I' for Income or 'E' for Expense")
    return get_category()

def get_description():
    return input("Enter a description (optional): ")


