from .db_connect import db_connect

def view_users():
    db=db_connect()
    if db is None:
        print("database connection failed")
        return False
    c=db.cursor(dictionary=True)

    c.execute("select user_id,username,role from users")
    user=c.fetchall()
    db.close()

    for i in user:
        print(f"ID: {i['user_id']} | {i['username']} - {i['role']}")
    
def change_role(user_id,new_role):
    db=db_connect()
    if db is None:
        print("database connection failed")
        return False
    c=db.cursor()

    try:
        c.execute("update users set role=%s where user_id=%s",(new_role,user_id))
        db.commit()
        print("Role changed successfully")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error chaning roles: {e}")
        return False
    finally:
        db.close()

def delete_user(user_id):
    db=db_connect()
    if db is None:
        print("database connection failed")
        return False
    c=db.cursor()

    try:    
        c.execute("delete from users where user_id=%s",(user_id,))
        db.commit()
        print(f"User id {user_id} deleted successfully")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error deleting user: {e}")
        return False
    finally:
        db.close()