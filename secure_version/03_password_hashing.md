# Securing Password Storage with bcrypt

## Vulnerability Type

Sensitive Data Exposure

## OWASP Category

A02 – Cryptographic Failures

## Description

Initially, user passwords were stored in the database as plaintext.

Example:

```
username | password
---------------------
user1    | pass1
admin    | admin123
```

If the database were compromised, attackers would immediately gain access to all user credentials.

To mitigate this risk, password hashing was implemented using **bcrypt**.

---

## Vulnerable Code

```python
cursor.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    (username, password, "user")
)
```

Passwords were stored exactly as provided by the user.

---

## Secure Implementation

Passwords are now hashed before storage using bcrypt.

```python
import bcrypt

hashed_password = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
)

cursor.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    (username, hashed_password.decode("utf-8"), "user")
)
```

During login, the password is verified using:

```python
bcrypt.checkpw(
    password.encode("utf-8"),
    user["password"].encode("utf-8")
)
```

---

## Example Stored Password

```
$2b$12$PvwuysfFCKPWN8MfrG/fje3elEzQmlEirPtF0VFK3ALS8UTyRIplW
```

Structure of bcrypt hash:

```
$2b$12$<salt><hashed_password>
```

* `2b` → bcrypt algorithm
* `12` → cost factor
* salt → random value used during hashing
* hash → final hashed password

---

## Why bcrypt is Secure

bcrypt provides several important protections:

* Built-in salting
* Slow hashing to prevent brute-force attacks
* Resistance against rainbow table attacks

Even if attackers obtain the database, recovering original passwords becomes extremely difficult.

---

## Security Principle

Passwords should **never be stored in plaintext**. Always use strong hashing algorithms such as:

* bcrypt
* Argon2
* PBKDF2
