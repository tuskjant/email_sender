import tkinter
from tkinter import messagebox
import re
from config import Configuration

FG = "#3f5f73"

class ConfigGui:
    def __init__(self, config_Object):
        self.configuration = config_Object
        self.config_parameters = self.configuration.read_config_file()
        self.config_window = tkinter.Toplevel()
        self.config_window.title("Configuration")
        self.config_window.geometry("400x300")
        self.config_window.config(padx=10, pady=10)
        self.config_window.iconbitmap("images/configuraciones.ico")



        # A Label widget to show in toplevel
        label_title = tkinter.Label(self.config_window,
                                    text="Sender email configuration", font=("Arial", 10, "bold"), fg=FG)
        label_title.grid(column=0, row=0, columnspan=2)

        label_sender_email = tkinter.Label(self.config_window, text="Email:", font=("Arial", 10, "bold"), fg=FG,
                                   width=15, anchor="e")
        label_sender_email.grid(column=0, row=1, pady=(50, 5))

        label_pwd = tkinter.Label(self.config_window, text="Password:", font=("Arial", 10, "bold"), fg=FG,
                                   width=15, anchor="e")
        label_pwd.grid(column=0, row=2, pady=(20, 5))

        label_smtp = tkinter.Label(self.config_window, text="SMTP:", font=("Arial", 10, "bold"), fg=FG,
                                   width=15, anchor="e")
        label_smtp.grid(column=0, row=3, pady=(20, 5))



        # Entries
        self.s_email = tkinter.StringVar()
        self.s_email.set(self.configuration.sender_email)
        self.sender_email = tkinter.Entry(self.config_window, textvariable=self.s_email, width=35)
        self.sender_email.grid(row=1, column=1, pady=(50, 5))

        self.s_pwd = tkinter.StringVar()
        self.s_pwd.set(self.configuration.pwd)
        self.sender_pwd = tkinter.Entry(self.config_window, textvariable=self.s_pwd, width=35)
        self.sender_pwd.grid(row=2, column=1, pady=(20, 5))

        self.s_smtp = tkinter.StringVar()
        self.s_smtp.set(self.configuration.smtp)
        self.sender_smtp = tkinter.Entry(self.config_window, textvariable=self.s_smtp, width=35)
        self.sender_smtp.grid(row=3, column=1, pady=(20, 5))

        # Button accept
        button_pwd_reset = tkinter.Button(self.config_window, text="Set data", width=25, fg=FG, command=self.submit)
        button_pwd_reset.grid(row=4, column=0, columnspan=2, pady=50)

        self.set_default_values()

    def submit(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not (re.fullmatch(regex, self.s_email.get())):
            messagebox.showinfo(title="Sender e-mail", message="You must enter a valid email", icon="warning")
            self.sender_email.focus_set()
        elif len(self.s_pwd.get()) < 1:
            messagebox.showinfo(title="Sender password", message="You must enter a valid password", icon="warning")
            self.sender_pwd.focus_set()
        elif len(self.s_smtp.get()) < 1:
            messagebox.showinfo(title="SMTP", message="You must enter valid email provider", icon="warning")
            self.sender_smtp.focus_set()
        else:
            self.configuration.set_config_data([self.s_email.get().strip(), self.s_pwd.get().strip(),
                                                self.s_smtp.get().strip()])
            self.config_window.destroy()

    def set_default_values(self):
        self.s_email.set(self.config_parameters["email"])
        self.s_pwd.set(self.config_parameters["password"])
        self.s_smtp.set(self.config_parameters["smtp"])
