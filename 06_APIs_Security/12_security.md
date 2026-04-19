# Security and Authentication

Security is not a feature; it is a foundational requirement. A secure application must ensure **Confidentiality**, **Integrity**, and **Availability**.

## Access Control
-   **RBAC (Role-Based Access Control)**: Permissions are assigned to roles (e.g., Admin, User, Guest) rather than individual users.
-   **Principle of Least Privilege**: Every module or user should have the minimum level of access required to perform its task.

## Authentication Mechanisms

### 1. Basic Auth
Client sends `Authorization` header with Base64 encoded `username:password`.
[WARNING]
Basic Auth is insecure because Base64 is easily reversible. It **must** be used with HTTPS to encrypt the channel.
[/CALLOUT]

### 2. Digest Auth
Uses hashing (like MD5 or SHA) and a **Nonce** (number used once) to prevent replay attacks and avoid sending passwords in plain text.

### 3. Cookies & Sessions
-   **Session Cookie**: A unique ID stored on the client.
-   **Server-side Session**: The server stores data associated with that ID.
-   **Security**: Cookies should be marked as `HttpOnly` (to prevent JS access) and `Secure` (to ensure they are only sent over HTTPS).

## Common Vulnerabilities

### SQL Injection
Occurs when user input is directly concatenated into a SQL query.
**Fix**: Use **Parameterized Queries** or an ORM (Object-Relational Mapper).

### Cross-Site Request Forgery (CSRF)
An attack that forces an authenticated user to execute unwanted actions on a web application in which they are currently authenticated.
**Fix**: Use **CSRF Tokens**.

[TIP]
**Password Hashing**: Never store passwords in plain text. Use a strong, salted hashing algorithm like **bcrypt** or **Argon2**.
[/CALLOUT]

## Glossary
- **Salt**: Random data added to a password before hashing to prevent rainbow table attacks.
- **Nonce**: A unique number used only once in a security protocol to prevent replay attacks.
- **HTTPS**: HTTP over TLS/SSL — encrypts the communication channel between client and server.
