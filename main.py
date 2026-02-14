import tkinter as tk
from tkinter import ttk, messagebox
import math


import tkinter as tk
from tkinter import ttk, messagebox
import math


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control Panel")
        self.geometry("900x600")
        self.configure(bg="#121826")

        self.history = []
        self.current_page = None

        style = ttk.Style(self)
        style.theme_use("clam")

        ACCENT = "#00c8ff"
        DARK = "#121826"
        BTN_BG = "#1b2333"
        BTN_HOVER = "#163a4d"

        style.configure("TFrame", background=DARK)
        style.configure("TLabel", background=DARK,
                        foreground="white", font=("Arial", 14))

        style.configure("Menu.TButton",
                        font=("Arial", 16),
                        padding=10,
                        background=BTN_BG,
                        foreground="white",
                        borderwidth=2)

        style.map("Menu.TButton",
                  background=[("active", BTN_HOVER)],
                  bordercolor=[("!active", ACCENT)])

        style.configure("Small.TButton",
                        font=("Arial", 12),
                        padding=6,
                        background=BTN_BG,
                        foreground="white",
                        borderwidth=2)

        style.map("Small.TButton",
                  background=[("active", BTN_HOVER)],
                  bordercolor=[("!active", ACCENT)])

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages = (
            MainMenu,
            ProgramsMenu,
            SettingsMenu,
            MotorsSensorsMenu,
            NetworkMenu,
            ServosMenu,
            MotorsMenu,
            SensorsMenu,
            AboutMenu,
        )

        for Page in pages:
            frame = Page(container, self)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu", add_history=False)

    def show_frame(self, name, add_history=True):
        if self.current_page and add_history:
            self.history.append(self.current_page)

        self.current_page = name
        self.frames[name].tkraise()

    def go_back(self):
        if self.history:
            prev = self.history.pop()
            self.current_page = prev
            self.frames[prev].tkraise()

    def reboot_prompt(self):
        if messagebox.askyesno("Reboot", "Reboot system?"):
            print("Reboot placeholder")

    def shutdown_prompt(self):
        if messagebox.askyesno("Shutdown", "Shutdown system?"):
            self.destroy()


# =========================
# Base Page Layout
# =========================
class BasePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Top bar
        self.topbar = ttk.Frame(self)
        self.topbar.grid(row=0, column=0, sticky="ew")

        self.topbar.grid_columnconfigure(0, weight=1)

        self.topbar_center = ttk.Frame(self.topbar)
        self.topbar_center.grid(row=0, column=0)

        self.back_btn = ttk.Button(
            self.topbar_center,
            text="← Back",
            style="Small.TButton",
            command=controller.go_back
        )
        self.back_btn.pack(side="left", padx=8, pady=10)

        # Content
        self.content = ttk.Frame(self)
        self.content.grid(row=1, column=0, sticky="nsew")

    def hide_back(self):
        self.back_btn.pack_forget()



# =========================
# Centered Template
# =========================
class CenteredPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.center = ttk.Frame(self.content)
        self.center.grid(row=0, column=0)


