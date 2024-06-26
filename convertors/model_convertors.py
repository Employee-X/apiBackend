import api.models.models as apiModels
import database.models.models as DbUserModels
from beanie import PydanticObjectId
import database.functions.recruiter as recruiter_db
from business.policy import *
from datetime import date,timezone,datetime,timedelta
from auth.aes_security import * 
from utils.utils import Applicant_Status,Job_Approval_Status

def apiUserToDbUser(user: apiModels.User_SignUp) -> DbUserModels.User:
    return DbUserModels.User(
        mobile= user.phone_number,
        roles = user.roles,
    )

def apiJobSeekerProfileToDbJobSeekerProfile(profile: apiModels.Job_Seeker_Profile, userId: PydanticObjectId) -> DbUserModels.Job_Seeker:
    return DbUserModels.Job_Seeker(
        userId = userId,
        fullname= profile.fullname,
        college = profile.college,
        email = profile.email,
        gender= profile.gender,
        phone_number = profile.phone_number,
        date_of_birth = profile.date_of_birth,
        about = profile.about,
        description = profile.description,
        profession = profile.profession,
        skills= profile.skills,
        location=profile.location,
    )

def dbJobSeekerProfileToApiJobSeekerProfileWithIdCv(profile: DbUserModels.Job_Seeker) -> apiModels.Job_Seeker_Profile_With_Id_CV:
    return apiModels.Job_Seeker_Profile_With_Id_CV(
        id= str(profile.userId),
        fullname= profile.fullname,
        college= profile.college,
        email= profile.email,
        gender=profile.gender,
        phone_number= profile.phone_number,
        date_of_birth= profile.date_of_birth,
        about = profile.about,
        profession = profile.profession,
        description = profile.description,
        skills= profile.skills,
        cv_url= profile.cv_url,
        location=profile.location,
        verification_doc_url= profile.verification_doc_url,
        cv_verified_status= profile.cv_verified_status,
        img_url = profile.img_url,
        cv_uploaded=profile.cv_uploaded,
        years_of_experience=profile.years_of_experience,
        speciality=profile.speciality,
        current_salary=profile.current_salary,
    )

def dbJobseekerToApiRecruiterWithoutCV(profile: DbUserModels.Job_Seeker,visited: bool) -> apiModels.Job_Seeker_Profile_Without_CV:
    return apiModels.Job_Seeker_Profile_Without_CV(
        id = str(profile.userId),
        fullname = profile.fullname,
        college=profile.college,
        gender=profile.gender,
        skills=profile.skills,
        img_url = profile.img_url,
        description = profile.description,
        visited = visited,
        location=profile.location,
        date_of_birth=profile.date_of_birth,
        cv_uploaded=profile.cv_uploaded,
        years_of_experience=profile.years_of_experience,
        speciality=profile.speciality,
        current_salary=profile.current_salary,
    )


def apiRecruiterProfileToDbRecruiterProfile(profile: apiModels.Recruiter_Profile, userId: PydanticObjectId) -> DbUserModels.Recruiter:
    return DbUserModels.Recruiter(
        userId= userId,
        your_name= profile.your_name,
        company_name= profile.company_name,
        email= profile.email,
        address= profile.address,
        phone_number= profile.phone_number,
        linkedin= profile.linkedin,
        description=profile.description,
        coins=encrypt(str(VERIFIED_RECRUITER_COINS)),
        earning_by_referral=encrypt(str(0)),
        date_of_signup=str(datetime.now(timezone(timedelta(hours=+5.5),'IST')).date().strftime("%d-%m-%Y")),
    )

def apiCollegeProfileToDbCollegeProfile(profile: apiModels.College_Profile, userId: PydanticObjectId) -> DbUserModels.College:
    return DbUserModels.College(
        userId= userId,
        your_name= profile.your_name,
        college_name= profile.college_name,
        email= profile.email,
        address= profile.address,
        phone_number= profile.phone_number,
        no_of_students= profile.no_of_students,
    )

def dbCollegeProfileToApiCollegeProfile(profile: DbUserModels.College) -> apiModels.College_Profile:
    return apiModels.College_Profile(
        your_name= profile.your_name,
        college_name= profile.college_name,
        email= profile.email,
        address= profile.address,
        phone_number= profile.phone_number,
        no_of_students= profile.no_of_students,
    )

def dbJobSeekerProfileToApiJobSeekerProfile(profile: DbUserModels.Job_Seeker) -> apiModels.Job_Seeker_Get_Profile:
    return apiModels.Job_Seeker_Get_Profile(
        fullname= profile.fullname,
        college= profile.college,
        email= profile.email,
        gender=profile.gender,
        phone_number= profile.phone_number,
        date_of_birth= profile.date_of_birth,
        about = profile.about,
        profession = profile.profession,
        description = profile.description,
        skills= profile.skills,
        img_url = profile.img_url,
        location=profile.location,
        cv_uploaded = profile.cv_uploaded,
        years_of_experience=profile.years_of_experience,
        speciality=profile.speciality,
        current_salary=profile.current_salary,
    )

