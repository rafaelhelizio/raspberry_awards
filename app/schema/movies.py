
from pydantic import BaseModel, Field

class Winners(BaseModel):
    producer: str = Field(example="Producer 1")
    interval: int = Field(example=1)
    previousWin: int = Field(example=2008)
    followingWin: int = Field(example=2009)

class WinnersResponse(BaseModel):
    min: Winners
    max: Winners


class ResponseFileSchema(BaseModel):
    message: str = Field(default="Upload completed successfully")

class ResponseErrorFileSchema(BaseModel):
    message: str = Field(default="Only CSV File")
