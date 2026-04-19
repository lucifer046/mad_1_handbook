## Project Structure
```text
experiment-flask-restful/
├── application
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── controllers.py
│   ├── database.py
│   ├── models.py
│   └── validation.py
├── local_run.sh
├── local_setup.sh
├── main.py
└── templates
    ├── articles.html
    └── articles_by_author.html
```

---

# Experiment 08: Flask-RESTful
This experiment introduces **REST API** development using the `Flask-RESTful` extension. This allows us to create clean, standard-compliant APIs that return JSON instead of HTML.

## Detailed Code Breakdown

### 1. The `Api` Object
*   `from flask_restful import Api`: This is the core class. We wrap our `f_app` with it: `api_inst = Api(app_inst)`.
*   The `Api` object manages the mapping between Resource classes and URL endpoints.

### 2. Registering Resources
*   `r_api.add_resource(UserAPI, "/api/user", ...)`: This is where we define our API endpoints.
*   Unlike traditional routes (which point to functions), RESTful routes point to **Classes** that inherit from `Resource`. These classes typically have `get()`, `post()`, `put()`, and `delete()` methods.

### 3. URL Parameters
*   `"/api/user/<string:username>"`: We can pass variables directly in the URL. Flask-RESTful will automatically pass these to our resource methods (e.g., `def get(self, username):`).

### 4. Hybrid Approach
*   Notice how we still have `from application.controllers import *`. This means our app is **Hybrid**: it serves both HTML pages (to humans) and JSON APIs (to other computers).
