import db_connector
from fastapi import FastAPI,HTTPException
from datetime import date
from typing import List
from pydantic import BaseModel


class Expense(BaseModel):
    amount: float
    category: str
    notes: str
    

app = FastAPI()

@app.get("/expenses/{expense_date}",response_model=List[Expense])
def get_expenses(expense_date:date):
    expenses = db_connector.fetch_expense_for_date(expense_date)
    validated_expenses = [Expense(**expense) for expense in expenses ]
    return validated_expenses

@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date:date,expenses:List[Expense]):
    for expense in expenses:
        db_connector.insert_expense(expense_date,expense.amount,expense.category,expense.notes)
    return {"message": "Expenses updated successfully"}

@app.post("/expenses/{expense_date}/delete")
def delete_expense(expense_date: date):
    # Call the delete_expense_for_date function
    try:
        db_connector.delete_expense_for_date(expense_date)
        return {"message": f"Expenses for date {expense_date} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
