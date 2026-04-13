import streamlit as st
import json
import random
import string
from pathlib import Path

# ------------------ BANK CLASS ------------------
class Bank:
    database = 'data.json'
    data = []

    # Load data
    if Path(database).exists():
        try:
            with open(database) as fs:
                data = json.load(fs)
        except:
            data = []

    @classmethod
    def update(cls):
        with open(cls.database, 'w') as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def generate_account(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        acc = alpha + num + spchar
        random.shuffle(acc)
        return "".join(acc)

    @classmethod
    def find_user(cls, acc, pin):
        return [i for i in cls.data if i['accountNo'] == acc and i['pin'] == pin]


bank = Bank()

# ------------------ UI ------------------
st.set_page_config(page_title="Bank App", page_icon="🏦")
st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox("Select Operation", [
    "Create Account",
    "Deposit Money",
    "Withdraw Money",
    "Show Details",
    "Update Details",
    "Delete Account"
])

# ------------------ CREATE ACCOUNT ------------------
if menu == "Create Account":
    st.subheader("🆕 Create Account")

    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=1)
    email = st.text_input("Enter your email")
    pin = st.text_input("Create 4-digit PIN", type="password")

    if st.button("Create Account"):
        if age < 18:
            st.error("❌ You must be at least 18 years old")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("❌ PIN must be exactly 4 digits")
        else:
            acc_no = bank.generate_account()
            user = {
                "name": name,
                "age": age,
                "email": email,
                "pin": pin,
                "accountNo": acc_no,
                "balance": 0
            }
            bank.data.append(user)
            bank.update()

            st.success("✅ Account created successfully!")
            st.info(f"📌 Your Account Number: {acc_no}")

# ------------------ DEPOSIT ------------------
elif menu == "Deposit Money":
    st.subheader("💰 Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Enter amount", min_value=1)

    if st.button("Deposit"):
        user = bank.find_user(acc, pin)

        if not user:
            st.error("❌ User not found")
        elif amount > 10000:
            st.warning("⚠️ Deposit limit is 10,000")
        else:
            user[0]['balance'] += amount
            bank.update()
            st.success("✅ Money deposited successfully")

# ------------------ WITHDRAW ------------------
elif menu == "Withdraw Money":
    st.subheader("💸 Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Enter amount", min_value=1)

    if st.button("Withdraw"):
        user = bank.find_user(acc, pin)

        if not user:
            st.error("❌ User not found")
        elif user[0]['balance'] < amount:
            st.warning("⚠️ Insufficient balance")
        else:
            user[0]['balance'] -= amount
            bank.update()
            st.success("✅ Withdrawal successful")

# ------------------ SHOW DETAILS ------------------
elif menu == "Show Details":
    st.subheader("📄 Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):
        user = bank.find_user(acc, pin)

        if not user:
            st.error("❌ User not found")
        else:
            st.success("✅ Account Found")
            st.json(user[0])

# ------------------ UPDATE ------------------
elif menu == "Update Details":
    st.subheader("✏️ Update Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    user = bank.find_user(acc, pin)

    if user:
        st.success("✅ User verified")

        name = st.text_input("Update Name", value=user[0]['name'])
        email = st.text_input("Update Email", value=user[0]['email'])
        new_pin = st.text_input("Update PIN", value=user[0]['pin'])

        if st.button("Update"):
            if len(new_pin) != 4 or not new_pin.isdigit():
                st.error("❌ PIN must be 4 digits")
            else:
                user[0]['name'] = name
                user[0]['email'] = email
                user[0]['pin'] = new_pin
                bank.update()
                st.success("✅ Details updated successfully")

# ------------------ DELETE ------------------
elif menu == "Delete Account":
    st.subheader("🗑️ Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        user = bank.find_user(acc, pin)

        if not user:
            st.error("❌ User not found")
        else:
            bank.data.remove(user[0])
            bank.update()
            st.success("✅ Account deleted successfully")