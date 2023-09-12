from datetime import datetime

from fastapi import APIRouter, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.dependencies import Pagination, pagination_parameters
from app.models import User, UserInDB
from app.shared_schemas import (ListResponseSchema, ResponseSchema,
                                ResponseSchemaWithData)

router = APIRouter(prefix="/users")


@router.post("", tags=["User"], responses={201: {"model": ResponseSchemaWithData}})
async def create_user(user: User):
    user_in_db = UserInDB(
        name=user.name,
        password=user.password,
        age=user.age,
        role=user.role,
        id=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    response = ResponseSchemaWithData(
        success=True, message="User created", data=user_in_db
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(response.dict(by_alias=True)),
    )


@router.get(
    "/{user_id}", tags=["User"], responses={200: {"model": ResponseSchemaWithData}}
)
async def get_user(user_id: int):
    user_in_db = UserInDB(
        name="test",
        password="test",
        age=123,
        role="MANAGER",
        id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    response = ResponseSchemaWithData(
        success=True, message="User found", data=user_in_db
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(response.dict(by_alias=True)),
    )


@router.get("", tags=["User"], responses={200: {"model": ListResponseSchema}})
async def get_users(
    request: Request, pagination: dict = Depends(pagination_parameters)
):
    user_in_db = UserInDB(
        name="test",
        password="test",
        age=123,
        role="MANAGER",
        id=123,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    response = ListResponseSchema(
        success=True,
        message="User found",
        data=[user_in_db, user_in_db, user_in_db],
        pagination=Pagination.parse_obj(
            {
                "total": 3,
                "page_size": pagination["page_size"],
                "pages": 1,
                "page": pagination["page"],
                "links": {
                    "previous": "/health",
                    "next": "/health",
                    "self": "/health",
                },
            }
        ),
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(response.dict(by_alias=True)),
    )


@router.put(
    "/{user_id}", tags=["User"], responses={200: {"model": ResponseSchemaWithData}}
)
async def update_user(user_id: int, user: User):
    user_in_db = UserInDB(
        name=user.name,
        password=user.password,
        age=user.age,
        role=user.role,
        id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    response = ResponseSchemaWithData(
        success=True, message="User updated", data=user_in_db
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(response.dict(by_alias=True)),
    )


@router.delete("/{user_id}", tags=["User"], responses={200: {"model": ResponseSchema}})
async def delete_user(user_id: int):

    response = ResponseSchema(success=True, message="User deleted")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(response.dict(by_alias=True)),
    )
