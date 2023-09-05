import os
from httpx import AsyncClient
from app.core.config import settings


class TestValidationApikey:
    async def test_valid_api_key(self, client: AsyncClient):
        url = os.environ.get("URL_TESTS") + settings.API_PATH + "/chatgtp/verify_apikey"
        data = {"apikey": os.environ.get("VALID_API_KEY")}
        response = await client.post(url, json=data)
        assert response.status_code == 200


    async def test_invalid_api_key(self, client: AsyncClient):
        url = os.environ.get("URL_TESTS") + settings.API_PATH + "/chatgtp/verify_apikey"
        data = {"apikey": os.environ.get("INVALID_API_KEY")}
        response = await client.post(url, json=data)
        assert response.status_code == 401


class TestUploadFile:
    async def test_upload_file_empty_csv(self, client: AsyncClient):
        with open("tests/files/empty.csv", "r") as file:
            csv_data = file.read()
        url = os.environ.get("URL_TESTS") + settings.API_PATH + "/chatgtp/upload-file"
        files = {"file": ("example.csv", csv_data)}
        data = {"apikey": os.environ.get("VALID_API_KEY")}

        response = await client.post(url, files=files, data=data)
        assert response.status_code == 400
        assert "Uploaded CSV is empty" in response.json()["error"]


    # Test Integration
    async def test_upload_file_integration(self, client: AsyncClient):
        with open("tests/files/example.csv", "rb") as file:
            csv_data = file.read()
        url = os.environ.get("URL_TESTS") + settings.API_PATH + "/chatgtp/upload-file"
        files = {"file": ("example.csv", csv_data)}
        data = {"apikey": os.environ.get("VALID_API_KEY")}

        response = await client.post(url, files=files, data=data)
        assert response.status_code == 200
        assert "CSV uploaded and initial analysis generated" in response.json()["message"]
        assert "data_description" in response.json()