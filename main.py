import json
import random
import string
from pathlib import Path

class Bank:
    database = Path(__file__).parent / 'data.json'
    data = []
    
    # Load existing data safely
    try:
        if database.exists():
            with open(database, 'r') as fs:
                content = fs.read()
                # Only load if the file isn't empty
                if content.strip(): 
                    data = json.loads(content)
        else:
            print('No such path exists, creating new database on first save.')   
    except Exception as err:
        print('An error occurred loading the database:', err)

    @staticmethod
    def _update():
        # This will print the EXACT location on your computer
        exact_path = Bank.database.resolve()
        print(f"\n[DEBUG] Saving data to: {exact_path}")
        
        with open(Bank.database, 'w') as fs:
            fs.write(json.dumps(Bank.data, indent=4))
            
        print("[DEBUG] Save complete!")
    
    @classmethod
    def _accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("@!#$%^&*", k=1)
        id_chars = alpha + num + spchar
        random.shuffle(id_chars)
        return "".join(id_chars)
    
    def create_account(self):
        print("\n--- Create Account ---")
        info = {
            'name': input('What is your name? '),
            'age': int(input('What is your age? ')),
            'email': input('What is your email? '),
            'pin': int(input('Enter your four number pin: ')),
            'accountno': Bank._accountgenerate(),
            'balance': 0
        }
        
        if info['age'] < 18 or len(str(info['pin'])) != 4:
            print('Sorry, you cannot create an account.')
        else:
            print('\nAccount has been created successfully!')
            print('-' * 20)
            for key, value in info.items():
                print(f'{key} : {value}')
            print('-' * 20)
            print('Please note down your account number!')
            
            Bank.data.append(info)
            Bank._update()
    
    def deposit_money(self):
        print("\n--- Deposit Money ---")
        accnumber = input('Please enter your account number: ')
        pin = input('Please tell me your pin: ')
        
        # FIX 1: Convert i['pin'] to string so it matches the input string
        userdata = [i for i in Bank.data if i['accountno'] == accnumber and str(i['pin']) == pin]
        
        # FIX 2: Check if the list is empty properly
        if not userdata:
            print('Account does not exist or incorrect pin.')
        else:
            try:
                amount = int(input('Enter the amount you want to deposit: '))
                if amount > 10000 or amount < 0:
                    print('Sorry, that amount is invalid (must be between 0 and 10,000).')
                else:
                    userdata[0]['balance'] += amount
                    Bank._update()
                    print(f'Amount deposited successfully! New balance: {userdata[0]["balance"]}')
            except ValueError:
                print("Please enter a valid numeric amount.")

    def withdraw_money(self):
        print("\n--- Withdraw Money ---")
        accnumber = input('Please enter your account number: ')
        pin = input('Please tell me your pin: ')
        
        # FIX 1: Convert i['pin'] to string so it matches the input string
        userdata = [i for i in Bank.data if i['accountno'] == accnumber and str(i['pin']) == pin]
        
        # FIX 2: Check if the list is empty properly
        if not userdata:
            print('Account does not exist or incorrect pin.')
        else:
            try:
                amount = int(input('Enter the amount you want to withdraw: '))
                if userdata[0]['balance'] < amount:
                    print('You do not have sufficient balance ')
                else:
                    print(userdata)
                    userdata[0]['balance']-=amount
                    Bank._update()
                    print('Amount withdrawn successfully')
            except ValueError:
                print("Please enter a valid numeric amount.")

    def show_details(self):
        accnumber=input('Enter your account number : ')
        pin=int(input("Enter your account's pin : "))
        userdata = [i for i in Bank.data if i['accountno']==accnumber and i['pin']==pin]
        print(userdata)
        for key in userdata[0]:
            print(f'{key} : {userdata[0][key]}')

    def update_details(Self):
        accnumber=input('Enter your account number : ')
        pin=int(input('Enter your pin : '))
        userdata = [x for x in Bank.data if x['accountno']==accnumber and x['pin']==pin]
        if not userdata:
            print('Your account does not exists')
        else:
            newdata = {
                'name' : input('Enter your name'),
                'email' : input('enter yout email or press enter to skip'),
                'pin' : input('enter new pin or press enter to skip: ')
            }
            if newdata['name']=='':
                newdata['name']= userdata[0]['name']
            if newdata['email']=='':
                newdata['email']= userdata[0]['email']
            if newdata['pin']=='':
                newdata['pin']= userdata[0]['pin']

            newdata['age']=userdata[0]['age']
            newdata['accountno']=userdata[0]['accountno']
            newdata['balance']=userdata[0]['balance']

            if type(newdata['pin'])==str:
                newdata['pin']=int(newdata['pin'])
            
            for i in newdata:
                if newdata[i]==userdata[0][i]:
                    continue
                else:
                    userdata[0][i]=newdata[i]
            
            Bank._update()
            
    def delete_account(self):
        accnumber=input('enter your account number')
        pin = int(input('enter your pin '))
        userdata = [i for i in Bank.data if i['accountno']==accnumber and i['pin']==pin]
        if userdata == False:
            print('sorry no such data exist')
        else:
            check = input('Press y if you want to delete or press n')
            if check == 'n' or check == 'N':
                pass
            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print('ACCOUNT DELETED SUCCESSFULLY')
                Bank._update()
# --- Main Application Loop ---
user = Bank()

while True:
    print('''
    1. Create an account
    2. Deposit Money
    3. Withdraw Money
    4. Account Details
    5. Update Details
    6. Delete Account
    7. Exit
    ''')

    try:
        check = int(input('ENTER YOUR RESPONSE: '))
        if check == 1:
            user.create_account()
        if check == 2:
            user.deposit_money()
        if check == 3:
            user.withdraw_money()
        if check==4:
            user.show_details()
        if check==5:
            user.update_details()
        if check==6:
            user.delete_account()
    except ValueError:
        print("Please enter a valid number.")