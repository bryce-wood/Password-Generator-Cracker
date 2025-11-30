import tkinter as tk
from generator import generate_password
from basic_cracker import demo as basic_demo
from advanced_cracker import demo as advanced_demo

def generate():
    if not (have_lower.get() or have_upper.get() or have_nums.get() or have_special.get()):
        password_display.config(state=tk.NORMAL)
        password_display.delete(1.0, tk.END)
        password_display.insert(tk.END, "Select at least one character type.")
        password_display.config(state=tk.DISABLED)
        return "Select at least one character type."
    password = generate_password(
        length=character_slider.get(),
        include_lower=bool(have_lower.get()),
        include_upper=bool(have_upper.get()),
        include_nums=bool(have_nums.get()),
        include_special=bool(have_special.get())
    )
    password_display.config(state=tk.NORMAL)
    password_display.delete(1.0, tk.END)
    password_display.insert(tk.END, password)
    password_display.config(state=tk.DISABLED)
    return password

window = tk.Tk()
window.geometry("400x300")
window.title("Password Generator")

generator_frame = tk.Frame(window)
generator_frame.grid(row=0, column=0, padx=10, pady=10)

character_slider = tk.Scale(generator_frame, from_=4, to=64, orient=tk.HORIZONTAL, label="Password Length")
character_slider.set(12)
character_slider.grid(row=0, column=0, padx=20, pady=5, sticky="ew")

checkbox_frame = tk.Frame(generator_frame)
checkbox_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

lower_label = tk.Label(checkbox_frame, text="Include Lower\n(e.g. a,b,c)")
lower_label.grid(row=0, column=0, sticky="ew")
have_lower = tk.IntVar(value=1)
lower_check = tk.Checkbutton(checkbox_frame, variable=have_lower)
lower_check.grid(row=1, column=0, sticky="ew")

upper_label = tk.Label(checkbox_frame, text="Include Upper\n(e.g. A,B,C)")
upper_label.grid(row=0, column=1, sticky="ew")
have_upper = tk.IntVar(value=1)
upper_check = tk.Checkbutton(checkbox_frame, variable=have_upper)
upper_check.grid(row=1, column=1, sticky="ew")

nums_label = tk.Label(checkbox_frame, text="Include Nums\n(e.g. 1,2,3)")
nums_label.grid(row=0, column=2, sticky="ew")
have_nums = tk.IntVar(value=1)
nums_check = tk.Checkbutton(checkbox_frame, variable=have_nums)
nums_check.grid(row=1, column=2, sticky="ew")

special_label = tk.Label(checkbox_frame, text="Include Special\n(e.g. !,@,#)")
special_label.grid(row=0, column=3, sticky="ew")
have_special = tk.IntVar(value=1)
special_check = tk.Checkbutton(checkbox_frame, variable=have_special)
special_check.grid(row=1, column=3, sticky="ew")

generate_button = tk.Button(generator_frame, text="Generate Password", command=generate)
generate_button.grid(row=2, column=0, padx=40, pady=5, sticky="ew")

password_display = tk.Text(generator_frame, height=2, width=32, state=tk.DISABLED)
password_display.grid(row=3, column=0, sticky="ew")


window.mainloop()

"""
sample_password = "Zac1"
print(f"Sample Password for Demo: {sample_password}\n")
basic_demo(sample_password)
advanced_demo(sample_password)

password = generate_password(4, True, True, True, False) # no special chars
print(f"\nGenerated Password: {password}\n")
basic_demo(password)
advanced_demo(password)
"""