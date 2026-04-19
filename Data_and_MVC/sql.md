# SQL and Databases

## What is a Database?

Think of a database as a super-powered, multi-sheet **Excel workbook**:
- Each "sheet" is a **Table**
- Each "row" is a **Record** (one entry, like one student)
- Each "column" is a **Field** (one property, like the student's name)
- The Excel app that runs it is the **Database Engine** (e.g., SQLite, PostgreSQL)

But unlike Excel, a database can:
- Handle **millions** of rows without slowing down
- Link tables together automatically (no copy-pasting!)
- Allow **multiple users** to read/write at the same time
- Protect data from loss even if the server crashes

---

## SQL: The Language to Talk to Databases

**SQL** (Structured Query Language, pronounced "see-kwel") is the language you use to talk to relational databases. It's remarkably close to plain English:

```
English:  "Give me all students whose marks are greater than 40"
SQL:      SELECT * FROM Students WHERE marks > 40;

English:  "Add a new student named Carol with marks 92"
SQL:      INSERT INTO Students (name, marks) VALUES ('Carol', 92);
```

---

## The Four Types of SQL Commands

### DDL — Data Definition Language (Building the Structure)

DDL creates the **skeleton** of the database — the tables and their column definitions.

```sql
-- Step 1: Create the Hostels table (must exist BEFORE Students, since Students reference it)
CREATE TABLE Hostels (
    hostel_id  INTEGER  PRIMARY KEY,   -- Unique ID for each hostel. Auto-numbered.
    name       VARCHAR(50) NOT NULL    -- Name of the hostel. Cannot be empty.
);

-- Step 2: Create the Students table
CREATE TABLE Students (
    student_id  INTEGER  PRIMARY KEY,      -- Unique student ID
    name        VARCHAR(100) NOT NULL,      -- Full name (max 100 chars)
    marks       INTEGER  DEFAULT 0,         -- Marks (defaults to 0 if not given)
    hostel_id   INTEGER,                   -- Which hostel are they in?
    
    -- This line LINKS hostel_id to the Hostels table
    FOREIGN KEY (hostel_id) REFERENCES Hostels(hostel_id)
);
```

### DML — Data Manipulation Language (Working with Data)

DML is for adding, changing, and removing data inside tables.

```sql
-- Adding data
INSERT INTO Hostels VALUES (1, 'Godavari');
INSERT INTO Hostels VALUES (2, 'Kaveri');
INSERT INTO Students VALUES (101, 'Alice', 85, 1);  -- Alice is in Godavari (hostel 1)
INSERT INTO Students VALUES (102, 'Bob',   35, 2);  -- Bob is in Kaveri (hostel 2)
INSERT INTO Students VALUES (103, 'Carol', 92, 1);  -- Carol is also in Godavari

-- Changing data
UPDATE Students SET marks = 40 WHERE student_id = 102;  -- Bob just passed the re-exam!

-- Removing data
DELETE FROM Students WHERE student_id = 103;  -- Remove Carol (she transferred)
```

### DQL — Data Query Language (The Most Important!)

Queries let you retrieve data using the powerful `SELECT` command.

```sql
-- SELECT all columns (*) from all students
SELECT * FROM Students;

-- SELECT only specific columns
SELECT name, marks FROM Students;

-- SELECT with a condition (WHERE)
SELECT * FROM Students WHERE marks >= 40;  -- Only passing students

-- SELECT with sorting
SELECT * FROM Students ORDER BY marks DESC;  -- Highest marks first

-- SELECT with pattern matching (LIKE)
SELECT * FROM Students WHERE name LIKE 'A%';  -- Names starting with 'A'
--                                       ↑
--                   % means "anything can come here"

-- SELECT with counting
SELECT COUNT(*) FROM Students;  -- How many students are there?
SELECT AVG(marks) FROM Students;  -- What is the average marks?
```

---

## Joins: Combining Data from Two Tables

This is where SQL becomes truly powerful. You can ask questions that **span multiple tables**.

```
  STUDENTS Table           HOSTELS Table
  ┌────┬───────┬──────┐    ┌────┬──────────┐
  │ ID │ Name  │ h_id │    │ ID │ Name     │
  ├────┼───────┼──────┤    ├────┼──────────┤
  │101 │ Alice │  1   │    │  1 │ Godavari │
  │102 │ Bob   │  2   │    │  2 │ Kaveri   │
  └────┴───────┴──────┘    └────┴──────────┘
                 ↑                ↑
                 These two columns are the "bridge"
```

```sql
-- INNER JOIN: "Show me each student AND their hostel name"
SELECT 
    Students.name       AS student_name,
    Hostels.name        AS hostel_name,
    Students.marks
FROM Students
INNER JOIN Hostels ON Students.hostel_id = Hostels.hostel_id;

-- Result:
-- student_name | hostel_name | marks
-- Alice        | Godavari    | 85
-- Bob          | Kaveri      | 35
```

### Types of Joins Explained

```
INNER JOIN: Only rows that MATCH in BOTH tables
  Table A:  [1, 2, 3]
  Table B:  [2, 3, 4]
  Result:   [2, 3]       ← Only the overlap

LEFT JOIN: ALL rows from LEFT table, matching rows from RIGHT (NULL if no match)
  Table A:  [1, 2, 3]
  Table B:  [2, 3, 4]
  Result:   [1=NULL, 2, 3]  ← Student 1 has no hostel, shown as NULL
```

---

## ACID Properties: Why Databases Are Trustworthy

Imagine you are transferring ₹500 from Alice's account to Bob's account. This involves two steps:
1. Deduct ₹500 from Alice
2. Add ₹500 to Bob

What if the server crashes **between step 1 and step 2**? Alice loses ₹500 and Bob gets nothing!

**ACID** is the set of guarantees that prevent this:

```
  ┌─────────────┬──────────────────────────────────────────────┐
  │ ACID        │ What it means                                │
  ├─────────────┼──────────────────────────────────────────────┤
  │ Atomicity   │ "All or Nothing"                             │
  │             │ Both steps complete, or neither happens      │
  ├─────────────┼──────────────────────────────────────────────┤
  │ Consistency │ Data always obeys the rules                  │
  │             │ (e.g., bank balance can't go below zero)     │
  ├─────────────┼──────────────────────────────────────────────┤
  │ Isolation   │ Two transactions don't interfere             │
  │             │ (Your transfer doesn't mess up mine)         │
  ├─────────────┼──────────────────────────────────────────────┤
  │ Durability  │ Once saved, it's saved forever               │
  │             │ (even if the server is unplugged right after)│
  └─────────────┴──────────────────────────────────────────────┘
```

---

## Full Example: SQLite in Python

```python
import sqlite3

# Connect to (or create) a database file
conn = sqlite3.connect("school.db")
cursor = conn.cursor()  # The cursor is how we send SQL commands

# ── DDL: Create tables ──────────────────────────────────────────
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT NOT NULL,
        marks      INTEGER DEFAULT 0
    )
""")

# ── DML: Insert some students ────────────────────────────────────
cursor.execute("INSERT INTO Students (name, marks) VALUES (?, ?)", ("Alice", 85))
cursor.execute("INSERT INTO Students (name, marks) VALUES (?, ?)", ("Bob", 35))
cursor.execute("INSERT INTO Students (name, marks) VALUES (?, ?)", ("Carol", 92))
conn.commit()  # Save the changes to disk!

# ── DQL: Query the data ──────────────────────────────────────────
print("\n--- All Students ---")
for row in cursor.execute("SELECT * FROM Students"):
    print(f"ID: {row[0]}, Name: {row[1]}, Marks: {row[2]}")

print("\n--- Passing Students (marks >= 40) ---")
for row in cursor.execute("SELECT * FROM Students WHERE marks >= 40"):
    print(f"{row[1]}: {row[2]}")

conn.close()
```

[TIP]
Notice the `?` in the SQL string? This is called a **Parameterized Query**. ALWAYS use it! If you write `f"INSERT INTO Students (name) VALUES ('{name}')"` instead, a user could type `'; DROP TABLE Students; --` as their name and **delete your entire database**. This attack is called SQL Injection.
[/CALLOUT]

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Table** | A grid of rows and columns, like a spreadsheet sheet |
| **Row / Record** | One entry in a table (one student, one product) |
| **Column / Field** | One property in a table (name, age, marks) |
| **Primary Key** | The unique ID for each row |
| **Foreign Key** | A column that links this table to another table's Primary Key |
| **JOIN** | An SQL operation that combines rows from two tables |
| **Transaction** | A group of SQL commands that run together as one unit |
| **ACID** | The four properties that guarantee database reliability |
| **SQL Injection** | An attack where malicious SQL is inserted into user input |
| **Normalization** | Organizing tables to remove redundant data |
