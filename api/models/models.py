from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    fullname: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Lorem Ipsum Dolor",
                "email": "abcd123@haha.dev",
                "password": "3xt3m#",
            }
        }

    class Settings:
        name = "user"

class UserData(BaseModel):
    fullname: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Lorem Ipsum Dolor",
                "email": "abcd123@haha.dev",
            }
        }

class UserSignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {
                "username": "abcd123@haha.dev",
                "password": "3xt3m#"
            }
        }
