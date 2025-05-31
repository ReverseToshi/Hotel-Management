import tkinter as tk
from sql import SQL

def login():
    # Holds the login boolean value
    result = {"login":False}

    # Check password on login
    def check_password():
        ctor = SQL()
        password = PasswordBox.get()
        is_login = ctor.check_login(password)
        if is_login:
            result["login"]=True
            ctor.close()
            LoginWindow.destroy()

    # Login Window layout
    LoginWindow = tk.Tk()
    LoginWindow.title("Login")
    LoginWindow.geometry("300x400")
    PasswordLabel = tk.Label(LoginWindow, text="Password").pack()
    PasswordBox = tk.Entry(LoginWindow, show="*")
    PasswordBox.pack()

    loginBtn = tk.Button(LoginWindow, text="Login", command=check_password).pack()

    LoginWindow.mainloop()

    return result["login"]
