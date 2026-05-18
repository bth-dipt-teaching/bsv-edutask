from locust import HttpUser, task, between

class EduTaskUser(HttpUser):
    # Simulates a user waiting between actions to avoid overwhelming the local DB
    wait_time = between(1, 4)

    @task(3)
    def view_tasks(self):
        # Using the exact Jane Doe ID from your project history
        user_id = "6a037ab02eec948ddcf1b0e7"
        self.client.get(f"/tasks/ofuser/{user_id}", name="/tasks/ofuser/[id]")

    @task(1)
    def create_todo(self):
        # Using the Task ID 'Top 7 Awesome Developer Tools' created in Assignment 4
        # This matches the schema expected by your todo_blueprint
        self.client.post("/todos/create", json={
            "task_id": "6a0380492eec948ddcf1b102",
            "description": f"Performance Test Item {self.user_id}"
        }, name="/todos/create")