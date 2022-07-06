import asana
import json

class AsanatUil:
    def __init__(self, token):
        self.client = asana.Client.access_token(token)
    def get_tasks(self, project_gid):
        result = self.client.tasks.get_tasks_for_project(project_gid, opt_fields=["name", "memberships.section.gid", "memberships.section.name", "assignee.name", "assignee.photo", "completed", "completed_at"])
        tasks = []
        for task in result:
            tasks.append(task)
        return tasks