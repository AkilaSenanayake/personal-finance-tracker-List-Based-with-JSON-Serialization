import json
from datetime import datetime

name = 'Personal finance tracker'

# Global list to store transactions
transactions = []

# File handling functions
def load_transactions():
    transactions = 0
    try:
        with open('transactions.json','r') as file: #Try to open the file in read mode
            transactions = json.load(file)  #Load the json data from the file
    except FileNotFoundError: 
        pass

#function to save transaction data to a json file
def save_transactions():
    with open('transactions.json','w') as file:
        json.dump(transactions, file)       #This function saves user inputs into a json file

# Feature implementations
#function to add a new transaction
def add_transaction():
    while True:        #Loop indefinitely until a valid amount is entered
        try:
            amount = float(input('Enter the amount : '))
            if amount <= 0:
                print('Enter the amount greater than 0.')
                continue
        except ValueError:
            print('Invalid amount. Please enter a number.')
            continue
        else:
            break

    #get the transaction category from the user
    category = input('Enter the category : ').capitalize()
    while True:
        t = input('Enter the type (Income/Expense) : ').capitalize() #prompt the user to select type
        if t in ['Income','Expense'] :
            break
        else:
            print('Invalid type. Please enter "income" or "Expense".')

    while True:
        try:
            date = datetime.strptime(input('Enter date (YYYY-MM-DD) : '), "%Y-%m-%d") #get the transaction date from the user
        except ValueError:
            print('Invalid date format. Please enter in YYYY-MM-DD format.')
        else:
            break
        
#append the transaction to the global transaction list
    transactions.append([amount, category, t, date.strftime("%Y-%m-%d")])
    print('Transaction added successfully.')
    save_transactions()  #save the updated transaction list to the json file
    

#function to view all transactions
def view_transactions():
    if not transactions:
        print('No transactions.')
    else:
        for i, transaction in enumerate(transactions, start=1):
            print(f"{i}. Amount: {transaction[0]}, Category: {transaction[1]}, Type: {transaction[2]}, Date: {transaction[3]}")
                  

#function to update all transactions
def update_transaction():
    view_transactions()
    if not transactions:  #Check if there are no transaction
        print('No transactions to update')
        add_new_transaction = False
        while True:
            print('Have to add a transaction?')
            selection = input('Enter "yes" or "no" : ').lower()
            if selection == 'yes':
                add_transaction()
                add_new_transaction = True
                break  # Exit the loop after adding a transaction
            elif selection == 'no':
                return  # Exit the function if the user chooses not to add a transaction
            else:
                print('Invalid selection. Please enter "yes" or "no".')

        if add_new_transaction:
            return  # Exit the function if the user added a new transaction
    try:
        index = int(input("Enter the number of the transaction to update: ")) - 1
        if 0 <= index < len(transactions):
            print("Current transaction details:")
            print(f"Amount: {transactions[index][0]}, Category: {transactions[index][1]}, Type: {transactions[index][2]}, Date: {transactions[index][3]}")
            transactions[index][0] = float(input("Enter updated amount: "))
            transactions[index][1] = input("Enter updated category: ").capitalize()
            transactions[index][2] = input("Enter updated type (Income/Expense): ").capitalize()
            transactions[index][3] = input("Enter updated date (YYYY-MM-DD): ")
            print("Transaction updated successfully.")
            save_transactions()
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid index.")  

#function to delete transaction
def delete_transaction():
    view_transactions()  #Display all transactions
    if not transactions:  #check if there are no transactions
        print("No any transactions to delete.")
        return
    try:
        index = int(input('Enter the number of the transaction to delete: ')) - 1
        if 0 <= index < len(transactions):
            del transactions[index]
            print('Deleted successfully.')
            save_transactions()
        else:
            print('Invalid transaction number.')
    except ValueError:
        print('Invalid transaction number.')


#function to display a summary of transactions
def display_summary():
    if not transactions:
        print('No summarized transactions.')
        return

    income_months = []
    expenses_months = []
    income_years = []
    expenses_years = []

    for trans in transactions:
        amount = trans[0]
        t = trans[2]
        date = datetime.strptime(trans[3], "%Y-%m-%d")
        month_key = date.strftime("%Y-%m")
        year_key = date.strftime("%Y")

        if t == 'Income':
            if month_key not in income_months:
                income_months.append((month_key, amount))
            else:
                for i, (month, _) in enumerate(income_months):
                    if month == month_key:
                        income_months[i] = (month, income_months[i][1] + amount)
                        break
            if year_key not in income_years:
                income_years.append((year_key, amount))
            else:
                for i, (year, _) in enumerate(income_years):
                    if year == year_key:
                        income_years[i] = (year, income_years[i][1] + amount)
                        break
        else:
            if month_key not in expenses_months:
                expenses_months.append((month_key, amount))
            else:
                for i, (month, _) in enumerate(expenses_months):
                    if month == month_key:
                        expenses_months[i] = (month, expenses_months[i][1] + amount)
                        break
            if year_key not in expenses_years:
                expenses_years.append((year_key, amount))
            else:
                for i, (year, _) in enumerate(expenses_years):
                    if year == year_key:
                        expenses_years[i] = (year, expenses_years[i][1] + amount)
                        break

    print('Transactions by Month : ')
    print('---------------------')
    for month, tot_income in sorted(income_months):
        tot_expenses = sum(amount for m, amount in expenses_months if m == month)
        net_balance = tot_income - tot_expenses
        print(f"Month: {month}, Total income: {tot_income}, Total expenses: {tot_expenses}, Net balance: {net_balance}")

    print('\nTransactions by Year : ')
    print('---------------------')
    for year, tot_income in sorted(income_years):
        tot_expenses = sum(amount for y, amount in expenses_years if y == year)
        net_balance = tot_income - tot_expenses
        print(f"Year: {year}, Total income: {tot_income}, Total Expenses: {tot_expenses}, Net balance: {net_balance}") 


#function for the main menu of the program
def main_menu(): 
    load_transactions()  # Load transactions at the start
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':  #if the user chooses to add a transaction
            add_transaction()  #call the add_transaction function
        elif choice == '2':  #if the user chooses to view transaction
            view_transactions()  #call the view_transaction function
        elif choice == '3':  #if the user chooses to update transcation
            update_transaction()  #call the update_transaction function
        elif choice == '4':  #if the user chooses to delete  a transaction
            delete_transaction()  #call the display_transaction function
        elif choice == '5':  #if the user chooses to display a summary
            display_summary()  #call the display_summary function
        elif choice == '6':  #if the user chooses to exit
            print("Transaction saved. Thank you!!")  #print exit message
            break  #break the loop to exit the application
        else:  #if the user enters an invalid choice
            print("Invalid choice. Please try again.")  #print an error message

if __name__ == "__main__":  #if the script is run as the main program
    main_menu()  #Call the main_menu function to start the application

#If you are paid to do this assignment pleae delete this line of comment

