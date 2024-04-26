import random

class Bank:
    def __init__(self):
        self.accounts = {}
        self.total_balance = 0
        self.total_loan_amount = 0
        self.loan_enabled = True
        self.is_bankrupt = False

    def create_account(self, name, email, address, account_type):
        account_number = random.randint(10000, 99999)
        while account_number in self.accounts:
            account_number = random.randint(10000, 99999)
        self.accounts[account_number] = {'name': name, 'email': email, 'address': address, 'type': account_type, 'balance': 0, 'loan_taken': 0, 'transaction_history': []}
        return account_number

    def delete_account(self, account_number):
        del self.accounts[account_number]

    def deposit(self, account_number, amount):
        self.accounts[account_number]['balance'] += amount
        self.total_balance += amount
        self.accounts[account_number]['transaction_history'].append(f"Deposited: {amount}")

    def withdraw(self, account_number, amount):
        if not self.is_bankrupt:
            if self.accounts[account_number]['balance'] >= amount:
                self.accounts[account_number]['balance'] -= amount
                self.total_balance -= amount
                self.accounts[account_number]['transaction_history'].append(f"Withdrew: {amount}")
                print("Withdraw Successfully!!")
            else:
                print("Withdrawal amount exceeded.")
        else:
            print("The Bank is Bankrupt. Withdrawal Not Allowed.")

    def check_balance(self, account_number):
        return self.accounts[account_number]['balance']

    def check_transaction_history(self, account_number):
        return self.accounts[account_number]['transaction_history']

    def take_loan(self, account_number, amount):
        if self.loan_enabled and self.accounts[account_number]['loan_taken'] < 2:
            self.accounts[account_number]['balance'] += amount
            self.accounts[account_number]['loan_taken'] += 1
            self.total_loan_amount += amount
            self.accounts[account_number]['transaction_history'].append(f"Loan Taken: {amount}")
        else:
            print("Sorry, you cannot take a loan at the moment.")

    def transfer(self, from_account_number, to_account_number, amount):
        if not self.is_bankrupt:
            if to_account_number not in self.accounts:
                print("Account does not exist")
            elif self.accounts[from_account_number]['balance'] >= amount:
                self.accounts[from_account_number]['balance'] -= amount
                self.accounts[to_account_number]['balance'] += amount
                self.accounts[from_account_number]['transaction_history'].append(f"Transferred: {amount} to {to_account_number}")
                self.accounts[to_account_number]['transaction_history'].append(f"Received: {amount} from {from_account_number}")
                print("Transfer Successful!!")
            else:
                print("Insufficient Balance for Transfer.")
        else:
            print("The Bank is Bankrupt. Transfer Not Allowed.")

class User:
    def __init__(self, bank):
        self.bank = bank

    def menu(self):
        print("\nUser Menu:")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Take Loan")
        print("7. Transfer")
        print("8. Exit")

    def create_account(self):
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        address = input("Enter your address: ")
        account_type = input("Enter account type (Savings/Current): ").lower()
        if account_type not in ['savings', 'current']:
            print("Invalid account type.")
            return
        account_number = self.bank.create_account(name, email, address, account_type)
        print(f"Account Created Successfully!! Your Account Number is: {account_number}")

    def deposit(self):
        account_number = int(input("Enter account number: "))
        amount = float(input("Enter amount to deposit: "))
        self.bank.deposit(account_number, amount)
        print("Deposit Successfully!!")

    def withdraw(self):
        account_number = int(input("Enter account number: "))
        amount = float(input("Enter amount to withdraw: "))
        balance = self.bank.check_balance(account_number)
        if balance == 0:
            print("You don't have any money in your account to withdraw.")
            return
        self.bank.withdraw(account_number, amount)

    def check_balance(self):
        account_number = int(input("Enter account number: "))
        balance = self.bank.check_balance(account_number)
        print(f"Available Balance: {balance}")

    def transaction_history(self):
        account_number = int(input("Enter account number: "))
        history = self.bank.check_transaction_history(account_number)
        print("Transaction History:")
        for transaction in history:
            print(transaction)

    def take_loan(self):
        account_number = int(input("Enter account number: "))
        amount = float(input("Enter loan amount: "))
        self.bank.take_loan(account_number, amount)
        print("Loan Taken Successfully!!")

    def transfer(self):
        from_account_number = int(input("Enter your account number: "))
        to_account_number = int(input("Enter recipient's account number: "))
        amount = float(input("Enter amount to transfer: "))
        from_account_balance = self.bank.check_balance(from_account_number)
        if from_account_balance == 0:
            print("You don't have any money in your account to transfer.")
            return
        self.bank.transfer(from_account_number, to_account_number, amount)