def dbRecruiterProfileToApiRecruiterProfile(profile: DbUserModels.Recruiter) -> apiModels.Recruiter_Profile:
    return apiModels.Recruiter_Profile(
        your_name= profile.your_name,
        company_name= profile.company_name,
        email= profile.email,
        address= profile.address,
        phone_number= profile.phone_number,
        linkedin= profile.linkedin,
        description=profile.description,
    )

def apiJobToDbJob(job: apiModels.Job, recruiterId: PydanticObjectId,logo_url: str,job_approval_status: Job_Approval_Status) -> DbUserModels.Job:
    return DbUserModels.Job(
        recruiterId = recruiterId,
        company_name= job.company_name,
        logo = logo_url,
        title = job.title,
        description = job.description,
        location= job.location,
        job_type= job.job_type,
        salary= job.salary,
        experience= job.experience,
        skills= job.skills,
        perks= job.perks,
        status= job.status,
        no_of_applicants = 0,
        category =job.category,
        date_posted=str(datetime.now(timezone(timedelta(hours=+5.5),'IST')).date().strftime("%d-%m-%Y")),
        coins=encrypt(str(COINS_ON_NEW_JOB)),
        job_approval_status=job_approval_status,
        no_of_openings=job.no_of_openings,
    )

def dbJobToApiJobWithId(job: DbUserModels.Job) -> apiModels.Job_with_id:
    return apiModels.Job_with_id(
        id=str(job.id),
        title= job.title,
        description= job.description,
        location= job.location,
        job_type= job.job_type,
        salary= job.salary,
        experience= job.experience,
        skills= job.skills,
        perks= job.perks,
        status= job.status,
        company_name= job.company_name,
        logo = job.logo,
        no_of_applicants = job.no_of_applicants,
        date_posted = job.date_posted,
        category = job.category,
        no_of_openings=job.no_of_openings,
    )

def dbJobToApiJobWithStatus(job: DbUserModels.Job, status: Applicant_Status) -> apiModels.Job_with_status:
    return apiModels.Job_with_status(
        id=str(job.id),
        title= job.title,
        description= job.description,
        location= job.location,
        job_type= job.job_type,
        salary= job.salary,
        experience= job.experience,
        skills= job.skills,
        perks= job.perks,
        status= job.status,
        company_name= job.company_name,
        application_status= status,
        logo = job.logo,
        no_of_applicants = job.no_of_applicants,
        date_posted = job.date_posted,
        category = job.category,
        no_of_openings=job.no_of_openings,
    )

def dbJobToApiPosterJob(job: DbUserModels.Job) -> apiModels.Job_as_Poster:
    return apiModels.Job_as_Poster(
        id=str(job.id),
        title= job.title,
        location= job.location,
        job_type= job.job_type,
        salary= job.salary,
        company_name= job.company_name,
        logo = job.logo,
        category = job.category,
        no_of_openings=job.no_of_openings,
        no_of_applicants=job.no_of_applicants,
    )

def dbRecruiterToApiAdmin(recruiter: DbUserModels.Recruiter) -> apiModels.Recruiter_with_approval_status:
    return apiModels.Recruiter_with_approval_status(
        id=str(recruiter.userId),
        recruiter_name=recruiter.your_name,
        email=recruiter.email,
        phone_number=recruiter.phone_number,
        date_of_signup=recruiter.date_of_signup,
        company_name=recruiter.company_name,
        approval_status=recruiter.approval_status,
    )

def dbJobToApiAdminJob(job: DbUserModels.Job) -> apiModels.Job_with_approval_status:
    return apiModels.Job_with_approval_status(
        id=str(job.id),
        title=job.title,
        company_name=job.company_name,
        logo=job.logo,
        description=job.description,
        location=job.location,
        job_type=job.job_type,
        salary=job.salary,
        experience=job.experience,
        skills=job.skills,
        perks=job.perks,
        status=job.status,
        category=job.category,
        job_approval_status = job.job_approval_status,
        no_of_openings=job.no_of_openings,
    )

def dbAdminToApiAdmin(admin: DbUserModels.Admin) -> apiModels.admin_log:
    return apiModels.admin_log(
        day_logins=admin.last_day_logins,
        day_new_users=admin.last_day_new_users,
        week_logins=admin.last_week_logins,
        week_new_users=admin.last_week_new_users,
        month_logins=admin.last_month_logins,
        month_new_users=admin.last_month_new_users,
        jobs=admin.jobs,
        active_jobs=admin.active_jobs,
        inactive_jobs=admin.inactive_jobs,
    )

def dbTransactionsToApiTransaction(transaction,name: str = None) -> apiModels.transaction_mssg:
    return apiModels.transaction_mssg(
        date=transaction[0],
        time=transaction[1],
        type=transaction[2],
        amount=transaction[3],
        name= name,
    )