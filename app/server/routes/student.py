#In the "routes" folder, create a new file called 
#student.py and add the following content to it:
#Chúng tôi sẽ sử dụng Bộ mã hóa tương thích JSON từ FastAPI để chuyển đổi 
#các mô hình của chúng tôi sang định dạng tương thích với JSON.
from fastapi import APIRouter, Body,Depends
from fastapi.encoders import jsonable_encoder
from auth.auth_bearer import JWTBearer

from server.database import (
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    update_student,
    # add_user,
)
from models.student import (
    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel,
)

# from server.database import (
#     add_user, 
# )

# from models.users import (
#     ErrorResponseModel,
#     ResponseModel,
#     UserregisterSchema,
#     # UpdateStudentModel,
# )


router = APIRouter()

#Nếu ứng dụng của bạn (bằng cách nào đó) không phải giao tiếp với bất kỳ 
#thứ gì khác và đợi nó phản hồi, hãy sử dụng async def.

#async có nghĩa là ngôn ngữ 💬 có cách để nói với máy tính / chương trình 🤖 
#rằng tại một thời điểm nào đó trong mã, nó 🤖 sẽ phải đợi một thứ khác 
#kết thúc ở một nơi khác. Giả sử rằng một thứ khác được gọi là "tệp chậm" 📝


#wait thường đề cập đến các hoạt động I / O tương đối "chậm" (so với tốc độ của bộ xử lý và bộ nhớ RAM), như chờ đợi:

#dữ liệu từ máy khách được gửi qua mạng
#dữ liệu do chương trình của bạn gửi để khách hàng nhận được thông qua mạng
#nội dung của một tệp trong đĩa được hệ thống đọc và cấp cho chương trình của bạn
#nội dung mà chương trình của bạn đã cung cấp cho hệ thống được ghi vào đĩa
#một hoạt động API từ xa
#một hoạt động cơ sở dữ liệu để kết thúc
#một truy vấn cơ sở dữ liệu để trả về kết quả
#Vân vân.

#Vì thời gian thực hiện được sử dụng chủ yếu bởi việc chờ đợi các hoạt động 
#I / O , họ gọi chúng là các hoạt động "I / O ràng buộc".

#Nó được gọi là "không đồng bộ" vì máy tính / chương trình không cần phải 
#"đồng bộ hóa" với tác vụ chậm, đợi thời điểm chính xác mà tác vụ kết thúc, 
#trong khi không làm gì, để có thể nhận kết quả tác vụ và tiếp tục công việc. .

#Các phiên bản Python hiện đại có một cách rất trực quan để 
#xác định mã không đồng bộ. Điều này làm cho nó trông giống như mã "tuần tự" 
#bình thường và thực hiện "đang chờ" bạn vào đúng thời điểm.

#Để await hoạt động, nó phải ở bên trong một chức năng hỗ trợ tính không đồng bộ 
#này. Để làm điều đó, bạn chỉ cần khai báo nó với async def:


  #ví dụ trong một model thông qua pydantic để chuyển 
    #đổi dữ liệu thành đối tượng json nhưng trong model 
    #có một số filed ko thể chuyền thành đối tượng json được nên ta phải 
    #sử dụng jsonable_encoder để toàn bộ các filed của đối tượng đó chuyển 
    #về dạng json
    # print(student)
    #await là nó phải trờ cho tác vụ của await add_student(student) xong 
    #thì mới lưu vào new_student

@router.post("/",response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)):
    ## using the JSON Compatible Encoder from FastAPI to convert our models into a format that's JSON compatible.
    student = jsonable_encoder(student) 
    new_student = await add_student(student)
    return ResponseModel(new_student, "Student added successfully.")


@router.get("/",response_description="Students retrieved")
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")


@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id):
    student = await retrieve_student(id)
    # print(student)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")


@router.put("/{id}",dependencies=[Depends(JWTBearer())],response_description="update")
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}#kiểm tra xem giá trị update có không
    updated_student = await update_student(id, req)
    if updated_student:
        return ResponseModel(
            # "Student with ID: {} name update is successful".format(id),
            updated_student,
            "Student name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )

@router.delete("/{id}",dependencies=[Depends(JWTBearer())],response_description="Student data deleted from the database")
async def delete_student_data(id: str):
    deleted_student = await delete_student(id)
    if deleted_student:
        return ResponseModel(
            "Student with ID: {} removed".format(id), "Student deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Student with id {0} doesn't exist".format(id)
    )


# #user
# @router.post("/user/register", response_description="add User")
# async def add_user_data(user: UserregisterSchema = Body(...)):
#     ## using the JSON Compatible Encoder from FastAPI to convert our models into a format that's JSON compatible.
#     # student = jsonable_encoder(student) 
#     new_user = await add_user(user)
#     return ResponseModel(new_user, "user added successfully.")

