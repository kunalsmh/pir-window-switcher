import threading
import time
import os
import subprocess
from flask import Flask
import pystray
import PIL.Image
from pystray import MenuItem as item
import win32gui
import win32con

# ---------------- Paths ----------------
script_dir = os.path.dirname(os.path.realpath(__file__))
icon_path = os.path.join(script_dir, "icon.png")
pdf_path = r"C:\Users\Kunal\Downloads\physics.pdf"

# ---------------- Setup ----------------
image = PIL.Image.open(icon_path)
app = Flask(__name__)
last_open_time = 0
COOLDOWN = 1  # seconds

def log(msg):
    print(msg)

# ---------------- PDF Handling ----------------
def open_pdf_and_minimize_others(path):
    # Open PDF
    subprocess.Popen(['start', '', path], shell=True)
    time.sleep(1)  # give it time to open

    # Get the handle of the PDF window
    def get_pdf_hwnd(hwnd, extra):
        title = win32gui.GetWindowText(hwnd)
        if os.path.basename(path) in title:
            extra.append(hwnd)
    pdf_windows = []
    win32gui.EnumWindows(get_pdf_hwnd, pdf_windows)

    # Minimize all other visible windows
    def minimize_others(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd) and hwnd not in pdf_windows:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    win32gui.EnumWindows(minimize_others, None)

    log("PDF opened, all other windows minimized")

def open_pdf(path):
    threading.Thread(target=open_pdf_and_minimize_others, args=(path,), daemon=True).start()

# ---------------- Flask Routes ----------------
@app.route('/motion', methods=['GET', 'POST'])
def motion():
    global last_open_time
    now = time.time()
    if now - last_open_time >= COOLDOWN:
        if os.path.exists(pdf_path):
            open_pdf(pdf_path)
        else:
            log("PDF not found")
        last_open_time = now
    return "OK", 200

@app.route('/ping', methods=['GET'])
def ping():
    log("Ping received")
    return "Pong", 200

# ---------------- Flask Thread ----------------
def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# ---------------- System Tray ----------------
def on_quit(icon, item):
    log("Exiting")
    os._exit(0)

menu = pystray.Menu(item("Quit", on_quit))
icon = pystray.Icon("motion_eyes", image, menu=menu)

# ---------------- Main ----------------
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    icon.run()
