
from typing import Dict
from pydantic import BaseModel, Field

class Winners(BaseModel):
    producer: str = Field(example="Producer 1")
    interval: int = Field(example=1)
    previousWin: int = Field(example=2008)
    followingWin: int = Field(example=2009)

class WinnersResponse(BaseModel):
    min: Winners
    max: Winners