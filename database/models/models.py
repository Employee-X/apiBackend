from beanie import Document
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from beanie import PydanticObjectId
from typing import Optional, List

from utils.utils import Roles,Gender,Profession


class User(Document):
    email: EmailStr
    mobile: PhoneNumber
    password: str
    roles: Roles
    email_verified: bool = False
    mobile_verified: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "email": "abc123@gmail.com",
                "mobile": "+918888887777",
                "password": "3xt3m",
                "roles": "job_seeker",
                "email_verified": False,
                "mobile_verified": False,
            }
        }

    class Settings:
        name = "user"


class Job_Seeker(Document):
    userId: PydanticObjectId
    fullname: Optional[str] = None
    college: Optional[str] = None
    email: EmailStr
    gender: Optional[Gender] = None
    phone_number: PhoneNumber
    date_of_birth: Optional[str] = None
    profession: List[Profession] = []
    about: Optional[str] = None
    description: Optional[str] = None
    cv_url: Optional[str] = None
    verification_doc_url: Optional[str] = None
    cv_verified_status: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "userId": "1234567890",
                "fullname": "Loren Ipsum  Dolor",
                "college": "University of Virginia",
                "email": "abc123@gmail.com",
                "gender": "male",
                "phone_number": "+918888887777",
                "date_of_birth": "2002-05-05",
                "profession": ["student"],
                "about": "I am a student",
                "description": "I am a student",
                "cv_url": "https://aws.s3.com/abc123.pdf",
                "verification_doc_url": "https://aws.s3.com/abc123.pdf",
                "cv_verified_status": False,
            }
        }
    
    
    class Settings:
        name = "job_seeker"


class College(Document):
    userId: PydanticObjectId
    your_name: Optional[str] = None
    college_name: Optional[str] = None
    email: EmailStr
    address: Optional[str] = None
    phone_number: PhoneNumber
    no_of_students: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "userId": "1234567890",
                "your_name": "Loren Ipsum  Dolor",
                "college_name": "University of Virginia",
                "email": "abc123@gmail.com",
                "address": "IIT Delhi, Hauz Khas, New Delhi, 110016",
                "phone_number": "+918888887777",
                "no_of_students": "500",
            }
        }
    
    class Settings:
        name = "college"


class Recruiter(Document):
    userId: PydanticObjectId
    your_name: Optional[str] = None
    company_name: Optional[str] = None
    email: EmailStr
    address: Optional[str] = None
    phone_number: PhoneNumber
    linkedin: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "userId": "1234567890",
                "your_name": "Loren Ipsum  Dolor",
                "company_name": "employeeX",
                "email": "abc123@gmail.com",
                "address": "IIT Delhi, Hauz Khas, New Delhi, 110016",
                "phone_number": "+918888887777",
                "linkedin": "xyz",
            }
        }
    
    class Settings:
        name = "recruiter"    
     



