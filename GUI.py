import tkinter as tk
from tkinter import messagebox


def input_gui():

    root = tk.Tk()
    root.title("Input Saver")

    entry = tk.Entry(root, width=40)
    entry.pack(padx=10, pady=10)

    save_button = tk.Button(root, text="Save", command=lambda: root.quit())
    save_button.pack(padx=10, pady=10)

    root.mainloop()

    user_input = entry.get()

    if user_input == "":
        messagebox.showerror("Error", "Input cannot be empty")
        root.destroy()
        input_gui()

    return user_input