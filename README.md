Inventory Management System (IMS)

temporary change

A full-stack Inventory Management System built with Flask, MySQL, and a custom HTML/CSS/JavaScript frontend. This project supports role-based access (Admin/Staff), inventory tracking, transaction logging, and user management.

🚀 Features

🔐 User Authentication (Login / Register)

👥 Role-based Access (Admin & Staff)

📦 Inventory Management (Add, Update, Delete items)

📊 Transaction Logging

🧑‍💼 User Management (Admin only)

🌐 REST API using Flask

🛠 Tech Stack

Backend:

Python (Flask)

MySQL

bcrypt (password hashing)

Frontend:

HTML

CSS

JavaScript (Fetch API)

📂 Project Structure

ims-project/

│

├── backend/

│   ├── app.py

│   ├── db_connect.py

│   ├── login.py

│   ├── register.py

│   ├── inventory.py

│   ├── transactions.py

│   └── admin.py

│

├── frontend/

│   ├── index.html

│   └── style.css

│

├── tests/

│   └── test_ims.py

│

├── pytest.ini

├── requirements.txt

└── README.md

⚙️ Setup Instructions

1. Clone the Repository

git clone https://github.com/saltymcguy/ims-project.git   
cd ims-project

2. Create Virtual Environment

python -m venv venv

venv\Scripts\activate

note: if it fails to create a Virtual Environment with an error:
cannot be loaded because running scripts is disabled on this system. For 
more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.

run:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the root directory:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=warehouse

5. Setup MySQL Database

Make sure MySQL is running, then create database:

CREATE DATABASE warehouse;

Create required tables (users, inventory, transactions) before running.

6. Run start.bat

Finally run start.bat file which runs the backend and frontend together

🔌 API Endpoints

Method

Endpoint

Description

POST

/api/login

User login

POST

/api/register

User registration

GET

/api/inventory

Get all items

POST

/api/inventory

Add item

PUT

/api/inventory/

Update item quantity

DELETE

/api/inventory/

Delete item

GET

/api/transactions

View transactions

GET

/api/users

View users

PUT

/api/users//role

Change user role

DELETE

/api/users/

Delete user

🚧 Future Improvements

Improve UI/UX

Add search & filtering

Implement pagination

🗄️ Database Schema

Below is the SQL schema required for the application:

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin','staff') DEFAULT 'staff'
);

CREATE TABLE inventory (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    quantity INT DEFAULT 0,
    location VARCHAR(100),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT,
    user_id INT,
    change_type ENUM('add','adjust','remove'),
    quantity_change INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES inventory(item_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

👤 Author

John Philipose
