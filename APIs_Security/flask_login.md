# Deep Dive: Flask-Login Extension

## The Problem with Manual Sessions

In the previous topic, we wrote the authentication manually. It works. But imagine you have 20 protected pages. You need to write this on EVERY page:

```python
if 'user' not in session:
    return redirect(url_for('sign_in'))
```

What if you build the 20th page and forget that check? Now your most important admin page is publicly accessible!

**Flask-Login** solves this with automation. Instead of forgetting a check, you just add a decorator and the library handles everything.

---

## How Flask-Login Changes the Architecture

```
  MANUAL SESSION (Previous topic):
  
  @app.route('/dashboard')
  def dashboard():
      if 'user' not in session:  ← You write this on EVERY page
          return redirect(...)
      # protected code here

  ──────────────────────────────────────────────────────

  FLASK-LOGIN (This topic):
  
  @app.route('/dashboard')
  @login_required               ← ONE line decorator does everything
  def dashboard():
      # protected code here (no manual check needed!)
```

---

## The 4 Key Components of Flask-Login

```
  ┌──────────────────────────────────────────────────────────────┐
  │                   FLASK-LOGIN SYSTEM                         │
  ├──────────────────────────────────────────────────────────────┤
  │                                                              │
  │  1. LoginManager    → The "brain". Configured once.         │
  │                       Handles redirects, session checks.     │
  │                                                              │
  │  2. User Class      → Your user model + UserMixin            │
  │     (UserMixin)       Provides: is_authenticated, get_id()   │
  │                                                              │
  │  3. User Loader     → Called on EVERY request                │
  │  (user_loader)        Converts a stored ID back to a User    │
  │                                                              │
  │  4. Decorators      → @login_required protects routes        │
  │                       current_user gives you the logged-in   │
  │                       User object everywhere                 │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step: How Flask-Login Works

### The User Loader: The Most Important Piece

Flask sessions only store **the user's ID** (a simple number or string). This is intentional — the session is very small.

But you need the whole User object (name, email, permissions) to do anything useful. The **user_loader** function bridges this gap on every request:

```
  REQUEST 1 (Login):
  
  User submits form → Flask-Login stores "42" in the session cookie
  
  ────────────────────────────────────────────────────────────────

  REQUEST 2 (Load dashboard):
  
  Browser sends request with cookie containing "42"
  Flask-Login reads the cookie: user_id = "42"
  Calls YOUR user_loader("42") function automatically
  Your function looks up user 42 in the database
  Returns a User(id=42, name="Alice", ...) object
  Now current_user is Alice everywhere in this request!
```

---

## Line-by-Line Code Walkthrough

```python
from flask import Flask, render_template, request, redirect, url_for
from flask_login import (
    LoginManager,     # The central manager object
    UserMixin,        # A mixin that provides standard User methods
    login_user,       # Function to start a session (login)
    login_required,   # Decorator to protect routes
    logout_user,      # Function to end a session (logout)
    current_user      # A proxy to the currently logged-in User object
)

app = Flask(__name__)
app.secret_key = 'sac_mad_one_flask_login_week'

# ────────────────────────────────────────────────────────────────
# STEP 1: Create and configure the LoginManager
# ────────────────────────────────────────────────────────────────
login_manager = LoginManager()
login_manager.init_app(app)  # Connect it to our Flask app

# VERY IMPORTANT: Tell Flask-Login where the login page is.
# If an unauthenticated user tries to access a @login_required page,
# they will be automatically redirected to this route.
login_manager.login_view = 'sign_in'


# ────────────────────────────────────────────────────────────────
# STEP 2: Define the User class
# ────────────────────────────────────────────────────────────────
# UserMixin provides 4 default methods that Flask-Login needs:
#   - is_authenticated: Returns True (this user IS logged in)
#   - is_active: Returns True (account is not banned)
#   - is_anonymous: Returns False (not an anonymous guest)
#   - get_id(): Returns self.id as a string
#
# Without UserMixin, you'd have to write all 4 yourself!
class User(UserMixin):
    def __init__(self, id, name):
        self.id = id        # REQUIRED by Flask-Login (used in user_loader)
        self.name = name    # Any custom attribute you need

# Mock database (in real apps, use SQLite/PostgreSQL)
users_db = {
    'admin': User(id='admin', name='Admin User'),
}


