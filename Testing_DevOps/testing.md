# Testing with Pytest

## Why Do We Test?

Imagine you built a student portal. It works fine on your laptop. You deploy it. A student types in 100 marks and the app crashes because you forgot to handle numbers above 99.

**Testing** is how we catch these bugs *before* users do. It's also how we make sure that when we fix one bug, we don't accidentally break three others.

---

## Types of Testing: Static vs. Dynamic

Before we dive into tools like Pytest, we must understand *how* we approach testing. Testing isn't just about running scripts; it’s about verifying correctness at different stages.

### 1. Static Testing (Testing the "Paper")
Static testing is performed **without executing the code**. It involves checking the code, documentation, and design to find errors.

*   **Examples:** Code reviews, walkthroughs, inspections, and using "Linters" (like Flake8) to catch syntax errors.
*   **Pros:** 
    *   **Early Detection:** Catches bugs before they ever reach a computer.
    *   **Cost-Effective:** Fixing a design flaw on paper is 10x cheaper than fixing it in production.
    *   **Quality Culture:** Encourages developers to write cleaner code.
*   **Cons:** 
    *   Cannot detect runtime errors (e.g., "Division by zero" which only happens during execution).
    *   Cannot verify performance or user experience.

### 2. Dynamic Testing (Testing the "Action")
Dynamic testing is performed **by executing the code**. You provide inputs and verify if the outputs match expectations.

*   **Examples:** Unit tests (Pytest), Integration tests, and User Acceptance Testing (UAT).
*   **Pros:** 
    *   **Runtime Validation:** Catches memory leaks, logic errors, and performance bottlenecks.
    *   **Functional Accuracy:** Ensures the app actually *works* for the user.
*   **Cons:** 
    *   More expensive to set up (requires a test environment).
    *   May miss bugs if the specific logic path isn't triggered by an input.

---

## Testing Methodologies: The "Box" Approach

How much should the tester know about the code? This determines the "color" of the box.

| Methodology | Definition | Pros | Cons |
|:--- |:--- |:--- |:--- |
| **Black Box** | Testing from the **user's perspective**. The tester has zero knowledge of the internal code. | User-centric; Tester doesn't need to be a developer. | Can lead to redundant tests; impossible to test every logic path. |
| **White Box** | Testing from the **developer's perspective**. The tester has full access to the source code and logic. | High code coverage; identifies hidden bugs in loops/logic. | Requires high technical skill; very time-consuming. |
| **Grey Box** | A **hybrid approach**. The tester has partial knowledge (e.g., knows the database schema or API endpoints but not the code). | Finds integration issues easily; combined benefits of both. | Coverage is limited compared to pure white box testing. |

---

## What is Pytest?

**Pytest** is a Python module (testing framework) used to write and run automated tests. It is the most popular testing tool in Python because of three key advantages:

```
   Pytest Advantages:

   1. Auto-Discovery  → Automatically finds and runs test files,
                        classes, and functions — no configuration
                        needed.

   2. Simple Syntax   → Uses plain Python assert statements.
                        No special syntax to learn.

   3. Parametrize     → Run the same test with many sets of input
                        data using a single decorator.
```

Install it with:
```bash
pip install pytest
```

---

## The Golden Rules: Naming Conventions

Pytest's auto-discovery relies entirely on naming. If you don't follow these rules, Pytest won't find your tests.

```
   Rule 1: FILES must start with "test_" or end with "_test"
           Good:  test_marks.py   marks_test.py
           Bad:   marks.py        check_marks.py

   Rule 2: FUNCTIONS must start with "test_"
           Good:  def test_case1():
           Bad:   def case1():    def check_case():

   Rule 3: CLASSES must start with "Test"
           Good:  class TestMarks:
           Bad:   class Marks:    class marks_test:
```

---

## The `assert` Keyword

The `assert` keyword is the fundamental building block of every test. It checks if a condition is `True`. If it's `False`, Python raises an `AssertionError` and the test fails.

```python
# assert <condition>, "Optional error message"

assert 2 + 2 == 4          # PASSES silently
assert 2 + 2 == 5          # FAILS with AssertionError
assert "hello" in "hello world"  # PASSES
assert [] == []             # PASSES
```

[NOTE]
`assert` is just a Python keyword — it's not special to Pytest. But Pytest intercepts the `AssertionError` and produces a clean, readable failure report with the actual vs. expected values.
[/CALLOUT]

---

## Running Pytest: CLI Commands

