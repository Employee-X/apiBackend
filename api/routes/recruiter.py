from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt

import database.functions.recruiter as recruiter_db
import convertors.model_convertors as convertors
import api.models.models as api_models


router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

# -----------------------------------------------RECRUITER-------------------------------------------------

@router.post("/login")
async def recruiter_login(user_credentials: api_models.Recruiter_SignIn = Body(...)):
    user_exists = await recruiter_db.get_recruiter_by_email(user_credentials.username)
    if user_exists:
        password = hash_helper.verify(user_credentials.password, user_exists.password)
        if password:
            return sign_jwt(user_credentials.username)
        
        raise HTTPException(status_code=403, detail = "Incorrect email or password")
    
    raise HTTPException(status_code=403, detail = "Incorrect x email or password")


@router.post("/signup", response_model=api_models.Recruiter_Data)
async def recruiter_signup(user:api_models.Recruiter = Body(...)):
    user_exists = await recruiter_db.get_recruiter_by_email(user.email)
    if user_exists:
        raise HTTPException(
            status_code=409, detail="User with email supplied already exists"
        )

    user.password = hash_helper.encrypt(user.password)
    
    dbUser = convertors.apiRecruiterToDbRecruiter(user)
    new_user = await recruiter_db.add_recruiter(dbUser)
    new_userData = convertors.dbRecruiterDataToApiRecruiterData(new_user)
    
    return new_userData
