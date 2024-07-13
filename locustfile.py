from locust import HttpUser, task

class TestClassifyProduct(HttpUser):
    @task
    def test_classify_product(self):
        self.client.post("/classify_product", json={"cnae_number": "4789099", "item_description": ["sal grosso cisne 1kg"], "provider":  "google"}
)