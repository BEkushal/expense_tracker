import db_connector
from fastapi import FastAPI,HTTPException
from datetime import date
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    notes: str
    
class DateRange(BaseModel):
    start_date: date
    end_date: date


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
    
@app.post("/analytics")
def get_analytics(date_range: DateRange):
    records = db_connector.fetch_expense_summary(date_range.start_date,date_range.end_date)
    if records is None:
        raise HTTPException(status_code=500,detail="Failed to retrieve expense summary from the database")
    
    # creating appropriate return
    return_type = {}
    
    # # creating percentage
    grand_total = 0
    for row in records:
        grand_total += row["TOTAL"]
    for row in records:
        pct = round((row["TOTAL"]/grand_total) * 100 if grand_total > 0 else 0,3)
        return_type[row["CATEGORY"]] = {"total":row["TOTAL"],"percentage":pct}
        
        
    return return_type


