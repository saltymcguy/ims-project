import bcrypt
from .db_connect import db_connect

def register(user, passwd, role="staff"):
    db = db_connect()
    if db is None:                  # FIX: was missing — crash if DB unreachable
        print("Database connection failed")
        return False
    c = db.cursor(dictionary=True)
    c.execute("select * from users where username= %s",(user,))
    euser=c.fetchone()

    if euser:
        print("User already exists")
        return False

    hash=bcrypt.hashpw(passwd.encode('utf-8'),bcrypt.gensalt()) 

    c.execute("insert into users (username,password_hash,role) values (%s,%s,%s)",(user,hash.decode('utf-8'),role))

    db.commit()
    print(f"user '{user}' registered successfully")

    c.close()
    db.close()
    return True


