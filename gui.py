import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime as dt
from gui_email import EmailGui
from gui_msg import MsgGui
from gui_config import ConfigGui
import tkinter.filedialog as fd
import csv
import re
from task_manager import TaskManager
from tkhtmlview import RenderHTML, HTMLText, HTMLScrolledText


LABEL_T1_FONT = ("Arial", 16, "bold")
LABEL_T2_FONT = ("Arial", 12, "bold")
BUTTON_FONT = ("Arial", 10, "bold")
FG = "#3f5f73"
TODAY = dt.datetime.now()

ATTRIBUTION = "Correo electrónico iconos creados por Uniconlabs - Flaticon"
ATTRIBUTION2 = "Ajustes iconos creados por srip - Flaticon"
ATTRIBUTION3 = "Signo de interrogación iconos creados por sonnycandra - Flaticon"
ATTRIBUTION4 = "Calendario iconos creados por Md Tanvirul Haque - Flaticon"
ATTRIBUTION5 = "Bloquear iconos creados por Flowicon - Flaticon"
ATTRIBUTION6 = "Correo electrónico iconos creados por Freepik - Flaticon"



class ProgramerGui:
    def __init__(self, func, config_object):
        self.recipients = []
        self.sender = []
        self.messages = []
        self.date_ini = None
        self.date_fi = None
        self.repetition = None
        self.email_basis = None
        self.msg_basis = None
        self.dict_task = {}
        self.config_object = config_object
        self.create_task = func
        self.task_manager = TaskManager()


        # Button config
        def config_sender():
            config_window = ConfigGui(self.config_object)

        # Button one email
        def get_one_recipient():
            mail_window = EmailGui(get_recipient_data)

        # One email gui function
        def get_recipient_data(recipient):
            activate_frame_1()
            self.recipients = recipient

        # Button email list
        def get_all_recipients():
            all_emails = []
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails_file = fd.askopenfile(parent=window, title='Choose a file: ', filetypes=[("Csv files", "*.csv")])
            if emails_file is None:
                return
            data = csv.reader(emails_file)
            for row in data:
                if len(row) < 2 or len(row) > 2:
                    return
                if not (re.fullmatch(regex, row[1].strip())):
                    return
                row_stripped = [x.strip() for x in row]
                all_emails.append(row_stripped)
            activate_frame_1()
            self.recipients = all_emails

        # Button one msg
        def get_one_msg():
            mail_window = MsgGui(get_message_data)

        # One msg gui function
        def get_message_data(message):
            activate_frame_2()
            self.messages = message

        # Button msg list
        def get_msg_list():
            emails_file = fd.askopenfilenames(parent=window, title='Choose files: ', filetypes=[("Txt files", "*.txt")])
            if len(emails_file) < 1:
                return
            activate_frame_2()
            self.messages = emails_file

        # Button schedule
        def add_daily():
            if check_config_data_ok():
                clean_tree_data()
                make_appointments("Daily")

        def add_weekly():
            if check_config_data_ok():
                clean_tree_data()
                make_appointments("Weekly")

        def add_monthly():
            if check_config_data_ok():
                clean_tree_data()
                make_appointments("Monthly")

        def add_yearly():
            if check_config_data_ok():
                clean_tree_data()
                make_appointments("Yearly")

        def add_single():
            if check_config_data_ok():
                clean_tree_data()
                make_appointments("Single")

        def make_appointments(type):
            # Collect previous radiobuttons data
            self.email_basis = email_basis.get()
            self.msg_basis = msg_basis.get()
            # Collect schedule data
            date_ini = cal_ini.selection_get()
            date_fi = cal_fi.selection_get()
            time_msg = dt.time(hour=int(spinval_h_ini.get()), minute=int(spinval_m_ini.get()))
            dt_ini = dt.datetime.combine(date_ini, time_msg)
            dt_fi = dt.datetime.combine(date_fi, time_msg)
            format_dt = "%Y%m%d - %H%m"
            activate_frame_3()
            self.date_ini = dt_ini
            self.date_fi = dt_fi
            self.repetition = type
            self.dict_task = self.create_task(self.recipients, self.email_basis, self.messages, self.msg_basis,
                             self.date_ini, self.date_fi, self.repetition)
            display_data(self.dict_task)

        def save_task():
            self.task_manager.add_task_to_file(self.dict_task)
            # clean tree and current task data
            self.show_message_box("Task has been added to list")
            for i in tree.get_children():
                tree.delete(i)
            self.dict_task = {}
            list_task()

        def delete_task():
            current_item = tree.focus()
            if len(current_item) > 0:
                parent_id = tree.parent(current_item)
                if parent_id:
                    current_row = tree.item(parent_id)['text']
                else:
                    current_row = tree.item(current_item)['text']
                if current_row[0] == "*":
                    num_selected_task = int(current_row[15:])
                    self.task_manager.delete_task_from_file(num_selected_task)
                    clean_tree_data()
                    self.dict_task = {}
                    list_task()
                else:
                    self.show_message_box("You must select the task number '* Task number: ' to delete.")
            else:
                self.show_message_box("You must select the task number '* Task number: '  to delete.")


        def list_task():
            clean_tree_data()
            all_tasks = self.task_manager.read_task_file()
            populate_tree(tree, "", all_tasks)
            btt_img_cancel_task.config(state=tkinter.NORMAL)
            btt_img_send_task.config(state=tkinter.DISABLED)

        def populate_tree(tree, parent, data):
            if isinstance(data, list):
                for index, item in enumerate(data):
                    if isinstance(item, dict):
                        # node = tree.insert(parent, "end", text=f"Item-{index}")
                        populate_tree(tree, parent, item)
                    else:
                        tree.insert(parent, "end", text=item)
            elif isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        if key == "schedule":
                            node = tree.insert(parent, "end", text="Dates")
                            populate_tree(tree, node, value)
                        else:
                            node = tree.insert(parent, "end", text=key.title())
                            populate_tree(tree, node, value)
                    else:
                        value_str = str(value)
                        if key == "sch_id" or key == "recipient_id" or key == "msg_id":
                            pass
                        elif key == "task_id":
                            node = tree.insert(parent, "end", text=f"* Task number: {value_str}")
                            populate_tree(tree, node, value)
                        elif key == "datetime":
                            tree.insert(parent, "end", text=f"Sending date: {value_str}")
                        elif key == "email_basis":
                            tree.insert(parent, "end", text=f"Sending_to type: {value_str}")
                        elif key == "message_basis":
                            tree.insert(parent, "end", text=f"Select message type: {value_str}")
                        else:
                            tree.insert(parent, "end", text=f"{key.title()}: {value_str}")

        def display_data(dict_task):
            populate_tree(tree, "", dict_task)

        def clean_tree_data():
            for i in tree.get_children():
                tree.delete(i)

        def check_config_data_ok():
            if self.config_object.check_existing_config():
                ProgramerGui.show_message_box(self.config_object.check_existing_config())
                return False
            return True



        # ------------------------------------------------------ Activate frames

        def activate_frame_1():
            one_msg_button.config(state=tkinter.NORMAL)
            list_msg_button.config(state=tkinter.NORMAL)
            msg_oao.config(state=tkinter.NORMAL)
            msg_oat.config(state=tkinter.NORMAL)

        def activate_frame_2():
            cal_ini.config(state=tkinter.NORMAL)
            cal_fi.config(state=tkinter.NORMAL)
            spb_h_ini.config(state=tkinter.NORMAL)
            spb_m_ini.config(state=tkinter.NORMAL)
            single_button.config(state=tkinter.NORMAL)
            daily_button.config(state=tkinter.NORMAL)
            weekly_button.config(state=tkinter.NORMAL)
            monthly_button.config(state=tkinter.NORMAL)
            yearly_button.config(state=tkinter.NORMAL)

        def activate_frame_3():
            btt_img_send_task.config(state=tkinter.NORMAL)
            btt_img_cancel_task.config(state=tkinter.NORMAL)

        # Show message box with information and instructions
        def show_help():
            new_window = tkinter.Toplevel(window)
            new_window.title("Help")
            new_window.geometry("800x500")
            new_window.iconbitmap("images/correo-electronico.ico")
            html_text = RenderHTML("help.html")
            text_h = HTMLScrolledText(new_window, html=html_text)
            text_h.pack(padx=25, pady=25)
            text_h.fit_height()


        # -------------------------------------------------------------- Tkinter GUI
        window = tkinter.Tk()
        window.title("Email schedule manager")
        window.iconbitmap("images/correo-electronico.ico")
        window.config(padx=20, pady=20)
    
        title_label = tkinter.Label(window, text="Mail schedule manager", font=LABEL_T1_FONT, fg="SkyBlue4")
        title_label.grid(column=0, row=0, columnspan=3, pady=(0, 20))

        btt_img_cfg = tkinter.PhotoImage(file="images/configuraciones.png")
        config_button = tkinter.Button(window, image=btt_img_cfg, command=config_sender)
        config_button.grid(column=2, row=0,  pady=(0, 20), padx=20, sticky="e")

        btt_img_info = tkinter.PhotoImage(file="images/pregunta.png")
        info_button = tkinter.Button(window, image=btt_img_info, command=show_help)
        info_button.grid(column=0, row=0,  pady=(0, 20), padx=20, sticky="w")
        
        # ------------------------------------------------------------------Frames
        mail_frame = ttk.Frame(window, width=200, height=600)
        mail_frame.config(relief="groove", borderwidth=4)
        mail_frame.grid(column=0, row=1, padx=10)
    
        sch_frame = ttk.Frame(window, width=200, height=600)
        sch_frame.config(relief="groove", borderwidth=4)
        sch_frame.grid(column=1, row=1, padx=10)
    
        tree_frame = ttk.Frame(window, width=300, height=600)
        tree_frame.config(relief="groove", borderwidth=4)
        tree_frame.grid(column=2, row=1, padx=10)

        # ---------- Mail-msg frame widgets
        # Email
        email_label = tkinter.Label(mail_frame, text="1- Recipients", font=LABEL_T1_FONT, fg=FG)
        email_label.grid(column=0, row=0, sticky="w", pady=(20,10), padx=20)
    
        one_mail_button = tkinter.Button(mail_frame, text="One email", width=20, font=BUTTON_FONT, fg=FG,
                                         command=get_one_recipient)
        one_mail_button.grid(column=0, row=1, padx=20, pady=(10, 5))
    
        list_mail_button = tkinter.Button(mail_frame, text="Email list file", width=20, font=BUTTON_FONT, fg=FG,
                                          command=get_all_recipients)
        list_mail_button.grid(column=0, row=2, padx=20, pady=(5, 5))
    
        email_basis = tkinter.StringVar()
        email_oao = ttk.Radiobutton(mail_frame, text='All at once', variable=email_basis, value='All at once',
                                    style='Radiobutton.TRadiobutton')
        email_oao.grid(column=0, row=3, sticky="w", padx=20)
        email_oat = ttk.Radiobutton(mail_frame, text='One at a time', variable=email_basis, value='One at a time',
                                    style='Radiobutton.TRadiobutton')
        email_oat.grid(column=0, row=4, sticky="w", padx=20, pady=(0, 20))
    
        # Messages
        msg_label = tkinter.Label(mail_frame, text="2- Messages", font=LABEL_T1_FONT, fg=FG)
        msg_label.grid(column=0, row=5, sticky="w", padx=20, pady=(20, 0))
    
        one_msg_button = tkinter.Button(mail_frame, text="One message", width=20, font=BUTTON_FONT, fg=FG,
                                        state=tkinter.DISABLED, command=get_one_msg)
        one_msg_button.grid(column=0, row=6, padx=20, pady=(10, 5))
    
        list_msg_button = tkinter.Button(mail_frame, text="Select message files", width=20, font=BUTTON_FONT, fg=FG,
                                         state=tkinter.DISABLED, command=get_msg_list)
        list_msg_button.grid(column=0, row=7, padx=20, pady=(5, 5))
    
        msg_basis = tkinter.StringVar()
        msg_oao = ttk.Radiobutton(mail_frame, text='All at once', variable=msg_basis, value='All at once',
                                    style='Radiobutton.TRadiobutton', state=tkinter.DISABLED)
        msg_oao.grid(column=0, row=8, sticky="w", padx=20)
        msg_oat = ttk.Radiobutton(mail_frame, text='One at a time', variable=msg_basis, value='One at a time',
                                    style='Radiobutton.TRadiobutton', state=tkinter.DISABLED)
        msg_oat.grid(column=0, row=9, sticky="w", padx=20, pady=(0, 35))
    
        # ---------- ---------------------------------------------------------------------------------Schedule frame widgets
        # Schedule
        sch_label = tkinter.Label(sch_frame, text="3- Schedule", font=LABEL_T1_FONT, fg=FG)
        sch_label.grid(column=0, row=0, columnspan=10, sticky="w", pady=(20, 20), padx=20)
    
        #----------------- ini date
        ini_label = tkinter.Label(sch_frame, text="Start sending date", font=LABEL_T2_FONT, fg=FG)
        ini_label.grid(column=0, row=1, columnspan=5, sticky="w", padx=20)
    
        cal_ini = Calendar(sch_frame, selectmode='day', year=TODAY.year, month=TODAY.month, day=TODAY.day,
                           state=tkinter.DISABLED)
        cal_ini.grid(column=0, row=2, columnspan=5, padx=(20, 10), pady=10)
    
        # --- time_ini
        ini_frame = ttk.Frame(sch_frame, width=200)
        ini_frame.grid(column=0, row=3, columnspan=5, padx=10)

        aux_time_label = tkinter.Label(ini_frame, text="Set time to seng msgs: ", font=LABEL_T2_FONT, fg=FG)
        aux_time_label.grid(column=0, row=0, padx=(20,0))

        spinval_h_ini = tkinter.StringVar()
        spb_h_ini = tkinter.Spinbox(ini_frame, from_=1, to=24, textvariable=spinval_h_ini,  width=3, font=BUTTON_FONT,
                                    fg=FG, state=tkinter.DISABLED)
        spb_h_ini.grid(column=1, row=0, padx=(20,0))
        spinval_h_ini.set(9)
    
        aux_h_label = tkinter.Label(ini_frame, text="H :", font=LABEL_T2_FONT, fg=FG)
        aux_h_label.grid(column=2, row=0)
    
        spinval_m_ini = tkinter.StringVar()
        spb_m_ini = tkinter.Spinbox(ini_frame, from_=1, to=60, textvariable=spinval_m_ini, width=3, font=BUTTON_FONT,
                                    fg=FG, state=tkinter.DISABLED)
        spb_m_ini.grid(column=3, row=0 )
        spinval_m_ini.set(30)
    
        aux_m_label = tkinter.Label(ini_frame, text="M", font=LABEL_T2_FONT, fg=FG)
        aux_m_label.grid(column=4, row=0)
    
    
        #------------------ end date
        end_label = tkinter.Label(sch_frame, text="Last sending date", font=LABEL_T2_FONT, fg=FG)
        end_label.grid(column=5, row=1, columnspan=5, sticky="e", padx=20)
    
        cal_fi = Calendar(sch_frame, selectmode='day', year=TODAY.year, month=TODAY.month, day=TODAY.day,
                          state=tkinter.DISABLED)
        cal_fi.grid(column=5, row=2, columnspan=5, padx=(10, 20), pady=10)

        # Schedule buttons
        single_button = tkinter.Button(sch_frame, text="Add\nsingle", width=10, font=BUTTON_FONT, fg=FG,
                                       state=tkinter.DISABLED, command=add_single)
        single_button.grid(row=4, column=0, columnspan=2, pady=(25,20))
    
        daily_button = tkinter.Button(sch_frame, text="Add\ndaily", width=10, font=BUTTON_FONT, fg=FG,
                                      state=tkinter.DISABLED, command=add_daily)
        daily_button.grid(row=4, column=2, columnspan=2, pady=(25,20))
    
        weekly_button = tkinter.Button(sch_frame, text="Add\nweekly", width=10, font=BUTTON_FONT, fg=FG,
                                       state=tkinter.DISABLED, command=add_weekly)
        weekly_button.grid(row=4, column=4, columnspan=2, pady=(25,20))
    
        monthly_button = tkinter.Button(sch_frame, text="Add\nmonthly", width=10, font=BUTTON_FONT, fg=FG,
                                        state=tkinter.DISABLED, command=add_monthly)
        monthly_button.grid(row=4, column=6, columnspan=2, pady=(25,20))
    
        yearly_button = tkinter.Button(sch_frame, text="Add\nyearly", width=10, font=BUTTON_FONT, fg=FG,
                                       state=tkinter.DISABLED, command=add_yearly)
        yearly_button.grid(row=4, column=8, columnspan=2, pady=(25, 20))
    
        # -------------------------------------------------- TREE VIEW

        send_task_label = tkinter.Label(tree_frame, text="4- Add task", font=LABEL_T1_FONT, fg=FG)
        send_task_label.grid(column=0, row=0, columnspan=3, sticky="w")

        # Treeview widget
        tree = ttk.Treeview(tree_frame, height=16)
        tree.grid(column=0, row=1, columnspan=3)
        #tree.grid(tree_frame, column=0, row=1, columnspan=2)


        # --------------------------------------------  SEND or CANCEL TASK BUTTON
        img_send_task = tkinter.PhotoImage(file="images/correo-electronico_prog.png")
        btt_img_send_task = tkinter.Button(tree_frame, image=img_send_task, bg="white", state=tkinter.DISABLED,
                                           command=save_task)
        btt_img_send_task.grid(row=2, column=0)

        img_cancel_task = tkinter.PhotoImage(file="images/error.png")
        btt_img_cancel_task = tkinter.Button(tree_frame, image=img_cancel_task, bg="white", state=tkinter.DISABLED,
                                           command=delete_task)
        btt_img_cancel_task.grid(row=2, column=1)

        img_list_task = tkinter.PhotoImage(file="images/correo-electronico_lista.png")
        btt_img_list_task = tkinter.Button(tree_frame, image=img_list_task, bg="white",
                                             command=list_task)
        btt_img_list_task.grid(row=2, column=2)



        # Credits and info
        button_credits = tkinter.Button(window, text="Credits & About", width=20, font=("Arial", 8, "italic"),
                                             foreground="SkyBlue4", borderwidth=0,
                                             command=self.show_atributions)
        button_credits.grid(row=4, column=0, columnspan=2, sticky="w", pady=10)
    
        # --------------------------------------------------- Styles ttk
        s = ttk.Style()
        s.configure('Radiobutton.TRadiobutton', font=("Arial", 10), foreground=FG)

        window.mainloop()




    # *************************************************************** Functions and commands
    
    # Show message box with about and attributions
    def show_atributions(self):
        message = f"This python code is made by Gemma Riu, inspired by an exercise from '100 Days of Code' by Angela Yu.\n \n" \
                  f"Icons from https://www.flaticon.es :\n•{ATTRIBUTION}\n•{ATTRIBUTION2}\n•{ATTRIBUTION3}\n•{ATTRIBUTION4}\n•{ATTRIBUTION5}\n•{ATTRIBUTION6}"
        messagebox.showinfo(title="Credits & About", message=message, icon="info")

    @staticmethod
    def show_message_box(msg_to_show):
        messagebox.showinfo(title="Error in data", message=msg_to_show, icon="warning")



    
