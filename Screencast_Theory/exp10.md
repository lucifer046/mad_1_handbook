## Project Structure
```text
experiment-fts/
├── application
│   ├── __init__.py
│   ├── config.py
│   ├── controllers.py
│   ├── database.py
│   └── models.py
├── local_run.sh
├── local_setup.sh
├── main.py
└── templates
    ├── articles.html
    ├── articles_by_author.html
    └── results.html
```

---

# Experiment 10: SQLite Full-Text Search (FTS)
This experiment demonstrates how to implement high-performance search using SQLite's **Full-Text Search (FTS)** extension. This is much faster and more accurate than using standard `LIKE` queries.

## Detailed Code Breakdown

### 1. The Virtual Table Model
*   `ArticleSearch`: This model doesn't represent a standard table. Instead, it represents a "Virtual Table" (FTS5) created specifically for indexing text.
*   In the database, this table is populated with the content of our articles so it can be searched incredibly quickly.

### 2. The `MATCH` Operator
*   `.op("MATCH")(query)`: This is the key line. Standard SQL uses `LIKE %term%`, which is slow because the database has to scan every single row.
*   The `MATCH` operator uses a pre-built index (similar to the index at the back of a textbook) to find relevant rows instantly.

### 3. Handling Query Parameters
*   `request.args.get('q')`: We retrieve the search term from the URL. For example, if the user visits `/search?q=flask`, the variable `query` will be `"flask"`.

### 4. Rendering Results
*   `render_template("results.html", ...)`: We pass both the search term (`query`) and the list of results (`res`) to the template so we can display a "Search results for..." message and list the matching articles.
