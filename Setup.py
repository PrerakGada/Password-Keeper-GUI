from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
import sqlite3

root = Tk()
root.title("Password Keeper")
root.iconbitmap('pass_icon.ico')
root.geometry("462x500")
root.resizable(0, 0)

title_frame = LabelFrame(root)
title_frame.grid(row=0, column=0, padx=5)

login_frame = LabelFrame(root)
login_frame.grid(row=1, column=0, pady=50)

conn = sqlite3.connect('pass_book.db')
c = conn.cursor()

c.execute("""CREATE TABLE login (admin_pass text)""")

# Setting users password
c.execute("INSERT INTO login VALUES (:ad_ps)",
          {
              'ad_ps': "password"
          })

c.execute("""CREATE TABLE data (
            name text,
            url text,
            username text,
            password text
            )""")

def create():
    conn = sqlite3.connect('pass_book.db')
    c = conn.cursor()

    c.execute("DROP TABLE data")

    c.execute("""CREATE TABLE data (
            name text,
            url text,
            username text,
            password text
            )""")

    conn.commit()
    conn.close()

def submit(pas, opas):
    conn = sqlite3.connect('pass_book.db')
    c = conn.cursor()

    c.execute("SELECT * FROM login")

    abc = c.fetchone()

    if list(abc)[0] != opas:
        messagebox.showerror("This is my Popup!", "Wrong Password!")
    else:
        c.execute("""UPDATE login SET
                        password = :password
                        WHERE oid = :oid""",
                  {
                      'password': admin_pass.get(),
                      'oid': 1
                  })
        btn = Button(login_frame, text="Click to Delete all Data", command=create)
        btn.grid(row=2, column=0, cloumnspan=2)

    conn.commit()
    conn.close()


Title1 = Label(title_frame, text=" Welcome to", fg="blue", font="Helvetica 19 bold")
Title2 = Label(title_frame, text="Password Keeper ", fg="red", font="System 23 bold")
Title1.grid(row=0, column=0)
Title2.grid(row=0, column=1, columnspan=2)

admin_pass_old_label = Label(login_frame, text="Create Admin Password :", font="Arial 15")
admin_pass_old_label.grid(row=0, column=0)

admin_pass_old = Entry(login_frame, width=20)
admin_pass_old.grid(row=0, column=1)

admin_pass_label = Label(login_frame, text="Create Admin Password :", font="Arial 15")
admin_pass_label.grid(row=1, column=0)

admin_pass = Entry(login_frame, width=20)
admin_pass.grid(row=1, column=1)

submit_btn = Button(login_frame, text="Submit", font="Arial 15", command=lambda: submit(admin_pass.get(), admin_pass_old.get()))
submit_btn.grid(row=1, column=2)

conn.commit()
conn.close()

root.mainloop()
