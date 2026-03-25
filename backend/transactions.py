from .db_connect import db_connect

def log_transaction(item_id,user_id,change_type,quantity_change):
    db=db_connect()
    if db is None:
        print("database connection failed")
        return False
    c=db.cursor()

    try:
        c.execute("insert into transactions (item_id,user_id,change_type,quantity_change) values (%s,%s,%s,%s)",(item_id,user_id,change_type,quantity_change))
        db.commit()
        print(f"Transaction logged: {change_type} {quantity_change} units for item {item_id} by user {user_id}")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error logging transaction: {e}")
        return False             # FIX: was returning None, breaking boolean checks in callers
    finally:
        db.close()

def view_transaction():
    db=db_connect()
    if db is None:
        print("database connection failed")
        return 
    c=db.cursor(dictionary=True)

    c.execute("select t.transaction_id,i.item_name,u.username,t.change_type,t.quantity_change,t.timestamp from transactions t join inventory i on t.item_id = i.item_id join users u on t.user_id = u.user_id order by t.timestamp desc")
    log=c.fetchall()
    db.close()

    if not log:
        print("No logs found")
        return
    
    for i in log:
        print(f"{i['timestamp']}: {i['username']} {i['change_type']} {i['quantity_change']} {i['item_name']}")