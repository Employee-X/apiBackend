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

def unique_filename_generator(filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (uuid.uuid4(), ext)
    return new_filename
