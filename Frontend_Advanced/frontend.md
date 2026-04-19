# Frontend Mechanisms

## What is the "Frontend"?

The **frontend** is everything the user can SEE and TOUCH in a web application. If the backend is the kitchen of a restaurant, the frontend is the dining room — the part that customers actually experience.

Frontend = HTML + CSS + JavaScript running inside the user's browser.

---

## Three Ways to Build a Web Page

Not all web pages are built the same way. There are three major approaches:

### Approach 1: Fully Static Pages

```
  How it works:
  
  Developer writes HTML file
       |
       ↓ (uploaded to server, never changes)
  Browser requests /index.html
       |
       ↓ Server sends the EXACT same file to everyone
  Browser displays page
  
  ┌─────────────────────────────────────────────────┐
  │  Pros: Extreme speed (CDN delivery)             │
  │        Simple to host (no Python, no database)  │
  │        Great security (nothing to hack)         │
  ├─────────────────────────────────────────────────┤
  │  Cons: Same for everyone (no personalization)   │
  │        Hard to update frequently                │
  │  Examples: Documentation sites, landing pages   │
  └─────────────────────────────────────────────────┘
```

### Approach 2: Server-Side Rendering (SSR)

This is what **Flask** does by default!

```
  Browser requests /students
       |
       ↓ 
  Flask runs Python code:
       1. Query database
       2. Fill Jinja2 template with data
       3. Generate complete HTML
       |
       ↓ (a different, personalized HTML page for each user)
  Browser displays page (user specific!)
  
  ┌─────────────────────────────────────────────────┐
  │  Pros: Dynamic content per user                 │
  │        Great for SEO (Google sees full HTML)    │
  │        Simpler frontend code                    │
  ├─────────────────────────────────────────────────┤
  │  Cons: Every click = full page reload           │
  │        More server load (generates HTML often)  │
  │  Examples: Old-school websites, Flask apps      │
  └─────────────────────────────────────────────────┘
```

### Approach 3: Client-Side Rendering (CSR / SPA)

Modern approach. Used by React, Vue, Angular.

```
  FIRST visit to the page:
  Browser requests / → Server sends tiny HTML + massive JS bundle
  
  JS runs in browser, builds the entire page from scratch
  
  EVERY click after that:
  Browser's JS → Fetch only the DATA (JSON) from the API
  JS updates only the specific part of the page that changed
  NO full page reload!
  
  ┌─────────────────────────────────────────────────┐
  │  Pros: Feels like an app, not a website!        │
  │        Very fast AFTER initial load             │
  │        Can update small parts without reloading │
  ├─────────────────────────────────────────────────┤
  │  Cons: Slow INITIAL load (huge JS bundle)       │
  │        SEO is harder (Google may not see data)  │
  │  Examples: Gmail, Twitter, Facebook, Notion     │
  └─────────────────────────────────────────────────┘
```

---

## Asynchronous Updates: AJAX / Fetch API

The **Fetch API** lets JavaScript request data from the server **in the background** without refreshing the page.

```
  TRADITIONAL (full page reload):
  
  User clicks "Like"
       |
       ↓
  Entire page reloads with like count updated
  (takes 1-2 seconds, annoying!)

  ──────────────────────────────────────────

  MODERN (async fetch):
  
  User clicks "Like"
       |
       ↓
  JavaScript sends background request to /api/like/42
  (the page stays the same, no flicker!)
       |
       ↓
  Server updates the database, returns: { "likes": 101 }
       |
       ↓
  JavaScript updates ONLY the like counter on screen
  (done in ~50 milliseconds!)
```

```javascript
// JavaScript Fetch API Example
// When the user clicks "Like":
async function likePost(postId) {
    // Sends a background POST request (page doesn't reload!)
    const response = await fetch(`/api/like/${postId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 42 })
    });
    
    // Parse the JSON response
    const data = await response.json();
    
    // Update ONLY the like counter on the page (no reload!)
    document.getElementById('like-count').innerText = data.likes;
}
```

---

## Single Page Applications (SPAs)

An SPA is an app where the browser **loads only once** and then updates the page dynamically:

```
  Traditional Website (Multiple Pages):
  
  Click Home  → Browser loads home.html
  Click About → Browser loads about.html (FULL RELOAD)
  Click Back  → Browser loads home.html again (FULL RELOAD)
  
  ──────────────────────────────────────────

  Single Page Application:
  
  Click Home  → JS shows the "Home" component (no reload)
  Click About → JS shows the "About" component (no reload, instant!)
  Click Back  → JS shows the "Home" component again (instant!)
  
  URL still changes (for bookmarking), but browser never reloads.
```

[NOTE]
This handbook you're reading RIGHT NOW is an SPA! When you click between topics, the page never reloads — JavaScript updates only the content pane. Check the network tab in your browser's developer tools to see the fetch calls!
[/CALLOUT]

---

## WebAssembly (WASM): Bringing Native Performance to the Web

JavaScript is powerful but not the fastest. **WebAssembly** allows other languages (like C++, Rust, Go) to run in the browser at near-native CPU speed.

```
  Traditional JS Pipeline:
  Code → Interpreted by JS engine → 10x slower than native
  
  WASM Pipeline:
  C++/Rust → Compiled to WASM binary → Runs at near-native speed!
```

Use cases:
- Video editing in the browser (like Figma's canvas engine)
- 3D games running in the browser (Doom, Unity games)
- Image processing (like Photoshop on the web)

---

## Browser Security: The Sandbox

Your browser runs JavaScript from ANY website. Without restrictions, a malicious website could:
- Read your files
- Access your webcam
- Contact other websites as you

The **Sandbox** prevents this:

```
  ┌──────────────────────────────────────────────────────────┐
  │              BROWSER SANDBOX                             │
  │  ┌────────────────────────────────────────────────────┐ │
  │  │  JavaScript / WASM                                 │ │
  │  │                                                    │ │
  │  │  ✅ Can: Read/write page DOM                       │ │
  │  │  ✅ Can: Make network requests (with restrictions) │ │
  │  │  ✅ Can: Use localStorage                          │ │
  │  │                                                    │ │
  │  │  ❌ Cannot: Read your local files                  │ │
  │  │  ❌ Cannot: Talk to other websites' servers        │ │
  │  │            (without CORS permission)               │ │
  │  │  ❌ Cannot: Access your hardware directly          │ │
  │  └────────────────────────────────────────────────────┘ │
  │                                                          │
  │  Your OS and Files are OUTSIDE the sandbox              │
  └──────────────────────────────────────────────────────────┘
```

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Frontend** | The part of the app users see and interact with (HTML, CSS, JS) |
| **Backend** | The server-side logic that powers the frontend |
| **SSR** | Server-Side Rendering — HTML is built on the server |
| **CSR** | Client-Side Rendering — HTML is built in the browser by JavaScript |
| **SPA** | Single Page Application — page never reloads; JS swaps content |
| **AJAX** | Asynchronous JavaScript — fetch data in background without page reload |
| **Fetch API** | Modern JavaScript method for making async HTTP requests |
| **WASM** | WebAssembly — runs C++/Rust in the browser at near-native speed |
| **Sandbox** | A restricted environment where browser code runs safely |
| **CDN** | Content Delivery Network — serves static files from a server near you |
