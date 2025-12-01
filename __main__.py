import tkinter as tk
from tkinter import scrolledtext
from generator import generate_password
from basic_cracker import demo as basic_demo
from advanced_cracker import demo as advanced_demo


# ----------- PAGE MANAGER -----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Security Demo")
        self.geometry("600x450")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for Page in (MainMenu, GeneratorPage, BasicCrackerPage, AdvancedCrackerPage):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show(MainMenu)

    def show(self, page):
        frame = self.frames[page]
        frame.tkraise()


# ----------- MAIN MENU PAGE -----------
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Password Security Demonstration",
                 font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(self, text="Password Generator",
                  font=("Arial", 14),
                  width=25,
                  command=lambda: controller.show(GeneratorPage)).pack(pady=10)

        tk.Button(self, text="Basic Cracker Demo",
                  font=("Arial", 14),
                  width=25,
                  command=lambda: controller.show(BasicCrackerPage)).pack(pady=10)

        tk.Button(self, text="Advanced Cracker Demo",
                  font=("Arial", 14),
                  width=25,
                  command=lambda: controller.show(AdvancedCrackerPage)).pack(pady=10)

        tk.Button(self, text="Exit", font=("Arial", 14),
                  width=25, command=controller.destroy).pack(pady=20)


# ----------- PASSWORD GENERATOR PAGE -----------
class GeneratorPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Password Generator", font=("Arial", 18, "bold")).pack(pady=10)

        # Settings Frame
        settings = tk.Frame(self)
        settings.pack(pady=10)

        self.length = tk.Scale(settings, from_=4, to=64, orient=tk.HORIZONTAL,
                               label="Length", length=300)
        self.length.set(12)
        self.length.grid(row=0, column=0, columnspan=4, pady=5)

        self.lower = tk.IntVar(value=1)
        self.upper = tk.IntVar(value=1)
        self.nums = tk.IntVar(value=1)
        self.special = tk.IntVar(value=1)

        tk.Checkbutton(settings, text="Lowercase", variable=self.lower).grid(row=1, column=0)
        tk.Checkbutton(settings, text="Uppercase", variable=self.upper).grid(row=1, column=1)
        tk.Checkbutton(settings, text="Numbers", variable=self.nums).grid(row=1, column=2)
        tk.Checkbutton(settings, text="Special", variable=self.special).grid(row=1, column=3)

        tk.Button(self, text="Generate", font=("Arial", 14),
                  command=self.do_generate).pack(pady=10)

        self.output = tk.Text(self, height=2, width=40, state=tk.DISABLED)
        self.output.pack()

        tk.Button(self, text="Back", command=lambda: controller.show(MainMenu)).pack(pady=20)

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


# ----------- BASIC CRACKER PAGE -----------
class BasicCrackerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Basic Password Cracker", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self, text="Enter password to demonstrate cracking:").pack()
        self.entry = tk.Entry(self, font=("Arial", 14))
        self.entry.pack(pady=5)

        tk.Button(self, text="Run Demo", font=("Arial", 14),
                  command=self.run_demo).pack(pady=10)

        self.log = scrolledtext.ScrolledText(self, width=70, height=15)
        self.log.pack()

        tk.Button(self, text="Back",
                  command=lambda: controller.show(MainMenu)).pack(pady=20)

    def run_demo(self):
        pwd = self.entry.get().strip()
        self.log.delete(1.0, tk.END)

        if not pwd:
            self.log.insert(tk.END, "Please enter a password.\n")
            return

        # Capture print output
        import io, sys
        buffer = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buffer

        basic_demo(pwd)

        sys.stdout = old_stdout
        self.log.insert(tk.END, buffer.getvalue())


# ----------- ADVANCED CRACKER PAGE -----------
class AdvancedCrackerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Advanced Cracker Demo", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self, text="Enter password to analyze & crack:").pack()
        self.entry = tk.Entry(self, font=("Arial", 14))
        self.entry.pack(pady=5)

        tk.Button(self, text="Run Demo", font=("Arial", 14),
                  command=self.run_demo).pack(pady=10)

        self.log = scrolledtext.ScrolledText(self, width=70, height=15)
        self.log.pack()

        tk.Button(self, text="Back",
                  command=lambda: controller.show(MainMenu)).pack(pady=20)

    def run_demo(self):
        pwd = self.entry.get().strip()
        self.log.delete(1.0, tk.END)

        if not pwd:
            self.log.insert(tk.END, "Enter a password first.\n")
            return

        import io, sys
        buffer = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buffer

        advanced_demo(pwd)

        sys.stdout = old_stdout
        self.log.insert(tk.END, buffer.getvalue())


# ----------- RUN APP -----------
if __name__ == "__main__":
    App().mainloop()
