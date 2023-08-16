from beanie import Document
from pydantic import EmailStr


class User(Document):
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
