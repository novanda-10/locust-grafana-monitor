from locust import HttpUser, TaskSet, task

def login(l):
    l.client.post("/login", {"username": "admin", "password": "admin"})

def index(l):
    l.client.get("/")

def profile(l):
    l.client.get("/profile")

class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}  # Use tasks attribute instead of task_set

    def on_start(self):
        login(self)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]  # Use tasks attribute
    min_wait = 1000
    max_wait = 1000
