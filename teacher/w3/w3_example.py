import sys;   
import datetime

#print(dir(sys))

class Account:
    def __new__(cls, *args, **kwargs):
        print('\nCreating instance')
        return super().__new__(cls)
    
    def __init__(self, name,balance):
        self.name = name
        self.balance = balance

    def __str__(self):
        return f'Account of {self.name} with starting balance: {self.balance}'

    def __delattr__(self, __name: str) -> None:
        pass    

    
    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return amount
        else:
            print('Insufficient funds')
            return 0

# Usage
account = Account("Jarron",1000)
print(f'{account.name} initial balance:', account.balance)

account.deposit(500)
print('Balance after deposit:', account.balance)

withdraw_amount = account.withdraw(800)
if withdraw_amount > 0:
    print('Withdrawn:', withdraw_amount)
print('Balance after withdrawal:', account.balance)

class SavingsAccount(Account):
    def __init__(self, name, balance):
        super().__init__(name, balance)
        self.interest_rate = 0.01

    def compute_interest(self, n_periods=1):
        return self.balance * ((1 + self.interest_rate) ** n_periods - 1)
    
           
    def deposit(self, amount,date=datetime.datetime.now()):
        self.balance += amount
        self.update_date= date
    
    
savingsaccount= SavingsAccount("Rick",1000)
print(f'{savingsaccount.name} initial balance:', savingsaccount.balance)  

savingsaccount.deposit(1000)
print('Balance after deposit:', savingsaccount.balance, 'saving date:', savingsaccount.update_date.strftime("%Y-%m-%d %H:%M:%S"))
savingsaccount.withdraw(1000)
print('Balance after withdrawal:', savingsaccount.balance)

print('Interest after 1 year:', savingsaccount.compute_interest(12))


# pip install openpyxl
# show read excel 

import openpyxl

# Replace with the path to your Excel file
excel_file_path = 'grade_list.xlsx'

# Load the Excel workbook and select the sheet
workbook = openpyxl.load_workbook(excel_file_path)
# Get the sheet names
sheet_names = workbook.sheetnames
sheet_name=sheet_names[0]
# Print the sheet names
print("Sheet names:", sheet_names)
sheet = workbook[sheet_name]

# Specify the cell coordinates (row and column indices, 1-based index)
# Access the cell range
cell_range_pattern='c5:j12'
cell_range = sheet[cell_range_pattern]

print(cell_range)
