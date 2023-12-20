from messages import Messages
from schedule import Schedule
import json

TASKS_DATA = "data/tasks_data.json"


class Task:
    def __init__(self, message: Messages, schedule: Schedule):
        self.num_msgs = message.get_num_messages()
        self.num_recipients = message.get_num_recipients()
        self.num_dates = schedule.get_num_dates()
        sch_dict = schedule.schedule_dict
        msg_dict = message.msg_dict
        last_task = self.get_num_last_saved_task()
        self.task = {"task_id": last_task}
        self.task.update(sch_dict)
        self.task.update(msg_dict)

    def get_num_last_saved_task(self):
        try:
            with open(TASKS_DATA, "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            return 1
        else:
            if len(data) < 1:
                return 1
            else:
                last_task_num = max(data, key=lambda x: x["task_id"])
                return last_task_num["task_id"] + 1

    def return_task_dict(self):
        return self.task

    def not_enough_messages(self):
        if self.task["message_basis"] == "One at a time":
            if self.num_msgs > self.num_dates:
                return "Not enough scheduled dates for all messages. Only firsts ones will be send."
            elif self.num_msgs < self.num_dates:
                return "Not enough messages for all scheduled dates. Only firsts ones will be send."
            else:
                return False
        return False

    def not_enough_recipients(self):
        if self.task["email_basis"] == "One at a time":
            if self.num_recipients > self.num_dates:
                return "Not enough scheduled dates for all recipients. Only firsts ones will be send."
            elif self.num_recipients < self.num_dates:
                return "Not enough recipients for all scheduled dates. Only firsts ones will be send."
            else:
                return False
        else:
            return False

    def not_subjects(self):
        for message in self.task["messages"]:
            if len(message["subject"]) < 1:
                return "Message files don't have correct format"
        return False

    def not_msg_basis(self):
        if len(self.task["message_basis"]) < 1:
            return "You must select one message method 'All at once' or 'One at a time'"
        return False

    def not_email_basis(self):
        if len(self.task["email_basis"]) < 1:
            return "You must select one mailing method 'All at once' or 'One at a time'"
        return False

