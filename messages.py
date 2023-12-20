class Messages:
    def __init__(self, recipients_list: list[list[str]], messages_list: list[str],
                 email_select: str, msg_select: str):
        self.email_list = [recipient[1] for recipient in recipients_list]
        self.names = [recipient[0] for recipient in recipients_list]
        self.messages = []
        self.subjects = []
        self.email_select = email_select
        self.msg_select = msg_select
        self.get_msgs_and_subjects(messages_list)

        self.msg_dict = {}
        self.generate_mail_dict()
        self.generate_msg_dict()
        self.generate_sending_type()

    def generate_mail_dict(self):
        app_dict_list = []
        for index, mail in enumerate(self.email_list):
            app_dict_list.append({"recipient_id": index,
                                  "name": self.names[index],
                                  "email": mail})
        self.msg_dict["recipients"] = app_dict_list

    def generate_msg_dict(self):
        app_dict_list = []
        for index, msg in enumerate(self.messages):
            app_dict_list.append({"msg_id": index,
                                  "subject": self.subjects[index],
                                  "msg": msg})
        self.msg_dict["messages"] = app_dict_list

    def generate_sending_type(self):
        self.msg_dict["email_basis"] = self.email_select
        self.msg_dict["message_basis"] = self.msg_select

    def get_num_messages(self):
        return len(self.messages)

    def get_num_recipients(self):
        return len(self.email_list)

    def get_msgs_and_subjects(self, message_list):
        all_subjects = []
        all_messages = []
        for message_file in message_list:
            try:
                with open(message_file, "r") as file:
                    file_lines = file.readlines()
            except Exception:
                return None
            else:
                all_subjects.append(file_lines[0])
                all_messages.append(''.join(file_lines[1:]))
        self.messages = all_messages
        self.subjects = all_subjects


