import json

from gui import ProgramerGui
from schedule import Schedule
from messages import Messages
from task import Task
from config import Configuration
import smtplib
import datetime as dt
import time


# Function passed and called from gui
def load_data(recipients, email_basis, messages, msg_basis, date_ini, date_fi, repetition):
    new_schedule = Schedule(date_ini, repetition, date_fi)
    new_message = Messages(recipients, messages, email_basis, msg_basis)
    new_task = Task(new_message, new_schedule)

    if new_task.not_enough_messages():
        ProgramerGui.show_message_box(new_task.not_enough_messages())
    elif new_task.not_enough_recipients():
        ProgramerGui.show_message_box(new_task.not_enough_recipients())
    elif new_task.not_subjects():
        ProgramerGui.show_message_box(new_task.not_subjects())
    elif new_task.not_msg_basis():
        ProgramerGui.show_message_box(new_task.not_msg_basis())
    elif new_task.not_email_basis():
        ProgramerGui.show_message_box(new_task.not_email_basis())
    return new_task.return_task_dict()


# UMAT PIJ STC Grans FDP
def sending_emails(config_params, recipient, subject, msg):
    # with smtplib.SMTP(config_params["smtp"]) as connection:
    #     connection.starttls()
    #     connection.login(config_params["email"], config_params["password"])
    #     connection.sendmail(
    #         from_addr=config_params["email"],
    #         to_addrs=recipient,
    #         msg=f"Subject:{subject}\n\n{msg}"
    #     )
    # ---------- TEST LINES - comment when in use
    print("sending:")
    print(recipient)
    print(subject)
    print(msg)
    print("************************")
    # ------------------------------


def read_config():
    try:
        with open("data/config.json", "r") as file:
            data = json.load(file)
    except Exception:
        return False
    else:
        return data


def read_tasks():
    try:
        with open("data/tasks_data.json", "r") as file:
            data = json.load(file)
    except Exception:
        return False
    else:
        return data


def find_dates(data, key_to_search, list_of_values, task_id_ini, list_of_tasks):
    if isinstance(data, list):
        for item in data:
            find_dates(item, key_to_search, list_of_values, task_id_ini, list_of_tasks)
    elif isinstance(data, dict):
        for key, value in data.items():
            if key == "task_id":
                task_id_ini = value
            if isinstance(value, (dict, list)):
                find_dates(value, key_to_search, list_of_values, task_id_ini, list_of_tasks)
            elif key == key_to_search:
                list_of_values.append(value)
                list_of_tasks.append(task_id_ini)
    return list_of_values, list_of_tasks


def execute_task(task_id, index, task_list, configuration):
    email_basis = [tsk["email_basis"] for tsk in task_list if tsk["task_id"] == task_id][0]
    msg_basis = [tsk["message_basis"] for tsk in task_list if tsk["task_id"] == task_id][0]
    recipient_list = []
    messages_list = []

    # Recipients
    recipients = [tsk["recipients"] for tsk in task_list if tsk["task_id"] == task_id][0]
    if email_basis == "One at a time":
        if len(recipients) <= index:
            exit(0)
        else:
            recipient_list = [recipients[index]]
    elif email_basis == "All at once":
        recipient_list = recipients

    # Messages
    messages = [tsk["messages"] for tsk in task_list if tsk["task_id"] == task_id][0]
    if msg_basis == "One at a time":
        if len(messages) <= index:
            exit(0)
        else:
            messages_list = [messages[index]]
    elif msg_basis == "All at once":
        messages_list = messages

    # Prepare data and send
    for recipient_dict in recipient_list:
        for msg_dict in messages_list:
            msg_text = msg_dict["msg"].replace("[NAME]", recipient_dict["name"])
            sending_emails(configuration, recipient_dict["email"], msg_dict["subject"], msg_text)


# Once started and closed gui, execute code every 30 minutes to check tasks
configuration = Configuration()
m = ProgramerGui(load_data, configuration)

while True:
    now = dt.datetime.now()
    tasks = read_tasks()
    configuration = read_config()

    # No tasks to do
    if len(tasks) < 1 or len(configuration) < 1:
        exit(0)

    # Search for dates and get task number
    dates_task = []
    for task in tasks:
        dates_task += [{"task_id": task["task_id"],
                      "date": schedule["datetime"]} for schedule in task["schedule"]]
    for item in dates_task:
        item["date"] = dt.datetime.strptime(item["date"], "%Y %m %d - %H:%M")

    # Compare to current time
    for index, scheduled_date in enumerate([[pair["date"], pair["task_id"]] for pair in dates_task]):
        print(now)
        print(scheduled_date[0])
        if now >= scheduled_date[0] and now < scheduled_date[0] + dt.timedelta(minutes=30):
            execute_task(scheduled_date[1], index, tasks, configuration)

    time.sleep(30*60)



