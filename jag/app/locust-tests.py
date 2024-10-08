from locust import HttpLocust, TaskSet, task
import resource

resource.setrlimit(resource.RLIMIT_NOFILE, (15000, 15000))

class ZstreamTests(TaskSet):
    @task
    def index(self):
        self.client.get("/")

    @task
    def static_css(self):
        self.client.get("/static/css/style.default.css")

    @task
    def api_list(self):
        self.client.get("/api/streams/")

    @task
    def videoplayer(self):
        self.client.get("/player/bsod")

class WebsiteUser(HttpLocust):
    task_set = ZstreamTests
    min_wait = 5000
    max_wait = 20000
