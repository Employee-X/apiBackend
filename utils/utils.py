from enum import Enum
import uuid

class Roles(str, Enum):
    job_seeker = "job_seeker"
    college = "college"
    recruiter = "recruiter"

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class Profession(str, Enum):
    student = "student"
    software_engineer = "software_engineer"
    data_scientist = "data_scientist"
    data_analyst = "data_analyst"
    data_engineer = "data_engineer"
    business_analyst = "business_analyst"
    product_manager = "product_manager"
    product_designer = "product_designer"
    ui_ux_designer = "ui_ux_designer"
    graphic_designer = "graphic_designer"
    web_developer = "web_developer"
    full_stack_developer = "full_stack_developer"
    front_end_developer = "front_end_developer"
    back_end_developer = "back_end_developer"
    mobile_developer = "mobile_developer"
    android_developer = "android_developer"
    ios_developer = "ios_developer"
    devops_engineer = "devops_engineer"
    cloud_architect = "cloud_architect"
    cloud_engineer = "cloud_engineer"
    cloud_consultant = "cloud_consultant"
    cloud_administrator = "cloud_administrator"
    cloud_security_engineer = "cloud_security_engineer"
    cloud_network_engineer = "cloud_network_engineer"
    cloud_operations_engineer = "cloud_operations_engineer"

def unique_filename_generator(filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (uuid.uuid4(), ext)
    return new_filename
