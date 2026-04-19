# Deep Dive: Session-Based Authentication

## What is Authentication?

**Authentication** answers one question: **"Who are you?"**

Before allowing someone into a restricted area (like a dashboard), your app must verify their identity. The most common way is **username + password**.

But here's the challenge: **HTTP is stateless**. The server forgets you the moment it answers your request. So how does it remember that you logged in?

The answer: **Sessions and Cookies**.

---

## The Cookie: Your "Visitor's Badge"

Think of it like visiting a library:
1. You show your ID at the counter (login with username/password)
2. The librarian gives you a **visitor's badge** with a number (a cookie)
3. Every time you want a book, you show your badge — you don't need to show your ID again
4. When you leave (logout), the librarian collects the badge and marks your number as "expired"

```
  YOUR BROWSER                              FLASK SERVER
       |                                         |
       | 1. POST /login {user: "alice", pwd: "x"}|
       |---------------------------------------->|
       |                                         |
       |                                 2. Check: alice+x correct? YES
       |                                 3. Create session: session["user"] = "alice"
       |                                 4. Sign a cookie (using secret_key)
       |                                         |
       | 5. Set-Cookie: session=AxB3...          |
       |<----------------------------------------|
       |                                         |
       | (Browser saves cookie automatically)    |
       |                                         |
       | 6. GET /dashboard  [Cookie: session=AxB3...]
       |---------------------------------------->|
       |                                         |
       |                                 7. Read cookie → Verify signature
       |                                 8. Decode: user = "alice"
       |                                 9. "alice" is in session → Access granted!
       |                                         |
       | 10. Dashboard HTML                      |
       |<----------------------------------------|
```

---

## Why the Secret Key is CRITICAL

The cookie that Flask sends to the browser looks like this:

```
eyJzdWIiOiJhbGljZSIsInJvbGUiOiJ1c2VyIn0.XlZhBg.secret_signature_here
```

It's just **base64 encoded** text, which anyone can decode and read. 

So what stops a user from editing their cookie to say `admin: True`?

The **digital signature** (generated using `app.secret_key`) is attached to the cookie. If anyone changes even ONE character of the cookie, the signature becomes invalid and Flask rejects it.

```
  Without secret_key:
  
  Cookie: {"user": "alice"}
  User edits: {"user": "alice", "is_admin": true}
  Server believes it! → SECURITY BREACH 💥

  With secret_key:
  
  Cookie: {"user": "alice"} + SIGNATURE (using secret_key)
  User edits the cookie data
  Signature no longer matches → Server REJECTS cookie → Safe! ✅
```

[WARNING]
**Never hardcode your secret_key in code that goes to GitHub!** Use environment variables instead:
```python
import os
app.secret_key = os.environ.get('SECRET_KEY')  # Set in server environment
```
If someone sees your secret key, they can forge any cookie and impersonate any user!
[/CALLOUT]

---

## Line-by-Line Code Walkthrough

```python
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

# ────────────────────────────────────────────────────────────────
# SECRET KEY — The signing key for session cookies
# Without this, Flask will raise a RuntimeError.
# This key should be long, random, and kept SECRET.
# ────────────────────────────────────────────────────────────────
app.secret_key = 'sac_mad_one_flask_login_week'


@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    # ── GET request: User is visiting the login page for the first time ──
    if request.method == 'GET':
        return render_template('login.html')
    
    # ── POST request: User submitted the login form ──
    if request.method == 'POST':
        username = request.form.get('username')  # From <input name="username">
        password = request.form.get('password')  # From <input name="password">
        
        # ── VERIFICATION ──────────────────────────────────────────────────
        # In a real app, you would:
        # 1. Look up the username in the database
        # 2. Compare the password with the HASHED version stored in DB
        # Here, we hardcode for simplicity (educational purposes only!)
        if username == 'admin' and password == '12345':
            
            # ── CREATE THE SESSION ─────────────────────────────────────────
            # session is a dictionary. Setting a key here causes Flask to:
            # 1. Serialize the session dict to JSON
            # 2. Sign it with the secret_key
            # 3. Send it to the browser as a cookie via "Set-Cookie" header
            session['user'] = username
            
            # ── REDIRECT AFTER POST ────────────────────────────────────────
            # We redirect so that refreshing the page doesn't resubmit the form
            return redirect(url_for('dashboard'))
        
        # Wrong credentials — send the error back
        return "Invalid credentials. Please try again.", 401


@app.route('/dashboard')
def dashboard():
    # ── MANUAL AUTHORIZATION CHECK ────────────────────────────────────────
    # The session is just a Python dict. We check if 'user' key exists.
    # If not present, the user hasn't logged in.
    # This check MUST be written on EVERY protected page.
    if 'user' not in session:
        # Not logged in → Send them to login page
        return redirect(url_for('sign_in'))
    
    # User is logged in → Show the dashboard
    # We can also get the username: session['user'] → 'admin'
    return render_template('dashboard.html', username=session['user'])


@app.route('/logout')
def sign_out():
    # ── CLEAR THE SESSION ─────────────────────────────────────────────────
    # session.clear() removes ALL keys from the session dictionary.
    # Flask then sends an updated (empty) cookie to the browser.
    # The browser still technically has a cookie, but the server
    # no longer recognizes it as having any logged-in state.
    session.clear()
    return redirect(url_for('sign_in'))


if __name__ == '__main__':
    app.run(debug=True)
```

---

## The Pros and Cons of Manual Sessions

| | Manual Session | Flask-Login |
|:---|:---|:---|
| **Complexity** | Simple | Slightly more setup |
| **Dependencies** | None (built-in) | `pip install flask-login` |
| **Safety** | You MUST remember checks | Checks are automatic |
| **Role Management** | DIY | DIY but structured |
| **Best For** | Tiny scripts, learning | Any real application |

---

## Common Security Mistakes to Avoid

```
  ❌ MISTAKE 1: Storing sensitive data in the session
  session['password'] = 'abc123'   ← NEVER do this!
  (The cookie is not fully encrypted — only signed)
  
  ❌ MISTAKE 2: Using a weak or common secret key
  app.secret_key = 'secret'        ← Easily guessed!
  app.secret_key = '12345'         ← Even worse!
  
  ✅ CORRECT: Generate a strong random key
  import secrets
  print(secrets.token_hex(32))     ← Generates a 64-char random key
  
  ❌ MISTAKE 3: Forgetting the authorization check on one page
  @app.route('/admin/delete-user')
  def delete_user():
      # Forgot the session check! Anyone can call this!
      ...
```

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Authentication** | Verifying WHO you are (login) |
| **Authorization** | Verifying WHAT you're allowed to do (admin check) |
| **Session** | Server-side dictionary that tracks a user's state |
| **Cookie** | A small piece of data stored in the browser, sent with every request |
| **Secret Key** | A private string used to digitally sign cookies |
| **Stateless** | HTTP's property of not remembering previous requests |
| **POST/Redirect/GET** | Pattern of redirecting after a form submission to prevent duplicates |
