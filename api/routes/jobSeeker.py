import datetime
from typing import Optional
from fastapi import Body, APIRouter, HTTPException, Depends, UploadFile, File, logger
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt

import database.functions.user as user_db
import database.functions.jobSeeker as jobSeeker_db
import database.functions.job as job_db

import convertors.model_convertors as convertors
import api.models.models as api_models
from auth.jwt_bearer import JWTBearer
from utils.utils import unique_filename_generator, otp_generator
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

async def validate_user_before_verify(user_id: str, email_id: Optional[str], mobile: Optional[str]):
    user = await user_db.get_user_by_id(user_id)
    if user and user.roles == "job_seeker":
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
    cv_url, verif_url, verif_status = await jobSeeker_db.get_cv(decoded_token[1])
    if not cv_url:
        raise HTTPException(status_code=404, detail="CV not found")
    if not verif_url:
        raise HTTPException(status_code=404, detail="Verification document not found")
    return api_models.CV_Response(
        cv_url = cv_url,
        verif_doc_url = verif_url,
        cv_verif_status=verif_status,
    )

# get all jobs
@router.get("/getAllJobs", response_model=api_models.Seeker_Job_List)
async def get_jobs(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    profile = await jobSeeker_db.get_job_seeker_profile_by_userId(decoded_token[1])
    applied_job_ids = profile.jobs_applied
    jobs = await job_db.get_all_jobs()
    apiJobs = []
    for job in jobs:
        status = job.id in applied_job_ids
        apiJobs.append(convertors.dbJobToApiJobWithStatus(job,status))
    return api_models.Seeker_Job_List(
        jobs = apiJobs
    )

# get job by id
@router.get("/getJob/{jobId}", response_model=api_models.Job_with_status)
async def get_job(jobId,decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    profile = await jobSeeker_db.get_job_seeker_profile_by_userId(decoded_token[1])
    applied_job_ids = profile.jobs_applied
    job = await job_db.get_job_by_id(jobId)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    status = job.id in applied_job_ids
    apiJob = convertors.dbJobToApiJobWithStatus(job,status)
    return apiJob

# apply for job
@router.put("/applyJob/{jobId}", response_model=api_models.Success_Message_Response)
async def apply_job(jobId,decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    profile = await jobSeeker_db.get_job_seeker_profile_by_userId(decoded_token[1])
    applied_job_ids = profile.jobs_applied
    if jobId in applied_job_ids:
        raise HTTPException(status_code=403, detail="Already applied for this job")
    job = await job_db.get_job_by_id(jobId)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    res = await job_db.apply_job(jobId,decoded_token[1])
    res = await jobSeeker_db.apply_job(jobId,decoded_token[1])
    return api_models.Success_Message_Response(
        message = "Applied for Job successfully"
    )

# get applied jobs
@router.get("/appliedJobs", response_model=api_models.Seeker_Job_List)
async def get_applied_jobs(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    profile = await jobSeeker_db.get_job_seeker_profile_by_userId(decoded_token[1])
    applied_job_ids = profile.jobs_applied
    apiJobs = []
    for job_id in applied_job_ids:
        job = await job_db.get_job_by_id(str(job_id))
        apiJobs.append(convertors.dbJobToApiJobWithStatus(job,True))
    return api_models.Seeker_Job_List(
        jobs = apiJobs
    )

# generate otp and send over email
@router.post("/generateOtp", response_model=api_models.Success_Message_Response)
async def generate_otp(decoded_token: (str,str) = Depends(token_listener),email_input: api_models.SendOtp = Body(...)):
    validated, msg = await validate_user_before_verify(decoded_token[1], email_input.email, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    user = await user_db.get_user_by_id(decoded_token[1])
    current_time = datetime.datetime.now()
    expiration_tim_str = user.otp_expiration
    if expiration_tim_str:
        expiration_time = datetime.datetime.fromisoformat(expiration_tim_str)
        # if otp already exists and is not expired
        if user.otp and user.otp_expiration and current_time < expiration_time:
            time_remaining = expiration_time - current_time
            time_instring = int(time_remaining.total_seconds())
            raise HTTPException(status_code=403, detail=f"OTP already sent and is not expired. Try again in {time_instring} seconds")
    otp = otp_generator()
    response_email = await s3_client.send_otp_email(otp,email_input.email)
    res = await user_db.update_otp(decoded_token[1],otp)
    return api_models.Success_Message_Response(
        message = "OTP sent successfully"
    )

# verify otp
@router.post("/verifyOtp", response_model=api_models.Success_Message_Response)
async def verify_otp(decoded_token: (str,str) = Depends(token_listener),otp_input: api_models.RecvOtp = Body(...)):
    validated, msg = await validate_user_before_verify(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    user = await user_db.get_user_by_id(decoded_token[1])
    current_time = datetime.datetime.now()
    expiration_tim_str = user.otp_expiration
    if expiration_tim_str:
        expiration_time = datetime.datetime.fromisoformat(expiration_tim_str)
        if user.otp and user.otp_expiration and current_time < expiration_time and user.otp == otp_input.otp:
            res = await user_db.update_email_verified(decoded_token[1])
            return api_models.Success_Message_Response(
                message = "Account verified successfully"
            )
    raise HTTPException(status_code=403, detail="OTP is invalid or expired")