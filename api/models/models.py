from fastapi import File, UploadFile
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional, List,Dict
from utils.utils import Roles,Gender,Profession,Applicant_Status,Recruiter_Status,Job_Approval_Status,Transactions

# User Auth Models
class User_SignUp(BaseModel):
    phone_number: PhoneNumber
    roles: Roles
    referral: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+918888887777",
                "roles": "job_seeker",
                "referral": "dgfdhf",
            }
        }

class User_Update(BaseModel):
    email: EmailStr
    password: str

    class config:
        json_schema_extra = {
            "example": {
                "email": "abc123@gmail.com",
                "password": "3xx##",
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
    phone_number: PhoneNumber

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+919988775566",
            }
        }

class RecvOtp(BaseModel):
    phone_number: PhoneNumber
    otp: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+919988775566",
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

class Job_Seeker_Email_Update(BaseModel):
    email: EmailStr
    phone_number: PhoneNumber

    class config:
        josn_schema_extra = {
            "example": {
                "email": "abc@gmail.com",
                "phone_number": "+917755668899",
            }
        }

# Job Seeker Profile Model
class Job_Seeker_Profile(BaseModel):
    fullname: Optional[str] = Field(default=None)
    college: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    gender: Optional[Gender] = Field(default=None)
    phone_number: PhoneNumber
    date_of_birth: Optional[str] = Field(default=None)
    profession: List[Profession] = []
    about: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    skills: List[str] = []
    img_url: Optional[str] = None
    location: Optional[str] = None
    years_of_experience: Optional[int] = None
    speciality: Optional[str] = None
    current_salary: Optional[str] = None
    

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Loren Ipsum  Dolor",
                "college": "University of Virginia",
                "email": "abc123@gmail.com",
                "gender": "Male",
                "phone_number": "+918888887777",
                "date_of_birth": "2002-05-05",
                "profession": ["student"],
                "about": "I am a student",
                "description": "I am a student",
                "skills": ["Python", "Java", "JavaScript"],
                "img_url": "https://aws.s3.com/abc123.pdf",
                "location": "Lucknow",
                "years_of_experience": "2",
                "speciality": "Web Development",
                "current_salary": "6 LPA",
            }
        }

class Job_Seeker_Get_Profile(Job_Seeker_Profile):
    cv_uploaded: Optional[bool] = False
    

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Loren Ipsum  Dolor",
                "college": "University of Virginia",
                "email": "abc123@gmail.com",
                "gender": "Male",
                "phone_number": "+918888887777",
                "date_of_birth": "2002-05-05",
                "profession": ["student"],
                "about": "I am a student",
                "description": "I am a student",
                "skills": ["Python", "Java", "JavaScript"],
                "img_url": "https://aws.s3.com/abc123.pdf",
                "location": "Lucknow",
                "cv_uploaded": "False",
                "years_of_experience": "2",
                "speciality": "Web Development",
                "current_salary": "6 LPA",
            }
        }

class Job_Seeker_Profile_With_Id_CV(Job_Seeker_Profile):
    id: str
    cv_url: Optional[str] = Field(default=None)
    verification_doc_url: Optional[str] = Field(default=None)
    cv_verified_status: bool = False
    img_url: Optional[str] = None
    cv_uploaded: Optional[bool] = False

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "fullname": "Loren Ipsum  Dolor",
                "college": "University of Virginia",
                "email": "abc123@gmail.com",
                "gender": "Male",
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
                "loaction": "Lucknow",
                'cv_uploaded': "False",
                "years_of_experience": "2",
                "speciality": "Web Development",
                "current_salary": "6 LPA",
            }
        }

class Job_Seeker_Profile_Without_CV(BaseModel):
    id: str
    fullname: Optional[str] = None
    college: Optional[str] = None
    gender: Optional[str] = None
    skills: List[str] = None
    img_url: Optional[str] = None
    description: Optional[str] = None
    visited: Optional[bool] = None
    location: Optional[str] = None
    date_of_birth: Optional[str] = None
    cv_uploaded: Optional[bool] = None
    years_of_experience: Optional[int] = None
    speciality: Optional[str] = None
    current_salary: Optional[str] = None

    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "fullname": "Loren Ipsum  Dolor",
                "college": "University of Virginia", 
                "gender": "Male",
                "skills": ["Python", "Java", "JavaScript"],
                "img_url": "https://aws.s3.com/abc123.pdf",
                "description": "I am a student",
                "visited": "False",
                "location": "Lucknow",
                "date_of_birth": "2002-05-05",
                "cv_uploaded": "False",
                "years_of_experience": "2",
                "speciality": "Web Development",
                "current_salary": "6 LPA",
            }
        }



