import json

CONFIG_DATA = "data/config.json"


class Configuration:
    def __init__(self):
        self.sender_email = ""
        self.pwd = ""
        self.smtp = ""
        self.config_parameters = self.read_config_file()

    @staticmethod
    def read_config_file():
        try:
            with open(CONFIG_DATA, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return {"email": "",
                    "password": "",
                    "smtp": ""}
        else:
            return data

    def save_config_file(self):
        with open(CONFIG_DATA, "w") as file:
            json.dump(self.config_parameters, file, indent=4)

    def set_config_data(self, config_data):
        self.sender_email = config_data[0]
        self.pwd = config_data[1]
        self.smtp = config_data[2]
        self.create_config_parameters()
        self.save_config_file()

    def get_config_data(self):
        return [self.sender_email, self.pwd, self.smtp]

    def create_config_parameters(self):
        self.config_parameters = {
            "email": self.sender_email,
            "password": self.pwd,
            "smtp": self.smtp
        }

    def check_existing_config(self):
        data_in_file = self.read_config_file()
        for k, v in data_in_file.items():
            if len(v) < 2:
                return "You must set sender email and data"
            else:
                return False