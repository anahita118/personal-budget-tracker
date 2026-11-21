import csv
import math
import os
from datetime import datetime

DATA_FILE = "budget_data.csv"
CATEGORIES = ["Food", "Travel", "Shopping", "Education",
              "Entertainment", "Bills", "Others"]


def load_data():
    data = {"income": 0.0, "expenses": [], "next_id": 1}

    if not os.path.exists(DATA_FILE):
        return data

    try:
        with open(DATA_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["type"] == "income":
                    data["income"] = float(row["amount"])
                elif row["type"] == "expense":
                    if row["category"] not in CATEGORIES:
                        raise ValueError("Unknown category")
                    expense = {
                        "id": int(row["id"]),
                        "description": row["description"],
                        "amount": float(row["amount"]),
                        "category": row["category"],
                        "date": row["date"],
                    }
                    data["expenses"].append(expense)
                    if expense["id"] >= data["next_id"]:
                        data["next_id"] = expense["id"] + 1
    except (OSError, KeyError, ValueError, csv.Error):
        print("Could not read the saved file. Starting with empty data.")
        return {"income": 0.0, "expenses": [], "next_id": 1}

    return data


def save_data(data):
    try:
        with open(DATA_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["type", "id", "date", "category", "amount", "description"])
            writer.writerow(["income", "", "", "", data["income"], "Total income"])
            for e in data["expenses"]:
                writer.writerow(["expense", e["id"], e["date"], e["category"],
                                 e["amount"], e["description"]])
    except OSError:
        print("Error: Could not save data to the file.")


def get_amount(prompt):
    while True:
        text = input(prompt).strip()
        try:
            amount = float(text)
        except ValueError:
            print("Error: Please enter a number (example: 250 or 99.50).")
            continue

        if not math.isfinite(amount):
            print("Error: Please enter a normal number.")
        elif amount <= 0:
            print("Error: Amount must be greater than zero.")
        else:
            return round(amount, 2)


def get_date(prompt):
    while True:
        text = input(prompt).strip()
        if text == "":
            return datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("Error: Use the format YYYY-MM-DD (example: 2026-11-21).")


def choose_category():
    print("\nCategories:")
    for number, name in enumerate(CATEGORIES, start=1):
        print(f"  {number}. {name}")

    while True:
        choice = input("Choose a category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print(f"Error: Enter a number from 1 to {len(CATEGORIES)}.")


def total_expenses(data):
    total = 0.0
    for expense in data["expenses"]:
        total += expense["amount"]
    return total


def print_expenses(expense_list):
    print(f"\n{'ID':<5}{'Date':<13}{'Category':<15}{'Amount':>10}  Description")
    print("-" * 60)
    for e in expense_list:
        print(f"{e['id']:<5}{e['date']:<13}{e['category']:<15}"
              f"{e['amount']:>10.2f}  {e['description']}")
    print("-" * 60)


def add_income(data):
    print("\n--- Add Monthly Income ---")
    amount = get_amount("Enter income amount: ")
    data["income"] += amount
    save_data(data)
    print(f"Success: Income added. Total income is now {data['income']:.2f}")


def add_expense(data):
    print("\n--- Add Expense ---")
    description = input("Description (example: Lunch): ").strip()
    if description == "":
        description = "No description"

    amount = get_amount("Amount: ")
    category = choose_category()
    date = get_date("Date (YYYY-MM-DD, press Enter for today): ")

    expense = {
        "id": data["next_id"],
        "description": description,
        "amount": amount,
        "category": category,
        "date": date,
    }
    data["expenses"].append(expense)
    data["next_id"] += 1
    save_data(data)
    print(f"Success: Expense added under '{category}' (ID {expense['id']}).")

    if total_expenses(data) > data["income"]:
        print("Warning: Your expenses are now more than your income!")


def view_expenses(data):
    print("\n--- All Expenses ---")
    if len(data["expenses"]) == 0:
        print("No expenses recorded yet.")
    else:
        print_expenses(data["expenses"])


def show_total_expenses(data):
    print("\n--- Total Expenses ---")
    print(f"Number of expenses : {len(data['expenses'])}")
    print(f"Total expenses     : {total_expenses(data):.2f}")


def show_balance(data):
    print("\n--- Remaining Balance ---")
    spent = total_expenses(data)
    balance = data["income"] - spent
    print(f"Total income   : {data['income']:.2f}")
    print(f"Total expenses : {spent:.2f}")
    print(f"Balance left   : {balance:.2f}")
    if balance < 0:
        print("Warning: You have spent more than your income.")


def view_by_category(data):
    print("\n--- Expenses by Category ---")
    if len(data["expenses"]) == 0:
        print("No expenses recorded yet.")
        return

    totals = {}
    for category in CATEGORIES:
        totals[category] = 0.0
    for e in data["expenses"]:
        totals[e["category"]] += e["amount"]

    for category in CATEGORIES:
        count = 0
        for e in data["expenses"]:
            if e["category"] == category:
                count += 1
        print(f"{category:<15}{totals[category]:>10.2f}   ({count} item(s))")


def search_expenses(data):
    print("\n--- Search Expenses ---")
    print("1. Search by category")
    print("2. Search by date")
    choice = input("Enter your choice (1-2): ").strip()

    results = []
    if choice == "1":
        category = choose_category()
        for e in data["expenses"]:
            if e["category"] == category:
                results.append(e)
    elif choice == "2":
        date = get_date("Enter date (YYYY-MM-DD): ")
        for e in data["expenses"]:
            if e["date"] == date:
                results.append(e)
    else:
        print("Error: Invalid choice. Please enter 1 or 2.")
        return

    if len(results) == 0:
        print("No matching expenses found.")
    else:
        print(f"Found {len(results)} matching expense(s):")
        print_expenses(results)


def delete_expense(data):
    print("\n--- Delete Expense ---")
    if len(data["expenses"]) == 0:
        print("No expenses to delete.")
        return

    print_expenses(data["expenses"])
    text = input("Enter the ID of the expense to delete: ").strip()
    if not text.isdigit():
        print("Error: ID must be a number.")
        return

    expense_id = int(text)
    for e in data["expenses"]:
        if e["id"] == expense_id:
            confirm = input(f"Delete '{e['description']}' ({e['amount']:.2f})? (y/n): ")
            if confirm.strip().lower() == "y":
                data["expenses"].remove(e)
                save_data(data)
                print("Success: Expense deleted.")
            else:
                print("Cancelled. Nothing was deleted.")
            return

    print("Error: No expense found with that ID.")


def show_menu():
    print("\n==============================")
    print("    PERSONAL BUDGET TRACKER")
    print("==============================")
    print("1. Add monthly income")
    print("2. Add an expense")
    print("3. View all expenses")
    print("4. Calculate total expenses")
    print("5. Calculate remaining balance")
    print("6. View expenses category-wise")
    print("7. Search expenses (category/date)")
    print("8. Delete an expense")
    print("9. Exit")


def main():
    data = load_data()
    print("Welcome to the Personal Budget Tracker!")

    try:
        while True:
            show_menu()
            choice = input("Enter your choice (1-9): ").strip()

            if choice == "1":
                add_income(data)
            elif choice == "2":
                add_expense(data)
            elif choice == "3":
                view_expenses(data)
            elif choice == "4":
                show_total_expenses(data)
            elif choice == "5":
                show_balance(data)
            elif choice == "6":
                view_by_category(data)
            elif choice == "7":
                search_expenses(data)
            elif choice == "8":
                delete_expense(data)
            elif choice == "9":
                save_data(data)
                print("Data saved. Goodbye!")
                break
            else:
                print("Error: Invalid choice. Please enter a number from 1 to 9.")
    except (KeyboardInterrupt, EOFError):
        save_data(data)
        print("\nProgram stopped. Data saved. Goodbye!")


if __name__ == "__main__":
    main()