class Admin:
    def __init__(self, bank):
        self.bank = bank
        self.username = "admin"
        self.password = "password"

    def authenticate(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        return username == self.username and password == self.password

    def menu(self):
        print("\nAdmin Menu:")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. View All Accounts")
        print("4. Check Total Balance")
        print("5. Check Total Loan Amount")
        print("6. Toggle Loan Feature")
        print("7. Toggle Bankruptcy")
        print("8. Logout")

    def create_account(self):
        name = input("Enter user's name: ")
        email = input("Enter user's email: ")
        address = input("Enter user's address: ")
        account_type = input("Enter account type (Savings/Current): ").lower()
        if account_type not in ['savings', 'current']:
            print("Invalid account type.")
            return
        account_number = self.bank.create_account(name, email, address, account_type)
        print(f"Account Created Successfully!! User's Account Number is: {account_number}")

    def delete_account(self):
        account_number = int(input("Enter account number to delete: "))
        self.bank.delete_account(account_number)
        print("Account Deleted Successfully!!")

    def view_all_accounts(self):
        print("\nAll Accounts:")
        for account_number, details in self.bank.accounts.items():
            print(f"Account Number: {account_number}, Name: {details['name']}, Email: {details['email']}, Address: {details['address']}, Balance: {details['balance']}")

    def check_total_balance(self):
        print(f"Total Balance: {self.bank.total_balance}")

    def check_total_loan_amount(self):
        print(f"Total Loan Amount: {self.bank.total_loan_amount}")

    def toggle_loan_feature(self):
        self.bank.loan_enabled = not self.bank.loan_enabled
        status = "Enabled" if self.bank.loan_enabled else "Disabled"
        print(f"Loan Feature is Now {status}")

    def toggle_bankruptcy(self):
        self.bank.is_bankrupt = not self.bank.is_bankrupt
        status = "Bankrupt" if self.bank.is_bankrupt else "Not Bankrupt"
        print(f"The Bank is Now {status}")

def main():
    bank = Bank()
    user = User(bank)
    admin = Admin(bank)

    while True:
        print("\nWelcome to Banking Management System")
        print("1. User")
        print("2. Admin")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                user.menu()
                option = input("Enter your option: ")

                if option == '1':
                    user.create_account()
                elif option == '2':
                    user.deposit()
                elif option == '3':
                    user.withdraw()
                elif option == '4':
                    user.check_balance()
                elif option == '5':
                    user.transaction_history()
                elif option == '6':
                    user.take_loan()
                elif option == '7':
                    user.transfer()
                elif option == '8':
                    break
                else:
                    print("Invalid option")

        elif choice == '2':
            if admin.authenticate():
                while True:
                    admin.menu()
                    option = input("Enter your option: ")

                    if option == '1':
                        admin.create_account()
                    elif option == '2':
                        admin.delete_account()
                    elif option == '3':
                        admin.view_all_accounts()
                    elif option == '4':
                        admin.check_total_balance()
                    elif option == '5':
                        admin.check_total_loan_amount()
                    elif option == '6':
                        admin.toggle_loan_feature()
                    elif option == '7':
                        admin.toggle_bankruptcy()
                    elif option == '8':
                        break
                    else:
                        print("Invalid option")
            else:
                print("Authentication failed")

        elif choice == '3':
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
