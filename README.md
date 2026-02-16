🔒 Secure Node Chat
Secure Node Chat is a lightweight, self-hosted communication hub designed for users who prioritize privacy and modern aesthetics. Unlike standard chat apps, this project doesn't store your admin credentials in the code or a database—you set them live in the terminal every time you start the engine.

🚀 Why use this?
Zero-Config Security: No setup menus. Your username, password, and the secret entrance URL are defined by you at the moment of execution.

Stealth Mode: The website returns a 404 Not Found to anyone who doesn't know your specific "Secret Path."

Modern Aesthetics: A beautiful, responsive interface built with Tailwind CSS, featuring frosted-glass effects (Glassmorphism) and smooth transitions.

Identity Control: Users choose a session nickname at login, which is then locked to their messages for that session.

Privacy First: A prominent "EXIT" button allows for a full session purge, ensuring no trace is left in the browser.

🛠️ Technical Stack
Backend: Python / Flask

Frontend: HTML5 / Tailwind CSS / JavaScript (ES6)

Data: JSON-based persistent storage

Security: Secrets module for cryptographically strong session tokens