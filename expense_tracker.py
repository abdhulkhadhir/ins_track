# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:58:19 2024

@author: seyedhyd
"""

import streamlit as st
import pandas as pd

# Initialize session state to store income, expenditure, and balance
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Type", "Amount"])

if "balance" not in st.session_state:
    st.session_state.balance = 0

# Function to update balance
def update_balance(transaction_type, amount):
    if transaction_type == "Income":
        st.session_state.balance += amount
    elif transaction_type == "Expenditure":
        st.session_state.balance -= amount

# Input section for income or expenditure
st.title("Irfan Treatment Income and Expenditure Tracker")

st.write(f"Current Balance: **${st.session_state.balance:.2f}**")

with st.form("transaction_form"):
    transaction_type = st.selectbox("Transaction Type", ["Income", "Expenditure"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    submit = st.form_submit_button("Add Transaction")

    if submit:
        # Update balance and transaction log
        update_balance(transaction_type, amount)
        new_transaction = pd.DataFrame({"Type": [transaction_type], "Amount": [amount]})
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction], ignore_index=True)
        st.success(f"Added {transaction_type} of ${amount:.2f}")

# Display transaction history
st.write("### Transaction History")
st.dataframe(st.session_state.transactions)
