#==========================
# TRANSATION FUNCTIONS
#=========================

def get_transaction_type():
 while True:
    transaction = input("Did you earn or spend money? (earn/spend): ").lower().strip()

    if transaction in ["earn", "spend"]:
        return transaction
    else:
        print("invalid transaction. Type 'earn' or 'spend'.")

def get_amount():
    while True:
        try:
            amount =  float(input("How much? $"))
            if amount > 0:
                return amount
            else:
                print("Amount must be greater  than 0.")
        except ValueError:
            print("invalid input. Please enter a number. ")
            
def get_category():
    while True:
        choice = input("Category (1: savings, 2: food, 3: transportation, 4: fun): ")

        categories = {"1": "savings", "2":"food", "3":"transportation", "4":"fun"}

        if choice in categories:
            return categories[choice]
        else:
            print("Please enter 1, 2, 3, or 4 only. ")

def save_transaction(transaction, amount, category):
    with open("transaction.txt", "a") as file:
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        file.write(f"{today},{transaction},{amount},{category}\n")
        print("Transaction saved successfully. ")

def view_transactions():
    try:
        with open("transaction.txt" , "r") as  file:
            transactions = file.readlines()
            if not transactions:
                print("No transactions recorded yet")
                
            else:
                print("\n===== YOUR TRANSACTIONS =====")
            for line in transactions:
                parts = parse_transaction(line)
                if len(parts) == 4:
                    print(f"{parts[0]} | {parts[1].upper()} | ${float(parts[2]):.2f} | {parts[3].capitalize()}")
                else:
                    print("Skipping corrupted entry.")
    except FileNotFoundError:
        print("No transactions file found yet.")

def calculate_split(amount):
    savings = amount * 0.60
    investing = amount * 0.20
    spending = amount * 0.20

    print("\n==== YOUR 60/20/20 SPLIT ====")
    print(f"Total Paycheck:       ${amount:.2f}")
    print(f"Savings   (60%):     ${savings:.2f}")
    print(f"Investing (20%):     ${investing:.2f}")
    print(f"Spending  (20%):     ${spending:.2f}")

def monthly_summary():
    try:
        transactions = get_parsed_transactions()

        if not transactions:
                print("No transactions recorded yet.")
                return
            
        total_earned = 0
        total_spent = 0
        transaction_count = 0
        category_totals = {}

        for parts in transactions:

            transaction_count +=1

            transaction_type = parts[1]
            amount = float(parts[2])
            category = parts[3]

            if transaction_type == "earn":
                total_earned += amount
                    
            else:
                total_spent += amount

                if category in category_totals:
                    category_totals[category] += amount
                else:
                    category_totals[category] = amount

        print_header("MONTHLY SUMMARY")
        print(f"Total Transcations: {transaction_count}")
        print(f"Total Earned:     ${total_earned:.2f}")
        print(f"Total Spent:      ${total_spent:.2f}")
        print(f"Net Balance:      ${total_earned - total_spent:.2f}")
        print("\n---- Spending by Category ----")
        for category, total in  category_totals.items():
            print(f"{category.capitalize()}: ${total:.2f}")

    except FileNotFoundError:
        print("No transaction file found yet.")

print("Transaction deleted successfully!")

def edit_transaction():
    transactions = load_transactions()

    if not transactions:
        print("No transactions recorded yet.")
        return
    
    for index, line in enumerate(transactions, start=1):
        print(f"{index}. {line.strip()}")

    edit_index = int(input("Choose transaction to edit: "))

    if edit_index < 1 or edit_index > len(transactions):
        print("Invalid transaction number.")
        return

    selected_transaction = transactions[edit_index - 1]

    parts = parse_transaction(selected_transaction)

    current_amount = parts[2]

    print(f"Current amount: ${current_amount}")

    new_amount = str(get_amount())

    parts[2] = new_amount

    updated_line = ",".join(parts)

    print("\nUpdated transaction: ") 
    print(f"{parts[0]} | "f"{parts[1].upper()} | "f"${float(parts[2]):.2f} | "f"{parts[3].capitalize()}")

    confirmation = input("Save these changes? (y/n): ").lower().strip()

    if confirmation == "y":

        transactions[edit_index - 1] = updated_line + "\n"

        with open("transaction.txt", "w") as file:
            for line in transactions:
                file.write(line)

        print("Transaction updated successfully!")

    else:
        print("Edit cancelled.")
        return