```bash
# Run all tests in the current directory (auto-discovery)
pytest

# Run with verbose mode — see each test name and PASSED/FAILED
pytest -v

# Run only tests whose name contains a keyword
pytest -k "increment"

# Run tests in a specific file
pytest test_compute.py

# Run a specific function in a specific file
pytest test_compute.py::test_increment
```

---

## Part 1: Testing Logic (Functions)

### The Application Code

This is a simple `compute` function we want to test — it either increments or decrements a value.

```python
# compute.py  (the code we are testing)

def compute(value, action):
    """
    Performs an arithmetic operation on a value.

    Args:
        value (int): The starting number.
        action (str): Either 'increment' or 'decrement'.

    Returns:
        int: The result of the operation.

    Raises:
        ValueError: If an unknown action is provided.
    """
    if action == "increment":
        return value + 1
    elif action == "decrement":
        return value - 1
    else:
        raise ValueError(f"Unknown action: {action}")
```

### The Test File

```python
# test_compute.py  (the test file — note the "test_" prefix)

import pytest
from compute import compute

# --- Basic Tests ---

def test_increment():
    """Verify that increment adds 1 to the value."""
    result = compute(5, "increment")
    assert result == 6

def test_decrement():
    """Verify that decrement subtracts 1 from the value."""
    result = compute(10, "decrement")
    assert result == 9

def test_increment_from_zero():
    """Edge case: incrementing zero should give 1."""
    assert compute(0, "increment") == 1

def test_invalid_action_raises_error():
    """An unknown action should raise a ValueError."""
    with pytest.raises(ValueError):
        compute(5, "multiply")  # Should throw ValueError
```

Run with `pytest -v` and you'll see:

```
test_compute.py::test_increment              PASSED
test_compute.py::test_decrement              PASSED
test_compute.py::test_increment_from_zero   PASSED
test_compute.py::test_invalid_action_raises_error PASSED
```

---

## Part 2: Pytest Markers

**Markers** are decorators (`@pytest.mark.<name>`) that attach metadata or special behavior to a test function.

### Built-in Marker 1: `@pytest.mark.skip`

Skips a test unconditionally. Use this when a feature is not yet implemented.

```python
@pytest.mark.skip(reason="Feature not yet implemented")
def test_multiply():
    result = compute(5, "multiply")
    assert result == 25
```

Output: `test_compute.py::test_multiply SKIPPED`

### Built-in Marker 2: `@pytest.mark.skipif`

Skips a test only if a condition is met. Great for OS-specific or environment-specific tests.

```python
import sys

@pytest.mark.skipif(sys.platform == "win32", reason="Does not run on Windows")
def test_linux_only_feature():
    # This test will be SKIPPED on Windows, but RUN on Linux/Mac
    assert True
```

### Built-in Marker 3: `@pytest.mark.parametrize`

The most powerful marker. Runs the **same test function** multiple times with different input data. This replaces writing 5 separate test functions for 5 cases.

```python
@pytest.mark.parametrize("value, action, expected", [
    (5,  "increment", 6),   # case 1
    (10, "increment", 11),  # case 2
    (10, "decrement", 9),   # case 3
    (0,  "decrement", -1),  # case 4 — edge case
    (99, "increment", 100), # case 5
])
def test_compute_parametrized(value, action, expected):
    assert compute(value, action) == expected
```

This generates 5 separate test cases from one function. Output:

```
test_compute.py::test_compute_parametrized[5-increment-6]    PASSED
test_compute.py::test_compute_parametrized[10-increment-11]  PASSED
test_compute.py::test_compute_parametrized[10-decrement-9]   PASSED
test_compute.py::test_compute_parametrized[0-decrement--1]   PASSED
test_compute.py::test_compute_parametrized[99-increment-100] PASSED
```

### Custom (User-Defined) Markers

You can create your own markers to group tests. Common groups are `smoke`, `regression`, and `slow`.

```python
# First, register your custom markers in pytest.ini:
# [pytest]
# markers =
#     smoke: Critical path tests that verify the app starts correctly.
#     regression: Tests that guard against previously fixed bugs.
#     slow: Tests that take a long time (e.g., database queries).

@pytest.mark.smoke
def test_app_starts():
    assert compute(1, "increment") == 2

@pytest.mark.regression
def test_known_bug_fix():
    # Bug report: compute(0, "decrement") used to return 0, not -1
    assert compute(0, "decrement") == -1

@pytest.mark.slow
def test_large_computation():
    for i in range(100000):
        compute(i, "increment")
```

Run only the `smoke` tests: `pytest -m smoke`

---

## Part 3: Testing Flask API Routes

