import tkinter as tk
from tkinter import scrolledtext
from generator import generate_password
from basic_cracker import demo as basic_demo
from advanced_cracker import demo as advanced_demo


# Global colors/styles
BG = "#f0f2f5"
CARD_BG = "#ffffff"
ACCENT = "#3b82f6"
ACCENT_HOVER = "#2563eb"
TEXT = "#1f2937"


def style_button(btn):
    """Apply modern styling & hover behavior to a Tkinter button."""
    btn.config(
        bg=ACCENT,
        fg="black",
        activebackground=ACCENT_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=10,
        pady=6,
        font=("Segoe UI", 12, "bold")
    )
    # Hover effects
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))

def style_clear_button(btn):
    btn.config(
        bg="#e5e7eb",
        fg="#111827",
        activebackground="#d1d5db",
        activeforeground="#111827",
        relief="flat",
        bd=0,
        padx=10,
        pady=6,
        font=("Segoe UI", 12, "bold")
    )


def create_card(parent):
    """A styled card-like frame used to group page contents."""
    frame = tk.Frame(parent, bg=CARD_BG, bd=1, relief="solid")
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    return frame


# ---------------------------------
# MAIN APP
# ---------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Security Demo")
        self.geometry("700x550")
        self.configure(bg=BG)

        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for Page in (MainMenu, GeneratorPage, BasicCrackerPage, AdvancedCrackerPage):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show(MainMenu)

    def show(self, page):
        self.frames[page].tkraise()


# ---------------------------------
# MAIN MENU PAGE
# ---------------------------------
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        card = create_card(self)

        title = tk.Label(card, text="Password Security Demonstration",
                         font=("Segoe UI", 20, "bold"), bg=CARD_BG, fg=TEXT)
        title.pack(pady=20)

        # Buttons
        btn_gen = tk.Button(card, text="Password Generator",
                            command=lambda: controller.show(GeneratorPage))
        btn_basic = tk.Button(card, text="Basic Cracker Demo",
                              command=lambda: controller.show(BasicCrackerPage))
        btn_adv = tk.Button(card, text="Advanced Cracker Demo",
                            command=lambda: controller.show(AdvancedCrackerPage))
        btn_exit = tk.Button(card, text="Exit", command=controller.destroy)

        for b in (btn_gen, btn_basic, btn_adv, btn_exit):
            style_button(b)
            b.pack(pady=10, ipadx=20)


