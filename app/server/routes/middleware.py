import time
from fastapi import Request,APIRouter

from models.middleware import (
    ErrorResponseModel,
    ResponseModel,
    Middlewarechema
)

from server.database import (
    add_middleware,
)


routerMiddleware = APIRouter()

# @routerMiddleware.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     middleware = await add_middleware()
#     if middleware:
#         return ResponseModel(middleware, "middleware data retrieved successfully")
#     return ResponseModel(middleware, "Empty list returned")
#     # return response
