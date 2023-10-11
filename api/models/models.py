from fastapi import File, UploadFile
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional, List
from utils.utils import Roles,Gender,Profession, Skills

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

class SendOtp(BaseModel):
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "abc123@gmail.com",
            }
        }

class RecvOtp(BaseModel):
    otp: int

    class Config:
        json_schema_extra = {
            "example": {
                "otp": 123456,
            }
        }

class User_SignIn_Response(BaseModel):
    access_token: str
    roles: Roles
    email_verified: bool = False
    mobile_verified: bool = False

    class Config:
        josn_schema_extra = {
            "example": {
                "access_token": "fvbfhfjveu423634h4vc54g43v42ghc4234523456gveewr",
                "roles": "job_seeker",
                "email_verified": False,
                "mobile_verified": False,
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
    skills: List[Skills] = []
    img_url: Optional[str] = None

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
                "skills": ["Python", "Java", "JavaScript"],
                "img_url": "https://aws.s3.com/abc123.pdf"
            }
        }

class Job_Seeker_Profile_With_Id_CV(Job_Seeker_Profile):
    id: str
    cv_url: Optional[str] = Field(default=None)
    verification_doc_url: Optional[str] = Field(default=None)
    cv_verified_status: bool = False
    img_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "fullname": "Loren Ipsum  Dolor",
                "college": "University of Virginia",
                "email": "abc123@gmail.com",
                "gender": "male",
                "phone_number": "+918888887777",
                "date_of_birth": "2002-05-05",
                "profession": ["student"],
                "about": "I am a student",
                "description": "I am a student",
                "skills": ["Python", "Java", "JavaScript"],
                "cv_url": "https://aws.s3.com/abc123.pdf",
                "verification_doc_url": "https://aws.s3.com/abc123.pdf",
                "cv_verified_status": False,
                "img_url": "https://aws.s3.com/abc123.pdf",
            }
        }

class Seeker_List(BaseModel):
    applicants: List[Job_Seeker_Profile_With_Id_CV] = []

    class Config:
        json_schema_extra = {
            "example": {
                "applicants": [
                    {
                        "id": "1234567890",
                        "fullname": "Loren Ipsum  Dolor",
                        "college": "University of Virginia",
                        "email": "abc123@gmail.com",
                        "gender": "male",
                        "phone_number": "+918888887777",
                        "date_of_birth": "2002-05-05",
                        "profession": ["student"],
                        "about": "I am a student",
                        "description": "I am a student",
                        "skills": ["Python", "Java", "JavaScript"],
                        "cv_url": "https://aws.s3.com/abc123.pdf",
                        "verification_doc_url": "https://aws.s3.com/abc123.pdf",
                        "cv_verified_status": False,
                        "img_url": "https://aws.s3.com/abc123.pdf",
                    },
                    {
                        "id": "1234567890",
                        "fullname": "Loren Ipsum  Dolor",
                        "college": "University of Virginia",
                        "email": "abc123@gmail.com",
                        "gender": "male",
                        "phone_number": "+918888887777",
                        "date_of_birth": "2002-05-05",
                        "profession": ["student"],
                        "about": "I am a student",
                        "description": "I am a student",
                        "skills": ["Python", "Java", "JavaScript"],
                        "cv_url": "https://aws.s3.com/abc123.pdf",
                        "verification_doc_url": "https://aws.s3.com/abc123.pdf",
                        "cv_verified_status": False,
                        "img_url": "https://aws.s3.com/abc123.pdf",
                    },
                ]
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
                "no_of_students": 500,
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
    description: Optional[str] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "your_name": "Loren Ipsum  Dolor",
                "company_name": "employeeX",
                "email": "abc123@gmail.com",
                "address": "IIT Delhi, Hauz Khas, New Delhi, 110016",
                "phone_number": "+918888887777",
                "linkedin": "xyz",
                "description": "I am a recruiter."
            }
        }

class CV_Response(BaseModel):
    cv_url: str
    verif_doc_url: str
    cv_verif_status: bool = False
    class Config:
        json_schema_extra = {
            "example": {
                "cv_url": "https://aws.s3.com/abc123.pdf",
                "verif_doc_url": "https://aws.s3.com/abc123.pdf",
                "cv_verif_status": False,
            }
        }

