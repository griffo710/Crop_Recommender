from app import app
from services.validator import InputValidator

validator = InputValidator()

def test_api_success():
    client = app.test_client()

    response = client.post("/api/recommend", json={
        "N": 90, "P": 40, "K": 90,
        "temperature": 25, "humidity": 80,
        "ph": 6.5, "rainfall": 200
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_api_no_data():
    client = app.test_client()

    response = client.post("/api/recommend", json={})

    assert response.status_code == 400


def test_extreme_warnings():
    response = {
        "N": 90, "P": 40, "K": 90,
        "temperature": 25, "humidity": 80,
        "ph": 1, "rainfall": 200
    }

    
    errors, warnings, clean_data = validator.validate(response)

    assert "Soil is extremely acidic" in warnings[0]

def test_unexpected_key_warning():
    data = {
        "N": 90, "P": 40, "K": 90,
        "temperature": 25, "humidity": 80,
        "ph": 6.5, "rainfall": 200,
        "extra": 100
    }

    errors, warnings, clean_data = validator.validate(data)

    assert len(warnings) > 0

def test_valid_input():
    data = {
        "N": 90, "P": 40, "K": 90,
        "temperature": 25, "humidity": 80,
        "ph": 6.5, "rainfall": 200
    }

    errors, warnings, clean_data = validator.validate(data)

    assert errors == []
    assert clean_data["N"] == 90.0
