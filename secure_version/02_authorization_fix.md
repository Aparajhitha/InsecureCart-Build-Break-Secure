# Fixing Broken Authorization (IDOR)

## Vulnerability Type

Broken Access Control / IDOR

## OWASP Category

A01 – Broken Access Control

## Description

The application originally allowed users to access cart data by specifying a user ID in the URL.

Example:

```
GET /cart/2
```

Because the server did not verify ownership of the resource, an authenticated user could access another user's cart by modifying the ID parameter.

This vulnerability is known as **Insecure Direct Object Reference (IDOR)**.

---

## Vulnerable Code

```python
@app.route("/cart/<int:user_id>", methods=["GET"])
def view_cart(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    items = cursor.execute(
        "SELECT * FROM cart WHERE user_id = ?",
        (user_id,)
    ).fetchall()
```

The application returned cart data without checking whether the requesting user actually owned the cart.

---

## Secure Implementation

Authorization checks were added using JWT authentication.

```python
@app.route("/cart/<int:user_id>", methods=["GET"])
@jwt_required()
def view_cart(user_id):

    current_user = int(get_jwt_identity())

    if current_user != user_id:
        return jsonify({"error": "Forbidden"}), 403
```

The application now verifies that the authenticated user matches the requested resource.

---

## Why This Fix Works

This fix ensures that:

* The request contains a valid JWT token
* The token identity is extracted
* The identity matches the resource owner

If a user attempts to access another user's cart, the request is rejected.

---

## Verification

Attack attempt:

```
GET /cart/2
Authorization: Bearer <token_of_user1>
```

Result:

```
{
  "error": "Forbidden"
}
```

Unauthorized access is successfully blocked.

---

## Security Principle

Applications must enforce **authorization checks on every protected resource** and verify that users can only access their own data.