class IMG_Response(BaseModel):
    img_url: str
    bgimg_url: str
    class Config:
        json_schema_extra = {
            "example": {
                "img_url": "https://aws.s3.com/abc123.pdf",
                "bgimg_url": "https://aws.s3.com/abc123.pdf"
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

class Job(BaseModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary: Optional[str] = None
    experience: Optional[str] = None
    skills: List[Skills] = []
    perks: Optional[str] = None
    status: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Software Engineer",
                "company_name": "employeeX",
                "logo":"https://aws.s3.com/abc123.pdf",
                "description": "Software Engineer",
                "location": "Delhi",
                "job_type": "Full Time",
                "salary": "10 LPA",
                "experience": "2 years",
                "skills": ["Python", "Java", "JavaScript"],
                "perks": "Health Insurance, Free Food",
                "status": "active",
            }
        }

class Job_with_id(Job):
    id: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "title": "Software Engineer",
                "company_name": "employeeX",
                "logo": "https://aws.s3.com/abc123.pdf",
                "description": "Software Engineer",
                "location": "Delhi",
                "job_type": "Full Time",
                "salary": "10 LPA",
                "experience": "2 years",
                "skills": ["Python", "Java", "JavaScript"],
                "perks": "Health Insurance, Free Food",
                "status": "active",
            }
        }

class Job_with_status(Job_with_id):
    application_status: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "title": "Software Engineer",
                "company_name": "employeeX",
                "logo": "https://aws.s3.com/abc123.pdf",
                "description": "Software Engineer",
                "location": "Delhi",
                "job_type": "Full Time",
                "salary": "10 LPA",
                "experience": "2 years",
                "skills": ["Python", "Java", "JavaScript"],
                "perks": "Health Insurance, Free Food",
                "status": "active",
                "application_status": False,
            }
        }

class Job_List(BaseModel):
    jobs: List[Job_with_id]

    class Config:
        json_schema_extra = {
            "example": {
                "jobs": [
                    {
                        "id": "1234567890",
                        "title": "Software Engineer",
                        "company_name": "employeeX",
                        "logo": "https://aws.s3.com/abc123.pdf",
                        "description": "Software Engineer",
                        "location": "Delhi",
                        "job_type": "Full Time",
                        "salary": "10 LPA",
                        "experience": "2 years",
                        "skills": ["Python", "Java", "JavaScript"],
                        "perks": "Health Insurance, Free Food",
                        "status": "active",
                    },
                    {
                        "id": "1234567890",
                        "title": "Software Engineer",
                        "company_name": "employeeX",
                        "logo": "https://aws.s3.com/abc123.pdf",
                        "description": "Software Engineer",
                        "location": "Delhi",
                        "job_type": "Full Time",
                        "salary": "10 LPA",
                        "experience": "2 years",
                        "skills": ["Python", "Java", "JavaScript"],
                        "perks": "Health Insurance, Free Food",
                        "status": "active",
                    },
                ]
            }
        }

class Seeker_Job_List(BaseModel):
    jobs: List[Job_with_status]

    class Config:
        json_schema_extra = {
            "example": {
                "jobs": [
                    {
                        "id": "1234567890",
                        "title": "Software Engineer",
                        "company_name": "employeeX",
                        "logo": "https://aws.s3.com/abc123.pdf",
                        "description": "Software Engineer",
                        "location": "Delhi",
                        "job_type": "Full Time",
                        "salary": "10 LPA",
                        "experience": "2 years",
                        "skills": ["Python", "Java", "JavaScript"],
                        "perks": "Health Insurance, Free Food",
                        "status": "active",
                        "application_status": False,
                    },
                    {
                        "id": "1234567890",
                        "title": "Software Engineer",
                        "company_name": "employeeX",
                        "logo": "https://aws.s3.com/abc123.pdf",
                        "description": "Software Engineer",
                        "location": "Delhi",
                        "job_type": "Full Time",
                        "salary": "10 LPA",
                        "experience": "2 years",
                        "skills": ["Python", "Java", "JavaScript"],
                        "perks": "Health Insurance, Free Food",
                        "status": "active",
                        "application_status": False,
                    },
                ]
            }
        }
