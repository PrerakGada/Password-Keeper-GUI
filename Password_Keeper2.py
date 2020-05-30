from tkinter import *
from tkinter import messagebox
import sqlite3

root = Tk()
root.title("Password Keeper")
root.iconbitmap('pass_icon.ico')
root.geometry("462x500")
root.resizable(0, 0)

# Frames start here

title_frame = LabelFrame(root)
title_frame.grid(row=0, column=0, padx=5)

login_frame = LabelFrame(root)
login_frame.grid(row=1, column=0, pady=50)

main_frame = LabelFrame(root, bd=0)
main_frame.grid(row=2, column=0, pady=10)

# Frames End here


conn = sqlite3.connect('pass_book.db')
c = conn.cursor()


# Functions Start Here

def show():
    conn = sqlite3.connect('pass_book.db')
    c = conn.cursor()

    main_frame_2 = LabelFrame(root, bd=2)
    main_frame_2.grid(row=3, column=0)

    c.execute("SELECT *, oid FROM data")
    records = c.fetchall()

    scrollbary = Scrollbar(main_frame_2)
    scrollbary.pack(side=RIGHT, fill=Y)

    scrollbarx = Scrollbar(main_frame_2, orient=HORIZONTAL)
    scrollbarx.pack(side=BOTTOM, fill=X)

    text = Text(main_frame_2, wrap=NONE, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set, height=14,
                width=50)
    text.pack()

    for record in records:
        text.insert(END, str(list(record)[4]) + ") ")
        text.insert(END, str(list(record)[0]) + "  ")
        text.insert(END, str(list(record)[1]) + "  ")
        text.insert(END, str(list(record)[2]) + "  ")
        text.insert(END, str(list(record)[3]) + "\n")

    # attach listbox to scrollbar
    text.config(yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=text.yview)
    scrollbarx.config(command=text.xview)

    conn.commit()
    conn.close()


def add():
    conn = sqlite3.connect('pass_book.db')
    c = conn.cursor()

    c.execute("INSERT INTO data VALUES (:name, :url, :username, :password)",
              {
                  'name': name_entry.get(),
                  'url': url_entry.get(),
                  'username': username_entry.get(),
                  'password': password_entry.get()
              })

    oid_entry.delete(0, END)
    name_entry.delete(0, END)
    url_entry.delete(0, END)
    username_entry.delete(0, END)
    password_entry.delete(0, END)

    conn.commit()
    conn.close()

    show()


def delete():
    conn = sqlite3.connect('pass_book.db')
    c = conn.cursor()

    c.execute("DELETE from data WHERE oid= " + oid_entry.get())

    conn.commit()
    conn.close()

    oid_entry.delete(0, END)
    show()


def edit():
    conn = sqlite3.connect('pass_book.db')
    c = conn.cursor()

    def save():
        conn = sqlite3.connect('pass_book.db')
        c = conn.cursor()
        record_id = oid_entry.get()
        c.execute("""UPDATE data SET
                name = :name,
                url = :url,
                username = :username,
                password = :password
                
                WHERE oid = :oid""",
                  {
                      'name': name_entry.get(),
                      'url': url_entry.get(),
                      'username': username_entry.get(),
                      'password': password_entry.get(),
                      'oid': record_id
                  })

        conn.commit()
        conn.close()

        oid_entry.delete(0, END)
        name_entry.delete(0, END)
        url_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)

        edit_btn.grid_forget()

        add_btn = Button(main_frame, text="Add Password", font="Arial 10", command=add, activebackground="blue")
        add_btn.grid(row=5, column=0, columnspan=2)

        show()

    add_btn.grid_forget()

    edit_btn = Button(main_frame, text="Save Changes", font="Arial 10", command=save, activebackground="blue")
    edit_btn.grid(row=5, column=0, columnspan=2)

    record_id = oid_entry.get()
    c.execute("SELECT * FROM data WHERE oid=" + record_id)
    records = c.fetchall()

    for record in records:
        name_entry.insert(0, record[0])
        url_entry.insert(0, record[1])
        username_entry.insert(0, record[2])
        password_entry.insert(0, record[3])

    conn.commit()
    conn.close()


def main():
    conn = sqlite3.connect('pass_book.db')
    c = conn.cursor()

    login_frame.grid_forget()

    global name_entry
    global url_entry
    global username_entry
    global password_entry
    global oid_entry
    global add_btn

    oid_label = Label(main_frame, text="Sr. No. :", font="Arial 15")
    oid_label.grid(row=1, column=3)

    oid_entry = Entry(main_frame, width=20)
    oid_entry.grid(row=1, column=4)

    name_label = Label(main_frame, text="Name :", font="Arial 15")
    name_label.grid(row=1, column=0, sticky=W)

    name_entry = Entry(main_frame, width=20)
    name_entry.grid(row=1, column=1)

    url_label = Label(main_frame, text="URL :", font="Arial 15")
    url_label.grid(row=2, column=0, sticky=W)

    url_entry = Entry(main_frame, width=20)
    url_entry.grid(row=2, column=1)

    username_label = Label(main_frame, text="Username :", font="Arial 15")
    username_label.grid(row=3, column=0)

    username_entry = Entry(main_frame, width=20)
    username_entry.grid(row=3, column=1)

    password_label = Label(main_frame, text="Password :", font="Arial 15")
    password_label.grid(row=4, column=0)

    password_entry = Entry(main_frame, width=20)
    password_entry.grid(row=4, column=1)

    add_btn = Button(main_frame, text="Add Password", font="Arial 10", command=add, activebackground="blue")
    add_btn.grid(row=5, column=0, columnspan=2)

    del_btn = Button(main_frame, text="Delete Password", command=delete, activebackground="blue")
    del_btn.grid(row=2, column=3, columnspan=2)

    edit_btn = Button(main_frame, text="Edit Password", command=edit, activebackground="blue")
    edit_btn.grid(row=3, column=3, columnspan=2)

    show()


def submit(pas):
    conn = sqlite3.connect('pass_book.db')
    c = conn.cursor()
    c.execute("SELECT * FROM login")

    abc = c.fetchone()

    if list(abc)[0] != pas:
        messagebox.showerror("This is my Popup!", "Wrong Password!")
    else:
        main()
    admin_pass.delete(0, END)
    conn.commit()
    conn.close()


# Functions Finish Here


# Displaying the Title
Title1 = Label(title_frame, text=" Welcome to", fg="blue", font="Helvetica 19 bold")
Title2 = Label(title_frame, text="Password Keeper ", fg="red", font="System 23 bold")
Title1.grid(row=0, column=0)
Title2.grid(row=0, column=1, columnspan=2)

# Login Details
admin_pass_label = Label(login_frame, text="Enter Admin Password :", font="Arial 15")
admin_pass_label.grid(row=1, column=0)

admin_pass = Entry(login_frame, width=20)
admin_pass.grid(row=1, column=1)

submit_btn = Button(login_frame, text="Submit", font="Arial 15", command=lambda: submit(admin_pass.get()),
                    highlightcolor="red", activebackground="blue")
submit_btn.grid(row=1, column=2)

conn.commit()
conn.close()

root.mainloop()
