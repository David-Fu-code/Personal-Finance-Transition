import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ["date", "amount", "category", "description"]
    format = "%d-%m-%Y"

    @classmethod
    def initialize_csv(self):
        try:
            pd.read_csv(self.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns= self.COLUMNS)
            df.to_csv(self.CSV_FILE, index=False)

    @classmethod
    def add_entry(self, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount" : amount,
            "category" : category,
            "description" : description
        }
        with open(self.CSV_FILE, "a", newline="") as csvfile: # Open in apend mode (append at the end of the file) // (Automatically close when you're done)
            writer = csv.DictWriter(csvfile, fieldnames=self.COLUMNS) # Take a dicctionary and write it into the csv file
            writer.writerow(new_entry)
        print("Added succesfully")

# Pandas Dataframe allows to access all of the columns
    @classmethod
    def get_transactions(self, start_date, end_date):
        df = pd.read_csv(self.CSV_FILE)
        # convert the date in datetime objects *
        df["date"] = pd.to_datetime(df["date"], format= self.format) 
        start_date = datetime.strptime(start_date, self.format)
        end_date = datetime.strptime(end_date, self.format)
        # create a mask (Like a filter)
        mask = (df["date"] >= start_date) & (df["date"] <= end_date) # '&' only used when working with pandas dataframe or mask, similary to 'and'
        filter_df = df.loc[mask] # returns a new filtered dataframe 

        if filter_df.empty:
            print("No transactions found in the given date range")
        else:
            print(f"\nTransactions from {start_date.strftime(self.format)} to {end_date.strftime(self.format)}:")
            # we convert the object to string and we format the string (the x are the datetime object that we convert before) *
            print(filter_df.to_string(index=False, formatters={"date": lambda x: x.strftime(self.format)}))

            total_income = filter_df[filter_df["category"] == "Income"]["amount"].sum() # we get all the rows and sum the amount of income
            total_expense = filter_df[filter_df["category"] == "Expense"]["amount"].sum() # we get all the rows and sum the amount of expense
            print("\nSummary")
            print(f"Total Income: {total_income:.2f}€") # Round to 2 decimals
            print(f"Total Expense: {total_expense:.2f}€") 
            print(f"Net Savings {(total_income - total_expense):.2f}")

        return filter_df

# Write a function that will call these functions in the order that we want in order to collect our data
def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

# Graph
def plot_transactions(df):
    df.set_index("date", inplace=True) # Allows to find diferent rows & entries using the data column
    #Incomes
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function
def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter a choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n)").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3")


if __name__ == "__main__":
    main()