class Seeker_List(BaseModel):
    applicants: List[Job_Seeker_Profile_Without_CV] = []

    class Config:
        json_schema_extra = {
            "example": {
                "applicants": [
                    {
                        "id": "1234567890",
                        "fullname": "Loren Ipsum  Dolor",
                        "college": "University of Virginia", 
                        "gender": "Male",
                        "skills": ["Python", "Java", "JavaScript"],
                        "img_url": "https://aws.s3.com/abc123.pdf",
                        "description": "I am a student",
                        "location": "Lucknow",
                        "visited": "false",
                        "date_of_birth": "2002-05-05",
                        "cv_uploaded": "False",
                        "years_of_experience": "2",
                        "speciality": "Web Development",
                        "current_salary": "6 LPA",
                    },
                    {
                        "id": "1234567890",
                        "fullname": "Loren Ipsum  Dolor",
                        "college": "University of Virginia", 
                        "gender": "Male",
                        "skills": ["Python", "Java", "JavaScript"],
                        "img_url": "https://aws.s3.com/abc123.pdf",
                        "description": "I am a student",
                        "location": "Lucknow",
                        "visited": "false",
                        "date_of_birth": "2002-05-05",
                        "cv_uploaded": "False",
                        "years_of_experience": "2",
                        "speciality": "Web Development",
                        "current_salary": "6 LPA",
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
    email: Optional[EmailStr] = Field(default=None)
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
    cv_url: Optional[str] = None
    verif_doc_url: Optional[str] = None
    cv_verif_status: Optional[bool] = False
    cv_uploaded: Optional[bool] = False
    class Config:
        json_schema_extra = {
            "example": {
                "cv_url": "https://aws.s3.com/abc123.pdf",
                "verif_doc_url": "https://aws.s3.com/abc123.pdf",
                "cv_verif_status": False,
                "cv_uploaded": False,
            }
        }

class IMG_Response(BaseModel):
    img_url: Optional[str] = None
    bgimg_url: Optional[str] = None
    class Config:
        json_schema_extra = {
            "example": {
                "img_url": "https://aws.s3.com/abc123.pdf",
                "bgimg_url": "https://aws.s3.com/abc123.pdf"
            }
        }

class Coin(BaseModel):
    coins: Optional[str] = None
    earning_by_referral: Optional[str] = None
    class Config:
        json_schema_extra={
            "example":{
                "coins":"absdjkfjd=dksd",
                "earning_by_referral":"jsafha-afjf=ff",
            }   
        }

class Success_Message_Response(BaseModel):
    message: Optional[str]  = None

    class Config:
        josn_schema_extra = {
            "example": {
                "message": "Hello world!",
            }
        }

class Recruiter_Referral_Response(BaseModel):
    referral_link: Optional[str] = None
    referral_code: Optional[str] = None
    class Config:
        json_schema_extra = {
            "example": {
                "referral_link": "https://www.employeex.co.in?ref='ahsjdjf'",
                "referral_code": "akfjdkh",
            }
        }

class transaction_mssg(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    type: Optional[Transactions] = None
    amount: Optional[int] = None
    name: Optional[str] = None
    class Config:
        json_schema_extra = {
            "example": {
                "date": "05-05-2020",
                "time": "8:20",
                "type": "referral",
                "amount": 500,
                "name": "Shivam",
            }
        }

class transaction_history(BaseModel):
    transactions: List[transaction_mssg] = []
    class Config:
        json_schema_extra = {
            "example": {
                "transactions":[
                    {
                        "date": "05-05-2020",
                        "time": "8:20",
                        "type": "referral",
                        "amount": 500,
                        "name": "Shivam",
                    },
                    {
                        "date": "05-05-2020",
                        "time": "8:20",
                        "type": "referral",
                        "amount": 500,   
                        "name": "Shivam",
                    }
                ]
            }
        }


class Job(BaseModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary: Optional[Dict[str,str]] = None
    experience: Optional[str] = None
    skills: List[str] = []
    perks: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    no_of_openings: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Software Engineer",
                "company_name": "employeeX",
                "logo":"https://aws.s3.com/abc123.pdf",
                "description": "Software Engineer",
                "location": "Delhi",
                "job_type": "Full Time",
                "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                "experience": "2 years",
                "skills": ["Python", "Java", "JavaScript"],
                "perks": "Health Insurance, Free Food",
                "status": "active",
                "category": "IT",
                "no_of_openings": "2",
            }
        }

class Job_with_id(Job):
    id: str
    no_of_applicants: Optional[int] = None
    date_posted: Optional[str] = None

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
                "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                "experience": "2 years",
                "skills": ["Python", "Java", "JavaScript"],
                "perks": "Health Insurance, Free Food",
                "status": "active",
                "category": "IT",
                "no_of_openings": "2",
                "no_of_applicants": "5",
                "date_posted": "2002-05-05"
                
            }
        }

class Job_with_status(Job_with_id):
    application_status: Optional[Applicant_Status]  = None

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
                "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                "experience": "2 years",
                "skills": ["Python", "Java", "JavaScript"],
                "perks": "Health Insurance, Free Food",
                "status": "active",
                "category": "IT",
                "no_of_openings": "2",
                "application_status": "unapplied",
                "no_of_applicants": "5",
                "date_posted": "2002-05-05"
            }
        }

