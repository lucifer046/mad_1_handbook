# Deployment and DevOps

**Deployment** is the process of making your application available for use. **DevOps** is a set of practices that combines software development (Dev) and IT operations (Ops) to shorten the systems development life cycle.

## Service Models

| Model | Name | Description | Examples |
| :--- | :--- | :--- | :--- |
| **IaaS** | Infrastructure as a Service | Renting raw servers/VMs. You manage the OS. | AWS EC2, DigitalOcean |
| **PaaS** | Platform as a Service | Renting a platform to run apps. Provider manages OS. | Heroku, Google App Engine |
| **SaaS** | Software as a Service | Using a complete software product. | Google Docs, Trello |

## CI/CD Pipeline
-   **Continuous Integration (CI)**: Automatically building and testing your code every time you push a change to version control (like GitHub).
-   **Continuous Deployment (CD)**: Automatically deploying your code to the production server if all tests pass.

## Containers with Docker
**Containers** allow you to package your application and its dependencies into a single "image" that runs identically on any machine.
-   **Isolation**: Apps run in their own sandbox.
-   **Portability**: "It works on my machine" is no longer an excuse.

[NOTE]
**Orchestration**: For complex apps with multiple containers (e.g., Flask + Postgres + Redis), we use tools like **Docker Compose** or **Kubernetes** to manage them.
[/CALLOUT]

## Logging & Monitoring
A production app must be monitored to ensure it's healthy.
-   **Access Logs**: Tracking who visited which URL.
-   **Error Logs**: Recording crashes and bugs for debugging.
-   **Time-Series Monitoring**: Tracking metrics like CPU usage or response time over time.

[TIP]
**Log Rotation**: Always set up log rotation. Otherwise, your log files will eventually fill up the entire disk, causing your server to crash.
[/CALLOUT]

## Glossary
- **DevOps**: A culture and set of practices for faster software delivery.
- **Image**: A read-only template with instructions for creating a Docker container.
- **Latency**: The time delay between a trigger and a response.
