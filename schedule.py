import datetime as dt
from dateutil.relativedelta import relativedelta


class Schedule:
    def __init__(self, initial_date: dt.datetime, repeat_basis: str, final_date: dt.datetime = dt.datetime(1, 1, 1)):
        self.initial_date = initial_date
        self.repeat_basis = repeat_basis
        self.final_date = final_date
        self.time_delta = dt.timedelta(0)
        self.format_date_time = "%Y %m %d - %H:%M"

        self.list_of_dates = []
        self.schedule_dict = {}

        self.generate_list_of_dates()
        self.generate_schedule_dict()

    def generate_list_of_dates(self):
        if self.repeat_basis == "Single":
            self.list_of_dates.append(self.initial_date)
            return
        elif self.repeat_basis == "Daily":
            self.time_delta = relativedelta(days=1)
        elif self.repeat_basis == "Weekly":
            self.time_delta = relativedelta(days=7)
        elif self.repeat_basis == "Monthly":
            self.time_delta = relativedelta(months=1)
        elif self.repeat_basis == "Yearly":
            self.time_delta = relativedelta(years=1)
        appointment = self.initial_date
        num_appointments = 1
        # limit the number of appointments in the list to 100
        while appointment <= self.final_date and num_appointments < 100:
            self.list_of_dates.append(appointment)
            appointment += self.time_delta
            num_appointments += 1

    def generate_schedule_dict(self):
        app_dict_list = []
        for index, date_time in enumerate(self.list_of_dates):
            app_dict_list.append({"sch_id": index,
                                  "datetime": date_time.strftime(self.format_date_time)})
        self.schedule_dict["schedule"] = app_dict_list

    def get_num_dates(self):
        return len(self.list_of_dates)