# ────────────────────────────────────────────────────────────────
# STEP 3: The User Loader (THE CRITICAL PIECE)
# ────────────────────────────────────────────────────────────────
# Flask-Login calls this function on EVERY request that has a session cookie.
# It passes the user_id string that was stored in the cookie.
# We must return the corresponding User object (or None if not found).
@login_manager.user_loader
def load_user(user_id):
    # user_id here is the string version of User.get_id()
    # We look it up in our "database" and return the full User object
    return users_db.get(user_id)
    # If the user doesn't exist (deleted account?), return None.
    # Flask-Login will treat None as "not logged in".


# ────────────────────────────────────────────────────────────────
# STEP 4: Login Route
# ────────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pwd')
        
        user = users_db.get(username)  # Look up the user
        
        if user and password == '123':  # In real apps, check hashed password!
            # login_user does TWO things:
            # 1. Stores user.get_id() in the session cookie
            # 2. Sets current_user to this User object for this request
            login_user(user)
            
            # Flask-Login also has a "next" system:
            # If user was redirected here from /dashboard,
            # it will redirect them BACK to /dashboard after login!
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        
        return "Invalid credentials", 401
    
    return render_template('login.html')


# ────────────────────────────────────────────────────────────────
# STEP 5: Protected Routes with @login_required
# ────────────────────────────────────────────────────────────────
@app.route('/dashboard')
@login_required  # Flask-Login checks session automatically. No manual if needed!
def dashboard():
    # current_user is the User object returned by load_user()
    # It's available in ALL templates and routes automatically
    return f"<h1>Welcome, {current_user.name}!</h1>"

@app.route('/admin')
@login_required  # Just one line to protect any route!
def admin_panel():
    return "<h1>Admin Panel</h1>"


# ────────────────────────────────────────────────────────────────
# STEP 6: Logout
# ────────────────────────────────────────────────────────────────
@app.route('/logout')
@login_required
def sign_out():
    # logout_user() does THREE things:
    # 1. Removes the user_id from the session
    # 2. Sets current_user to an AnonymousUser object
    # 3. Clears any "remember me" tokens
    logout_user()
    return redirect(url_for('sign_in'))


if __name__ == '__main__':
    app.run(debug=True)
```

---

## The `current_user` Object

One of the best features of Flask-Login — available EVERYWHERE after login:

```python
# In any route:
from flask_login import current_user

@app.route('/profile')
@login_required
def profile():
    print(current_user.id)      # 'admin'
    print(current_user.name)    # 'Admin User'
    print(current_user.is_authenticated)  # True
    return f"Hello {current_user.name}"

# In Jinja2 templates (automatically available, no import needed!):
# <p>Hello, {{ current_user.name }}!</p>
# {% if current_user.is_authenticated %}
#   <a href="/logout">Logout</a>
# {% else %}
#   <a href="/login">Login</a>
# {% endif %}
```

---

## Pros and Cons: Flask-Login vs. Manual

| Feature | Manual Session | Flask-Login |
|:---|:---|:---|
| **Setup complexity** | Minimal | Moderate (3 steps) |
| **Protection mechanism** | Manual `if` check | `@login_required` decorator |
| **Forgetting a check** | Easy to miss a page | Impossible (decorator is obvious) |
| **current_user access** | `session['user']` | `current_user` (rich object) |
| **Template support** | Manual | Auto-injected `current_user` |
| **Remember Me** | DIY (complex) | `login_user(user, remember=True)` |
| **Best For** | Learning, scripts | All real applications |

[TIP]
**Conclusion**: If you are building an app that real users will sign into, **always use Flask-Login**. The small amount of extra setup pays off enormously in safety and features. The `@login_required` decorator is simply too valuable to give up.
[/CALLOUT]

---

## Glossary

| Term | Meaning |
|:---|:---|
| **LoginManager** | The central Flask-Login object that controls sessions |
| **UserMixin** | A Python class that provides the 4 properties Flask-Login expects |
| **user_loader** | A function you write that converts a user ID back into a User object |
| **@login_required** | A decorator that automatically protects a route from unauthenticated access |
| **login_user()** | Flask-Login function that starts an authenticated session |
| **logout_user()** | Flask-Login function that ends an authenticated session |
| **current_user** | A Flask-Login proxy that represents the currently logged-in user |
