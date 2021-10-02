from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI

#In the code above, we defined a Pydantic Schema called StudentSchema that represents how the student data will be stored in your MongoDB database.

class StudentSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    course_of_study: str = Field(...)
    year: int = Field(..., gt=0, lt=9)
    gpa: float = Field(..., le=4.0)
    iamge :str = Field(...)

    #gtvà lttrong yeartrường đảm bảo rằng giá trị được truyền lớn hơn 0 và nhỏ hơn 9 
    #. Do đó, các giá trị như 0 , 10 , 11 , sẽ dẫn đến lỗi.

    #letrình xác thực trong gpa trường đảm bảo rằng giá trị được truyền nhỏ hơn hoặc bằng 4,0 .

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources engineering",
                "year": 2,
                "gpa": "3.0",
                "iamge":"iamge",
            }
        }


class UpdateStudentModel(BaseModel):
    fullname: Optional[str] #Optional là một kiểu khai báo biết tùy chọn và nó cũng có thể là none
    email: Optional[EmailStr]
    course_of_study: Optional[str]
    year: Optional[int]
    gpa: Optional[float]
    image: Optional[str] 

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources and environmental engineering",
                "year": 4,
                "gpa": "4.0",
                "iamge": "image",
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

#FastAPI sử dụng Lược đồ Pyantic 
#để tự động ghi lại các mô hình dữ liệu kết hợp với Lược đồ Json 
#. Sau đó, giao diện người dùng Swagger hiển thị dữ liệu từ các 
#mô hình dữ liệu đã tạo.