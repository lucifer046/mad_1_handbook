# Flask and Routing

## What is Flask?

Imagine you want to open a shop. You need:
1. A building (the web server)
2. A counter where customers come to ask for things (the route)
3. A person behind the counter who fulfills requests (the Python function)

**Flask** is a Python library that lets you build all three in just a few lines of code.

Flask is called a "**micro**framework" because it's tiny by default — it only does what you need it to, without imposing a massive structure on you.

---

## Your First Flask App: The Minimal Version

Let's build the simplest possible web server:

```python
# ── Step 1: Import Flask from the flask library ──────────────────
from flask import Flask

# ── Step 2: Create the application instance ──────────────────────
# __name__ tells Flask the name of this file (so it can find templates, etc.)
app = Flask(__name__)

# ── Step 3: Create a ROUTE ──────────────────────────────────────
# A route = "when a user visits this URL, run this function"
@app.route('/')            # The '/' means the homepage (e.g., http://localhost:5000/)
def home():
    return "<h1>Hello, World!</h1><p>My first Flask app!</p>"

# ── Step 4: Start the server ──────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)    # debug=True shows errors nicely during development
```

**Run it**: Open a terminal and type `python app.py`. Then visit `http://localhost:5000` in your browser.

---

## How Routing Works

A **route** is the connection between a URL and a Python function.

```
  User types URL          Flask finds matching route         Function runs
  ───────────────         ──────────────────────────         ─────────────
  /                  →    @app.route('/')              →    home()
  /about             →    @app.route('/about')         →    about()
  /students          →    @app.route('/students')      →    list_students()
  /student/42        →    @app.route('/student/<id>')  →    show_student(id=42)
```

### Dynamic Routes: Capture Parts of the URL

You can capture variable parts of the URL using `<variable_name>`:

```python
@app.route('/student/<int:student_id>')
def show_student(student_id):
    # student_id is now a Python integer!
    # e.g., visiting /student/42 → student_id = 42
    return f"<h1>Profile page for Student #{student_id}</h1>"

@app.route('/user/<username>')
def show_user(username):
    # username is a string
    # e.g., visiting /user/alice → username = "alice"
    return f"<p>Hello, {username}!</p>"
```

### Handling Different HTTP Methods

By default, routes only listen to **GET** requests (loading a page). For forms, you need **POST**:

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # User is just visiting the page → Show the login form
        return render_template('login.html')
    
    elif request.method == 'POST':
        # User submitted the form → Process the login
        username = request.form.get('username')
        password = request.form.get('password')
        # ... verify and respond
```

---

## How Flask Works Under the Hood

Flask is built on **WSGI** (Web Server Gateway Interface). Here's the lifecycle of a request:

```
  Your Browser                  Flask (WSGI App)              Your Python Code
       |                               |                               |
       | 1. HTTP GET /students         |                               |
       |──────────────────────────────>|                               |
       |                               |                               |
       |                               | 2. Parse the HTTP request     |
       |                               |   ("Method: GET, Path: /students")
       |                               |                               |
       |                               | 3. Find matching route        |
       |                               |   @app.route('/students')     |
       |                               |──────────────────────────────>|
       |                               |                               |
       |                               |                  4. Run the   |
       |                               |                     function  |
       |                               |                     return "" |
       |                               |<──────────────────────────────|
       |                               |                               |
       |                               | 5. Build HTTP response        |
       |                               |   (Status: 200 OK)            |
       |<──────────────────────────────|                               |
       |                               |                               |
       | 6. Browser renders the HTML   |                               |
```

---

## Templates with Jinja2: Separating Python from HTML

Writing HTML **inside** Python strings is messy:

```python
# ❌ BAD: HTML inside Python strings
def show_students(students):
    html = "<html><body><ul>"
    for s in students:
        html += f"<li>{s['name']}</li>"
    html += "</ul></body></html>"
    return html
```

The better way is to put HTML in **template files** and use **Jinja2** to inject Python data into them:

```
my_flask_app/
├── app.py                ← Python logic (Controller)
└── templates/            ← HTML files (View)
    ├── layout.html       ← Base template (header, footer)
    ├── home.html         ← Homepage
    └── students.html     ← Students list page
```

```python
# ✅ GOOD: app.py keeps Python, template has HTML
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/students')
def list_students():
    students = [
        {"name": "Alice", "marks": 85},
        {"name": "Bob",   "marks": 35},
    ]
    # Pass the list to the template
    return render_template('students.html', students=students)
```

```html
<!-- templates/students.html -->
<!DOCTYPE html>
<html>
<head><title>Students</title></head>
<body>
  <h1>Student List</h1>
  <ul>
    <!-- Jinja2 FOR loop: {{ double curly }} for variables, {% %} for logic -->
    {% for student in students %}
      <li>
        {{ student.name }}  ← This prints the name variable
        {% if student.marks >= 40 %}
          ✅ PASS
        {% else %}
          ❌ FAIL
        {% endif %}
      </li>
    {% endfor %}
  </ul>
</body>
</html>
```

---

## Jinja2 Quick Reference

| Syntax | Purpose | Example |
|:---|:---|:---|
| `{{ variable }}` | Print a value | `{{ student.name }}` |
| `{% if ... %}` | Conditional | `{% if marks > 40 %}` |
| `{% for x in list %}` | Loop | `{% for s in students %}` |
| `{% block content %}` | Template inheritance block | Used in layout.html |
| `{% extends "base.html" %}` | Use a base template | `{% extends "layout.html" %}` |

---

## Handling Form Data

When a user submits an HTML form, Flask's `request` object captures everything:

```python
from flask import Flask, request, redirect, url_for

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Access form data by the 'name' attribute of the HTML input
        student_name = request.form.get('name')
        marks = int(request.form.get('marks', 0))
        
        # ... save to database ...
        
        # Always redirect after a POST to prevent form re-submission on refresh
        return redirect(url_for('list_students'))
    
    return render_template('add_student.html')
```

[NOTE]
**Why `redirect(url_for(...))`?** If you just return HTML after a POST, and the user refreshes the page, their browser will ask "Re-submit the form?" — and the data gets saved twice! Always redirect after a POST. This is called the **Post/Redirect/Get (PRG) Pattern**.
[/CALLOUT]

[TIP]
Use `url_for('function_name')` instead of hardcoding `/students`. If you ever change the URL of a route, `url_for` will automatically use the new URL everywhere. Hardcoded URLs break.
[/CALLOUT]

---

## Flask Project Structure

```
my_flask_app/
├── app.py                    ← Main application (routes, config)
├── requirements.txt          ← List of Python packages needed
│
├── templates/                ← Jinja2 HTML templates
│   ├── base.html             ← Master layout (header, footer)
│   ├── home.html             ← Home page
│   ├── login.html            ← Login form
│   └── students.html         ← Students list
│
└── static/                   ← Files served directly (no processing)
    ├── style.css             ← Your CSS
    ├── script.js             ← Your JavaScript
    └── logo.png              ← Images
```

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Flask** | A lightweight Python library for building web servers |
| **Route** | A mapping from a URL path to a Python function |
| **Decorator** | A Python `@syntax` that wraps a function (e.g., `@app.route('/home')`) |
| **WSGI** | The standard interface between Python web apps and web servers |
| **Jinja2** | The template engine Flask uses to insert Python values into HTML |
| **request** | Flask's object containing data from the browser's HTTP request |
| **render_template** | A Flask function that fills a template with data and returns HTML |
| **redirect** | A Flask function that sends the user to a different URL |
| **url_for** | A Flask function that generates URLs from function names |
