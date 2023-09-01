from pydantic import BaseModel
from fastapi import UploadFile

class CSVFile(BaseModel):
    file: UploadFile

class ApiKeyRequest(BaseModel):
    apikey: str