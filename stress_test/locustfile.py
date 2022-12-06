from locust import HttpUser,task, between


class APIUser(HttpUser):

    # Put your stress tests here.
    # See https://docs.locust.io/en/stable/writing-a-locustfile.html for help.
    # TODO

    wait_time = between(1,5)

    @task
    def index(self):
        self.client.get("http://0.0.0.0/")
    
    @task
    def model(self):
        file = [('file', ('dog.jpeg', open("dog.jpeg", "rb"), "image/jpeg"))]
        headers = {}
        payload = {}
        self.client.post("http://0.0.0.0/predict", files=file, headers=headers)

#Si uso "payload" como argumento para el post me tira errores, 
# lo quité y funciona bien: - 
# self.client.post("http://0.0.0.0/predict", headers=headers, files=files)