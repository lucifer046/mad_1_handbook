# SQL and Databases

**SQL** (Structured Query Language) is the standard language for communicating with Relational Databases (like SQLite, PostgreSQL, MySQL). It allows you to create schemas, insert data, and perform complex queries across millions of records efficiently.

## Relational Principles
In a relational database, data is organized into tables (Relations).
-   **Primary Key**: A column that uniquely identifies each row. E.g., `student_id`.
-   **Foreign Key**: A column that creates a link between two tables. E.g., placing a `hostel_id` in the Students table links a student to a specific hostel.

### 1. Creating Tables (DDL)
Data Definition Language (DDL) commands define the structure of the database.

```sql
CREATE TABLE Hostels (
    hostel_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hostel_id INTEGER,
    FOREIGN KEY (hostel_id) REFERENCES Hostels(hostel_id)
);
```

### 2. Inserting Data (DML)
Data Manipulation Language (DML) commands modify the data inside the tables.

```sql
INSERT INTO Hostels (hostel_id, name) VALUES (1, 'Godavari');
INSERT INTO Students (student_id, name, hostel_id) VALUES (101, 'Alice', 1);
```

### 3. Querying Data
The `SELECT` statement is the most common SQL operation used to retrieve data.

```sql
-- Select all students whose names start with 'A'
SELECT * FROM Students WHERE name LIKE 'A%';
```

## Joins: Combining Data
**Joins** allow you to retrieve data from multiple tables by connecting them on a related column (the Foreign Key).

-   **INNER JOIN**: Returns records that have matching values in both tables.
-   **LEFT JOIN**: Returns all records from the left table, and the matched records from the right. If there is no match, it returns NULL.

```sql
-- Find out which hostel Alice lives in
SELECT Students.name, Hostels.name AS hostel_name
FROM Students
INNER JOIN Hostels ON Students.hostel_id = Hostels.hostel_id;
```

[TIP]
Use the `LIKE` operator for pattern matching. `%` matches multiple characters, while `_` matches a single character.
[/CALLOUT]

## ACID Properties
To ensure reliability and prevent data corruption, robust databases follow the **ACID** model for transactions (a transaction is a group of SQL queries executed together):

1.  **Atomicity**: "All or nothing." If you transfer money, the deduction and the deposit must *both* succeed, or the entire transaction is cancelled.
2.  **Consistency**: Data always remains valid according to rules (e.g., balance cannot go below zero).
3.  **Isolation**: Multiple simultaneous transactions don't interfere with each other.
4.  **Durability**: Once saved, the data is safe even if someone unplugs the server.

## Glossary
- **Normalization**: The process of organizing data into multiple tables to reduce redundancy and improve data integrity.
- **Index**: A hidden data structure created by the database engine that vastly improves the speed of data retrieval operations (like the index of a book).
- **Transaction**: A single logical unit of work consisting of one or more SQL statements.
