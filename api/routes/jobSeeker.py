import datetime
from typing import Optional
from fastapi import Body, APIRouter, HTTPException, Depends, UploadFile, File, logger
from passlib.context import CryptContext
from beanie import PydanticObjectId


from auth.jwt_handler import sign_jwt

import database.functions.user as user_db
import database.functions.jobSeeker as jobSeeker_db
import database.functions.job as job_db

import convertors.model_convertors as convertors
import api.models.models as api_models
from auth.jwt_bearer import JWTBearer
from utils.utils import unique_filename_generator
from auth.otp import otp_generator,send_otp_phone
from config.config import s3_client
import database.functions.admin as admin_db

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


async def validate_user_without_verification(user_id: str,
                                        email_id: Optional[str],
                                        mobile: Optional[str]):
    user = await user_db.get_user_by_id(user_id)
    # raise HTTPException(status_code=404,detail=str(user))
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
    validated, msg = await validate_user_without_verification(decoded_token[1],job_seeker_profile.email,job_seeker_profile.phone_number)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)

    _ = await jobSeeker_db.update_profile(job_seeker_profile,decoded_token[1])
    return api_models.Success_Message_Response(
        message = "Profile updated successfully"
    )
    
# get profile
@router.get("/profile", response_model=api_models.Job_Seeker_Get_Profile)
async def get_profile(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)

    profile = await jobSeeker_db.get_job_seeker_profile_by_userId(decoded_token[1])
    apiProfile = convertors.dbJobSeekerProfileToApiJobSeekerProfile(profile)
    return apiProfile

# update CV
@router.post("/updateCV", response_model=api_models.Success_Message_Response)
async def updateCV(decoded_token: (str,str) = Depends(token_listener),cvobject: UploadFile = File(...),verifobject: UploadFile = None):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    filename = cvobject.filename
    new_filename = unique_filename_generator(filename)
    data = cvobject.file._file
    uploads3 = await s3_client.upload_fileobj(filename=new_filename, fileobject=data)
    if uploads3:
        s3_url = f"https://{s3_client.bucket}.s3.{s3_client.region}.amazonaws.com/{s3_client.key}{new_filename}"
        _,s3_url2,__,__ = await jobSeeker_db.get_cv(decoded_token[1])
        _, past_cv, past_verif_doc = await jobSeeker_db.update_cv(s3_url,s3_url2,decoded_token[1])
        if past_cv:
            status = await s3_client.delete_fileobj(past_cv.split('/')[-1])
            if not status:
                print("Failed to delete old cv")
    else:
        raise HTTPException(status_code=400, detail="Failed to upload")
    if verifobject:
        filename2 = verifobject.filename
        new_filename2 = unique_filename_generator(filename2)
        data2 = verifobject.file._file
        uploads32 = await s3_client.upload_fileobj(filename=new_filename2, fileobject=data2)
        if uploads32:
            s3_url,_,__ = await jobSeeker_db.get_cv(decoded_token[1])
            s3_url2 = f"https://{s3_client.bucket}.s3.{s3_client.region}.amazonaws.com/{s3_client.key}{new_filename2}"
            _, past_cv, past_verif_doc = await jobSeeker_db.update_cv(s3_url,s3_url2,decoded_token[1])
            if past_verif_doc:
                status = await s3_client.delete_fileobj(past_verif_doc.split('/')[-1])
                if not status:
                    print("Failed to delete old verif doc")
        else:
            raise HTTPException(status_code=400, detail="Failed to upload")
    return api_models.Success_Message_Response(
            message = "CV uploaded successfully"
        )

