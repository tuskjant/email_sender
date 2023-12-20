import tkinter
from tkinter import messagebox
import re

FG = "#3f5f73"

class EmailGui:
    def __init__(self, func_emaildata):
        self.email_window = tkinter.Toplevel()
        self.email_window.title("Recipient")
        self.email_window.geometry("400x300")
        self.email_window.config(padx=10, pady=10)
        self.email_window.iconbitmap("images/correo-electronico.ico")

        self.get_email_data = func_emaildata

        # A Label widget to show in toplevel
        label_alert = tkinter.Label(self.email_window,
                                    text="Recipient data", font=("Arial", 10, "bold"), fg=FG)
        label_alert.grid(column=0, row=0, columnspan=2)

        label_pwd1 = tkinter.Label(self.email_window, text="Name:", font=("Arial", 10, "bold"), fg=FG,
                                   width=15, anchor="e")
        label_pwd1.grid(column=0, row=1, pady=(50, 5))

        label_pwd2 = tkinter.Label(self.email_window, text="Email:", font=("Arial", 10, "bold"), fg=FG,
                                   width=15, anchor="e")
        label_pwd2.grid(column=0, row=2, pady=(20, 5))

        # Entries
        self.name = tkinter.StringVar()
        self.entry_name = tkinter.Entry(self.email_window, textvariable=self.name, width=35)
        self.entry_name.grid(row=1, column=1, pady=(50, 5))

        self.email = tkinter.StringVar()
        self.entry_email = tkinter.Entry(self.email_window, textvariable=self.email, width=35)
        self.entry_email.grid(row=2, column=1, pady=(20, 5))

        # Button accept
        button_pwd_reset = tkinter.Button(self.email_window, text="Add data", width=25, fg=FG, command=self.submit)
        button_pwd_reset.grid(row=3, column=0, columnspan=2, pady=50)

    def submit(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not (re.fullmatch(regex, self.email.get())):
            messagebox.showinfo(title="Recipient e-mail", message="You must enter a valid email", icon="warning")
            self.entry_email.focus_set()
        elif len(self.name.get()) < 1:
            messagebox.showinfo(title="Recipient name", message="You must enter a valid name", icon="warning")
            self.entry_name.focus_set()
        else:
            self.get_email_data([[self.name.get().strip(), self.email.get().strip()]])
            self.email_window.destroy()


