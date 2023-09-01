import os
from http import client

import requests
from app.core.config import settings




def test_upload_file_valid_api_key():
    url = "http://172.25.0.4:9000" + settings.API_PATH + "/is_api_key_valid"
    data = {"api_key": os.environ.get("VALID_API_KEY")}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert "CSV uploaded and initial analysis generated" in response.json()["message"]
    assert "data_description" in response.json()

def test_upload_file_empty_csv():
    with open("tests/files/empty.csv", "r") as file:
        csv_data = file.read()
    url = "http://172.25.0.4:9000" + settings.API_PATH + "/upload-file"
    files = {"file": ("example.csv", csv_data)}
    data = {"api_key": os.environ.get("VALID_API_KEY")}

    response = requests.post(url, files=files, data=data)
    assert response.status_code == 400
    assert "Uploaded CSV is empty" in response.json()["error"]


def test_upload_file_invalid_api_key():
    url = "http://172.25.0.4:9000" + settings.API_PATH + "/is_api_key_valid"
    data = {"api_key": os.environ.get("INVALID_API_KEY")}
    response = requests.post(url, data=data)
    assert response.status_code == 401

# Test Integration
def test_upload_file_integration():
    with open("tests/files/example.csv", "rb") as file:
        csv_data = file.read()
    url = "http://172.25.0.4:9000" + settings.API_PATH + "/upload-file"
    files = {"file": ("example.csv", csv_data)}
    data = {"api_key": os.environ.get("VALID_API_KEY")}

    response = requests.post(url, files=files, data=data)
    assert response.status_code == 200
    assert "CSV uploaded and initial analysis generated" in response.json()["message"]
    assert "data_description" in response.json()