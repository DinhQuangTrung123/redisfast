from typing import Optional
from fastapi import FastAPI

from pydantic import BaseModel,Field
#In the code above, we defined a Pydantic Schema called StudentSchema that represents how the student data will be stored in your MongoDB database.

class Middlewarechema(BaseModel):
    time: str = Field(...)

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

