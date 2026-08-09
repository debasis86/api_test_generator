import requests
import pytest

BASE_URL = "https://petstore.swagger.io/v2"

def test_get_pet_by_id_success():
    """
    Test case for successful retrieval of a pet by ID (200 OK).
    """
    pet_id = 1 # Assuming pet with ID 1 exists
    response = requests.get(f"{BASE_URL}/pet/{pet_id}")

    assert response.status_code == 200
    assert response.json() is not None
    assert "id" in response.json()
    assert response.json()["id"] == pet_id
    # Add more assertions for expected pet properties if known from schema
    assert "name" in response.json()
    assert "status" in response.json()

def test_get_pet_by_id_invalid_id():
    """
    Test case for invalid pet ID (400 Bad Request).
    """
    invalid_pet_id = "abc" # Invalid ID type
    response = requests.get(f"{BASE_URL}/pet/{invalid_pet_id}")

    assert response.status_code == 400
    assert response.json() is not None
    assert "message" in response.json()
    assert response.json()["message"] == "Invalid ID supplied" # Example message based on OpenAPI spec

def test_get_pet_by_id_not_found():
    """
    Test case for pet not found (404 Not Found).
    """
    non_existent_pet_id = 999999999 # A very high ID unlikely to exist
    response = requests.get(f"{BASE_URL}/pet/{non_existent_pet_id}")

    assert response.status_code == 404
    assert response.json() is not None
    assert "message" in response.json()
    assert response.json()["message"] == "Pet not found" # Example message based on OpenAPI spec
