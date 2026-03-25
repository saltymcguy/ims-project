import mysql.connector as m
from .db_connect import db_connect
from .transactions import log_transaction

def additem(name,quantity,location,user_id):
    db=db_connect()
    if db is None:
        print("database connection failed")
        return False
    c=db.cursor()
    try:
        c.execute("insert into inventory (item_name,quantity,location) values (%s,%s,%s)",(name,quantity,location))
        db.commit()
        print(f"item {name} added with quantity {quantity}")
        item_id=c.lastrowid
        log_transaction(item_id,user_id,"add",quantity)
        return True
    except Exception as e:
        db.rollback()
        print(f"Error could not add item:{e}")
        return False
    finally:
        db.close()
    

def update_quantity(item_id,new_qty,user_id):
    db=db_connect()
    if db is None:
        print("database connection failed")
        return False
    c=db.cursor()

    try:
        c.execute("update inventory set quantity = %s where item_id = %s",(new_qty,item_id))
        db.commit()
        print(f"Quantity updated to {new_qty} at item id: {item_id}")
        log_transaction(item_id,user_id,"adjust",new_qty)
        return True
    except Exception as e:
        db.rollback()
        print(f"Error could not update qauntity: {e}")
        return False
    finally:
        db.close()
    
    
def delete_items(item_id,user_id):
    db=db_connect()
    if db is None:
        print("database connection failed")
        return False
    c=db.cursor()

    try:
        log_transaction(item_id,user_id,change_type="remove",quantity_change=0)
        c.execute("delete from inventory where item_id=%s",(item_id,))
        db.commit()
        print(f"Item id {item_id} deleted successfully")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error deleting item: {e}")
        return False
    finally:
        db.close()

def view_items():
    db=db_connect()
    if db is None:
        print("database connection failed")
        return False
    c=db.cursor(dictionary=True)
    
    c.execute("select * from inventory")
    items=c.fetchall()
    db.close()

    if not items:
        print("No items in inventory")
    
    print("=" * 70)
    print(f"{'ID':<5} {'Item Name':<20} {'Qty':<8} {'Location':<12} {'Last Updated':<20}")
    print("=" * 70)

    for item in items:
        print(f"{item['item_id']:<5} {item['item_name']:<20} {item['quantity']:<8} {item['location']:<12} {str(item['last_updated'])[:19]:<20}")

    print("=" * 70)
    return items