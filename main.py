import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
from tkinter import ttk
SCROLLBAR_WIDTH = 12  # Approx 1 terminal column


class BotballGUI(tk.Tk):
.text_color,
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
