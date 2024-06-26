from beanie import Document
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from beanie import PydanticObjectId
from typing import Optional, List, Dict
from business.policy import *
from utils.utils import Roles,Gender,Profession,Job_Status,Applicant_Status,Recruiter_Status,Job_Approval_Status
from datetime import date,timezone,datetime,timedelta


class User(Document):
    email: Optional[EmailStr] = None
    mobile: PhoneNumber
    password: Optional[str] = None
    roles: Roles
    email_verified: bool = False
    mobile_verified: bool = False
    otp: Optional[int] = 000000
    otp_expiration: Optional[str] = "2023-04-01T05:00:30.001000"
    otp_resend: Optional[str] = "2023-04-01T05:00:30.001000"
    referral: Optional[str] = None

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
                "otp_resend": "2021-05-05 12:00:00",
                "referral": "fdjfkjflfj"
            }
        }

    class Settings:
        name = "user"


class Job_Seeker(Document):
    userId: PydanticObjectId

    email: Optional[EmailStr] = None
    phone_number: PhoneNumber
    fullname: Optional[str] = None
    college: Optional[str] = None
    gender: Optional[Gender] = None
    date_of_birth: Optional[str] = None
    profession: List[Profession] = []
    about: Optional[str] = None
    description: Optional[str] = None
    skills: List[str] = []
    location: Optional[str] = None
    cv_url: Optional[str] = None
    verification_doc_url: Optional[str] = None
    cv_uploaded: Optional[bool] = False
    cv_verified_status: bool = False
    img_url: Optional[str] = "https://employeex.s3.ap-south-1.amazonaws.com/Default+pics/Def_User.png"
    years_of_experience: Optional[int] = None
    speciality: Optional[str] = None
    current_salary: Optional[str] = None
    jobs_applied: Optional[Dict[PydanticObjectId,Applicant_Status]] = {}

    class Config:
        json_schema_extra = {
            "example": {
                "userId": "1234567890",
                "fullname": "Loren Ipsum  Dolor",
                "college": "University of Virginia",
                "email": "abc123@gmail.com",
                "gender": "Male",
                "phone_number": "+918888887777",
                "date_of_birth": "2002-05-05",
                "profession": ["student"],
                "about": "I am a student",
                "description": "I am a student",
                "location": "Lucknow",
                "skills": ["Python", "Django", "Flask"],
                "cv_url": "https://aws.s3.com/abc123.pdf",
                "verification_doc_url": "https://aws.s3.com/abc123.pdf",
                "cv_uploaded": False,
                "cv_verified_status": False,
                "img_url": "https://aws.s3.com/abc123.pdf",
                "years_of_experience": "2",
                "speciality": "Web Development",
                "current_salary": "6 LPA",
                "jobs_applied": {"1234567890":"applied"},
            }
        }
    
    
    class Settings:
        name = "job_seeker"


class College(Document):
    userId: PydanticObjectId
    your_name: Optional[str] = None
    college_name: Optional[str] = None
    email: Optional[EmailStr] = None
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
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone_number: PhoneNumber
    linkedin: Optional[str] = None
    description: Optional[str] = None
    img_url: Optional[str] = "https://employeex.s3.ap-south-1.amazonaws.com/Default+pics/Def_Rec.png"
    bgimg_url: Optional[str] = "https://employeex.s3.ap-south-1.amazonaws.com/Default+pics/CompanyBg.png"
    coins: Optional[str] = None
    free_jobs: Optional[int] = NUMBER_OF_FREE_JOBS
    approval_status: Optional[Recruiter_Status] = "awaiting"
    date_of_signup: Optional[str] = None
    referral_id: Optional[str] = None
    transactions: List[tuple] = []
    earning_by_referral: Optional[str] = None

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
                "coins":"absdjkfjd=dksd",
                "free_jobs":"5",
                "approval_status":"awaiting",
                "date_of_signup":"05-05-2020",
                "referral_id": "djfhkjkfjdkf",
                "transactions": [("05-05-2020","8:20","referral",500,None),("05-05-2020","9:40","job_posting",300,None)],
                "earning_by_referral": "fahhfjjkddf",
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
    salary: Optional[Dict[str,str]] = None
    experience: Optional[str] = None
    skills: List[str] = []
    perks: Optional[str] = None
    status: Optional[Job_Status] = "active"
    applicants: Optional[Dict[PydanticObjectId,bool]] = {}
    no_of_applicants: Optional[int] = 0
    date_posted: Optional[str] = None
    category: Optional[str] = None
    coins: Optional[str] = None
    job_approval_status: Optional[Job_Approval_Status] = "unhold"
    no_of_openings: Optional[int] = None

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
                "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                "experience": "2 years",
                "skills": ["Python", "Java", "JavaScript"],
                "perks": "Health Insurance, Free Food",
                "status": "active",
                "applicants": {"1234567890":False},
                "no_of_applicants": "5",
                "date_posted": "05-05-2020",
                "category": "others",
                "coins": "WpEvpO05dTtSIOcU0vXojA==",
                "job_approval_status":"unhold",
                "no_of_opening": "2",
            }
        }

    class Settings:
        name = "jobs"

class Admin(Document):
    adminId: PydanticObjectId 
    day_logins: Optional[int] = 0
    day_new_users: Optional[int] = 0
    week_logins: Optional[int] = 0
    week_new_users: Optional[int] = 0
    month_logins: Optional[int] = 0
    month_new_users: Optional[int] = 0
    jobs: Optional[int] = 0
    active_jobs: Optional[int] = 0
    inactive_jobs: Optional[int] = 0
    last_day_logins: Optional[int] = 0
    last_day_new_users: Optional[int] = 0
    last_week_logins: Optional[int] = 0
    last_week_new_users: Optional[int] = 0
    last_month_logins: Optional[int] = 0
    last_month_new_users: Optional[int] = 0
    day_end_epoch: Optional[int] = (datetime.now()+timedelta(days=1)).strftime('%s')
    week_end_epoch: Optional[int] = (datetime.now()+timedelta(days=7)).strftime('%s')
    month_end_epoch: Optional[int] = (datetime.now()+timedelta(days=30)).strftime('%s')

    class Config:
        json_schema_extra = {
            "example": {
                "adminId": "1234567890",
                "day_logins": 0,
                "day_new_users": 0,
                "week_logins": 0,
                "week_new_users": 0,
                "month_logins": 0,
                "month_new_users": 0,
                "jobs": 0,
                "active_jobs": 0,
                "inactive_jobs": 0,
                "last_day_logins": 0,
                "last_day_new_users": 0,
                "last_week_logins": 0,
                "last_week_new_users": 0,
                "last_month_logins": 0,
                "last_month_new_users": 0,
                "day_end_epoch": 0,
                "week_end_epoch": 0,
                "month_end_epoch": 0,
            }
        }

    class Settings:
        name = "admin"
