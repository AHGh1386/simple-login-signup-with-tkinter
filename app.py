import tkinter as tk
from tkinter import messagebox
import sqlite3


conn = sqlite3.connect('users.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS users
                (username TEXT PRIMARY KEY, password TEXT)''')
conn.commit()


def sign_up():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        try:
    
            c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo('Success', 'Sign up successful!')
        except sqlite3.IntegrityError:
            messagebox.showerror('Error', 'Username already exists!')
    else:
        messagebox.showerror('Error', 'Please enter username and password.')


def sign_in():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
     
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()

        if result:
       
            window.destroy()
            open_user_options(username)
        else:
            messagebox.showerror('Error', 'Invalid username or password.')
    else:
        messagebox.showerror('Error', 'Please enter username and password.')

def open_user_options(username):
    user_options_window = tk.Tk()
    user_options_window.title("User Options")


    def change_password():
        current_password = current_password_entry.get()
        new_password = new_password_entry.get()

        if current_password and new_password:
         
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, current_password))
            result = c.fetchone()

            if result:
             
                c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
                conn.commit()
                messagebox.showinfo('Success', 'Password changed successfully!')
            else:
                messagebox.showerror('Error', 'Invalid current password.')
        else:
            messagebox.showerror('Error', 'Please enter current and new password.')

  
    def delete_account():
     
        c.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        messagebox.showinfo('Success', 'Account deleted successfully!')
        user_options_window.destroy()


    current_password_label = tk.Label(user_options_window, text="Current Password" , background="lightskyblue")
    current_password_label.pack()
    current_password_entry = tk.Entry(user_options_window, show="*")
    current_password_entry.pack()


    new_password_label = tk.Label(user_options_window, text="New Password", background="crimson")
    new_password_label.pack()
    new_password_entry = tk.Entry(user_options_window, show="*")
    new_password_entry.pack()


    change_password_button = tk.Button(user_options_window, text="Change Password", command=change_password , background="lightskyblue")
    change_password_button.pack()


    delete_account_button = tk.Button(user_options_window, text="Delete Account", command=delete_account , background="crimson")
    delete_account_button.pack()

    user_options_window.mainloop()


window = tk.Tk()
window.title("Login")


username_label = tk.Label(window, text="Username")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()


password_label = tk.Label(window, text="Password")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()


sign_up_button = tk.Button(window, text="Sign Up", command=sign_up)
sign_up_button.pack()


sign_in_button = tk.Button(window, text="Sign In", command=sign_in)
sign_in_button.pack()

window.mainloop()


conn.close()