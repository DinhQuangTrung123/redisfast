from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserregisterSchema(BaseModel):
    fullname: str =Field(...)
    email : EmailStr =Field(...)
    password :str =Field(...)

    class Config:
        schema_extra={
            "example":{
                "fullname":"myname",
                "email":"example@gmail.com",
                "password":"password",
                # "status":False
            }
        }


class UserloginSchema(BaseModel):
    email :EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra={
            "example":{
                "email":"example@gmail.com",
                "password":"password"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
