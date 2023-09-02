from fastapi import File, UploadFile
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional, List
from utils.utils import Roles,Gender,Profession

# User Auth Models
class User_SignUp(BaseModel):
    email: EmailStr
    phone_number: PhoneNumber
    password: str
    confirm_password: str
    roles: Roles

    class Config:
        json_schema_extra = {
            "example": {
                "email": "abc123@gmail.com",
                "phone_number": "+918888887777",
                "password": "3xt3m#",
                "confirm_password": "3xt3m#",
                "roles": "job_seeker",
            }
        }

class User_SignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {
                "username": "abc123@gmail.com",
                "password": "3xt3m#",
            }
        }

class User_SignIn_Response(BaseModel):
    access_token: str
    roles: Roles

    class Config:
        josn_schema_extra = {
            "example": {
                "access_token": "fvbfhfjveu423634h4vc54g43v42ghc4234523456gveewr",
                "roles": "job_seeker"
            }
        }

# Job Seeker Profile Model
class Job_Seeker_Profile(BaseModel):
    fullname: Optional[str] = Field(default=None)
    college: Optional[str] = Field(default=None)
    email: EmailStr
    gender: Optional[Gender] = Field(default=None)
    phone_number: PhoneNumber
    date_of_birth: Optional[str] = Field(default=None)
    profession: List[Profession] = []
    about: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Loren Ipsum  Dolor",
                "college": "University of Virginia",
                "email": "abc123@gmail.com",
                "gender": "male",
                "phone_number": "+918888887777",
                "date_of_birth": "2002-05-05",
                "profession": ["student"],
                "about": "I am a student",
                "description": "I am a student",
            }
        }

# College Profile Model

class College_Profile(BaseModel):
    your_name: Optional[str] = Field(default=None)
    college_name: Optional[str] = Field(default=None)
    email: EmailStr
    address: Optional[str] = Field(default=None)
    phone_number: PhoneNumber
    no_of_students: Optional[int] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "your_name": "Loren Ipsum  Dolor",
                "college_name": "University of Virginia",
                "email": "abc123@gmail.com",
                "address": "IIT Delhi, Hauz Khas, New Delhi, 110016",
                "phone_number": "+918888887777",
                "no_of_students": "500",
            }
        }


# Recruiter Profile Model

class Recruiter_Profile(BaseModel):
    your_name: Optional[str] = Field(default=None)
    company_name: Optional[str] = Field(default=None)
    email: EmailStr
    address: Optional[str] = Field(default=None)
    phone_number: PhoneNumber
    linkedin: Optional[str] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "your_name": "Loren Ipsum  Dolor",
                "company_name": "employeeX",
                "email": "abc123@gmail.com",
                "address": "IIT Delhi, Hauz Khas, New Delhi, 110016",
                "phone_number": "+918888887777",
                "linkedin": "xyz",
            }
        }

class CV_Response(BaseModel):
    cv_url: str
    verif_doc_url: str
    class Config:
        json_schema_extra = {
            "example": {
                "cv_url": "https://aws.s3.com/abc123.pdf",
                "verif_doc_url": "https://aws.s3.com/abc123.pdf",
            }
        }

class Success_Message_Response(BaseModel):
    message: str

    class Config:
        josn_schema_extra = {
            "example": {
                "message": "Hello world!",
            }
        }