def search_transactions():

    category = input("Enter category to search: ").strip().lower()

    found = False

    for parts in get_parsed_transactions():

        transaction_category = parts[3]

        if transaction_category == category:

            print(f"{parts[0]} | "f"{parts[1].upper()} | "f"${float(parts[2]):.2f} | "f"{parts[3].capitalize()}")

            found = True

    if not found:
        print("No transactions found in that category.")

def financial_dashboard():
    while True:
        print_header("FINANCIAL DASHBOARD")
       
        print("1. Set Goal")
        print("2. View Goals")
        print("3. Delete Goal")
        print("4. Edit Goal")
        print("5. Goal Progress")
        print("6. Graphs")
        print("7. Calculate")
        print("8. Financial Health")
        print("9. Back")

        choice = input("Choose an option: ")

        if choice == "1":
            set_goal()

        elif choice == "2":
            view_goals()

        elif choice == "3":
            delete_goal()

        elif choice == "4":
            edit_goal()

        elif choice == "5":
            goal_progress()

        elif choice == "6":
            graphs()

        elif choice == "7":
            calculate()

        elif choice == "8":
            financial_health()
            
        elif choice == "9":
            break
        else:
            print("Invalid choice. Please enter 1-8.")

#=========================
# GOAL FUNCTIONS
#========================

def set_goal():
    goals = []

    try:
        with open("goals.txt", "r") as file:
            for line in file:
                line = line.strip()
                if "=" in line:
                    category, amount = line.split("=")
                    goals.append([category, amount])
    except FileNotFoundError:
        pass
        
    print("Current goals:", goals)

    category = input("Enter category: ").strip().lower()
    amount = input("Enter amount: ").strip()

    found_index = None
    for i, pair in enumerate(goals):
        if pair[0] == category:
            found_index = i
            break
    print("Found index:", found_index)

    if found_index is not None:
        choice = input(f"Goal for '{category}' already exists. Replace it? (y/n): ")
        print("User choice:", choice)

        if choice.lower() == "y":
            goals[found_index][1] = amount
            print("Update goals:", goals)
        else:
            print("User choice not to be replace, Going back.")
            return
        
    else:
        print("Category not found, will append later.")
        goals.append([category, amount])
        print("Appended goals:", goals)
     
    with open("goals.txt", "w") as file:
        for goal_category, goal_amount in goals:
            file.write(f"{goal_category}={goal_amount}\n")

    print("Goals saved to file.")

def delete_goal():
    try:
        with open("goals.txt", "r") as file:
            goals = file.readlines()

        if not goals:
            print("No goals set yet.")
            return

        for index, line in enumerate(goals, start=1):
            print(f"{index}. {line.strip()}")

        delete_index = int(input("Choose goal to delete: "))

        if delete_index < 1 or delete_index > len(goals):
            print("Invalid goal number.")
            return

        goals.pop(delete_index - 1)

        with open("goals.txt", "w") as file:
            file.writelines(goals)

        print("Goal deleted successfully!")
                            
    except FileNotFoundError:
        print("No goal file found yet.")

def edit_goal():
    try:
        with open("goals.txt", "r") as file:
            goals = file.readlines()

            if not goals:
                print("No goals set yet.")
                return

            for index, line in enumerate(goals, start=1):
                print(f"{index}. {line.strip()}")

            edit_index = int(input("Choose a goal to edit: "))

            if edit_index < 1 or edit_index > len(goals):
                print("Invalid goal number.")
                return
            
            selected_goal = goals[edit_index - 1]

            parts = parse_goal(selected_goal)

            current_amount = parts[1]

            print(f"Current amount: ${current_amount}")

            new_amount = str(get_amount())

            parts[1] = new_amount

            updated_line = "=".join(parts)

            goals[edit_index - 1] = updated_line + "\n"

            with open("goals.txt", "w") as file:
                file.writelines(goals)

            print("Goal updated successfully!")

    except FileNotFoundError:
        print("No goal file found yet.")

