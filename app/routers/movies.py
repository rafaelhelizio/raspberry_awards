from threading import Thread
from fastapi import APIRouter, Response, UploadFile, HTTPException
from app.use_cases.movies import get_intervals, upload_csv
from app.schema.movies import WinnersResponse

app = APIRouter()

@app.post("/upload/")
async def upload_csv_endpoint(file: UploadFile):
    try:
        if file.content_type != "text/csv":
            raise HTTPException(status_code=400, detail="Only CSV files!")

        contents = await file.read()
        result = Thread(target=upload_csv, args=(contents,), daemon=False, name='ImportCSV')

        return Response(status_code=200) if result else HTTPException(status_code=500, detail="Internal error!")

    except Exception as e:
        return {"error": str(e)}


@app.get("/winners/intervals/", response_model=WinnersResponse)
async def get_intervals_endpoint():
    try:
        result = get_intervals()
        return result
    except Exception as e:
        return {"error": str(e)}
