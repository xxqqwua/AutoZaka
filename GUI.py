import tkinter as tk
from tkinter import messagebox


def on_entry_click(event, entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, "end")
        entry.config(fg='black')

def on_focusout(event, entry, placeholder_text):
    if entry.get() == '':
        entry.insert(0, placeholder_text)
        entry.config(fg='grey')


def input_gui():

    root = tk.Tk()
    root.title("Input Saver")

    placeholder_token = 'Enter token...'
    placeholder_cookie = 'Enter cookie...'

    Token = tk.Entry(root, width=40, fg='grey')
    Token.insert(0, placeholder_token)
    Token.bind('<FocusIn>', lambda event: on_entry_click(event, Token, placeholder_token))
    Token.bind('<FocusOut>', lambda event: on_focusout(event, Token, placeholder_token))
    Token.pack(padx=10, pady=10)

    Cookie = tk.Entry(root, width=40, fg='grey')
    Cookie.insert(0, placeholder_cookie)
    Cookie.bind('<FocusIn>', lambda event: on_entry_click(event, Cookie, placeholder_cookie))
    Cookie.bind('<FocusOut>', lambda event: on_focusout(event, Cookie, placeholder_cookie))
    Cookie.pack(padx=10, pady=10)

    save_button = tk.Button(root, text="Save", command=lambda: root.quit())
    save_button.pack(padx=10, pady=10)

    root.mainloop()

    TOKEN = Token.get().replace(placeholder_token, "")
    COOKIE = Cookie.get().replace(placeholder_cookie, "")

    if TOKEN == "" or COOKIE == "":
        messagebox.showerror("Error", "Input cannot be empty")
        root.destroy()
        input_gui()

    return TOKEN, COOKIE