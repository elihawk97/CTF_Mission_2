import tkinter as tk
from tkinter import messagebox

# Preprogrammed correct location name
correct_name = "Hanoi"

# Check if the user-entered name is correct
def check_name():
    user_name = name_entry.get()

    if user_name.strip().lower() == correct_name.lower():
        messagebox.showinfo("Result", "Congratulations! You have won!")
    else:
        messagebox.showerror("Error", "Wrong name! Please try again.")

# Create the main window
window = tk.Tk()
window.title("Location Name Checker")

# Create and place widgets
tk.Label(window, text="Enter the location name:").pack(pady=10)
name_entry = tk.Entry(window, width=50)
name_entry.pack(pady=5)
tk.Button(window, text="Submit", command=check_name).pack(pady=20)

# Start the GUI event loop
window.mainloop()
