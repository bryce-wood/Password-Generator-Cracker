import tkinter as tk
from generator import generate_password
from basic_cracker import demo as basic_demo
from advanced_cracker import demo as advanced_demo

def generate():
    password = generate_password(character_slider.get(), True, True, True, True)
    password_display.config(state=tk.NORMAL)
    password_display.delete(1.0, tk.END)
    password_display.insert(tk.END, password)
    password_display.config(state=tk.DISABLED)
    return password

window = tk.Tk()
window.geometry("300x200")
window.title("Password Generator")

generator_frame = tk.Frame(window)
generator_frame.grid(row=0, column=0, padx=10, pady=10)

character_slider = tk.Scale(generator_frame, from_=4, to=64, orient=tk.HORIZONTAL, label="Password Length")
character_slider.set(12)
character_slider.grid(row=0, column=0, padx=20, pady=5, sticky="ew")

generate_button = tk.Button(generator_frame, text="Generate Password", command=generate)
generate_button.grid(row=1, column=0, padx=30, pady=5, sticky="ew")

password_display = tk.Text(generator_frame, height=2, width=32, state=tk.DISABLED)
password_display.grid(row=2, column=0, sticky="ew")


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