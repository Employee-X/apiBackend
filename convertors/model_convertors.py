import api.models.models as apiModels
import database.models.models as DbUserModels
from beanie import PydanticObjectId

def apiUserToDbUser(user: apiModels.User_SignUp) -> DbUserModels.User:
    return DbUserModels.User(
        email = user.email,
        mobile= user.phone_number,
        password = user.password,
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

def dbJobSeekerProfileToApiJobSeekerProfile(profile: DbUserModels.Job_Seeker) -> apiModels.Job_Seeker_Profile:
    return apiModels.Job_Seeker_Profile(
        fullname= profile.fullname,
        college= profile.college,
        email= profile.email,
        gender=profile.gender,
        phone_number= profile.phone_number,
        date_of_birth= profile.date_of_birth,
        about = profile.about,
        profession = profile.profession,
        description = profile.description,
    )

def dbRecruiterProfileToApiRecruiterProfile(profile: DbUserModels.Recruiter) -> apiModels.Recruiter_Profile:
    return apiModels.Recruiter_Profile(
        your_name= profile.your_name,
        company_name= profile.company_name,
        email= profile.email,
        address= profile.address,
        phone_number= profile.phone_number,
        linkedin= profile.linkedin,
    )

def apiJobToDbJob(job: apiModels.Job, recruiterId: PydanticObjectId) -> DbUserModels.Job:
    return DbUserModels.Job(
        recruiterId = recruiterId,
        title = job.title,
        description = job.description,
        location= job.location,
        job_type= job.job_type,
        salary= job.salary,
        experience= job.experience,
        skills= job.skills,
        perks= job.perks,
        status= job.status,
    )

def dbJobToApiJobWithId(job: DbUserModels.Job, company_name :str) -> apiModels.Job_with_id:
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
        company_name= company_name,
    )
