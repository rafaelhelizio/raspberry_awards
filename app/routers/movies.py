from fastapi import APIRouter, Response, UploadFile
from fastapi.responses import JSONResponse
from app.use_cases.movies import get_intervals, upload_csv
from app.schema.movies import ResponseErrorFileSchema, ResponseFileSchema, WinnersResponse

app = APIRouter()

@app.post("/upload/", response_model=ResponseFileSchema, responses={422: {"model": ResponseErrorFileSchema}})
async def upload_csv_endpoint(file: UploadFile):
    try:
        if file.content_type != "text/csv":
            return JSONResponse(status_code=422, content={"message": "Only CSV files"})
        
        file_content = await file.read()
        
        result = upload_csv(file_content)
        if result:
            return JSONResponse(status_code=200, content={"message": "Upload completed successfully"})
        else:
            return JSONResponse(status_code=500, content={"message": "Error when uploading"})

    except Exception as e:
        return {"error": str(e)}


@app.get("/winners/", response_model=WinnersResponse)
async def get_intervals_endpoint():
    try:
        return get_intervals()
    except Exception as e:
        return {"error": str(e)}
