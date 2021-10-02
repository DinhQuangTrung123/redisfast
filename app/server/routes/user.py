from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder



from server.database import (
    add_user, 
    check_user
)

from models.users import (
    ErrorResponseModel,
    ResponseModel,
    UserregisterSchema,
    UserloginSchema
    # UpdateStudentModel,
)

routeruser = APIRouter()



@routeruser.post("/register", response_description="add User")
async def add_user_data(user: UserregisterSchema = Body(...)):
    ## using the JSON Compatible Encoder from FastAPI to convert our models into a format that's JSON compatible.
    user = jsonable_encoder(user) 
    new_user = await add_user(user)
    # print(new_user.email)
    # return ResponseModel(new_user, "user added successfully.")
    return {"Token":new_user}

@routeruser.post("/login",response_description="login User")
async def user_login(user: UserloginSchema = Body(...)):
    user=await check_user(user)
    if user:
        return {"Token":user}
    return {
        "error": "Wrong login details!"
    }



