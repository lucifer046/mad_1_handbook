# Flask and Routing

**Flask** is a micro web framework written in Python. It is classified as a "microframework" because it does not require particular tools or libraries. It keeps the core simple but extensible. You don't have to learn a massive system just to get a server running.

## Core Concepts

### WSGI & Werkzeug
Flask is based on the **WSGI** (Web Server Gateway Interface) standard. It uses the **Werkzeug** toolkit behind the scenes to handle the complex HTTP requests and responses, so you don't have to parse raw HTTP text manually.

### Routing (The Controller)
Routing is the process of mapping URLs (like `/home` or `/about`) to specific Python functions. In Flask, this is done using **Decorators**.

### Full "Hello World" Example
Here is a complete, runnable Flask application in just 7 lines of code:

```python
from flask import Flask

app = Flask(__name__) # Create the application instance

@app.route('/') # Decorator: "When a user visits '/', run the function below"
def home():
    return "<h1>Hello, World!</h1><p>Welcome to Flask.</p>"

if __name__ == '__main__':
    app.run(debug=True) # Starts the server on port 5000
```

### URL Variables (Dynamic Routing)
You can capture parts of the URL as variables to make your routes dynamic. This is how sites load specific user profiles based on the URL.

```python
@app.route('/user/<username>')
def show_user_profile(username):
    return f"User Profile for: {username}"
```

[NOTE]
**Statelessness in Flask**: Since the web is stateless, we use **URL Parameters** (GET) or **Form Data** (POST) to pass information between pages. The server forgets who you are the moment it sends the response!
[/CALLOUT]

## Templates with Jinja2 (The View)
Instead of writing messy HTML inside Python strings, we use **Templates**. Flask uses the **Jinja2** engine to merge Python variables into HTML files securely.

-   **Interpolation**: Injecting variables. `<h1>Hello, {{ user_name }}!</h1>`
-   **Control Flow**: IF statements. `{% if is_admin %} <button>Delete</button> {% endif %}`
-   **Loops**: FOR loops. 
    ```html
    <ul>
      {% for student in class_list %}
        <li>{{ student.name }}</li>
      {% endfor %}
    </ul>
    ```

## Form Handling
When a user submits an HTML form, Flask provides the `request` object to access that data.
-   `request.form.get('email')`: Access data sent via POST (like a login form).
-   `request.args.get('search')`: Access data sent via GET parameters (like `?search=python`).

[TIP]
Always use `redirect` and `url_for` instead of hardcoding URLs in your HTML. `url_for('home')` will automatically generate the correct path to the `home` function, even if you change the URL later!
[/CALLOUT]

## Glossary
- **Decorator**: A function that wraps another function to modify its behavior (e.g., `@app.route`). It looks like an `@` symbol above a function.
- **Jinja2**: The default templating engine for Flask.
- **Middleware**: Software that acts as a bridge between an operating system or database and applications.