def view_goals():
    try:
        with open("goals.txt", "r") as file:
            goals = file.readlines()
            if not goals:
                print("No goals set yet.")

            else:
                for index, line in enumerate(goals, start=1):
                    parts = parse_goal(line)
                    if len(parts) == 2:
                        category = parts[0]
                        goal = parts[1]
                        print(f"{index}. {category.capitalize()} Goal: ${float(goal):.2f}")
                    else:
                        print("Skipping corrupted goal.")
    except FileNotFoundError:
        print("No goal file found yet")

def goal_progress():
    try:
        with open("goals.txt","r") as file:
            goals = file.readlines()

            if not goals:
                print("No goals set yet.")
                return
            
            for line in goals:
                parts = parse_goal(line)
                if len(parts) == 2:
                    category = parts[0]
                    goal = float(parts[1])

                    progress = 0

                    for parts in get_parsed_transactions():
                        
                        if len(parts) == 4:
                            transaction_type = parts[1]
                            amount = float(parts[2])
                            transaction_category = parts[3]

                            if transaction_category == category:
                                if transaction_type == "spend":
                                        progress += amount

                    remaining = max(0, goal - progress)

                    if progress >= goal:
                        print(f"{category.capitalize()} Goal Completed! ")
                    
                    print(f"\n{category.capitalize()} Goal")
                    print(f"Goal Amount: ${goal:.2f}")
                    print(f"Current Progress: ${progress:.2f}")
                    print(f"Remaining: ${remaining:.2f}")

    except FileNotFoundError:
        print("No file found yet.")

#=========================
# GRAPHS & CALCULATIONS
#========================

