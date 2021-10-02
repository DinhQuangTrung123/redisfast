from fastapi import FastAPI,Request,BackgroundTasks
from server.routes.student import router as StudentRouter
from server.routes.user import routeruser as UserRouter
from server.routes.middleware import routerMiddleware as MiddlewareRouter
from fastapi import FastAPI, File, UploadFile,Form
import time
from fastapi.encoders import jsonable_encoder
app = FastAPI()# gọi constructor và gán vào biến app
from time import sleep
# timetoresquest=[]
from server.redisfastapi.apiredis import *




from models.middleware import (
    ErrorResponseModel,
    ResponseModel,
    Middlewarechema
)

from server.database import (
    add_middleware,
    middleware_collection,
    add_backgroundtask,
    backgroundtasks_collection,  
)


from models.backgroundtask import(
    Backgroundtaskchema,
    ResponseModel,
    ErrorResponseModel
)


def middleware_helper(time):
    return {
        "id":str(time["_id"]),
        "respone":str(time["time"])
}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    # middleware1 = jsonable_encoder(response) 
    middleware = await middleware_collection.insert_one({"time":response.headers["X-Process-Time"]})
    new_middleware = await middleware_collection.find_one({"_id": middleware.inserted_id})
    # print(new_middleware)
    # a = middleware_helper(new_middleware)
    # middleware1 = jsonable_encoder(response) 
    # middleware = await add_middleware(middleware1)
    # return ResponseModel(middleware, "Empty list returned")
    # return middleware_helper(new_middleware)
    # print(response.headers["X-Process-Time"])
    return response


# def write_notification(email: str, message=""):
#     with open("log.txt", mode="w") as email_file:
#         content = f"notification for {email}: {message}"
#         email_file.write(content)
#         return content

# def sen_mail(message):
#     sleep(5)
#     print("sending mail: ",message)

# @app.post("/send-notification",tags=["postbackgroundtasksemail"])
# async def send_notification(background_tasks: BackgroundTasks):
#     background_tasks.add_task(sen_mail,"some notification")
#     # print(BackgroundTasks)
#     return {"message": "Notification sent in the background"}

from pydantic import BaseModel

class product(BaseModel):
    product: str
   


@app.post("/order/", tags=["redis"])#Tags are identifiers used to group routes. Routes with the same tags are grouped into a section on the API documentation.
async def nameorder_redis(Product:product):# do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    print(Product)
    Producer.publish('product',Product.product)
    print(Product.product)
    # print(Producer.publish('product',Product.product))
    # print(Producer.publish('product',Product.product))
    # Producer.publish('Order', Product.product)
    # print(Product.product)
    # print(Producer.publish('Order', 'Order 1'))
    # data = {'api_dev_key':'http://localhost:5000/order/',
    #         'api_option':'paste',
    #         'api_paste_code':source_code,
    #         'api_paste_format':'python'
    # }
    return {"message": "Welcome to this fantastic app!"}



@app.get("/getorder/", tags=["redis"])#Tags are identifiers used to group routes. Routes with the same tags are grouped into a section on the API documentation.
async def nameorderget_redis():# do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    # bob_p.get_message()
    # # now bob can find alice’s music by simply using get_message()
    # new_music = bob_p.get_message()['data']
    # print(new_music)
    bob_p.subscribe('product')
    while True:
        data = bob_p.get_message()
        # print(data)
        if data:
            message = data['data']
            if message and message != 1:
                print("Message: {}".format(message))
        else: 
            break
        time.sleep(0.1)
    # new_music = bob_p.get_message()['data']
    # print(new_music)
    return {"message": "Welcome to this fantastic app!"}




@app.post("/add_redis/", tags=["redis"])#Tags are identifiers used to group routes. Routes with the same tags are grouped into a section on the API documentation.
async def append_redis():# do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    r.mset({"Germenay":"Berlin","France":"Paris"})
    #float,str,datetime...........................
    return {"message": "Welcome to this fantastic app!"}


@app.get("/get_redis/", tags=["redis"])#Tags are identifiers used to group routes. Routes with the same tags are grouped into a section on the API documentation.
async def append_redis():# do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    # get_redis = r.get({"Germenay"})
    try:
        # print(r)
        # b = r.mset({"contruy1":"Berlin"})
        get_redis = r.get("France")
        # -->dict 
        # get_redis = r.get("France")
        # get_redis = r.get("contruy1")
        # print(get_redis)
        # print("vào")
    except Exception as e:
        print(e)
    return get_redis



def write_notification(email: str, message=""):
    sleep(5)
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)





@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    print(email)
    print(background_tasks)
    # print(write_notification(email,"some notification"))
    backgroundtask = await backgroundtasks_collection.insert_one({"resqest_background":str(background_tasks)})
    new_backgroundtask = await backgroundtasks_collection.find_one({"_id": backgroundtask.inserted_id})
    return {"message": "Notification sent in the background"}



app.include_router(MiddlewareRouter, tags=["middleware"], prefix="/middleware")
app.include_router(StudentRouter, tags=["Student"], prefix="/student")
app.include_router(UserRouter, tags=["user"], prefix="/user")
#cái tag root này ta định nghĩa ở bên giao diện 
@app.get("/", tags=["Root"])#Tags are identifiers used to group routes. Routes with the same tags are grouped into a section on the API documentation.
async def read_root():# do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    return {"message": "Welcome to this fantastic app!"}

# @app.get("/studentapp", tags=["studentapp"])

@app.post("/files/",tags=["uploadfile"])
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@app.post("/uploadfile/",tags=["uploadfile"])
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}


@app.post("/predict",tags=["uploadfile"])
async def predict(
        industry: str = Form(...),
        file: UploadFile = File(...)
):
    # rest of your logic
    return {"industry": industry, "filename": file.filename}

