import api.models.models as apiModels
import database.models.models as DbUserModels

def dbJobSeekerDataToApiJobSeekerData(user: DbUserModels.Job_Seeker):
    return apiModels.Job_Seeker_Data(
        fullname = user.fullname,
        college = user.college,
        email = user.email,
        gender = user.gender,
        phone_number = user.phone_number,
        date_of_birth = user.date_of_birth
    )

def apiJobSeekerToDbJobSeeker(user: apiModels.Job_Seeker):
    return DbUserModels.Job_Seeker(
        fullname = user.fullname,
        college = user.college,
        email = user.email,
        gender = user.gender,
        phone_number = user.phone_number,
        date_of_birth = user.date_of_birth,
        password = user.password
    )

def dbCollegeDataToApiCollegeData(user: DbUserModels.College):
    return apiModels.College_Data(
        your_name = user.your_name,
        college_name =  user.college_name,
        email = user.email,
        address = user.address,
        phone_number = user.phone_number,
        no_of_students = user.no_of_students
    )

def apiCollegeToDbCollege(user: apiModels.College):
    return DbUserModels.College(
        your_name = user.your_name,
        college_name =  user.college_name,
        email = user.email,
        address = user.address,
        phone_number = user.phone_number,
        no_of_students = user.no_of_students,
        password = user.password
    )

def dbRecruiterDataToApiRecruiterData(user: DbUserModels.Recruiter):
    return apiModels.Recruiter_Data(
        your_name = user.your_name,
        company_name =  user.company_name,
        email = user.email,
        address = user.address,
        phone_number = user.phone_number,
        linkedin = user.linkedin
    )

def apiRecruiterToDbRecruiter(user: apiModels.Recruiter):
    return DbUserModels.Recruiter(
        your_name = user.your_name,
        company_name =  user.company_name,
        email = user.email,
        address = user.address,
        phone_number = user.phone_number,
        linkedin = user.linkedin,
        password = user.password
    )
