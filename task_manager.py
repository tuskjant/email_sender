import json
from task import Task

TASKS_DATA = "data/tasks_data.json"

class TaskManager:
    def __init__(self):
        self.all_tasks = self.read_task_file()

    def delete_task_from_file(self, task_number):
        # Update variable
        self.all_tasks = [dict for dict in self.all_tasks if not (dict["task_id"] == task_number)]
        # Update file
        self.write_file(self.all_tasks)
    
    def add_task_to_file(self, task):
        # Update variable
        self.all_tasks.append(task)
        # Update file
        self.write_file(self.all_tasks)
    
    def read_task_file(self):
        try:
            with open(TASKS_DATA, "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            return []
        else:
            return data

    def write_file(self, task_list):
        with open(TASKS_DATA, "w") as data_file:
            json.dump(task_list, data_file, indent=4)
            
    