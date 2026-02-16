# 🔒 Secure Node Chat

A high-security, private chat room with a modern **Glassmorphism** UI. Built for users who need a quick, encrypted-session communication hub that leaves no trace.

---

## ✨ Features

* **Zero-Config Security**: No hardcoded credentials. Set your username and password via terminal at runtime.
* **Stealth Entrance**: The login page is hidden behind a secret URL path of your choice.
* **Modern UI**: Beautiful dark-mode interface using Tailwind CSS with frosted-glass effects.
* **Identity Lock**: Choose your chat nickname at the login screen.
* **Session Purge**: The "EXIT" button clears all session cookies immediately.
* **Persistent Logs**: Messages are saved to a local `chat_history.json` file.

---

## 🚀 Installation & Setup

### **Express Setup (Ubuntu/Debian)**
If you are on an Ubuntu server, you can install everything and start the chat with this one-liner:

**For accessing go to: http://IPADDRASS:2626/YourPanelSecretURL

```bash
git clone https://github.com/salmankazerounitimsar-ux/Secure-Local-Chat-For-Ubuntu.git && cd Secure-Local-Chat-For-Ubuntu && bash setup.sh

