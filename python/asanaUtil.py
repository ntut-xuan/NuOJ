import asana
import json

class AsanatUil:
    def __init__(self, token):
        self.client = asana.Client.access_token(token)
    def get_section_completed_percentage(self, section_gid):
        result = self.client.tasks.get_tasks_for_section(section_gid, {}, opt_fields=["name", "completed_at"])
        completed_tasks = []
        tasks = []
        for task in result:
            tasks.append(task)
            if task["completed_at"] != None:
                completed_tasks.append(task)
        if len(tasks) == 0:
            return 0
        return len(completed_tasks) / len(tasks)
    def get_tasks(self, project_gid):
        result = self.client.tasks.get_tasks_for_project(project_gid, opt_fields=["name", "memberships.section.gid", "memberships.section.name", "assignee.name", "completed", "completed_at"])
        tasks = []
        for task in result:
            tasks.append(task)
        return tasks