# get CV
@router.get("/getCV", response_model=api_models.CV_Response)
async def getCV(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    cv_url, verif_url, verif_status,cv_uploaded = await jobSeeker_db.get_cv(decoded_token[1])
    if not cv_url:
        cv_url = None
    if not verif_url:
        verif_url = ""
        # raise HTTPException(status_code=404, detail="Verification document not found")
    return api_models.CV_Response(
        cv_url = cv_url,
        verif_doc_url = verif_url,
        cv_verif_status=verif_status,
        cv_uploaded=cv_uploaded,
    )

# get all jobs
@router.get("/getAllJobs", response_model=api_models.Seeker_Job_List)
async def get_jobs(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    profile = await jobSeeker_db.get_job_seeker_profile_by_userId(decoded_token[1])
    applied_job_ids = profile.jobs_applied.keys()
    jobs = await job_db.get_all_jobs()
    apiJobs = []
    for job in jobs:
        if job.job_approval_status == "hold":
            continue
        application_status = 'unapplied'
        if job.id in applied_job_ids:
            application_status = profile.jobs_applied[job.id]
        apiJobs.append(convertors.dbJobToApiJobWithStatus(job,application_status))
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
    application_status = 'unapplied'
    if job.id in applied_job_ids:
        application_status = profile.jobs_applied[job.id]
    apiJob = convertors.dbJobToApiJobWithStatus(job,application_status)
    return apiJob

# jobs by filtering
@router.get("/filteredJobs",response_model=api_models.Seeker_Job_List)
async def get_jobs_by_filter(decoded_token: (str,str) = Depends(token_listener),
                             location: str = None,
                             job_type: str= None,
                             category: str = None,
                             job_role: str = None,
                             min_salary: int = None):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    profile = await jobSeeker_db.get_job_seeker_profile_by_userId(decoded_token[1])
    applied_job_ids = profile.jobs_applied.keys()
    jobs = await job_db.get_all_jobs()
    apiJobs = []
    for job in jobs:
        if job.job_approval_status == "hold":
            continue
        if location!=None and (job.location==None or job.location!=location):
            continue
        if job_type!=None and (job.job_type==None or job.job_type!=job_type):
            continue
        if category!=None and (job.category==None or job.category!=category):
            continue
        if job_role!=None and (job.title==None or job.title!=job_role):
            continue
        if min_salary!=None and (job.salary==None or ("max" in job.salary and int(job.salary["max"])<min_salary)):
            continue
        application_status = 'unapplied'
        if job.id in applied_job_ids:
            application_status = profile.jobs_applied[job.id]
        apiJobs.append(convertors.dbJobToApiJobWithStatus(job,application_status))
    return api_models.Seeker_Job_List(
        jobs = apiJobs
    )
    # validated, msg = await validate_user(decoded_token[1], None, None)
    # if not validated:
    #     raise HTTPException(status_code=403, detail=msg)
    # profile = await jobSeeker_db.get_job_seeker_profile_by_userId(decoded_token[1])
    # applied_job_ids = profile.jobs_applied
    # jobs = await job_db.get_job_by_filter(category,location,job_type,job_role)
    # if not jobs:
    #     raise HTTPException(status_code = 404, detail="Jobs not found")
    # apiJobs = []
    # for job in jobs:
    #     if job.job_approval_status == 'hold':
    #         continue
    #     application_status = 'unapplied'
    #     if job.id in applied_job_ids:
    #         application_status = profile.jobs_applied[job.id]
    #     apiJobs.append(convertors.dbJobToApiJobWithStatus(job,application_status))
    # return api_models.Seeker_Job_List(
    #     jobs = apiJobs
    # )

# apply for job
@router.put("/applyJob/{jobId}", response_model=api_models.Success_Message_Response)
async def apply_job(jobId,decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    profile = await jobSeeker_db.get_job_seeker_profile_by_userId(decoded_token[1])
    applied_job_ids = profile.jobs_applied.keys()
    objectID = PydanticObjectId(jobId)
    if objectID in applied_job_ids:
        raise HTTPException(status_code=403, detail="Already applied for this job")
    job = await job_db.get_job_by_id(jobId)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status == "inactive":
        raise HTTPException(status_code=404, detail="Inactive Job")
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
    applied_jobs = profile.jobs_applied.items()
    apiJobs = []
    removed_jobs = []
    for job_id,status in applied_jobs:
        job = await job_db.get_job_by_id(str(job_id))
        if job:
            apiJobs.append(convertors.dbJobToApiJobWithStatus(job,status))
    return api_models.Seeker_Job_List(
        jobs = apiJobs
    )

#update profile image
@router.post("/updateIMG",response_model=api_models.Success_Message_Response)
async def updateIMG(decode_token: (str,str) = Depends(token_listener),imgobject: UploadFile = File(...)):
    validated,msg = await validate_user(decode_token[1],None,None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    filename = imgobject.filename
    new_filename = unique_filename_generator(filename)
    data = imgobject.file._file
    upload3 = await s3_client.upload_fileobj(filename=new_filename, fileobject=data)
    if upload3:
        s3_url = f"https://{s3_client.bucket}.s3.{s3_client.region}.amazonaws.com/{s3_client.key}{new_filename}"
        _, past_img = await jobSeeker_db.update_img(s3_url,decode_token[1])
        if past_img:
            status = await s3_client.delete_fileobj(past_img.split('/')[-1])
            if not status:
                print("Failed to delete old image")
        return api_models.Success_Message_Response(
            message = "Images uploaded successfully"
        )
    else:
        raise HTTPException(status_code = 400, detail="Failed to upload")
    
#get profile image
@router.get("/getIMG", response_model = api_models.IMG_Response)
async def getIMG(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1],None,None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    img_url = await jobSeeker_db.get_img(decoded_token[1])
    if not img_url:
        raise HTTPException(status_code=404,detail="image not found")
    return api_models.IMG_Response(
        img_url = img_url,
        bgimg_url = ""
    )