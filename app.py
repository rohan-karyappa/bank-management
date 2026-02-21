#IMPORVISED VERSION OF MAIN.PY WITH STREAMLIT INTEGRATION
import streamlit as st
import json
import random
import string
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Nexus Bank", page_icon="🏦", layout="centered")

# --- BACKEND LOGIC (The Bank Class) ---
class Bank:
    database = Path(__file__).parent / 'data.json'
    
    @classmethod
    def load_data(cls):
        try:
            if cls.database.exists():
                with open(cls.database, 'r') as fs:
                    content = fs.read()
                    if content.strip(): 
                        return json.loads(content)
            return []
        except Exception as err:
            st.error(f'An error occurred loading the database: {err}')
            return []

    @classmethod
    def _update(cls, data):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(data, indent=4))
    
    @classmethod
    def _accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("@!#$%^&*", k=1)
        id_chars = alpha + num + spchar
        random.shuffle(id_chars)
        return "".join(id_chars)

# Load data into session state so Streamlit remembers it between clicks
if 'bank_data' not in st.session_state:
    st.session_state.bank_data = Bank.load_data()

# --- FRONTEND UI ---

st.title("🏦 Nexus Bank Portal")
st.markdown("Welcome to the modern banking experience.")

# Sidebar Navigation
menu = ["Create Account", "Deposit Money", "Withdraw Money", "Account Details", "Update Details", "Delete Account"]
choice = st.sidebar.radio("Navigate", menu)

# -----------------------------------------
# 1. CREATE ACCOUNT
# -----------------------------------------
if choice == "Create Account":
    st.subheader("✨ Open a New Account")
    
    with st.form("create_account_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("Full Name")
        age = col2.number_input("Age", min_value=1, max_value=120, step=1)
        email = st.text_input("Email Address")
        pin = st.text_input("Create a 4-digit PIN", type="password", max_chars=4)
        
        submit = st.form_submit_button("Create Account")
        
        if submit:
            if age < 18:
                st.error("Sorry, you must be at least 18 to create an account.")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("Please enter a valid 4-digit numeric PIN.")
            elif not name or not email:
                st.error("Please fill in all fields.")
            else:
                new_account = {
                    'name': name,
                    'age': age,
                    'email': email,
                    'pin': pin, # Stored as string to keep leading zeros safely
                    'accountno': Bank._accountgenerate(),
                    'balance': 0
                }
                st.session_state.bank_data.append(new_account)
                Bank._update(st.session_state.bank_data)
                
                st.success(f"Account created successfully for {name}!")
                st.info(f"**YOUR ACCOUNT NUMBER IS:** `{new_account['accountno']}`\n\nPlease write this down!")

# -----------------------------------------
# 2. DEPOSIT MONEY
# -----------------------------------------
elif choice == "Deposit Money":
    st.subheader("💵 Deposit Funds")
    
    with st.form("deposit_form", clear_on_submit=True):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input("Amount to Deposit", min_value=1, step=100)
        submit = st.form_submit_button("Deposit")
        
        if submit:
            account = next((item for item in st.session_state.bank_data if item["accountno"] == acc_no and str(item["pin"]) == pin), None)
            if account:
                if amount > 10000:
                    st.error("Deposit limit exceeded. Maximum deposit is 10,000 at a time.")
                else:
                    account['balance'] += amount
                    Bank._update(st.session_state.bank_data)
                    st.success(f"Successfully deposited ${amount:,}! New Balance: ${account['balance']:,}")
            else:
                st.error("Invalid Account Number or PIN.")

# -----------------------------------------
# 3. WITHDRAW MONEY
# -----------------------------------------
elif choice == "Withdraw Money":
    st.subheader("🏧 Withdraw Funds")
    
    with st.form("withdraw_form", clear_on_submit=True):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input("Amount to Withdraw", min_value=1, step=100)
        submit = st.form_submit_button("Withdraw")
        
        if submit:
            account = next((item for item in st.session_state.bank_data if item["accountno"] == acc_no and str(item["pin"]) == pin), None)
            if account:
                if account['balance'] < amount:
                    st.error(f"Insufficient funds! Your current balance is ${account['balance']:,}")
                else:
                    account['balance'] -= amount
                    Bank._update(st.session_state.bank_data)
                    st.success(f"Successfully withdrew ${amount:,}. Remaining Balance: ${account['balance']:,}")
            else:
                st.error("Invalid Account Number or PIN.")

# -----------------------------------------
# 4. ACCOUNT DETAILS
# -----------------------------------------
elif choice == "Account Details":
    st.subheader("📊 View Account Details")
    
    with st.form("details_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        submit = st.form_submit_button("Show Details")
        
        if submit:
            account = next((item for item in st.session_state.bank_data if item["accountno"] == acc_no and str(item["pin"]) == pin), None)
            if account:
                st.success("Account Verified!")
                st.metric(label="Current Balance", value=f"${account['balance']:,}")
                
                st.divider()
                st.write(f"**Name:** {account['name']}")
                st.write(f"**Age:** {account['age']}")
                st.write(f"**Email:** {account['email']}")
                st.write(f"**Account ID:** `{account['accountno']}`")
            else:
                st.error("Invalid Account Number or PIN.")

# -----------------------------------------
# 5. UPDATE DETAILS
# -----------------------------------------
elif choice == "Update Details":
    st.subheader("⚙️ Update Profile")
    st.write("First, verify your account.")
    
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    
    account = next((item for item in st.session_state.bank_data if item["accountno"] == acc_no and str(item["pin"]) == pin), None)
    
    if account:
        st.success("Account verified! You may update your details below.")
        with st.form("update_form"):
            new_name = st.text_input("Name", value=account['name'])
            new_email = st.text_input("Email", value=account['email'])
            new_pin = st.text_input("New PIN (Leave as is to keep current)", value=str(account['pin']), type="password", max_chars=4)
            
            submit = st.form_submit_button("Save Changes")
            
            if submit:
                if len(new_pin) != 4 or not new_pin.isdigit():
                    st.error("PIN must be 4 digits.")
                else:
                    account['name'] = new_name
                    account['email'] = new_email
                    account['pin'] = new_pin
                    Bank._update(st.session_state.bank_data)
                    st.success("Account updated successfully!")
                    st.balloons()

# -----------------------------------------
# 6. DELETE ACCOUNT
# -----------------------------------------
elif choice == "Delete Account":
    st.subheader("⚠️ Close Account")
    st.warning("This action cannot be undone!")
    
    with st.form("delete_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        confirm = st.checkbox("I understand that my account and data will be permanently deleted.")
        
        submit = st.form_submit_button("Delete My Account", type="primary")
        
        if submit:
            account = next((item for item in st.session_state.bank_data if item["accountno"] == acc_no and str(item["pin"]) == pin), None)
            if not account:
                st.error("Invalid Account Number or PIN.")
            elif not confirm:
                st.error("You must check the confirmation box to proceed.")
            else:
                st.session_state.bank_data.remove(account)
                Bank._update(st.session_state.bank_data)
                st.success("Account deleted successfully.")