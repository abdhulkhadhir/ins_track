# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:58:19 2024

@author: seyedhyd
"""

import streamlit as st
import pandas as pd
import os

# Path to the CSV file in your Git repository (it should be part of your repository)
CSV_FILE = 'transactions.csv'

# Function to read data from CSV into a DataFrame
def get_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Details", "IN", "OUT"])

# Function to save DataFrame back to the CSV
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Initialize session state for transactions and balance
if "transactions" not in st.session_state:
    st.session_state.transactions = get_data()

if "balance" not in st.session_state:
    st.session_state.balance = st.session_state.transactions['IN'].sum() - st.session_state.transactions['OUT'].sum()

# Function to update CSV and session state
def update_csv(date, details, income, expense):
    new_data = {"Date": date, "Details": details, "IN": income, "OUT": expense}
    st.session_state.transactions = st.session_state.transactions.append(new_data, ignore_index=True)
    save_data(st.session_state.transactions)  # Update the CSV file
    st.session_state.balance = st.session_state.transactions['IN'].sum() - st.session_state.transactions['OUT'].sum()

# Input section for income or expenditure
st.title("Irfan Treatment Income and Expenditure Tracker")

st.write(f"### Total Income: ₹{st.session_state.transactions['IN'].sum():,.2f}")
st.write(f"### Total Outgoing: ₹{st.session_state.transactions['OUT'].sum():,.2f}")
st.write(f"### Current Balance: ₹{st.session_state.balance:,.2f}")

with st.form("transaction_form"):
    date = st.date_input("Date")
    details = st.text_input("Details/Description")
    income = st.number_input("Income (₹)", min_value=0.0, step=0.01)
    expense = st.number_input("Expenditure (₹)", min_value=0.0, step=0.01)
    submit = st.form_submit_button("Add Transaction")

    if submit:
        # Update balance and transaction log
        update_csv(date, details, income, expense)
        st.success(f"Added: {details}")

# Display transaction history
st.write("### Transaction History")
st.dataframe(st.session_state.transactions)
