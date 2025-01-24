import streamlit as st 
import pandas as pd
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

st.title("Expense Management System")
tab1,tab2 = st.tabs(["Add/Update","Analytics"])

# Configuring Add/Update tab
with tab1:
    selected_date = st.date_input("Enter date:",datetime(2024,8,1))
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
        
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []
        
categories = ["Rent","Food","Shopping","Entertainment","Other"]

# Display the columns      
with st.form(key = "expense_form"):
    c1,c2,c3 = st.columns(3)
    with c1:
        st.text("Amount")
    with c2:
        st.text("Category")
    with c3:
        st.text("Notes")
    
    # Container to store values entered by user 
    expenses = []
    
    # Maxium 5 entries allowed
    for i in range(5):
        if i < len(existing_expenses):
            amount = existing_expenses[i]['amount']
            category = existing_expenses[i]["category"]
            notes = existing_expenses[i]["notes"]
        else:
            amount = 0.0
            category = "Shopping"
            notes = ""

        with c1:
            amount_input = st.number_input(label="Amount",min_value=0.0, step=1.0, value=amount, key=f"amount_{i}",label_visibility="collapsed")
        with c2:
            category_input = st.selectbox(label="Category",options = categories, index=categories.index(category), key=f"category_{i}",label_visibility="collapsed")
        with c3:
            notes_input = st.text_input(label="NA", value=notes, key=f"notes_{i}",label_visibility="collapsed")
            
        expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })
            
    submit = st.form_submit_button()
    if submit:
        # Only Push those records to the backend/db which are expenses
        filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
        
        response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
        if response.status_code == 200:
            st.success("Expenses updated successfully!")
        else:
            st.error("Failed to update expenses.")
