import tkinter as tk
from generator import generate_password
from basic_cracker import demo as basic_demo
from advanced_cracker import demo as advanced_demo

sample_password = "Zac1"
print(f"Sample Password for Demo: {sample_password}\n")
basic_demo(sample_password)
advanced_demo(sample_password)

password = generate_password(4, True, True, True, False) # no special chars
print(f"\nGenerated Password: {password}\n")
basic_demo(password)
advanced_demo(password)