import tkinter
from tkinter import messagebox
import datetime as dt

FG = "#3f5f73"

class MsgGui:
    def __init__(self, func_msgdata):
        self.msg_window = tkinter.Toplevel()
        self.msg_window.title("Message")
        self.msg_window.geometry("650x450")
        self.msg_window.config(padx=10, pady=10)
        self.msg_window.iconbitmap("images/correo-electronico.ico")

        self.get_msg_data = func_msgdata

        # A Label widget to show in toplevel
        label_alert = tkinter.Label(self.msg_window,
                                    text="Email content", font=("Arial", 10, "bold"), fg=FG)
        label_alert.grid(column=0, row=0, columnspan=2)

        label_subject = tkinter.Label(self.msg_window, text="Subject:", font=("Arial", 10, "bold"), fg=FG,
                                   width=15, anchor="e")
        label_subject.grid(column=0, row=1, pady=(50, 5))

        label_msg = tkinter.Label(self.msg_window, text="Message:", font=("Arial", 10, "bold"), fg=FG,
                                   width=15, anchor="e")
        label_msg.grid(column=0, row=2, pady=(20, 5))

        # Entries
        self.subject = tkinter.StringVar()
        self.entry_subject = tkinter.Entry(self.msg_window, textvariable=self.subject, width=55)
        self.entry_subject.grid(row=1, column=1, pady=(50, 5))

        self.entry_msg = tkinter.Text(self.msg_window,  width=55, height=10)
        self.entry_msg.grid(row=2, column=1, pady=(20, 5))

        # Button accept
        button_pwd_reset = tkinter.Button(self.msg_window, text="Add data", width=25, fg=FG, command=self.submit)
        button_pwd_reset.grid(row=3, column=0, columnspan=2, pady=50)

    def submit(self):
        if len(self.entry_msg.get(1.0, "end")) < 1:
            messagebox.showinfo(title="Message", message="You must enter a valid message", icon="warning")
            self.entry_msg.focus_set()
        elif len(self.subject.get()) < 1:
            messagebox.showinfo(title="Subject", message="You must enter a valid subject", icon="warning")
            self.entry_subject.focus_set()
        else:
            msg_file ="data/temp_" + dt.datetime.now().strftime("%Y%m%d%H%M") + ".txt"
            subject = self.subject.get()
            mssg = self.entry_msg.get(1.0, "end")
            text = subject + "\n" + mssg
            with open(msg_file, "w") as file:
                file.write(text)
            self.get_msg_data([msg_file])
            self.msg_window.destroy()