class Job_as_Poster(BaseModel):
    id: str
    title: Optional[str] = None
    company_name: Optional[str] = None
    logo: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary: Optional[Dict[str,str]] = None
    category: Optional[str] = None
    no_of_openings: Optional[int] = None
    no_of_applicants: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "title": "Software Engineer",
                "company_name": "employeeX",
                "logo":"https://aws.s3.com/abc123.pdf",
                "location": "Delhi",
                "job_type": "Full Time",
                "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                "category": "IT",
                "no_of_openings": "2",
                "no_of_applicants": "5",
            }
        }

class Job_as_Poster_List(BaseModel):
    jobs : List[Job_as_Poster]

    class Config:
        json_schema_extra = {
            "example": {
                "jobs": [
                    {
                        "id": "1234567890",
                        "title": "Software Engineer",
                        "company_name": "employeeX",
                        "logo":"https://aws.s3.com/abc123.pdf",
                        "location": "Delhi",
                        "job_type": "Full Time",
                        "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                        "category": "IT",
                        "no_of_openings": "2",
                        "no_of_applicants": "5",
                    },
                    {
                        "id": "1234567890",
                        "title": "Software Engineer",
                        "company_name": "employeeX",
                        "logo":"https://aws.s3.com/abc123.pdf",
                        "location": "Delhi",
                        "job_type": "Full Time",
                        "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                        "category": "IT",
                        "no_of_openings": "2",
                        "no_of_applicants": "5",
                    }
                ]
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
                        "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                        "experience": "2 years",
                        "skills": ["Python", "Java", "JavaScript"],
                        "perks": "Health Insurance, Free Food",
                        "status": "active",
                        "category": "IT",
                        "no_of_openings": "2",
                        "no_of_applicants": "5",
                        "date_posted": "2002-05-05"
                    },
                    {
                        "id": "1234567890",
                        "title": "Software Engineer",
                        "company_name": "employeeX",
                        "logo": "https://aws.s3.com/abc123.pdf",
                        "description": "Software Engineer",
                        "location": "Delhi",
                        "job_type": "Full Time",
                        "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                        "experience": "2 years",
                        "skills": ["Python", "Java", "JavaScript"],
                        "perks": "Health Insurance, Free Food",
                        "status": "active",
                        "category": "IT",
                        "no_of_openings": "2",
                        "no_of_applicants": "5",
                        "date_posted": "2002-05-05"
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
                        "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                        "experience": "2 years",
                        "skills": ["Python", "Java", "JavaScript"],
                        "perks": "Health Insurance, Free Food",
                        "status": "active",
                        "category": "IT",
                        "no_of_openings": "2",
                        "no_of_applicants": "5",
                        "date_posted": "2002-05-05",
                        "application_status": "applied",
                    },
                    {
                        "id": "1234567890",
                        "title": "Software Engineer",
                        "company_name": "employeeX",
                        "logo": "https://aws.s3.com/abc123.pdf",
                        "description": "Software Engineer",
                        "location": "Delhi",
                        "job_type": "Full Time",
                        "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                        "experience": "2 years",
                        "skills": ["Python", "Java", "JavaScript"],
                        "perks": "Health Insurance, Free Food",
                        "status": "active",
                        "category": "IT",
                        "no_of_openings": "2",
                        "no_of_applicants": "5",
                        "date_posted": "2002-05-05",
                        "application_status": "applied",
                    },
                ]
            }
        }

