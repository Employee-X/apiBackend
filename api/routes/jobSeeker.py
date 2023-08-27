from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt

import database.functions.jobSeeker as jobSeeker_db
import convertors.model_convertors as convertors
import api.models.models as api_models


router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

# -----------------------------------------JOB SEEKER-------------------------------------------------

@router.post("/login")
async def job_seeker_login(user_credentials: api_models.Job_Seeker_SignIn = Body(...)):
    user_exists = await jobSeeker_db.get_job_seeker_by_email(user_credentials.username)
    if user_exists:
        password = hash_helper.verify(user_credentials.password, user_exists.password)
        if password:
            return sign_jwt(user_credentials.username)
        
        raise HTTPException(status_code=403, detail = "Incorrect email or password")
    
    raise HTTPException(status_code=403, detail = "Incorrect x email or password")


@router.post("/signup",response_model=api_models.Job_Seeker_Data)
async def job_seeker_signup(user: api_models.Job_Seeker = Body(...)):
    user_exists = await jobSeeker_db.get_job_seeker_by_email(user.email)
    if user_exists:
        raise HTTPException(
            status_code=409, detail = "User with email supplied already exists"
        )
    
    user.password = hash_helper.encrypt(user.password)

    dbUser =  convertors.apiJobSeekerToDbJobSeeker(user)
    new_user = await jobSeeker_db.add_job_seeker(dbUser)
    new_user_data = convertors.dbJobSeekerDataToApiJobSeekerData(new_user)
    return new_user_data
