import bcrypt,mysql.connector as m
from .db_connect import db_connect

def login(user, passwd):
    db = db_connect()
    if db is None:                  # FIX: was missing — crash if DB unreachable
        print("Database connection failed")
        return None
    c = db.cursor(dictionary=True)
    
    c.execute("select * from users where username=%s",(user,))
    euser=c.fetchone()

    if not euser:
        print("User not found")
        c.close()
        db.close()
        return None
    
    stored_pass= euser['password_hash'].encode('utf-8')
    if not bcrypt.checkpw(passwd.encode('utf-8'),stored_pass):
        print("Invalid password")
        c.close()
        db.close()
        return None
    
    print(f"Logged in successfully, welcome {euser['username']} ({euser['role']})")
    c.close()
    db.close()

    return {'user_id': euser['user_id'],'username': euser['username'],'role': euser['role']}
