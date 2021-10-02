import time 
from typing import Dict
import jwt
#decoupledùng để đọc biến môi trường .env
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    # return {
    #     "access_token": token
    # }
    return token

def token_responserefress(refresstoken: str):
    # return {
    #     "refress_token": refresstoken
    # }
    return refresstoken



def signJWT(user_email:str) ->Dict[str,str]:
    payload={
        "user_email":user_email,
        "expires":time.time()+600 #là 10 phút
    }
    token= jwt.encode(payload,JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def signJWTrefress(user_email:str) ->Dict[str,str]:
    payload={
        "user_email":user_email,
        "expires":time.time()+3600 #là 1 tiếng
    }
    refresstoken= jwt.encode(payload,JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(refresstoken)



def decodeJWT(token:str)->dict:
    try:
        decode_token = jwt.decode(token,JWT_SECRET , algorithms= [JWT_ALGORITHM])
        return decode_token if decode_token["expires"] >=time.time() else None
    except:
        return{}



def decoderefressJWT(token:str)->dict:
    try:
        decode_refresstoken = jwt.decode(refresstoken,JWT_SECRET , algorithms= [JWT_ALGORITHM])
        return decode_refresstoken if decode_refresstoken["expires"] >=time.time() else None
    except:
        return{}