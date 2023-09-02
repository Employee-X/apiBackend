from typing import Optional
from fastapi import Body, APIRouter, HTTPException, Depends, UploadFile, File, logger
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt

import database.functions.user as user_db
import database.functions.jobSeeker as jobSeeker_db
import convertors.model_convertors as convertors
import api.models.models as api_models
from auth.jwt_bearer import JWTBearer
from utils.utils import unique_filename_generator
from config.config import s3_client

token_listener = JWTBearer()

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

async def validate_user(user_id: str, email_id: Optional[str], mobile: Optional[str]):
    user = await user_db.get_user_by_id(user_id)
    if user and user.roles == "job_seeker" and user.email_verified and user.mobile_verified:
        if email_id:
            if user.email != email_id:
                return False, "Email does not match"
        if mobile:
            if user.mobile != mobile:
                return False, "Mobile does not match"
        return True, ""
    return False, "Unauthorized Access"

# -----------------------------------------JOB SEEKER POST LOGIN ROUTES-------------------------------------------------
# update profile
@router.post("/updateProfile", response_model=api_models.Success_Message_Response)
async def update_profile(decoded_token: (str,str) = Depends(token_listener),job_seeker_profile: api_models.Job_Seeker_Profile = Body(...)):
    validated, msg = await validate_user(decoded_token[1],job_seeker_profile.email,job_seeker_profile.phone_number)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)

    _ = await jobSeeker_db.update_profile(job_seeker_profile,decoded_token[1])
    return api_models.Success_Message_Response(
        message = "Profile updated successfully"
    )
    
# get profile
@router.get("/profile", response_model=api_models.Job_Seeker_Profile)
async def get_profile(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)

    profile = await jobSeeker_db.get_job_seeker_profile_by_userId(decoded_token[1])
    apiProfile = convertors.dbJobSeekerProfileToApiJobSeekerProfile(profile)

    return apiProfile

# update CV
@router.post("/updateCV", response_model=api_models.Success_Message_Response)
async def updateCV(decoded_token: (str,str) = Depends(token_listener),cvobject: UploadFile = File(...),verifobject: UploadFile = File(...)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    filename = cvobject.filename
    new_filename = unique_filename_generator(filename)
    data = cvobject.file._file
    uploads3 = await s3_client.upload_fileobj(filename=new_filename, fileobject=data)
    filename2 = verifobject.filename
    new_filename2 = unique_filename_generator(filename2)
    data2 = verifobject.file._file
    uploads32 = await s3_client.upload_fileobj(filename=new_filename2, fileobject=data2)
    if uploads3 and uploads32:
        s3_url = f"https://{s3_client.bucket}.s3.{s3_client.region}.amazonaws.com/{s3_client.key}{new_filename}"
        s3_url2 = f"https://{s3_client.bucket}.s3.{s3_client.region}.amazonaws.com/{s3_client.key}{new_filename2}"
        _, past_cv, past_verif_doc = await jobSeeker_db.update_cv(s3_url,s3_url2,decoded_token[1])
        if past_cv:
            status = await s3_client.delete_fileobj(past_cv.split('/')[-1])
            if not status:
                print("Failed to delete old cv")
        if past_verif_doc:
            status = await s3_client.delete_fileobj(past_verif_doc.split('/')[-1])
            if not status:
                print("Failed to delete old verif doc")

        return api_models.Success_Message_Response(
            message = "CV uploaded successfully"
        )
    else:
        raise HTTPException(status_code=400, detail="Failed to upload")

# get CV
@router.get("/getCV", response_model=api_models.CV_Response)
async def getCV(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    cv_url, verif_url = await jobSeeker_db.get_cv(decoded_token[1])
    if not cv_url:
        raise HTTPException(status_code=404, detail="CV not found")
    if not verif_url:
        raise HTTPException(status_code=404, detail="Verification document not found")
    return api_models.CV_Response(
        cv_url = cv_url,
        verif_doc_url = verif_url,
    )
