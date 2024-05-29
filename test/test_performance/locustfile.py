from locust import HttpUser, task, between

class ProjectPerfTest(HttpUser):
    # wait_time = between(5, 15)

    @task
    def index(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.post("/showSummary", {
            "email": "admin@irontemple.com"
        })

    @task
    def book(self):
        self.client.get("/book/Spring Festival/Simply Lift")

    @task
    def purchasePlaces(self):
        self.client.post("/purchasePlaces", {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "1"
        })

    @task
    def logout(self):
        self.client.get("/logout")