class Recruiter_with_approval_status(BaseModel):
    id: str
    recruiter_name: Optional[str] = None
    company_name: Optional[str] = None
    email: EmailStr
    phone_number: PhoneNumber
    date_of_signup: Optional[str] = None
    approval_status: Optional[Recruiter_Status] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "fdfdfjds2131",
                "recruiter_name": "Loren Ipsum  Dolor",
                "company_name": "employeeX",
                "email": "abc123@gmail.com",
                "phone_number": "+918888887777",
                "date_of_signup": "05-05-2020",
                "approval_status":"awaiting",
            }
        }

class Recriters_with_approval_status_list(BaseModel):
    recruiters: List[Recruiter_with_approval_status]
    class Config:
        json_schema_extra = {
            "example": {
                "recruiters":[
                    {
                        "id": "fdfdfjds2131",
                        "recruiter_name": "Loren Ipsum  Dolor",
                        "company_name": "employeeX",
                        "email": "abc123@gmail.com",
                        "phone_number": "+918888887777",
                        "date_of_signup": "05-05-2020",
                        "approval_status":"awaiting",
                    },
                    {
                        "id": "fdfdfjds2131",
                        "recruiter_name": "Loren Ipsum  Dolor",
                        "company_name": "employeeX",
                        "email": "abc123@gmail.com",
                        "phone_number": "+918888887777",
                        "date_of_signup": "05-05-2020",
                        "approval_status":"awaiting",
                    },
                ]
            }
        }

class Job_with_approval_status(BaseModel):
    id: str 
    title: Optional[str] = None
    company_name: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary: Optional[Dict[str,str]] = None
    experience: Optional[str] = None
    skills: List[str] = []
    perks: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    no_of_openings: Optional[int] = None
    job_approval_status: Optional[Job_Approval_Status] = None

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
                "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                "experience": "2 years",
                "skills": ["Python", "Java", "JavaScript"],
                "perks": "Health Insurance, Free Food",
                "status": "active",
                "category": "others",
                "no_of_openings": "2",
                "job_approval_status": "unhold",
            }
        }

class Job_with_approval_status_list(BaseModel):
    jobs: List[Job_with_approval_status]
    class Config:
        json_schema_extra = {
            "example": {
                "jobs":[
                    {
                        "id": "1234567890",
                        "title": "Software Engineer",
                        "company_name": "employeeX",
                        "logo": "https://aws.s3.com/abc123.pdf",
                        "description": "Software Engineer",
                        "location": "Delhi",
                        "job_type": "Full Time",
                        "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                        "experience": "2 years",
                        "skills": ["Python", "Java", "JavaScript"],
                        "perks": "Health Insurance, Free Food",
                        "status": "active",
                        "category": "others",
                        "no_of_openings": "2",
                        "job_approval_status": "unhold",
                    },
                    {
                        "id": "1234567890",
                        "title": "Software Engineer",
                        "company_name": "employeeX",
                        "logo": "https://aws.s3.com/abc123.pdf",
                        "description": "Software Engineer",
                        "location": "Delhi",
                        "job_type": "Full Time",
                        "salary": {"min":"10","max":"15","currency":"inr","type":"lpa"},
                        "experience": "2 years",
                        "skills": ["Python", "Java", "JavaScript"],
                        "perks": "Health Insurance, Free Food",
                        "status": "active",
                        "category": "others",
                        "no_of_openings": "2",
                        "job_approval_status": "unhold",
                    },
                ]
            }
        }

class admin_log(BaseModel):
    day_logins: int = 0
    day_new_users: int = 0
    week_logins: int = 0
    week_new_users: int = 0
    month_logins: int = 0
    month_new_users: int = 0
    jobs: int = 0
    active_jobs: int = 0
    inactive_jobs: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "day_logins": 0,
                "day_new_users": 0,
                "week_logins": 0,
                "week_new_users": 0,
                "month_logins": 0,
                "month_new_users": 0,
                "jobs": 0,
                "active_jobs": 0,
                "inactive_jobs": 0
            }
        }


