from typing import Optional
from fastapi import Body, APIRouter, HTTPException, Depends
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt

import database.functions.user as user_db
import database.functions.recruiter as recruiter_db
import convertors.model_convertors as convertors
import api.models.models as api_models
from auth.jwt_bearer import JWTBearer

token_listener = JWTBearer()

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

async def validate_user(user_id: str, email_id: Optional[str], mobile: Optional[str]):
    user = await user_db.get_user_by_id(user_id)
    if user and user.roles == "recruiter" and user.email_verified and user.mobile_verified:
        if email_id:
            if user.email != email_id:
                return False, "Email does not match"
        if mobile:
            if user.mobile != mobile:
                return False, "Mobile does not match"
        return True, ""
    return False, "Unauthorized Access"

# -----------------------------------------------RECRUITER POST LOGIN ROUTES-------------------------------------------------
# update profile
@router.post("/updateProfile", response_model=api_models.Success_Message_Response)
async def update_profile(decoded_token: (str,str) = Depends(token_listener),recruiter_profile: api_models.Recruiter_Profile = Body(...)):
    validated, msg = await validate_user(decoded_token[1],recruiter_profile.email,recruiter_profile.phone_number)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)

    _ = await recruiter_db.update_profile(recruiter_profile,decoded_token[1])
    return api_models.Success_Message_Response(
        message = "Profile updated successfully"
    )

# get profile
@router.get("/profile", response_model=api_models.Recruiter_Profile)
async def get_profile(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)

    profile = await recruiter_db.get_recruiter_profile_by_userId(decoded_token[1])
    apiProfile = convertors.dbRecruiterProfileToApiRecruiterProfile(profile)
    
    return apiProfile
