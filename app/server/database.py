import motor.motor_asyncio

#bson comes installed as a dependency of motor.
#bson được cài đặt như một phụ thuộc của motor
from bson.objectid import ObjectId
from auth.auth_handler import signJWT,signJWTrefress

MONGO_DETAILS = "mongodb://127.0.0.1:27017" #connect 
#Trong đoạn mã trên, chúng tôi đã nhập Motor, xác định chi tiết kết nối và tạo một ứng dụng khách qua AsyncIOMotorClient .
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

databasestudent = client.students #We then referenced a database called students 
# databaseuser = client.users
#collection students_collection nó giống như là bảng
student_collection = databasestudent.get_collection("students_collection")
users_collection = databasestudent.get_collection("users_collection")
middleware_collection = databasestudent.get_collection("middleware_collection")
backgroundtasks_collection = databasestudent.get_collection("backgroundtasks_collection")
#chúng ta đã định nghĩa các hoạt động không đồng bộ để tạo, đọc, cập nhật và xóa dữ liệu sinh viên trong cơ sở dữ liệu thông qua motor
#Trong thao tác cập nhật và xóa, sinh viên được tìm kiếm trong cơ sở dữ liệu 
#để quyết định có thực hiện thao tác đó hay không. Giá trị trả về hướng dẫn 
#cách gửi phản hồi cho người dùng mà chúng tôi sẽ làm việc trong phần tiếp theo.


#database và colection sẽ được tạo nếu chúng chưa tồn tại.
#Tiếp theo, tạo một hàm trợ giúp nhanh để phân tích kết quả 
#từ một truy vấn cơ sở dữ liệu thành một câu lệnh Python.
#create a quick helper function for parsing the results from a database 
#query into a Python dict.

def student_helper(student):
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
        "Image":student["iamge"]
    }

def user_helper(user):
    return {
        "id":str(user["_id"]),
        "fullname":user["fullname"],
        "email":user["email"],
        "password":user["password"]
    }

def middleware_helper(time):
    return {
        "id":str(time["_id"]),
        "respone":str(time["time"])
    }

def backgroundtask_helper(email):
    return {
        "id":str(email["_id"]),
        "respone":str(email["time"])
    }





# Retrieve all students present in the database
async def retrieve_students():
    students = []
    # async for student in student_collection.find():
    for student in await student_collection.find().to_list(length=1000):
        students.append(student_helper(student))
    return students
    # return student_helper(students)
#insert_one
#If the document does not specify an _id field, then mongod 
#will add the _id field and assign(gán) a unique ObjectId() for 
#the document before inserting. Most drivers create an ObjectId 
#and insert the _id field, but the mongod will create and populate 
#the _id if the driver or application does not


#The insert_one method response includes the _id of the newly created student. 
#After we insert the student into our collection, we use the inserted_id to 
#find the correct document and return this in our JSONResponse.


# Add a new student into to the database
async def add_student(student_data: dict):
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)

# Retrieve a student with a matching ID
async def retrieve_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


# Update a student with a matching ID
async def update_student(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        # if updated_student:
        #     # return True
        #     return True
        # return False
    if (student := await student_collection.find_one({"_id": ObjectId(id)})) is not None:
        # print("lalalala")
        # print(student_helper(existing_student))
        return student_helper(student)



# Delete a student from the database
async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    findemail = await student_collection.find_one({"status":False})
    print(findemail)
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True



#user
async def add_user(user_data: dict):
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    # return signJWT(new_user)
    # print(new_user)
    return {
            "accesstoken":signJWT(user_helper(new_user)),
            "refressaccesstoken":signJWTrefress(user_helper(new_user))
        }
    # return signJWT(user_helper(new_user))
        # signJWTrefress(user_helper(new_user))



async def check_user(data: dict):
    user = await users_collection.find_one({"password": data.password,"email":data.email})
    # print(data.password)
    # useremail = users_collection.find({"email":data.email})
    # print(useremail)
    # print(user)
    if user:
        return {
            "accesstoken":signJWT(user_helper(user)),
            "refressaccesstoken":signJWTrefress(user_helper(user))
        }
    return {}


async def add_middleware(middleware_data: dict):
    middleware = await middleware_collection.insert_one(middleware_data)
    new_middleware = await middleware_collection.find_one({"_id": middleware.inserted_id})
    return middleware_helper(new_middleware)

async def add_backgroundtask(backgroundtask_data: dict):
    backgroundtask = await backgroundtasks_collection.insert_one(backgroundtask_data)
    new_backgroundtask = await backgroundtasks_collection.find_one({"_id": backgroundtask.inserted_id})
    return backgroundtask_helper(new_backgroundtask)



