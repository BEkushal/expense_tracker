import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics_months_tab():
    response = requests.get(f"{API_URL}/monthly_summary/")
    monthly_summary = response.json()

    df = pd.DataFrame(monthly_summary)
    df.rename(columns={
        "EXPENSE_MONTH": "MONTH NUMBER",
        "MONTH": "MONTH NAME",
        "TOTAL_EXPENSE": "OVERALL_EXPENSE"
    }, inplace=True)
    df_sorted = df.sort_values(by="MONTH NUMBER", ascending=False)
    df_sorted.set_index("MONTH NUMBER", inplace=True)

    st.title("Expense Breakdown By Months")

    st.bar_chart(data=df_sorted.set_index("MONTH NAME")['OVERALL_EXPENSE'], width=0, height=0, use_container_width=True)

    df_sorted["OVERALL_EXPENSE"] = df_sorted["OVERALL_EXPENSE"].map("{:.2f}".format)

    st.table(df_sorted.sort_index())