# ---------------------------------
# PASSWORD GENERATOR PAGE
# ---------------------------------
class GeneratorPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        card = create_card(self)

        tk.Label(card, text="Password Generator",
                 font=("Segoe UI", 18, "bold"), bg=CARD_BG, fg=TEXT).pack(pady=10)

        settings = tk.Frame(card, bg=CARD_BG)
        settings.pack(pady=10)

        self.length = tk.Scale(
            settings, from_=4, to=64, orient=tk.HORIZONTAL,
            label="Length", length=300, bg=CARD_BG, foreground=TEXT
        )
        self.length.set(12)
        self.length.grid(row=0, column=0, columnspan=4, pady=5)

        self.lower = tk.IntVar(value=1)
        self.upper = tk.IntVar(value=1)
        self.nums = tk.IntVar(value=1)
        self.special = tk.IntVar(value=1)

        boxes = [
            ("Lowercase", self.lower),
            ("Uppercase", self.upper),
            ("Numbers", self.nums),
            ("Special", self.special)
        ]

        for i, (label, var) in enumerate(boxes):
            tk.Checkbutton(settings, text=label, variable=var,
                           bg=CARD_BG, fg=TEXT, selectcolor=CARD_BG).grid(row=1, column=i, padx=5)

        btn_gen = tk.Button(card, text="Generate", command=self.do_generate)
        style_button(btn_gen)
        btn_gen.pack(pady=10)

        self.output = tk.Text(card, height=2, width=50, state=tk.DISABLED, font=("Consolas", 12))
        self.output.pack(pady=10)

        btn_clear = tk.Button(card, text="Clear", command=self.clear_output)
        style_clear_button(btn_clear)
        btn_clear.pack(pady=5)

        btn_back = tk.Button(card, text="Back", command=lambda: controller.show(MainMenu))
        style_button(btn_back)
        btn_back.pack(pady=10)

    def do_generate(self):
        if not (self.lower.get() or self.upper.get() or self.nums.get() or self.special.get()):
            self._show("Select at least one character type.")
            return

        pwd = generate_password(
            length=self.length.get(),
            include_lower=bool(self.lower.get()),
            include_upper=bool(self.upper.get()),
            include_nums=bool(self.nums.get()),
            include_special=bool(self.special.get())
        )
        self._show(pwd)

    def _show(self, text):
        self.output.config(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state=tk.DISABLED)

    def clear_output(self):
        self.output.config(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        self.output.config(state=tk.DISABLED)



# ---------------------------------
# BASIC CRACKER PAGE
# ---------------------------------
class BasicCrackerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        card = create_card(self)

        tk.Label(card, text="Basic Password Cracker",
                 font=("Segoe UI", 18, "bold"), bg=CARD_BG, fg=TEXT).pack(pady=10)

        tk.Label(card, text="Enter password:", bg=CARD_BG, fg=TEXT).pack()
        self.entry = tk.Entry(card, font=("Segoe UI", 14))
        self.entry.pack(pady=5)

        btn_run = tk.Button(card, text="Run Demo", command=self.run_demo)
        style_button(btn_run)
        btn_run.pack(pady=10)

        self.log = scrolledtext.ScrolledText(card, width=70, height=15, font=("Consolas", 11))
        self.log.pack(pady=10)

        btn_clear = tk.Button(card, text="Clear", command=self.clear_fields)
        style_clear_button(btn_clear)
        btn_clear.pack(pady=5)


        btn_back = tk.Button(card, text="Back", command=lambda: controller.show(MainMenu))
        style_button(btn_back)
        btn_back.pack(pady=10)

    def run_demo(self):
        pwd = self.entry.get().strip()
        self.log.delete(1.0, tk.END)

        if not pwd:
            self.log.insert(tk.END, "Please enter a password.\n")
            return
        
        # Capture print output
        import io, sys
        buffer = io.StringIO()
        old = sys.stdout
        sys.stdout = buffer

        basic_demo(pwd)

        sys.stdout = old
        self.log.insert(tk.END, buffer.getvalue())

    def clear_fields(self):
        self.entry.delete(0, tk.END)
        self.log.delete(1.0, tk.END)



# ---------------------------------
# ADVANCED CRACKER PAGE
# ---------------------------------
class AdvancedCrackerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        card = create_card(self)

        tk.Label(card, text="Advanced Password Cracker",
                 font=("Segoe UI", 18, "bold"), bg=CARD_BG, fg=TEXT).pack(pady=10)

        tk.Label(card, text="Enter password:", bg=CARD_BG, fg=TEXT).pack()
        self.entry = tk.Entry(card, font=("Segoe UI", 14))
        self.entry.pack(pady=5)

        btn_run = tk.Button(card, text="Run Demo", command=self.run_demo)
        style_button(btn_run)
        btn_run.pack(pady=10)

        self.log = scrolledtext.ScrolledText(card, width=70, height=15, font=("Consolas", 11))
        self.log.pack(pady=10)

        btn_clear = tk.Button(card, text="Clear", command=self.clear_fields)
        style_clear_button(btn_clear)
        btn_clear.pack(pady=5)

        btn_back = tk.Button(card, text="Back", command=lambda: controller.show(MainMenu))
        style_button(btn_back)
        btn_back.pack(pady=10)

    def run_demo(self):
        pwd = self.entry.get().strip()
        self.log.delete(1.0, tk.END)

        if not pwd:
            self.log.insert(tk.END, "Please enter a password.\n")
            return

        import io, sys
        buffer = io.StringIO()
        old = sys.stdout
        sys.stdout = buffer

        advanced_demo(pwd)

        sys.stdout = old
        self.log.insert(tk.END, buffer.getvalue())

    def clear_fields(self):
        self.entry.delete(0, tk.END)
        self.log.delete(1.0, tk.END)

# ---------------------------------
# RUN
# ---------------------------------
if __name__ == "__main__":
    App().mainloop()
