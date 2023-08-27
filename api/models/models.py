from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr, root_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

# --------------------------------------------------------------------------------------------

class Job_Seeker(BaseModel):
    fullname: str
    college: str
    email: EmailStr
    gender: str
    phone_number: PhoneNumber
    date_of_birth: str
    password: str
    confirm_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Loren Ipsum  Dolor",
                "college": "University of Virginia",
                "email": "abc123@gmail.com",
                "gender": "male",
                "phone_number": "+918888887777",
                "date_of_birth": "2002-05-05",
                "password": "3xt3m#",
                "confirm_password": "3xt3m#",
            }
        }

    class Settings:
        name = "job_seeker"


class Job_Seeker_Data(BaseModel):
    fullname: str
    college: str
    email: EmailStr
    gender: str
    phone_number: PhoneNumber
    date_of_birth: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Loren Ipsum  Dolor",
                "college": "University of Virginia",
                "email": "abc123@gmail.com",
                "gender": "male",
                "phone_number": "+918888887777",
                "date_of_birth": "2002-05-05",
            }
        }

class Job_Seeker_SignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {
                "username": "abc123@gmail.com",
                "password": "3xtxm#",
            }
        }

# --------------------------------------------------------------------------------------------

class College(BaseModel):
    your_name: str
    college_name: str
    email: EmailStr
    address: str
    phone_number: PhoneNumber
    no_of_students: int
    password: str
    confirm_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "your_name": "Loren Ipsum  Dolor",
                "college_name": "University of Virginia",
                "email": "abc123@gmail.com",
                "address": "IIT Delhi, Hauz Khas, New Delhi, 110016",
                "phone_number": "+918888887777",
                "no_of_students": "500",
                "password": "3xt3m#",
                "confirm_password": "3xt3m#"
            }
        }

    class Settings:
        name = "college"


class College_Data(BaseModel):
    your_name: str
    college_name: str
    email: EmailStr
    address: str
    phone_number: PhoneNumber
    no_of_students: int

    class Config:
        json_schema_extra = {
            "example": {
                "your_name": "Loren Ipsum  Dolor",
                "college_name": "University of Virginia",
                "email": "abc123@gmail.com",
                "address": "IIT Delhi, Hauz Khas, New Delhi, 110016",
                "phone_number": "+918888887777",
                "no_of_students": "500"
            }
        }

class College_SignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {
                "username": "abc123@gmail.com",
                "password": "3xt3m#"
            }
        }

# --------------------------------------------------------------------------------------------

class Recruiter(BaseModel):
    your_name: str
    company_name: str
    email: EmailStr
    address: str
    phone_number: PhoneNumber
    linkedin: str
    password: str
    confirm_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "your_name": "Loren Ipsum  Dolor",
                "company_name": "employeeX",
                "email": "abc123@gmail.com",
                "address": "IIT Delhi, Hauz Khas, New Delhi, 110016",
                "phone_number": "+918888887777",
                "linkedin": "xyz",
                "password": "3xt3m#",
                "confirm_password": "3xt3m#"
            }
        }

    class Settings:
        name = "recruiter"


class Recruiter_Data(BaseModel):
    your_name: str
    company_name: str
    email: EmailStr
    address: str
    phone_number: PhoneNumber
    linkedin: str

    class Config:
        json_schema_extra = {
            "example": {
                "your_name": "Loren Ipsum  Dolor",
                "company_name": "employeeX",
                "email": "abc123@gmail.com",
                "address": "IIT Delhi, Hauz Khas, New Delhi, 110016",
                "phone_number": "+918888887777",
                "linkedin": "xyz"
            }
        }

class Recruiter_SignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {
                "username": "abc123@gmail.com",
                "password": "3xt3m#"
            }
        }