# =========================
# Main Menu
# =========================
class MainMenu(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.hide_back()

        ttk.Button(self.topbar_center, text="About",
                   style="Small.TButton",
                   command=lambda: controller.show_frame("AboutMenu")
                   ).pack(side="left", padx=8)

        ttk.Button(self.topbar_center, text="Reboot",
                   style="Small.TButton",
                   command=controller.reboot_prompt
                   ).pack(side="left", padx=8)

        ttk.Button(self.topbar_center, text="Shutdown",
                   style="Small.TButton",
                   command=controller.shutdown_prompt
                   ).pack(side="left", padx=8)

        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        center = ttk.Frame(self.content)
        center.grid(row=0, column=0)

        for text, target in [
            ("Programs", "ProgramsMenu"),
            ("Motors & Sensors", "MotorsSensorsMenu"),
            ("Settings", "SettingsMenu"),
        ]:
            ttk.Button(center,
                       text=text,
                       width=25,
                       style="Menu.TButton",
                       command=lambda t=target: controller.show_frame(t)
                       ).pack(pady=15)


# Remaining classes unchanged (ProgramsMenu, SettingsMenu, NetworkMenu,
# MotorsSensorsMenu, ServosMenu, MotorsMenu, SensorsMenu, AboutMenu)
# You can keep them exactly as in the previous version.




# =========================
# Simple Center Pages
# =========================
class ProgramsMenu(CenteredPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        ttk.Label(self.center, text="Programs Placeholder").pack()


class SettingsMenu(CenteredPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ttk.Button(self.center, text="Network",
                   width=20,
                   style="Menu.TButton",
                   command=lambda: controller.show_frame("NetworkMenu")
                   ).pack(pady=10)

        ttk.Button(self.center, text="GUI",
                   width=20,
                   style="Menu.TButton").pack(pady=10)

        ttk.Button(self.center, text="Hide UI",
                   width=20,
                   style="Menu.TButton",
                   command=controller.iconify).pack(pady=10)


class NetworkMenu(CenteredPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        mode = tk.StringVar(value="AP")

        ttk.Radiobutton(self.center, text="AP Mode",
                        variable=mode, value="AP").pack(pady=5)

        ttk.Radiobutton(self.center, text="Client Mode",
                        variable=mode, value="Client").pack(pady=5)


class MotorsSensorsMenu(CenteredPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ttk.Button(self.center, text="Servos",
                   width=20,
                   style="Menu.TButton",
                   command=lambda: controller.show_frame("ServosMenu")
                   ).pack(pady=10)

        ttk.Button(self.center, text="Motors",
                   width=20,
                   style="Menu.TButton",
                   command=lambda: controller.show_frame("MotorsMenu")
                   ).pack(pady=10)

        ttk.Button(self.center, text="Sensors",
                   width=20,
                   style="Menu.TButton",
                   command=lambda: controller.show_frame("SensorsMenu")
                   ).pack(pady=10)


# =========================
# Servo Dial (Fixed)
# =========================
class ServosMenu(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        layout = ttk.Frame(self.content)
        layout.grid(row=0, column=0)

        self.active_servo = tk.IntVar(value=0)

        btns = ttk.Frame(layout)
        btns.pack(pady=10)

        for i in range(4):
            ttk.Radiobutton(btns, text=f"Servo {i}",
                            variable=self.active_servo,
                            value=i).pack(side="left", padx=10)

        self.canvas = tk.Canvas(layout, width=300, height=300,
                                bg="#121826", highlightthickness=0)
        self.canvas.pack()

        self.angle = 0
        self.draw_dial()

        self.canvas.bind("<B1-Motion>", self.update_dial)

    def draw_dial(self):
        self.canvas.delete("all")

        cx, cy = 150, 150
        r = 110

        # Arc
        self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r,
                               start=40, extent=200,
                               style="arc", outline="#00c8ff", width=3)

        # Min/Max markers
        for deg in (-100, 100):
            rad = math.radians(deg)
            x = cx + r * math.cos(rad)
            y = cy - r * math.sin(rad)
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="#00c8ff")

        # Needle
        rad = math.radians(self.angle - 100)
        x = cx + 90 * math.cos(rad)
        y = cy - 90 * math.sin(rad)
        self.canvas.create_line(cx, cy, x, y, fill="#00c8ff", width=4)

    def update_dial(self, event):
        cx, cy = 150, 150
        dx = event.x - cx
        dy = cy - event.y

        angle = math.degrees(math.atan2(dy, dx))
        angle = max(-100, min(100, angle))

        self.angle = angle + 100
        self.draw_dial()

        value = int((self.angle / 200) * 2047)
        value = max(0, min(2047, value))

        print(f"Servo {self.active_servo.get()} → {value}")


# =========================
# Motors
# =========================
class MotorsMenu(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        layout = ttk.Frame(self.content)
        layout.grid(row=0, column=0)

        self.active_motor = tk.IntVar(value=0)

        btns = ttk.Frame(layout)
        btns.pack(pady=10)

        for i in range(4):
            ttk.Radiobutton(btns, text=f"Motor {i}",
                            variable=self.active_motor,
                            value=i).pack(side="left", padx=10)

        ttk.Scale(layout,
                  from_=-1500,
                  to=1500,
                  length=400,
                  command=self.on_change).pack(pady=20)

    def on_change(self, val):
        print(f"Motor {self.active_motor.get()} → {int(float(val))}")


class SensorsMenu(CenteredPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        ttk.Label(self.center, text="Sensors Placeholder").pack()


class AboutMenu(CenteredPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        ttk.Label(self.center, text="Control Interface v1.0").pack()


# =========================
if __name__ == "__main__":
    app = App()
    app.mainloop()
