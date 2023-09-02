import api.models.models as apiModels
import database.models.models as DbUserModels

def apiUserToDbUser(user: apiModels.User_SignUp) -> DbUserModels.User:
    return DbUserModels.User(
        email = user.email,
        mobile= user.phone_number,
        password = user.password,
        roles = user.roles
    )

def apiJobSeekerProfileToDbJobSeekerProfile(profile: apiModels.Job_Seeker_Profile, userId: str) -> DbUserModels.Job_Seeker:
    return DbUserModels.Job_Seeker(
        userId = userId,
        fullname= profile.fullname,
        college = profile.college,
        email = profile.email,
        gender= profile.gender,
        phone_number = profile.phone_number,
        date_of_birth = profile.date_of_birth
    )

def apiRecruiterProfileToDbRecruiterProfile(profile: apiModels.Recruiter_Profile, userId: str) -> DbUserModels.Recruiter:
    return DbUserModels.Recruiter(
        userId= userId,
        your_name= profile.your_name,
        company_name= profile.company_name,
        email= profile.email,
        address= profile.address,
        phone_number= profile.phone_number,
        linkedin= profile.linkedin
    )

def apiCollegeProfileToDbCollegeProfile(profile: apiModels.College_Profile, userId) -> DbUserModels.College:
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
        date_of_birth= profile.date_of_birth
    )

def dbRecruiterProfileToApiRecruiterProfile(profile: DbUserModels.Recruiter) -> apiModels.Recruiter_Profile:
    return apiModels.Recruiter_Profile(
        your_name= profile.your_name,
        company_name= profile.company_name,
        email= profile.email,
        address= profile.address,
        phone_number= profile.phone_number,
        linkedin= profile.linkedin
    )
