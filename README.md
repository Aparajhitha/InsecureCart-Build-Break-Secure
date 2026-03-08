# InsecureCart – Build, Break & Secure a Vulnerable Web Application

## Quick Start

1. Clone the repository

git clone https://github.com/Aparajhitha/InsecureCart-Build-Break-Secure.git

2. Navigate into the project

cd InsecureCart-Build-Break-Secure

3. Create virtual environment

python3 -m venv venv
source venv/bin/activate

4. Install dependencies

pip install -r requirements.txt

5. Initialize database

python init_db.py

6. Run the server

python app.py

## Overview

**InsecureCart** is a deliberately vulnerable e-commerce API built using Flask and SQLite.
The goal of the project is to simulate real-world web application vulnerabilities, exploit them as an attacker, and then implement secure coding practices to fix them.

This project follows a **Build → Break → Secure** methodology used in real cybersecurity training and penetration testing labs.

It demonstrates how common vulnerabilities occur and how they should be mitigated in production systems.

---

## Architecture

Client (curl / API requests)
        │
        ▼
Flask API (app.py)
        │
        ▼
SQLite Database
        │
        ▼
Authentication: JWT
Password Storage: bcrypt

## Tech Stack

* **Python 3**
* **Flask**
* **SQLite**
* **bcrypt** (password hashing)
* **flask-jwt-extended** (JWT authentication)
* **curl** for API testing

Environment used:

* Ubuntu (WSL)
* Python Virtual Environment

---

## Project Structure

```
insecurecart
│
├── app.py
├── database.py
├── models.py
├── init_db.py
├── config.py
├── requirements.txt
│
├── routes/
│   ├── auth.py
│   ├── cart.py
│   ├── products.py
│   └── orders.py
│
├── exploit/
│   ├── 01_sqli_login_bypass.md
│   ├── 02_sqli_data_exfiltration.md
│   ├── 03_idor_cart_access.md
│   └── 04_business_logic_negative_quantity.md
│
├── secure_version/
│   ├── 01_sqli_fix.md
│   ├── 02_authorization_fix.md
│   └── 03_password_hashing.md
│
└── README.md
```

---

## Vulnerabilities Demonstrated

This project intentionally introduces several common web security vulnerabilities.

### SQL Injection

User input was directly embedded into SQL queries, allowing attackers to manipulate the query logic.

Example payload:

```
' OR '1'='1' --
```

Impact:

* Authentication bypass
* Data extraction

---

### IDOR (Insecure Direct Object Reference)

The API allowed users to access other users’ resources by modifying IDs in requests.

Example:

```
GET /cart/2
```

Impact:

* Horizontal privilege escalation
* Unauthorized data access

---

### Business Logic Flaw

The checkout endpoint accepted invalid quantities such as negative values.

Example:

```
quantity = -5
```

Impact:

* Manipulated transaction values
* Invalid purchase flows

---

### Insecure Token Handling

Initially authentication used randomly generated tokens stored in memory.

Problems:

* Tokens lost after server restart
* No signature verification
* Not scalable

---

### Sensitive Data Exposure

The `/users` endpoint exposed password hashes in API responses.

---

## Security Fixes Implemented

After exploiting the vulnerabilities, the application was refactored using secure coding practices.

### Parameterized SQL Queries

SQL queries were rewritten using parameterized statements to prevent injection.

Example:

```python
cursor.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
)
```

---

### Authorization Enforcement

Resource ownership is validated before returning sensitive data.

Example:

```python
current_user = int(get_jwt_identity())

if current_user != user_id:
    return jsonify({"error": "Forbidden"}), 403
```

---

### Password Hashing

Passwords are securely stored using **bcrypt**.

Example hash:

```
$2b$12$PvwuysfFCKPWN8MfrG/fje3elEzQmlEirPtF0VFK3ALS8UTyRIplW
```

Benefits:

* Salted hashing
* Resistant to brute force attacks

---

### JWT Authentication

Authentication now uses signed JSON Web Tokens.

Example request:

```
Authorization: Bearer <token>
```

Benefits:

* Stateless authentication
* Token expiration
* Signature verification

---

### Business Logic Validation

Input validation prevents invalid operations.

Example:

```python
if quantity <= 0:
    return jsonify({"error": "Invalid quantity"}), 400
```

---

### Secure API Responses

Sensitive fields such as passwords are no longer exposed in API responses.

---

## Example API Flow

Register a user:

```
POST /register
```

Login:

```
POST /login
```

Response:

```
{
  "access_token": "JWT_TOKEN"
}
```

Access protected endpoint:

```
GET /cart/1
Authorization: Bearer JWT_TOKEN
```

---

## Learning Outcomes

Through this project, the following concepts were implemented and demonstrated:

* SQL Injection exploitation and prevention
* Authentication vs Authorization
* IDOR vulnerabilities
* Business logic security
* Password hashing with bcrypt
* Token-based authentication using JWT
* Secure API design principles

---

## Key Security Lessons

- Never concatenate user input directly into SQL queries.
- Always enforce authorization checks for resource access.
- Passwords must be hashed using strong algorithms like bcrypt.
- Token-based authentication should use signed JWT tokens.
- Business logic must validate all user inputs.

## Future Improvements

Possible extensions to this project include:

* Rate limiting to prevent brute-force attacks
* Refresh token implementation
* Role-based access control (RBAC)
* Logging and monitoring
* Automated security testing

---

## Author

Cybersecurity learning project focused on understanding real-world web application vulnerabilities and secure development practices.
