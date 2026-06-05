import json
from locust import HttpUser, task, events
import logging

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)

class UserBehavior(HttpUser):
    wait_time = lambda self: 1

    @task(1)
    def login(self):
        # Send GET request to fetch the login page and extract any necessary tokens
        response = self.client.get("/login")


        login_data = {
            "user": "admin",
            "password": "admin"
        }

        # Add headers for JSON content type
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Origin": "http://localhost:3000",
            "Referer": "http://localhost:3000/login",
        }

        # Send POST request with login data in JSON format
        response = self.client.post(
            "/login",
            data=json.dumps(login_data),  # Send the data as JSON
            headers=headers
        )

        # Log the response details for debugging
        LOGGER.info(f"Login response status code: {response.status_code}")
        LOGGER.info(f"Login response text: {response.text}")

        # Check for successful login by examining the response
        if response.status_code == 200 and "grafana_session" in response.cookies:
            LOGGER.info("Login successful")
        else:
            LOGGER.error("Login failed")



    @task(2)
    def index(self):
        self.client.get("/")


    @task(4)
    def dashboards(self):
        self.client.get("/dashboards")

    @task(4)
    def alerting(self):
        self.client.get("/alerting")


    @task(2)
    def search_dashboards(self):
        self.client.get("/dashboards/find?query=my_dashboard")

    @task(3)
    def explore_dashboard(self):
        self.client.get("/d/dashboard_uid/my-dashboard")

    @task(1)
    def create_dashboard(self):
        self.client.get("/dashboards/new")


    @task(2)
    def alert_rules(self):
        self.client.get("/alerting/rules")

    @task(2)
    def data_sources(self):
        self.client.get("/datasources")

    @task(1)
    def create_alert(self):
        self.client.get("/alerting/alerts/new")


# Event hooks for logging
@events.request.add_listener
def request_handler(request_type, name, response_time, response_length, **kwargs):
    LOGGER.info(f'Request: {request_type}, Name: {name}, Response Time: {response_time}, Response Length: {response_length}')

@events.test_start.add_listener
def test_start(**kwargs):
    LOGGER.info('Test started!')

@events.test_stop.add_listener
def test_stop(**kwargs):
    LOGGER.info('Test stopped!')

@events.quitting.add_listener
def quitting(**kwargs):
    LOGGER.info('Quitting fired!')