To test Flask routes, we use the `requests` library to send real HTTP requests to the running application.

### The Flask Application

```python
# app.py  (the Flask app we want to test)

from flask import Flask, request, jsonify

app = Flask(__name__)

students = []  # In-memory store (for demo purposes)

@app.route('/students', methods=['GET'])
def get_students():
    """Returns all students. Status: 200 OK"""
    return jsonify(students), 200

@app.route('/students', methods=['POST'])
def add_student():
    """Adds a new student. Status: 201 Created"""
    data = request.get_json()
    students.append(data)
    return jsonify({"message": "Student added", "student": data}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### The API Test File

```python
# test_api.py  (tests for the Flask API routes)

import requests

BASE_URL = "http://127.0.0.1:5000"

# IMPORTANT: Start the Flask app manually before running these tests.
# In a separate terminal: python app.py

def test_get_students_status_code():
    """The GET /students endpoint should return 200 OK."""
    response = requests.get(f"{BASE_URL}/students")

    # Check the HTTP status code
    assert response.status_code == 200

def test_get_students_returns_list():
    """The GET /students endpoint should return a JSON list."""
    response = requests.get(f"{BASE_URL}/students")
    data = response.json()

    assert isinstance(data, list)  # Must be a list, not a dict

def test_post_student_status_code():
    """The POST /students endpoint should return 201 Created."""
    new_student = {"name": "Alice", "marks": 85}

    response = requests.post(
        f"{BASE_URL}/students",
        json=new_student  # Sends data as JSON body with Content-Type: application/json
    )

    assert response.status_code == 201

def test_post_student_response_body():
    """After POSTing, the response body should confirm the student was added."""
    new_student = {"name": "Bob", "marks": 70}

    response = requests.post(f"{BASE_URL}/students", json=new_student)
    body = response.json()

    assert "message" in body
    assert body["student"]["name"] == "Bob"
```

[TIP]
**Status Codes to Remember**:
- `200 OK` — GET request succeeded
- `201 Created` — POST request created a new resource
- `400 Bad Request` — Invalid input from client
- `401 Unauthorized` — Login required
- `402 Payment Required` — Digital payment needed
- `403 Forbidden` — Permission denied
- `404 Not Found` — Resource doesn't exist
- `500 Internal Server Error` — Bug in your code
[/CALLOUT]

---

## The Testing Pyramid

```

                       ACCEPTANCE TESTS
                      (Slow, Few, Manual)
                    Test the entire user flow.
                           /\
                          /  \
                         /    \
                        / INT. \
                       / TESTS  \
                      / Routes & \
                     / Database   \
                    / interaction  \
                   /\              /\
                  /  \            /  \
                 /                    \
                /    UNIT TESTS        \
               /  (Fast, Many, Auto)   \
              / Pure logic, functions   \
             /  Run on every code push  \
            /____________________________\

```

---

## How `pytest -k` Works

The `-k` flag filters tests by a keyword match against their name.

```bash
# Run only tests whose name contains "increment"
pytest -k "increment"

# Run tests whose name contains "increment" OR "decrement"
pytest -k "increment or decrement"

# Run all tests EXCEPT those containing "slow"
pytest -k "not slow"
```

---

## Glossary

| Term | Meaning |
|:---|:---|
| **pytest** | Python testing framework with auto-discovery and clean syntax |
| **assert** | Python keyword that checks a condition — fails with `AssertionError` if `False` |
| **Marker** | A decorator (`@pytest.mark.*`) that adds metadata or behavior to a test |
| **@pytest.mark.skip** | Unconditionally skips a test |
| **@pytest.mark.skipif** | Skips a test only if a condition is `True` |
| **@pytest.mark.parametrize** | Runs one test function with multiple sets of inputs |
| **Custom Marker** | User-defined group tag (e.g., `@pytest.mark.smoke`) for selective test runs |
| **`pytest -v`** | Verbose mode — shows each test name and its result |
| **`pytest -k`** | Keyword filter — runs only tests whose name matches a keyword |
| **Status Code 200** | HTTP response meaning the request succeeded (GET) |
| **Status Code 201** | HTTP response meaning a new resource was created (POST) |
| **Static Testing** | Testing code/docs without execution (Reviews, Linting) |
| **Dynamic Testing** | Testing by executing code (Unit tests, Integration) |
| **Black Box** | Testing from a user perspective with zero code knowledge |
| **White Box** | Testing from a developer perspective with full code access |
| **Grey Box** | Hybrid testing with partial knowledge of internals |
