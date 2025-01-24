import streamlit as st 
import pandas as pd
from add_update_ui import add_or_update_tab
from analytics_ui import analytics_tab

API_URL = "http://localhost:8000"

st.title("Expense Management System")
tab1,tab2 = st.tabs(["Add/Update","Analytics"])

# Configuring Add/Update tab
with tab1:
    add_or_update_tab()
with tab2:
    analytics_tab()
    
