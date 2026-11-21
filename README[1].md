# Personal Budget Tracker

A menu-driven Python program to record income and expenses in the terminal. Records are saved in a CSV file, so they are still there the next time the program runs.

## Features
1. Add monthly income
2. Add an expense (Food, Travel, Shopping, Education, Entertainment, Bills, Others)
3. View all expenses
4. Calculate total expenses
5. Calculate remaining balance
6. View expenses category-wise
7. Search expenses by category or date
8. Delete an expense
9. Exit

## Files
- budget_tracker.py : the program
- Personal_Budget_Tracker.ipynb : the same program as a Colab notebook
- sample_budget_data.csv : sample data, rename it to budget_data.csv to load it
- requirements.txt : empty, no extra packages are needed

## How to run
In Colab, upload the notebook, run the first cell, then run the second cell and type your choices in the box.

On a computer with Python 3:

    python budget_tracker.py

Amounts must be greater than zero. Dates are written as YYYY-MM-DD, and pressing Enter uses today's date.
