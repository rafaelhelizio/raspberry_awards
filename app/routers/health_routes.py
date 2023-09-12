from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.shared_schemas import ResponseSchema

router = APIRouter()


@router.get("/health", tags=["Health"], responses={200: {"model": ResponseSchema}})
async def health_check():
    response = ResponseSchema(success=True, message="I'm alive")
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(response.dict())
    )
