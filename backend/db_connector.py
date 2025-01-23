import mysql.connector
from contextlib3 import contextmanager
from logging_setup import setup_logger

logger = setup_logger("db_connector")



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

            

def fetch_expense_for_date(expense_date):
    logger.info(f"fetch_expense_for_date called for {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM EXPENSES WHERE EXPENSE_DATE = %s;",(expense_date,))
        expenses = cursor.fetchall()
    return expenses
            

def insert_expense(expense_date,amount,category,notes):
    logger.info(f"insert_expense called for {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO EXPENSES (expense_date,amount,category,notes) VALUES (%s,%s,%s,%s);",
                       (expense_date,amount,category,notes))
            
            
def delete_expense_for_date(expense_date):
    logger.info(f"delete_expense_for_date called for {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM EXPENSES WHERE EXPENSE_DATE = %s;",(expense_date,))
            
def fetch_expense_summary(start_date,end_date):
    logger.info(f"fetch_expense_summary called for dates between {start_date} (inclusive) and {end_date} (inclusive)")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT CATEGORY,SUM(AMOUNT) AS TOTAL FROM EXPENSES WHERE EXPENSE_DATE BETWEEN %s AND %s GROUP BY CATEGORY;",
                       (start_date,end_date))
        data = cursor.fetchall()
    return data


if __name__ == "__main__":
    exp = fetch_expense_for_date("2024-09-03")
    print(exp)
    rec = fetch_expense_summary("2024-08-01","2024-09-02")
    print(rec)
