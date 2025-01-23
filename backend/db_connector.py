import mysql.connector
from contextlib3 import contextmanager



@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host = "localhost",
        user = "cbpython",
        password = "cbpython",
        database = "expense_manager"
    )
    
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()
    

def fetch_all_records():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM EXPENSES;")
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)
            

def fetch_expense_for_date(expense_date):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM EXPENSES WHERE EXPENSE_DATE = %s;",(expense_date,))
        expenses = cursor.fetchall()
    return expenses
            

def insert_expense(expense_date,amount,category,notes):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO EXPENSES (expense_date,amount,category,notes) VALUES (%s,%s,%s,%s);",
                       (expense_date,amount,category,notes))
            
            
def delete_expense_for_date(expense_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM EXPENSES WHERE EXPENSE_DATE = %s;",(expense_date,))
            
def fetch_expense_summary(start_date,end_date):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT CATEGORY,SUM(AMOUNT) AS TOTAL FROM EXPENSES WHERE EXPENSE_DATE BETWEEN %s AND %s GROUP BY CATEGORY;",
                       (start_date,end_date))
        data = cursor.fetchall()
    return data


