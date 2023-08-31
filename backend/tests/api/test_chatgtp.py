from fastapi.testclient import TestClient

from app.core.config import settings

valid_api_key = "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"
invalid_api_key = "ghp_YyshuBLjejeGZB4i9tAKrexPp0cTumd0Mqbn9"


def test_upload_file_valid_api_key():

    with open("example.csv", "rb") as file:
        csv_data = file.read()

    response = client.post( settings.API_PATH +
        "/upload-file",
        files={"file": ("example.csv", csv_data)},
        data={"api_key": valid_api_key}
    )
    assert response.status_code == 200
    assert "CSV uploaded and initial analysis generated" in response.json()["message"]
    assert "data_description" in response.json()

def test_upload_file_empty_csv():
    with open("empty.csv", "r") as file:
        csv_data = file.read()
    response = client.post(settings.API_PATH +
        "/upload-file",
        files={"file": ("empty.csv", csv_data)},
        data={"api_key": valid_api_key}
    )
    assert response.status_code == 400
    assert "Uploaded CSV is empty" in response.json()["error"]

def test_upload_file_invalid_api_key():
    with open("example.csv", "r") as file:
        csv_data = file.read()
    response = client.post(settings.API_PATH +
        "/upload-file",
        files={"file": ("data.csv", csv_data)},
        data={"api_key": invalid_api_key}
    )
    assert response.status_code == 401

# Test Integration
def test_upload_file_integration():
    with open("example.csv", "rb") as file:
        csv_data = file.read()
    response = client.post(settings.API_PATH +
        "/upload-file",
        files={"file": ("data.csv", csv_data)},
        data={"api_key": valid_api_key}
    )
    assert response.status_code == 200
    assert "CSV uploaded and initial analysis generated" in response.json()["message"]
    assert "data_description" in response.json()