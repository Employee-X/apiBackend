from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt

import database.functions.college as college_db
import convertors.model_convertors as convertors
import api.models.models as api_models


router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

# ------------------------------------------------COLLEGE--------------------------------------------------

@router.post("/login")
async def college_login(user_credentials: api_models.College_SignIn = Body(...)):
    user_exists = await college_db.get_college_by_email(user_credentials.username)
    if user_exists:
        password = hash_helper.verify(user_credentials.password, user_exists.password)
        if password:
            return sign_jwt(user_credentials.username)
        
        raise HTTPException(status_code=403, detail = "Incorrect email or password")
    
    raise HTTPException(status_code=403, detail = "Incorrect x email or password")


@router.post("/signup", response_model=api_models.College_Data)
async def college_signup(user:api_models.College = Body(...)):
    user_exists = await college_db.get_college_by_email(user.email)
    if user_exists:
        raise HTTPException(
            status_code=409, detail="User with email supplied already exists"
        )

    user.password = hash_helper.encrypt(user.password)
    
    dbUser = convertors.apiCollegeToDbCollege(user)
    new_user = await college_db.add_college(dbUser)
    new_userData = convertors.dbCollegeDataToApiCollegeData(new_user)
    
    return new_userData
