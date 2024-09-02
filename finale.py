import tkinter as tk
from tkinter import messagebox
import webbrowser
import os

def play_video():
    # Path to the video file
    video_path = "your_video.mp4"

    # Open the video file using the default player
    if os.path.exists(video_path):
        webbrowser.open(video_path)
    else:
        messagebox.showerror("Error", "Video file not found!")

def check_password():
    user_input = entry.get()
    if user_input == correct_password:
        root.destroy()  # Close the pop-up
        #play_video()  # Play the video
    else:
        messagebox.showerror("Access Denied", "Incorrect password, intruder detected!")

# Correct password
correct_password = "M4rtySh4w"

# Create the main window
root = tk.Tk()
root.title("Spy Access Panel")
root.geometry("300x150")
root.configure(bg="black")

# Spy-themed label
label = tk.Label(root, text="Enter Secret Code:", font=("Courier", 14), fg="lime", bg="black")
label.pack(pady=10)

# Entry field for password
entry = tk.Entry(root, font=("Courier", 14), show="*", fg="lime", bg="black")
entry.pack(pady=10)

# Submit button
button = tk.Button(root, text="Enter", font=("Courier", 14), command=check_password, fg="lime", bg="black")
button.pack(pady=10)

# Start the GUI loop
root.mainloop()
