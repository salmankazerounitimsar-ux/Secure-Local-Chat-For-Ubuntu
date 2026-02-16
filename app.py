import json
import os
import secrets
import sys
from flask import Flask, render_template_string, request, jsonify, session, redirect

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# --- DYNAMIC CONFIGURATION ---
if len(sys.argv) < 4:
    print("\n" + "!"*50)
    print("ERROR: Missing arguments!")
    print("USAGE: python3 app.py <username> <password> <secret_url_path>")
    print("EXAMPLE: python3 app.py root pass123 my-private-chat")
    print("Go here: http://IPADDRESS:2626/YOUR_SECRET")
    print("!"*50 + "\n")
    sys.exit(1)

USER_DATA = {sys.argv[1]: sys.argv[2]}
SECRET_URL = sys.argv[3]
CHAT_FILE = "chat_history.json"

# --- DATA PERSISTENCE ---
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, 'w') as f: json.dump([], f)

def get_history():
    try:
        with open(CHAT_FILE, 'r') as f: return json.load(f)
    except: return []

def save_to_history(display_name, message):
    history = get_history()
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M")
    history.append({"name": display_name, "message": message, "time": timestamp})
    if len(history) > 100: history.pop(0)
    with open(CHAT_FILE, 'w') as f: json.dump(history, f)

# --- UI TEMPLATES ---
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Secure Entry</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;900&display=swap" rel="stylesheet">
    <style>
        body { background: #020617; font-family: 'Inter', sans-serif; }
        .glow { box-shadow: 0 0 20px rgba(59, 130, 246, 0.4); }
    </style>
</head>
<body class="h-screen flex flex-col items-center justify-center p-6 text-slate-300">
    <div class="w-full max-w-md bg-slate-900 border border-slate-800 p-10 rounded-[2.5rem] shadow-2xl">
        <div class="text-center mb-8">
            <h2 class="text-white text-3xl font-black tracking-tight">Secure Access</h2>
            <p class="text-blue-400 text-sm mt-2 font-medium italic">"Don't forget to click exit at the end"</p>
        </div>
        <form method="POST" class="space-y-4">
            <input type="text" name="u" placeholder="Admin Username" required autocomplete="off" class="w-full p-4 rounded-2xl bg-slate-800 text-white border border-slate-700 outline-none focus:border-blue-500 transition">
            <input type="password" name="p" placeholder="Password" required class="w-full p-4 rounded-2xl bg-slate-800 text-white border border-slate-700 outline-none focus:border-blue-500 transition">
            <input type="text" name="nickname" placeholder="Your Chat Nickname" required autocomplete="off" class="w-full p-4 rounded-2xl bg-slate-950 text-white border border-purple-900/50 outline-none focus:border-purple-500 transition">
            <button class="w-full bg-blue-600 text-white py-4 rounded-2xl font-bold hover:bg-blue-500 transition glow mt-6">Enter Chat Room</button>
        </form>
    </div>
</body>
</html>
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Node</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #0f172a; color: white; overflow: hidden; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); }
        .chat-scroll::-webkit-scrollbar { width: 4px; }
        .chat-scroll::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    </style>
</head>
<body class="h-screen flex flex-col items-center justify-center p-2 sm:p-4">
    <div class="w-full max-w-4xl h-[92vh] flex flex-col glass rounded-3xl shadow-2xl overflow-hidden">
        <div class="p-4 bg-slate-800/80 border-b border-slate-700 flex items-center justify-between">
            <div class="flex items-center gap-4">
                <div class="h-10 w-10 rounded-xl bg-blue-600 flex items-center justify-center font-black italic">S</div>
                <div>
                    <p class="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Identity Active</p>
                    <p class="text-sm font-bold text-blue-400">{{ session.nickname }}</p>
                </div>
            </div>
            <div class="flex items-center gap-6">
                <p class="hidden md:block text-[11px] font-medium text-slate-400 italic">"Don't forget to click exit at the end"</p>
                <a href="/logout" class="text-xs bg-red-500/10 hover:bg-red-500 text-red-500 hover:text-white px-5 py-2 rounded-xl transition-all border border-red-500/20 font-bold">EXIT</a>
            </div>
        </div>
        <div id="chat-box" class="flex-grow chat-scroll overflow-y-auto p-6 space-y-4 bg-slate-900/40"></div>
        <div class="p-6 bg-slate-800/40 border-t border-slate-700/50 flex gap-3">
            <input type="text" id="msg-input" placeholder="Type a message..." autocomplete="off" class="flex-grow bg-slate-950/50 border border-slate-700 rounded-2xl px-5 py-4 text-white focus:outline-none focus:border-blue-500/50 transition">
            <button onclick="send()" class="bg-blue-600 hover:bg-blue-500 text-white px-10 rounded-2xl font-black transition-all shadow-lg">SEND</button>
        </div>
    </div>
    <script>
        let lastCount = 0;
        const chatBox = document.getElementById('chat-box');
        const msgInput = document.getElementById('msg-input');
        async function fetchMsg() {
            try {
                const res = await fetch('/api/get');
                const data = await res.json();
                if (data.length !== lastCount) {
                    const myName = "{{ session.nickname }}";
                    chatBox.innerHTML = data.map(m => `
                        <div class="flex flex-col ${m.name === myName ? 'items-end' : 'items-start'}">
                            <div class="flex items-center gap-2 mb-1 mx-2">
                                <span class="text-[9px] text-slate-500 font-mono uppercase">${m.name}</span>
                                <span class="text-[8px] text-slate-600">${m.time || ''}</span>
                            </div>
                            <div class="max-w-[80%] px-5 py-3 rounded-2xl shadow-sm ${m.name === myName ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-slate-800 text-slate-200 border border-slate-700 rounded-tl-none'}">
                                ${m.message}
                            </div>
                        </div>
                    `).join('');
                    chatBox.scrollTop = chatBox.scrollHeight;
                    lastCount = data.length;
                }
            } catch (e) {}
        }
        async function send() {
            const msg = msgInput.value.trim();
            if (!msg) return;
            await fetch('/api/send', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message: msg}) });
            msgInput.value = ''; fetchMsg();
        }
        msgInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') send(); });
        setInterval(fetchMsg, 1500); fetchMsg();
    </script>
</body>
</html>
"""

@app.route(f'/{SECRET_URL}', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u, p = request.form.get('u'), request.form.get('p')
        nickname = request.form.get('nickname', 'User').strip()
        if USER_DATA.get(u) == p:
            session['user'] = u
            session['nickname'] = nickname[:15]
            return redirect('/chat')
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/chat')
def chat():
    if 'user' not in session: return redirect(f'/{SECRET_URL}')
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/get')
def get_messages():
    if 'user' not in session: return jsonify([]), 403
    return jsonify(get_history())

@app.route('/api/send', methods=['POST'])
def send():
    if 'user' not in session: return "Unauthorized", 403
    msg = request.json.get('message')
    if msg: save_to_history(session['nickname'], msg)
    return jsonify({"status": "ok"})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(f'/{SECRET_URL}')

@app.route('/')
def index(): return "404 Not Found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2626)
