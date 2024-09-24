import tkinter as tk
from tkinter import messagebox

def on_entry_click(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.insert(0, '')
        entry.config(fg='black')

def on_focusout(event, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg='grey')

def input_gui():
    root = tk.Tk()
    root.title("Input Saver")

    placeholder_token = 'Enter login...'
    placeholder_cookie = 'Enter password...'

    Login = tk.Entry(root, width=40, fg='grey')
    Login.insert(0, placeholder_token)
    Login.bind('<FocusIn>', lambda event: on_entry_click(event, Login, placeholder_token))
    Login.bind('<FocusOut>', lambda event: on_focusout(event, Login, placeholder_token))
    Login.pack(padx=10, pady=10)

    Password = tk.Entry(root, width=40, fg='grey')
    Password.insert(0, placeholder_cookie)
    Password.bind('<FocusIn>', lambda event: on_entry_click(event, Password, placeholder_cookie))
    Password.bind('<FocusOut>', lambda event: on_focusout(event, Password, placeholder_cookie))
    Password.pack(padx=10, pady=10)

    # Переменная для отслеживания закрытия окна
    inputs = {"LOGIN": "", "PASSWORD": ""}

    def on_save():
        inputs["LOGIN"] = Login.get()
        inputs["PASSWORD"] = Password.get()
        root.quit()  # Останавливаем цикл, но не уничтожаем виджеты

    save_button = tk.Button(root, text="Save", command=on_save)
    save_button.pack(padx=10, pady=10)

    root.mainloop()

    LOGIN = inputs["LOGIN"].replace(placeholder_token, "")
    PASSWORD = inputs["PASSWORD"].replace(placeholder_cookie, "")

    # Закрываем окно после того, как получили данные
    root.destroy()

    if LOGIN == "" or PASSWORD == "":
        messagebox.showerror("Error", "Input cannot be empty")
        input_gui()  # Перезапускаем ввод, если данные пусты

    return LOGIN, PASSWORD