def graphs():
    while True:
        print("\n==== GRAPHS ====")

        print("1. Income by Category")
        print("2. Expense by Category")
        print("3. Back")

        choice = input("Choose an option: ")

        if choice == "1":

            income_by_category = {}

            for parts in get_parsed_transactions():
                
                transaction_type = parts[1]
                amount = float(parts[2])
                category = parts[3]

                if transaction_type == "earn":

                    if category not in income_by_category:
                        income_by_category[category] = amount

                    else:
                        income_by_category[category] += amount

            print("\nIncome by  category")
            print("(1 █ = $ 10)\n")

            for category, amount in income_by_category.items():

                blocks = int(amount // 10)

                bars = "█" * blocks

                print(f"{category.capitalize():10} {bars} ${amount:.2f}")
                
        elif choice == "2":

            expense_by_category = {}

            for parts in get_parsed_transactions():

                transaction_type = parts[1]
                amount = float(parts[2])
                category = parts[3]

                if transaction_type == "spend":

                    if category not in expense_by_category:
                        expense_by_category[category] = amount

                    else:
                        expense_by_category[category] += amount

            print("\nExpense by  category")
            print("(1 █ = $ 10)\n")

            for category, amount in expense_by_category.items():

                blocks = int(amount // 10)

                bars = "█" * blocks

                print(f"{category.capitalize():10} {bars} ${amount:.2f}")
                
        elif choice == "3":
            return
        
        else:
            print("Invalid choice.")

#==========================
# HELPER FUNCTIONS
#=========================

def load_transactions():

    try:
        with open("transaction.txt", "r") as file:
            return file.readlines()

    except FileNotFoundError:
        return []
    
def print_header(title):
    print("=" * 40)
    print(title.center(40))
    print("=" * 40)

def pause():
    input("\nPress Enter to contiune...")

def parse_transaction(line):
    parts = [part.strip() for part in line.split(",")]
    return parts

def parse_goal(line):
    parts = [part.strip() for part in line.split("=")]
    return parts

def get_parsed_transactions():
    parsed_transactions = []

    transactions = load_transactions()

    for line in transactions:
        parts = parse_transaction(line)

        if len(parts) == 4:
            parsed_transactions.append(parts)

    return parsed_transactions

def calculate():
    while True:
        print("\n==== CALCULATE ====")

        print("1. Total Income")
        print("2. Total Expenses")
        print("3. Current Balance")
        print("4. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":

            total_income = 0

            for parts in get_parsed_transactions():
                
                transaction_type = parts[1]
                amount = float(parts[2])

                if transaction_type == "earn":
                    total_income += amount
            print(f"Total Income: ${total_income:.2f}")

        elif choice == "2":
            
            total_expense = 0

            for parts in get_parsed_transactions():
                
                transaction_type = parts[1]
                amount = float(parts[2])

                if transaction_type == "spend":
                    total_expense += amount
            print(f"Total Expense: ${total_expense:.2f}")

        elif choice == "3":
            
            total_income = 0
            total_expense = 0

            for parts in get_parsed_transactions():
                
                if len(parts) == 4:
                    transaction_type = parts[1]
                    amount = float(parts[2])

                    if transaction_type == "earn":
                        total_income += amount

                    elif transaction_type == "spend":
                        total_expense += amount

            balance = total_income - total_expense

            print(f"Current Balance: ${balance:.2f}")

            print("\nFinancial Status:0")

            if balance > total_income * 0.5:
                print("🟢 Excellent! You're saving more than your're spending.")

            elif balance >= 0:
                print("🟡 Good, but watch your spending.")

            else:
                print("🔴 Warning! You're spending more than you've earned.")

        elif choice == "4":
            return

        else:
            print("Invalid choice.")

def financial_health():
    print("\n" + "=" * 30)
    print("     FINANCIAL HEALTH")
    print("=" * 35)

    total_income = 0
    total_expense = 0

    for parts in get_parsed_transactions():
        if len(parts) == 4:
            transaction_type = parts[1]
            amount = float(parts[2])

            if transaction_type == "earn":
                total_income += amount
            elif transaction_type == "spend":
                total_expense += amount

    balance = total_income - total_expense

    if total_income > 0:
        savings_rate = (balance / total_income) * 100
    else:
        savings_rate = 0

    print(f"Income:   ${total_income:.2f}")
    print(f"Expenses: ${total_expense:.2f}")
    print(f"Balance:  ${balance:.2f}")
    print(f"Savings Rate: {savings_rate:.1f}%")
    
def delete_transaction():
    try: 
        transactions = load_transactions() 
    
        if not transactions:
            print("No transactions recorded yet.") 
            return
         
        for index, line in enumerate(transactions, start=1): 
            print(f"{index}. {line.strip()}")

        delete_index = int(input("Choose transaction to delete: ")) 

        if delete_index < 1 or delete_index > len(transactions): 
            print("Invalid transaction number.") 
            return

        selected_transaction = transactions[delete_index - 1]  

        parts = parse_transaction(selected_transaction)

        print("\nYou are about to delete:") 
        print(f"{parts[0]} | "f"{parts[1].upper()} | "f"${float(parts[2]):.2f} | "f"{parts[3].capitalize()}")

        confirmation = input("Are you sure you want to delete this transaction? (y/n): ").lower().strip() 
     
        if confirmation == "y":

            transactions.pop(delete_index - 1)

            with open("transaction.txt","w") as file: 
                file.writelines(transactions) 
        
            print("Transaction deleted successfully!")

        else:
            print("Deletion cancelled.")
            return
        
    except FileNotFoundError: 
        print("No transaction file found yet.")     

    except ValueError:
        print("Please enter a valid transaction number.")
        
"""
Personal Finance Tracker

Author: Dawens
Version: 1.0

Features
--------
- Add transactions
- View transactions
- Edit transactions
- Delete transactions
- Search transactions
- Savings goals
- Monthly summary
- Dashboard
- Graphs
"""
#=========================
# MAIN PROGRAM
#========================

def main():
    while True:
        
        print_header("PERSONAL FINANCE TRACKER v1.0".center(40))
        
        print("\nTransactions")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Calculate 60/20/20 Split")
        print("4. Delete Transaction")
        print("5. Edit Transaction")
        print("6. Search Transactions")

        print("\nReports")
        print("7. Monthly Summary")
        print("8. Financial Dashboard")

        print("\nSystem")
        print("9. Exit")

        choice = input("\nChoose an option: ")
        
        if choice == "1":
            transaction = get_transaction_type()
            amount = get_amount()
            category = get_category()
            print(f"Transaction recorded: {transaction} of ${amount} for {category}")
            save_transaction(transaction, amount, category)
            pause()
        
        elif choice == "2":
            view_transactions()
            pause()

        elif choice == "3":
            amount = get_amount()
            calculate_split(amount)
            pause()

        elif choice == "4":
            delete_transaction()
            pause()

        elif choice == "5":
            edit_transaction()
            pause()

        elif choice == "6":
            search_transactions()
            pause()

        elif choice == "7":
            monthly_summary()
            pause()

        elif choice == "8":
            financial_dashboard()
        
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-9.")
            
main() 