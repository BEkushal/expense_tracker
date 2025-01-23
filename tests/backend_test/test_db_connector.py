from backend import db_connector


def test_fetch_expense_for_date():
    records = db_connector.fetch_expense_for_date("2024-08-05")
    assert len(records) == 5
    assert records[0]["amount"] == 350.0
    assert records[0]["category"] == "Rent"
    assert records[0]["notes"] == "Shared rent payment"
    
#------------ Any Test cases can be tested here above is just an example --------------#