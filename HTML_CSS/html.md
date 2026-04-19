# HTML and the Document Object Model

## What is HTML?

Imagine you are building a house. Before the painter comes, before the interior designer arrives, you need a **skeleton** — the basic structure of walls, rooms, and a roof.

**HTML (HyperText Markup Language)** is the skeleton of every webpage. It defines:
- Where the heading goes
- Where the paragraph goes
- Where the image goes
- Which words are links

HTML does NOT decide colors, fonts, or spacing — that's CSS's job!

---

## What Does an HTML File Look Like?

An HTML file is just a **text file** with special tags wrapped in `< >` brackets. The browser reads these tags and knows how to display the content.

```
<tag>Content goes here</tag>
  ↑                      ↑
Opening tag          Closing tag (has a /)
```

---

## The Structure of Every HTML Page

Every HTML file in the world has the same basic skeleton:

```html
<!DOCTYPE html>              ← Tells the browser "this is HTML5"
<html lang="en">             ← The root tag. Everything is inside this.
  
  <head>                     ← INVISIBLE section (info FOR the browser)
    <meta charset="UTF-8">   ← "Use UTF-8 encoding for all characters"
    <title>My Page</title>   ← What appears in the browser tab
  </head>
  
  <body>                     ← VISIBLE section (what users SEE)
    <h1>Hello World!</h1>    ← A big heading
    <p>My first page.</p>    ← A paragraph of text
  </body>

</html>
```

---

## The HTML Tree (DOM)

When a browser reads your HTML file, it builds it into a **tree structure** in memory. This is called the **Document Object Model (DOM)**.

Think of it like a **family tree**:

```
                    document
                       |
                      html
                    /       \
                head         body
               /   \        /     \
          title   meta     h1      p
            |               |      |
        "My Page"        "Hello"  "Text"
```

Each item in the tree is called a **node**. JavaScript can walk through this tree and change any part of the page without reloading!

---

## Core HTML Tags: Your Toolbox

### Structural Tags (For organizing sections)

```html
<header>   → Top section of a page (logo, navigation)
<nav>      → Navigation links
<main>     → The main content area
<section>  → A thematic group of content
<article>  → A self-contained piece of content (like a blog post)
<footer>   → Bottom section (copyright, contact)
<div>      → A generic container (no meaning, just grouping)
```

### Content Tags (For actual content)

```html
<h1>Largest Heading</h1>
<h2>Smaller Heading</h2>        ← h1 to h6 (h6 is smallest)
<p>A paragraph of text.</p>
<a href="https://google.com">Click me!</a>   ← A link
<img src="photo.jpg" alt="My photo">         ← An image
<ul>                                          ← Unordered list (bullets)
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
<ol>                                          ← Ordered list (numbers)
  <li>First</li>
  <li>Second</li>
</ol>
<strong>Bold text</strong>
<em>Italic text</em>
<span>Inline wrapper (no meaning, just grouping inline text)</span>
```

### Form Tags (For user input)

```html
<form method="POST" action="/submit">
  <label for="email">Email:</label>
  <input type="email" id="email" name="email" placeholder="you@example.com">
  
  <label for="password">Password:</label>
  <input type="password" id="password" name="password">
  
  <button type="submit">Login</button>
</form>
```

---

## Semantic HTML: Using the RIGHT Tag

Two ways to write "navigation links":

```html
<!-- ❌ BAD: Generic div (no meaning) -->
<div class="navigation">
  <div><a href="/">Home</a></div>
  <div><a href="/about">About</a></div>
</div>

<!-- ✅ GOOD: Semantic nav tag (meaningful!) -->
<nav>
  <a href="/">Home</a>
  <a href="/about">About</a>
</nav>
```

**Why does it matter?**
- Screen readers for blind users know `<nav>` is navigation
- Google's search engine understands the structure better
- Other developers reading your code understand it immediately

[NOTE]
**Accessibility Rule**: Always add an `alt` attribute to every `<img>` tag. Screen readers read this aloud to visually impaired users. `<img src="cat.jpg" alt="A fluffy orange cat sitting on a chair">` is much better than `<img src="cat.jpg">`.
[/CALLOUT]

---

## The DOM: JavaScript's Gateway to the Page

The DOM is not just a tree for the browser to look at — JavaScript can **modify it in real time**!

```
 HTML File (Static)          Browser Memory (DOM)           Screen
                        
 <h1 id="title">             document                     ┌──────────┐
   Hello                     └── html                     │  Hello   │
 </h1>                            └── body                └──────────┘
                                       └── h1
                                             └── "Hello"
                                                  ↑
                          JavaScript can come here
                          and change "Hello" to "Goodbye"!
                          
                          document.getElementById("title").innerText = "Goodbye";
                                                            ↓
                                                     ┌──────────┐
                                                     │ Goodbye  │
                                                     └──────────┘
```

This is the magic behind all interactive websites — the page changes **without reloading!**

---

## What is a DOM Reflow?

Every time you add, remove, or resize an element, the browser has to **recalculate** where every element on the page goes. This is called a **Reflow**.

```
Before change:
  Box A: top=10px, left=5px
  Box B: top=50px, left=5px

You insert a new box between A and B...

After change (reflow needed):
  Box A: top=10px, left=5px   ← stays same
  NEW:   top=50px, left=5px   ← new element
  Box B: top=90px, left=5px   ← pushed down!
```

Reflows are computationally expensive. Modern JavaScript frameworks (like React) use a "Virtual DOM" — they calculate changes in memory FIRST, then apply everything at once, minimizing reflows.

---

## A Complete Real-World HTML Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student Profile</title>
</head>
<body>

    <header>
        <h1>Student Portal</h1>
        <nav>
            <a href="/home">Home</a>
            <a href="/grades">Grades</a>
            <a href="/logout">Logout</a>
        </nav>
    </header>

    <main>
        <section>
            <h2>Profile: Alice</h2>
            <img src="alice.jpg" alt="Alice's profile photo">
            <p>Roll Number: 21CS001</p>
            <p>Department: Computer Science</p>
        </section>

        <section>
            <h2>Enrolled Courses</h2>
            <ol>
                <li>Modern Application Development (MAD-I)</li>
                <li>Database Systems</li>
                <li>Machine Learning Foundations</li>
            </ol>
        </section>
    </main>

    <footer>
        <p>IIT Madras — Online Degree Program</p>
    </footer>

</body>
</html>
```

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Tag** | An HTML keyword wrapped in `< >` brackets |
| **Element** | An opening tag + content + closing tag together |
| **Attribute** | Extra information inside a tag (e.g., `href="url"`, `src="image.jpg"`) |
| **DOM** | The tree structure a browser builds from your HTML |
| **Semantic** | Tags that describe MEANING, not just appearance |
| **Reflow** | When the browser recalculates all element positions |
| **Entity** | Special character codes like `&copy;` (©) or `&amp;` (&) |
