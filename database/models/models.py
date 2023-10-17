from beanie import Document
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from beanie import PydanticObjectId
from typing import Optional, List, Dict

from utils.utils import Roles,Gender,Profession,Skills


class User(Document):
    email: EmailStr
    mobile: PhoneNumber
    password: str
    roles: Roles
    email_verified: bool = False
    mobile_verified: bool = True
    otp: Optional[int] = 000000
    otp_expiration: Optional[str] = "2023-04-01T05:00:30.001000"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "abc123@gmail.com",
                "mobile": "+918888887777",
                "password": "3xt3m",
                "roles": "job_seeker",
                "email_verified": False,
                "mobile_verified": False,
                "otp": 000000,
                "expiration": "2021-05-05 12:00:00",
            }
        }

    class Settings:
        name = "user"


class Job_Seeker(Document):
    userId: PydanticObjectId

    email: EmailStr
    phone_number: PhoneNumber

    fullname: Optional[str] = None
    college: Optional[str] = None
    gender: Optional[Gender] = None
    date_of_birth: Optional[str] = None
    profession: List[Profession] = []
    about: Optional[str] = None
    description: Optional[str] = None
    skills: List[Skills] = []

    cv_url: Optional[str] = None
    verification_doc_url: Optional[str] = None
    cv_verified_status: bool = False
    img_url: Optional[str] = None

    jobs_applied: List[PydanticObjectId] = []

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
                "skills": ["Python", "Django", "Flask"],
                "cv_url": "https://aws.s3.com/abc123.pdf",
                "verification_doc_url": "https://aws.s3.com/abc123.pdf",
                "cv_verified_status": False,
                "img_url": "https://aws.s3.com/abc123.pdf",
                "jobs_applied": ["1234567890"],
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
    description: Optional[str] = None
    img_url: Optional[str] = None
    bgimg_url: Optional[str] = None
    coins: Optional[str] = None

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
                "description": "I am a recruiter.",
                "img_url":"https://aws.s3.com/abc123.jpg",
                "bgimg_url":"https://aws.s3.com/abc123.jpg",
                "coins":"absdjkfjd=dksd"
            }
        }

    class Settings:
        name = "recruiter"    

class Job(Document):
    recruiterId: PydanticObjectId
    company_name: Optional[str] = None
    logo: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary: Optional[str] = None
    experience: Optional[str] = None
    skills: List[Skills] = []
    perks: Optional[str] = None
    status: Optional[str] = None
    applicants: Optional[Dict[PydanticObjectId,bool]] = {}
    no_of_applicants: Optional[int] = 0
    date_posted: Optional[str] = None
    category: Optional[str] = None
    coins: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "recruiterId": "1234567890",
                "company_name": "employeeX",
                "logo": "https://aws.s3.com/abc123.pdf",
                "title": "Software Engineer",
                "description": "Software Engineer",
                "location": "Delhi",
                "job_type": "Full Time",
                "salary": "10 LPA",
                "experience": "2 years",
                "skills": ["Python", "Java", "JavaScript"],
                "perks": "Health Insurance, Free Food",
                "status": "active",
                "applicants": {"1234567890":False},
                "no_of_applicants": "5",
                "date_posted": "2002-05-05",
                "category": "IT",
                "coins": "abskcedfj=",
            }
        }

    class Settings:
        name = "jobs"
