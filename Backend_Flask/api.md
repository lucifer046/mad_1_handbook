# API Design and REST

## What is an API?

Imagine you are at a restaurant again. You don't walk into the kitchen and grab food yourself. You talk to the **waiter**. The waiter takes your request, goes to the kitchen, and brings back what you asked for.

An **API (Application Programming Interface)** is the waiter for software. It's a defined way for two different programs to communicate with each other — without either program needing to know what's happening "inside" the other.

```
  YOUR APP                  WEATHER API                  WEATHER DATABASE
  (Frontend)                                              (Backend)
     |                           |                             |
     | "GET /weather?city=Mumbai"|                             |
     |──────────────────────────>|                             |
     |                           | "SELECT * FROM weather..."  |
     |                           |────────────────────────────>|
     |                           |           data              |
     |                           |<────────────────────────────|
     |  { "temp": 32, "rain": 0 }|                             |
     |<──────────────────────────|                             |
     |                           |                             |
     | Display "Mumbai: 32°C"    |                             |
```

---

## REST: The Rules that Make APIs Consistent

Many companies could design their APIs however they like. To avoid chaos, most follow **REST** (Representational State Transfer) — a set of guidelines that makes APIs predictable and easy to use.

Think of REST like **traffic rules**. Without rules, cars crash. With REST, developers from any company can use any API immediately.

### The 6 REST Principles

```
  ┌──────────────────┬────────────────────────────────────────────────────┐
  │ Principle        │ Simple Explanation                                 │
  ├──────────────────┼────────────────────────────────────────────────────┤
  │ Client-Server    │ App and database/server are SEPARATE. They         │
  │                  │ communicate only through the API.                   │
  ├──────────────────┼────────────────────────────────────────────────────┤
  │ Stateless        │ Each request carries ALL needed info.              │
  │                  │ Server doesn't "remember" previous requests.        │
  ├──────────────────┼────────────────────────────────────────────────────┤
  │ Cacheable        │ Responses say "you can save this for X minutes"    │
  │                  │ so clients don't re-fetch the same data.            │
  ├──────────────────┼────────────────────────────────────────────────────┤
  │ Uniform Interface│ Resources use consistent URLs and HTTP verbs.      │
  │                  │ /students always means students, not /getStudents   │
  ├──────────────────┼────────────────────────────────────────────────────┤
  │ Layered System   │ Client can't tell if it's talking to the main      │
  │                  │ server or a middleman (load balancer, cache, CDN). │
  ├──────────────────┼────────────────────────────────────────────────────┤
  │ Code on Demand   │ Optional: Server can send executable code          │
  │ (Optional)       │ (like JavaScript) to the client.                   │
  └──────────────────┴────────────────────────────────────────────────────┘
```

---

## Resources and URLs: The Naming Convention

In REST, everything is a **resource**. A resource is anything you can name: a student, a course, a hostel.

Resources are accessed through **URLs** (Uniform Resource Locators):

```
  Resource: Students

  GET    /api/students         → Get a list of ALL students
  POST   /api/students         → Create a NEW student
  GET    /api/students/101     → Get ONE specific student (ID = 101)
  PUT    /api/students/101     → Update student 101 completely
  DELETE /api/students/101     → Delete student 101

  Notice the PATTERN:
  - Collection: /api/students      (plural noun)
  - Individual: /api/students/101  (noun + ID)
  - No VERBS in URLs! (Not /getStudent, /deleteStudent)
```

---

## A Complete CRUD API Example in Flask

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Our "database" for demonstration (in real life, use SQLite/PostgreSQL)
students_db = {
    101: {"name": "Alice", "marks": 85},
    102: {"name": "Bob",   "marks": 35},
}
next_id = 103  # Next available ID

# ── READ: Get all students ────────────────────────────────────────
@app.route('/api/students', methods=['GET'])
def get_students():
    """
    GET /api/students
    Returns the full list of students as JSON.
    """
    return jsonify(students_db), 200  # 200 = OK

# ── READ: Get one student ─────────────────────────────────────────
@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """
    GET /api/students/101
    Returns one student, or a 404 error if not found.
    """
    student = students_db.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404  # 404 = Not Found
    return jsonify(student), 200

# ── CREATE: Add a new student ─────────────────────────────────────
@app.route('/api/students', methods=['POST'])
def create_student():
    """
    POST /api/students
    Body: {"name": "Carol", "marks": 92}
    Creates a new student and returns their ID.
    """
    global next_id
    data = request.get_json()  # Parse the JSON body
    
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400  # 400 = Bad Request
    
    students_db[next_id] = {"name": data['name'], "marks": data.get('marks', 0)}
    new_id = next_id
    next_id += 1
    
    return jsonify({"id": new_id, "message": "Student created"}), 201  # 201 = Created

# ── DELETE: Remove a student ──────────────────────────────────────
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """
    DELETE /api/students/102
    Removes the student from the database.
    """
    if student_id not in students_db:
        return jsonify({"error": "Not found"}), 404
    
    del students_db[student_id]
    return jsonify({"message": "Student deleted"}), 200
```

---

## JSON: The Language APIs Use

APIs mostly communicate using **JSON** (JavaScript Object Notation). It's a lightweight way to represent data.

```json
{
    "student_id": 101,
    "name": "Alice",
    "marks": 85,
    "is_passing": true,
    "courses": ["MAD-I", "Database Systems"],
    "address": {
        "hostel": "Godavari",
        "room": "A204"
    }
}
```

JSON supports:
- **String**: `"Alice"` (text in double quotes)
- **Number**: `85` (no quotes)
- **Boolean**: `true` or `false` (lowercase)
- **Array**: `["item1", "item2"]`
- **Object**: `{"key": "value"}`
- **Null**: `null`

---

## HTTP Verbs and Idempotency

| Verb | Action | Idempotent? | Why? |
|:---|:---|:---|:---|
| **GET** | Read data | YES | Reading the same data 10 times still gives the same result |
| **PUT** | Replace data | YES | Setting a value to "Alice" 10 times still results in "Alice" |
| **DELETE** | Remove data | YES | Deleting once and deleting 10 times both result in "gone" |
| **POST** | Create new | NO | Each POST creates a NEW record — you'd get 10 duplicates! |

[NOTE]
**What is Idempotency?** An operation is **idempotent** if doing it multiple times gives the same result as doing it once. Light switches are idempotent: flipping UP twice is the same as flipping UP once.
[/CALLOUT]

---

## Testing Your API with Postman or curl

You don't need a frontend to test an API. Use tools like **Postman** (graphical) or **curl** (command line):

```bash
# GET all students
curl http://localhost:5000/api/students

# POST a new student (send JSON in the body)
curl -X POST http://localhost:5000/api/students \
     -H "Content-Type: application/json" \
     -d '{"name": "Carol", "marks": 92}'

# DELETE student 102
curl -X DELETE http://localhost:5000/api/students/102
```

---

## Glossary

| Term | Meaning |
|:---|:---|
| **API** | Application Programming Interface — a defined way for programs to talk |
| **REST** | Representational State Transfer — guidelines for consistent API design |
| **Resource** | Any nameable thing your API manages (student, course, product) |
| **Endpoint** | A specific URL in your API (e.g., `/api/students/101`) |
| **JSON** | JavaScript Object Notation — the most common data format for APIs |
| **CRUD** | Create, Read, Update, Delete — the four basic API operations |
| **Idempotent** | An operation that produces the same result no matter how many times you run it |
| **Status Code** | A 3-digit number in HTTP responses that tells you what happened |
| **Serialization** | Converting Python objects to JSON (and back) |
