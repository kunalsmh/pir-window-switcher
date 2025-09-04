import threading
import time
import os
import subprocess
from flask import Flask
import pystray
import PIL.Image
from pystray import MenuItem as item

script_dir = os.path.dirname(os.path.realpath(__file__))
icon_path = os.path.join(script_dir, "icon.png")
pdf_path = r"C:\Users\x\y\z.pdf" # Replace this with your file location

image = PIL.Image.open(icon_path)

app = Flask(__name__)
last_open_time = 0
COOLDOWN = 120

def log(msg):
    print(msg)

@app.route('/motion', methods=['GET', 'POST'])
def motion():
    global last_open_time
    current_time = time.time()

    if current_time - last_open_time >= COOLDOWN:
        log("Opening PDF now...")
        if os.path.exists(pdf_path):
            try:
                subprocess.Popen([pdf_path], shell=True)
                log(f"Opened {pdf_path}")
            except Exception as e:
                log(f"Error opening PDF: {e}")
        else:
            log(f"File not found: {pdf_path}")
        last_open_time = current_time
    else:
        remaining = int(COOLDOWN - (current_time - last_open_time))
        log(f"PDF opened recently. Wait {remaining} seconds.")

    return "Request received!", 200

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# ---------------- System Tray ----------------
def on_quit(icon, item):
    log("Exiting Web API")
    os._exit(0)

menu = pystray.Menu(item("Quit", on_quit))
icon = pystray.Icon("motion_eyes", image, menu=menu)

def start_tray():
    icon.run()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    start_tray()