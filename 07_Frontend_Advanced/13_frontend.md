# Frontend Mechanisms

The **Frontend** is the part of the application that users interact with directly. In web applications, this means the HTML, CSS, and JavaScript running inside a browser.

## Page Generation Approaches

### 1. Fully Static Pages
-   **Mechanism**: Server sends pre-compiled HTML files.
-   **Pros**: Extreme speed, easy to host (CDNs).
-   **Cons**: Content is the same for all users; hard to update frequently.

### 2. Runtime Server-Side Rendering (SSR)
-   **Mechanism**: Server generates HTML on-the-fly for every request (e.g., Flask, PHP).
-   **Pros**: Dynamic content, SEO-friendly.
-   **Cons**: Server load, slower response times.

### 3. Client-Side Rendering (CSR)
-   **Mechanism**: Server sends a minimal HTML file and a large JavaScript bundle. JS builds the UI inside the browser.
-   **Pros**: App-like feel, interactive.
-   **Cons**: Slower initial load, SEO challenges.

## Async Updates (AJAX / Fetch)
Instead of reloading the entire page, modern apps use the **Fetch API** to request data in the background and update only specific parts of the DOM.

[NOTE]
The core idea of **Single Page Applications (SPAs)** is to load the page once and use async updates for all subsequent interactions.
[/CALLOUT]

## WebAssembly (WASM)
WASM is a binary instruction format for a stack-based virtual machine. It allows languages like C++, Rust, and Go to run on the web at near-native speeds.

[TIP]
**Sandboxing**: JavaScript and WASM run in a restricted environment called a "sandbox." They cannot access your files or hardware directly unless you give explicit permission.
[/CALLOUT]

## Glossary
- **AJAX**: Asynchronous JavaScript and XML — a technique for background data loading.
- **SPA**: Single Page Application.
- **V8**: The high-performance JavaScript engine used by Chrome and Node.js.
