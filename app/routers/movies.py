from fastapi import FastAPI, File, UploadFile, HTTPException
from db.database import SessionLocal
from models.movies import Movie
import pandas as pd
import io
from use_cases import get_intervals, upload_csv

app = FastAPI()


@app.post("/upload/")
async def upload_csv_endpoint(file: UploadFile):
    try:
        if file.content_type != "text/csv":
            raise HTTPException(status_code=400, detail="Apenas arquivos CSV são permitidos.")

        contents = await file.read()

        db = SessionLocal()
        result = upload_csv(db, contents)
        db.close()

        return result

    except Exception as e:
        return {"error": str(e)}


@app.get("/winners/intervals/")
async def get_intervals_endpoint():
    return get_intervals()
