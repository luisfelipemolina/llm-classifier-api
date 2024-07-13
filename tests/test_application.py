import json
from fastapi.testclient import TestClient

from app.definition import app_definition

app = app_definition()

client = TestClient(app)

def test_response_healthchecker_sucess():
    response = client.get("/health")
    assert response.status_code == 200

def test_response_classify_product_success():
    data = {"cnae_number": "4722902", "item_description": ["sal grosso cisne 1kg", "gasolina comum"], "provider":  "google"}
    response = client.post("/classify_product", json=data)
    
    assert response.status_code == 200


def test_response_list_log_events_bad_request():
    data = {"cnae_number": "4722902", "item_description": ["sal grosso cisne 1kg", "gasolina comum"]}
    response = client.post("/classify_product", json=data)
    
    assert response.status_code == 422
