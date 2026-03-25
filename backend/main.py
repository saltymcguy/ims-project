from .login import login
from .register import register
from .db_connect import db_connect
from .transactions import log_transaction,view_transaction
from .inventory import additem,delete_items,update_quantity,view_items
from .admin import view_users,change_role,delete_user
import getpass
import time

def staff_menu(user):
    while True:
        print("\n======= Staff Menu =======")
        print("1.view items")
        print("2.update Item Quantity")
        print("3.View Transactions")
        print("4.logout")

        try:
            choice=int(input("Enter your choice: "))

            if choice==1:
                view_items()
            elif choice==2:
                item_id=int(input("Enter the item id: "))
                new_qty=int(input("Enter the new quantity: "))
                update_quantity(item_id,new_qty,user['user_id'])
            elif choice==3:
                view_transaction()
            elif choice==4:
                print("logging out")
                break
            else:
                print("Invalid Choice")
        except ValueError:
            print("Invalid input please enter a number")
            continue

def admin_menu(user):
     while True:
        print("\n====== Admin Menu ======")
        print("1. View Items")
        print("2. Add Item")
        print("3. Update Item Quantity")
        print("4. Delete Item")
        print("5. View Transactions")
        print("6. Manage Users")
        print("7. Logout")

        try:
            choice=int(input("Enter your choice: "))

            if choice==1:
                view_items()
            elif choice==2:
                name=input("Enter the item name: ")
                qty=int(input("Enter the quantity: "))
                location=input("Enter the location: ")
                additem(name,qty,location,user['user_id'])
            elif choice==3:
                item_id=int(input("Enter the item id: "))
                new_qty=int(input("Enter the new quantity: "))
                update_quantity(item_id,new_qty,user['user_id'])
            elif choice==4:
                item=int(input("Enter the item id: "))
                delete_items(item,user['user_id'])
            elif choice==5:
                view_transaction()
            elif choice==6:
                while True:
                    view_users()
                    try:    
                        ch=int(input("1.Change Role\n2.Delete User\n3.Exit\nEnter your choice: "))
                        if ch==1:
                            user_id=int(input("Enter the user id to change the role: "))
                            role=input("enter the role to change to(staff,admin): ")
                            change_role(user_id,role)
                        elif ch==2:
                            u=int(input("Enter the user id to delete: "))
                            delete_user(u)
                        elif ch==3:
                            print("Exiting...")
                            break
                    except ValueError:
                        print("Invalid input enter a number")
                        continue
            elif choice==7:
                print("logging out")
                break
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input enter a number")
            continue

def main():
    print("====== Inventory Management System ======")
    while True:
        print("\n1.Login")
        print("2.Register")
        print("3.Exit")

        try:
            choice=int(input("Enter your choice: "))

            if choice==1:
                username=input("Enter your username: ")
                passwd=getpass.getpass("Enter your password: ")
                user=login(username,passwd)
                if user:
                    print(f"Welcome {user['username']} - ({user['role']})")
                    if user["role"] == "admin":
                        admin_menu(user)
                    else:
                        staff_menu(user)
                else:
                    print("Login Failed")
            
            elif choice==2:
                username1=input("Enter a username: ")
                new_pass=getpass.getpass("Enter the password: ")
                conf_pass=getpass.getpass("Confirm the password: ")
                if new_pass == conf_pass:
                    register(username1,new_pass)
                else:
                    print("Passwords do not match")
            
            elif choice==3:
                title="Exiting... \nThank You for using IMS"
                for i in title:
                    print(i,end='')
                    time.sleep(0.1)
                break
            else:
                print("Invalid Choice")
        except ValueError:
            print("Invalid input please enter a number")
            continue

if __name__ == "__main__":
    main()