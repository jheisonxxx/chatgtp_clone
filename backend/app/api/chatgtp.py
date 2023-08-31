from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
import openai
import pandas as pd
from pydantic import BaseModel
import os

router = APIRouter(prefix="/chatgtp")

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
MAX_ROWS = 100  # Límite máximo de filas

@router.post("/verify_apikey")
def is_api_key_valid(api_key: str = ''):
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt="This is a test.",
            max_tokens=5
        )
        if response['id'] is not None:
            return JSONResponse(content={
                "message": "Valid API token. You can use de API."
            }, status_code=200)
        else:
            return JSONResponse(content={
                "message": "API token invalid. Verify your token and the configuration.",
            }, status_code=401)

    except Exception as e:
        return JSONResponse(content={
            "message": "Error to validate API token:",
            "data_description": str(e)
        }, status_code=401)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def verify_csv(file: UploadFile):

    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido")

    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Tipo de archivo incorrecto")

    file_start_position = file.file.tell()
    file_content = file.file.read()
    file_size = file.file.tell() - file_start_position  # Tamaño del archivo sin cargar en memoria
    file.file.seek(file_start_position)

    if file_size > 1024 * 1024:  # 1MB
        raise HTTPException(status_code=400, detail="El archivo es demasiado grande")

    df = pd.read_csv(file.file)
    # Verificar cantidad de columnas
    if len(df.columns) > 10:  # Cambiar el número según tus necesidades
            raise HTTPException(status_code=400, detail="Cantidad incorrecta de columnas")

    # Limitar la cantidad de filas
    if len(df) > MAX_ROWS:
        raise HTTPException(status_code=400, detail=f"Se excede el límite máximo de filas ({MAX_ROWS})")

    return df

class CSVFile(BaseModel):
    file: UploadFile




@router.post('/upload-file')
def upload_file(file: UploadFile = File(...), api_key: str = ''):
    response = is_api_key_valid(api_key)
    if response.status_code == 200:
        df = verify_csv(file)
        try:
            # Analizar columnas y generar una descripción inicial usando ChatGPT
            columns = ", ".join(df.columns)
            description_prompt = f"Este es un CSV con las siguientes columnas: {columns}. ¿Puedes proporcionar una descripción inicial de los datos y sugerir análisis?"

            chat_response = openai.Completion.create(
                engine="davinci",
                prompt=description_prompt,
                max_tokens=150
            )

            # Interpretar la respuesta generada por ChatGPT y presentarla al usuario
            analysis_suggestions = chat_response.choices[0].text.strip()

            return JSONResponse(content={
                "message": "CSV uploaded and initial analysis generated",
                "data_description": analysis_suggestions
            }, status_code=200)

        except pd.errors.EmptyDataError:
            return JSONResponse(content={"error": "Uploaded CSV is empty"}, status_code=400)
        except Exception as e:
            return JSONResponse(content={"error": "No puedo darte un analisis ahora"}, status_code=500)

    else:
        return response

