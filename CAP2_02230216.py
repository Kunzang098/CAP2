# https://www.freecodecamp.org/news/how-to-build-an-online-banking-system-python-oop-tutorial/
#https://www.youtube.com/watch?v=BRssQPHZMrc

import os
import random

# Account base class
class Account:
    def __init__(self, account_holder, account_number, password, balance, account_type):
        # Initialize account with account_holder, account number, password, balance, and account type
        self.account_holder = account_holder
        self.account_number = account_number
        self.password = password
        self.balance = balance
        self.account_type = account_type

    def deposit(self, amount):
        # Deposit money into account
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        # Withdraw money from account if sufficient balance is available
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def check_balance(self):
        # Check the balance of the account
        return self.balance

# Business account class, inherits from Account
class BusinessAccount(Account):
    def __init__(self, account_holder, account_number, password, balance):
        # Initialize with account type "Business"
        super().__init__( account_holder, account_number, password, balance, "Business")

# Personal account class, inherits from Account
class PersonalAccount(Account):
    def __init__(self, account_holder, account_number, password, balance):
        # Initialize with account type "Personal"
        super().__init__(account_holder, account_number, password, balance, "Personal")

# Bank class to handle account creation, login, etc.
class Bank:
    def __init__(self):
        # Initialize with an empty dictionary of accounts and load accounts from file
        self.accounts = {}
        self.load_accounts()

    def load_accounts(self):
        # Load accounts from "accounts.txt" file if it exists
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as file:
                while True:
                    # Read account details from file
                    account_holder_line = file.readline().strip()
                    if not account_holder_line:
                        break
                    account_number_line = file.readline().strip()
                    password_line = file.readline().strip()
                    account_type_line = file.readline().strip()
                    balance_line = file.readline().strip()

                    # Skip the blank line between accounts
                    file.readline()

                    try:
                        # Parse account details
                        account_holder = account_holder_line.split(": ")[1]
                        account_number = account_number_line.split(": ")[1]
                        password = password_line.split(": ")[1]
                        account_type = account_type_line.split(": ")[1]
                        balance = float(balance_line.split(": ")[1])
                    except IndexError:
                        # Handle any errors in reading account information
                        print("Error reading account information. Skipping entry.")
                        continue

                    # Create account objects based on account type
                    if account_type == "Business":
                        self.accounts[account_number] = BusinessAccount(account_holder, account_number, password, balance)
                    else:
                        self.accounts[account_number] = PersonalAccount(account_holder, account_number, password, balance)

    def save_accounts(self):
        # Save all account details to "accounts.txt" file
        with open("accounts.txt", "w") as file:
            for account in self.accounts.values():
                file.write(f"account holder: {account.account_holder}\n")
                file.write(f"account number: {account.account_number}\n")
                file.write(f"account password: {account.password}\n")
                file.write(f"account type: {account.account_type}\n")
                file.write(f"balance: {account.balance}\n\n")

    def create_account(self, account_type):
        # Create a new account with a random account number and password
        account_holder = input("Enter your name: ")
        account_number = str(random.randint(100000000, 999999999))
        password = str(random.randint(1000, 9999))
        if account_type == "business" or account_type == "b":
            account = BusinessAccount(account_holder, account_number, password, 0.0)
        else:
            account = PersonalAccount(account_holder, account_number, password, 0.0)
        self.accounts[account_number] = account
        self.save_accounts()
        return account_number, password

    def login(self, account_number, password):
        # Login to an account using account number and password
        if account_number in self.accounts:
            if self.accounts[account_number].password == password:
                return self.accounts[account_number]
        return None

    def transfer_money(self, from_account, to_account_number, amount):
        # Transfer money from one account to another
        if to_account_number in self.accounts:
            # Confirm password before transferring money
            confirm_password = input("Enter your password to confirm the transfer: ")
            if confirm_password == from_account.password:
                if from_account.withdraw(amount):
                    self.accounts[to_account_number].deposit(amount)
                    self.save_accounts()
                    return True
            else:
                print("Invalid password! Transfer failed.")
        return False

    def delete_account(self, account_number):
        # Delete an account
        if account_number in self.accounts:
            del self.accounts[account_number]
            self.save_accounts()
            return True
        return False

def main():
    bank = Bank()
    while True:
        # Display main menu
        print("\nWelcome to the Bank of CST")
        print("1. Open Account")
        print("2. Login")
        print("3. Exit")
        option = input("Choose an option: ")

        if option == '1':
            # Open a new account
            account_type = input("Enter account type (Business/Personal): ")
            account_number, password = bank.create_account(account_type)
            print(f"Account created successfully!\nAccount Number: {account_number}\nPassword: {password}")

        elif option == '2':
            # Login to an existing account
            account_number = input("Enter your account number: ")
            password = input("Enter your password: ")
            account = bank.login(account_number, password)
            if account:
                print("Login successful!")
                while True:
                    # Display account menu
                    print("\nWelcome to your account", account.account_holder)
                    print("\n1. Check Balance")
                    print("2. Deposit Money")
                    print("3. Withdraw Money")
                    print("4. Transfer Money")
                    print("5. Delete Account")
                    print("6. Logout")
                    sub_option = input("Choose an option: ")

                    if sub_option == '1':
                        # Check balance
                        print(f"Your balance is: Nu.{account.check_balance()}")

                    elif sub_option == '2':
                        # Deposit money
                        amount = float(input("Enter amount to deposit: "))
                        if account.deposit(amount):
                            bank.save_accounts()
                            print(f"Nu.{amount} deposited successfully")
                        else:
                            print("Invalid deposit amount")

                    elif sub_option == '3':
                        # Withdraw money
                        amount = float(input("Enter amount to withdraw: "))
                        if account.withdraw(amount):
                            bank.save_accounts()
                            print(f"Nu.{amount} withdrawn successfully")
                        else:
                            print("Insufficient funds")

                    elif sub_option == '4':
                        # Transfer money
                        to_account_number = input("Enter recipient account number: ")
                        amount = float(input("Enter amount to transfer: "))
                        if bank.transfer_money(account, to_account_number, amount):
                            print(f"Nu.{amount} transferred successfully")
                        else:
                            print("Transfer failed! Check account details or balance.")

                    elif sub_option == '5':
                        # Delete account
                        confirm = input("Are you sure you want to delete your account? (yes/no): ")
                        if confirm.lower() == 'yes':
                            if bank.delete_account(account.account_number):
                                print("Account deleted successfully")
                                break
                            else:
                                print("Account deletion failed")
                        else:
                            print("Account deletion canceled.")

                    elif sub_option == '6':
                        # Logout
                        print("Logged out successfully")
                        break

                    else:
                        print("Invalid option! Please choose again.")
            else:
                print("Invalid login credentials")

        elif option == '3':
            # Exit the application
            print("Thank you for using Bank of CST.")
            break

        else:
            print("Invalid option! Please choose again.")

if __name__ == "__main__":
    main()
