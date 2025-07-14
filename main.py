import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
from tkinter import ttk

import os
import signal
import glob
import sys

sys.path.append("/usr/lib")
import _kipr as k

# === Default Color Theme ===
TEXT_COLOR = "#00FFAA"
BG_COLOR = "black"

PROGRAM_BASE_PATH = "/home/kipr/Documents/KISS/Default User"
TERMINAL_WIDTH = 772  # 81 * 12
TERMINAL_HEIGHT = 384  # 24 * 16
SCROLLBAR_WIDTH = 12  # Approx 1 terminal column


class BotballGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # âœ… Initialize colors before anything else
        self.text_color = TEXT_COLOR
        self.bg_color = BG_COLOR

        self.update_colors_loop()

        self.attributes('-fullscreen', True)
        self.configure(bg=self.bg_color)

        try:
            serial_output = subprocess.check_output(
                ["/home/kipr/wombat-os/flashFiles/wallaby_get_serial.sh"],
                text=True
            ).strip()
            self.title(f"NovaUI: {serial_output}-wombat")
        except Exception as e:
            self.title("NovaUI: Unknown Wombat")
            print(f"[ERROR] Failed to get serial: {e}")

        self.geometry(f"{TERMINAL_WIDTH}x{TERMINAL_HEIGHT}")
        self.current_program_path = None
        self.process = None
        self.main_menu()

    def shutdown(self):
        os.system("sudo shutdown now")

    def refresh_colors(self):
        def recolor(widget):
            try:
                widget_type = widget.winfo_class()
                if widget_type in ["Label", "Button", "Frame", "TFrame", "Canvas", "TLabel", "TButton"]:
                    widget.configure(bg=self.bg_color)
                if widget_type in ["Label", "Button", "TLabel", "TButton"]:
                    widget.configure(
                        fg=self.text_color,
                        highlightbackground=self.text_color,
                        highlightcolor=self.text_color
                    )
                if isinstance(widget, scrolledtext.ScrolledText):
                    widget.configure(
                        bg=self.bg_color,
                        fg=self.text_color,
                        insertbackground=self.text_color
                    )
            except Exception as e:
                print(f"[DEBUG] Failed to recolor {widget}: {e}")
            for child in widget.winfo_children():
                recolor(child)

        recolor(self)


    def update_colors_loop(self):
        # Read and sum gyro values
        gyro_value = k.accel_z() * 2.25#k.gyro_x() + k.gyro_y() + k.gyro_z()
        #print(str(gyro_value))

        # Clamp to Â±1000
        gyro_value = max(-1000, min(1000, gyro_value))

        # Map to 0â€“255
        normalized = int((gyro_value + 1000) / 2000 * 255)

        # Pick a green-blue gradient (adjust mode below)
        # Mode 1: green only
        #r, g, b = 0, normalized, 0

        # Mode 2: blue only
        # r, g, b = 0, 0, normalized

        # Mode 3: green to cyan
        r, g, b = 0, normalized, 255 - normalized

        hex_color = f"#{r:02x}{g:02x}{b:02x}"

        self.text_color = hex_color
        self.refresh_colors()

        self.after(10, self.update_colors_loop)


    def main_menu(self):
        self.clear_window()
        self.configure(bg=self.bg_color)
        try:
            serial_output = subprocess.check_output(
                ["/home/kipr/wombat-os/flashFiles/wallaby_get_serial.sh"],
                text=True
            ).strip()
            tk.Label(self, text=f"NovaUI: {serial_output}-wombat", font=("Helvetica", 16),
                     bg=self.bg_color, fg=self.text_color).pack(pady=10)
        except Exception as e:
            tk.Label(self, text="NovaUI: Unknown Wombat", font=("Helvetica", 16),
                     bg=self.bg_color, fg=self.text_color).pack(pady=10)
            print(f"[ERROR] Failed to get serial: {e}")

        top_right_frame = tk.Frame(self, bg=self.bg_color)
        top_right_frame.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)
        tk.Button(top_right_frame, text="Exit UI", font=("Helvetica", 12),
                  bg=self.bg_color, fg=self.text_color, highlightbackground=self.text_color,
                  command=self.destroy).pack(side=tk.LEFT, padx=5)
        tk.Button(top_right_frame, text="Shutdown Controller", font=("Helvetica", 12),
                  bg=self.bg_color, fg=self.text_color, highlightbackground=self.text_color,
                  command=self.shutdown).pack(side=tk.LEFT, padx=5)

        canvas_frame = tk.Frame(self, bg=self.bg_color)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        canvas = tk.Canvas(canvas_frame, bg=self.bg_color, highlightthickness=0)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background=self.text_color,
                        darkcolor=self.text_color,
                        lightcolor=self.text_color,
                        troughcolor=self.bg_color,
                        bordercolor=self.text_color,
                        arrowcolor=self.text_color,
                        relief="flat")

        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", style="Vertical.TScrollbar", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner_frame = tk.Frame(canvas, bg=self.bg_color)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", on_configure)

        programs = glob.glob(os.path.join(PROGRAM_BASE_PATH, "*/bin/botball_user_program"))
        if not programs:
            tk.Label(inner_frame, text="No programs found.", font=("Helvetica", 12),
                     bg=self.bg_color, fg=self.text_color).pack(pady=20)
            return

        button_width_chars = 30
        for full_path in programs:
            program_dir = os.path.basename(os.path.dirname(os.path.dirname(full_path)))
            btn = tk.Button(
                inner_frame, text=program_dir, font=("Helvetica", 14),
                width=button_width_chars,
                bg=self.bg_color, fg=self.text_color, highlightbackground=self.text_color,
                command=lambda p=full_path, n=program_dir: self.launch_program_ui(p, n)
            )
            btn.pack(pady=3, anchor="w", padx=5)

    def launch_program_ui(self, path, name):
        self.current_program_path = path
        self.clear_window()
        self.configure(bg=self.bg_color)

        btn_frame = tk.Frame(self, bg=self.bg_color)
        btn_frame.pack(side=tk.TOP, fill=tk.X, pady=4)

        tk.Label(btn_frame, bg=self.bg_color, fg=self.text_color,
                 text=f"Program: {name}", font=("Helvetica", 14)).pack(side=tk.LEFT, padx=10)

        self.run_btn = tk.Button(btn_frame, text="Run", font=("Helvetica", 14),
                                 bg=self.bg_color, fg=self.text_color, highlightbackground=self.text_color,
                                 command=self.start_process)
        self.run_btn.pack(side=tk.LEFT, padx=10)

        self.stop_btn = tk.Button(btn_frame, text="Stop", font=("Helvetica", 14),
                                  bg=self.bg_color, fg=self.text_color, highlightbackground=self.text_color,
                                  command=self.stop_process)
        self.stop_btn.pack(side=tk.LEFT, padx=10)

        self.exit_btn = tk.Button(btn_frame, text="Exit", font=("Helvetica", 14),
                                  bg=self.bg_color, fg=self.text_color, highlightbackground=self.text_color,
                                  command=self.return_to_menu)
        self.exit_btn.pack(side=tk.RIGHT, padx=10)

        self.output_box = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, height=18, font=("Courier", 10),
            bg=self.bg_color, fg=self.text_color, insertbackground=self.text_color
        )
        self.output_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(4, 10))

    def start_process(self):
        if self.process and self.process.poll() is None:
            self.log_output("Process already running.\n")
            return

        def run():
            try:
                self.process = subprocess.Popen(
                    [self.current_program_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    preexec_fn=os.setsid
                )
                for line in self.process.stdout:
                    self.log_output(line)
            except Exception as e:
                self.log_output(f"[ERROR] {str(e)}\n")

        threading.Thread(target=run, daemon=True).start()

    def stop_process(self):
        if self.process and self.process.poll() is None:
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                self.log_output("[INFO] Process terminated.\n")
            except Exception as e:
                self.log_output(f"[ERROR] Failed to stop process: {str(e)}\n")
        else:
            self.log_output("[INFO] No running process.\n")

    def return_to_menu(self):
        self.stop_process()
        self.current_program_path = None
        self.main_menu()

    def log_output(self, text):
        self.output_box.insert(tk.END, text)
        self.output_box.see(tk.END)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg=self.bg_color)


if __name__ == "__main__":
    app = BotballGUI()
    app.mainloop()
