# Fixing SQL Injection Vulnerability

## Vulnerability Type

SQL Injection

## OWASP Category

A03 – Injection

## Description

The application was vulnerable to SQL Injection because user input was directly embedded into SQL queries using string formatting. Attackers could manipulate the query logic and bypass authentication or extract sensitive data.

The issue was fixed by using **parameterized SQL queries**, which separate SQL code from user-supplied input.

---

## Vulnerable Code

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
user = cursor.execute(query).fetchone()
```

Because user input was directly concatenated into the query, attackers could inject SQL payloads such as:

```
' OR '1'='1' --
```

This allowed attackers to bypass authentication.

---

## Secure Implementation

The vulnerable query was replaced with a **parameterized query**.

```python
user = cursor.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password)
).fetchone()
```

Parameterized queries ensure that user input is treated strictly as **data**, not executable SQL.

---

## Why This Fix Works

Parameterized queries:

* Separate SQL instructions from user input
* Prevent malicious input from altering query structure
* Ensure the database interprets injected strings as plain text

Even if an attacker submits:

```
' OR '1'='1' --
```

the database treats it as a literal string rather than SQL logic.

---

## Verification

After implementing parameterized queries, the previous SQL injection attack was tested again.

Exploit attempt:

```bash
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d "{\"username\":\"' OR '1'='1' -- \",\"password\":\"x\"}"
```

Result:

```
{
  "message": "Invalid credentials"
}
```

The injection attack no longer works.

---

## Security Principle

Always use **parameterized queries or ORM frameworks** when interacting with databases to prevent injection attacks.
