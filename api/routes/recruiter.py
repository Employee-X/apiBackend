from typing import Optional
from fastapi import Body, APIRouter, HTTPException, Depends, UploadFile, File, logger
from passlib.context import CryptContext
from beanie import PydanticObjectId
from datetime import datetime,timedelta

from auth.jwt_handler import sign_jwt

import database.functions.user as user_db
import database.functions.jobSeeker as jobSeeker_db
import database.functions.recruiter as recruiter_db
import database.functions.job as job_db
import database.functions.admin as admin_db
import convertors.model_convertors as convertors
import api.models.models as api_models
from auth.jwt_bearer import JWTBearer
from utils.utils import unique_filename_generator
from config.config import s3_client
from auth.aes_security import *
from business.policy import *



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

# Add job
@router.post("/addJob", response_model=api_models.Success_Message_Response)
async def add_job(decoded_token: (str,str) = Depends(token_listener),job: api_models.Job = Body(...)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    recruiter = await recruiter_db.get_recruiter_profile_by_userId(decoded_token[1])
    logo = recruiter.img_url
    free_jobs = recruiter.free_jobs
    if free_jobs>0:
        coins = await recruiter_db.get_coins(decoded_token[1])
        new_coin_value = int(decrypt(coins)) + COINS_ON_NEW_JOB
        coins = encrypt(str(new_coin_value))
        _ = await recruiter_db.update_free_job(decoded_token[1],-1)
        _ = await recruiter_db.update_coin(decoded_token[1],coins)
    job_approval_status = "hold"
    if recruiter.approval_status == "allowed":
        job_approval_status = "unhold"
    dbJob = convertors.apiJobToDbJob(job, PydanticObjectId(decoded_token[1]),logo,job_approval_status)
    job_approval_status = "hold"
    if recruiter.approval_status == "allowed":
        job_approval_status = "unhold"
    _ = await job_db.add_job(dbJob)
    _ = await admin_db.incr_job()
    return api_models.Success_Message_Response(
        message = "Job added successfully"
    )

@router.get("/getJobs", response_model=api_models.Job_List)
async def get_my_jobs(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)

    jobs = await job_db.get_jobs_by_recruiter_id(decoded_token[1])
    apiJobs = []
    for job in jobs:
        if job.status == "active":
            apiJobs.append(convertors.dbJobToApiJobWithId(job))
    return api_models.Job_List(
        jobs = apiJobs
    )

# update job
@router.post("/updateJob/{jobId}", response_model=api_models.Success_Message_Response)
async def update_job(jobId,decoded_token: (str,str) = Depends(token_listener),job: api_models.Job = Body(...)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    recruiter = await recruiter_db.get_recruiter_profile_by_userId(decoded_token[1])
    company_name = recruiter.company_name
    if job.company_name != company_name:
        raise HTTPException(status_code=403, detail="Company name does not match")
    dbJob = convertors.apiJobToDbJob(job, PydanticObjectId(decoded_token[1]),job.logo)
    print(dbJob)
    _ = await job_db.update_job(dbJob,jobId)

    return api_models.Success_Message_Response(
        message = "Job updated successfully"
    )

# delete job
@router.delete("/deleteJob/{jobId}", response_model=api_models.Success_Message_Response)
async def delete_job(jobId,decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    # decreasing coins corresponding to that job on deleting job
    _ = await job_db.delete_job(jobId)
    _ = await admin_db.decr_jobs()
    return api_models.Success_Message_Response(
        message = "Job deleted successfully"
    )

# get job applicants
@router.get("/getJobApplicants/{jobId}", response_model=api_models.Seeker_List)
async def get_job_applicants(jobId,decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)

    job = await job_db.get_job_by_id(jobId)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    applicants = job.applicants.items()
    apiApplicants = []
    for applicant_id,visited in applicants:
        applicant = await jobSeeker_db.get_job_seeker_profile_by_userId(str(applicant_id))
        apiApplicants.append(convertors.dbJobseekerToApiRecruiterWithoutCV(applicant,visited))
    return api_models.Seeker_List(
        applicants=apiApplicants
    )

# job applicants filter
@router.get("/filterApplicants/{jobId}",response_model=api_models.Seeker_List)
async def filter_applicants(jobId,age_min: int = None,age_max: int = None,location: str = None,gender: str = None,decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)

    job = await job_db.get_job_by_id(jobId)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    applicants = job.applicants.items()
    apiApplicants = []
    for applicant_id,visited in applicants:
        applicant = await jobSeeker_db.get_job_seeker_profile_by_userId(str(applicant_id))
        api_applicant = convertors.dbJobseekerToApiRecruiterWithoutCV(applicant,visited)
        _gender = api_applicant.gender
        _location = api_applicant.location
        _dob = datetime.strptime(api_applicant.date_of_birth,"%Y-%m-%d")
        _today = datetime.now()
        _age  = _today.year - _dob.year
        if _today.month < _dob.month or (_today.month==_dob.month and _today.day < _dob.date):
            _age -= 1
        if(age_min!=None and _age<age_min):
            continue
        if (age_max!=None and age_max<_age):
            continue
        if(location!=None and location!=_location):
            continue
        if(gender!=None and gender!=_gender):
            continue
        apiApplicants.append(api_applicant)
    return api_models.Seeker_List(
        applicants=apiApplicants
    )

# get user profile
@router.get("/getUserProfile/{userId}", response_model=api_models.Job_Seeker_Profile_With_Id_CV)
async def get_user_profile(userId,job_id,decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    profile = await jobSeeker_db.get_job_seeker_profile_by_userId(userId)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    job_profile = await job_db.get_job_by_id(job_id)
    if not job_profile:
        raise HTTPException(status_code=404, detail="Job not found")
    is_visited_profile = job_profile.applicants[PydanticObjectId(userId)]
    if not is_visited_profile:
        # decreasing the total coins and giving insufficint mssg for CV view
        coins = await recruiter_db.get_coins(decoded_token[1])
        value_of_coins = int(decrypt(coins))
        new_value = value_of_coins - COINS_DECREASE_ON_CV_VIEW
        if new_value<0:
            HTTPException(status_code=404,detail="Insufficient Coins")
        coins = encrypt(str(new_value))
        _ = await recruiter_db.update_coin(decoded_token[1],coins)
        _ = await job_db.mark_visited_applicant(job_id,userId)

        # decreasing coins allocated with the particular job
        job_assoc_coin = int(decrypt(job_profile.coins))
        if job_assoc_coin>=COINS_DECREASE_ON_CV_VIEW:
            job_assoc_coin -= COINS_DECREASE_ON_CV_VIEW
            _ = await job_db.update_coin(job_id,encrypt(str(job_assoc_coin)))
        
        # updating the global coins count and marking the applicant visited
        coins = encrypt(str(new_value))
        _ = await recruiter_db.update_coin(decoded_token[1],coins)
        _ = await job_db.mark_visited_applicant(job_id,userId)


    apiProfile = convertors.dbJobSeekerProfileToApiJobSeekerProfileWithIdCv(profile)
    return apiProfile

#remove job applicants
@router.delete("/removeApplicant/{userId}/{jobId}",response_model=api_models.Success_Message_Response)
async def remove_job_applicant(userId,jobId,decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1], None, None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    job = await job_db.get_job_by_id(jobId)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    _ = await job_db.update_applicant_list(jobId,userId)
    _ = await jobSeeker_db.update_job_rejection(jobId,userId)
    return api_models.Success_Message_Response(
        message = "Applicant removed successfully"
    )



#update company logo/image
@router.post("/updateIMG",response_model=api_models.Success_Message_Response)
async def updateIMG(decode_token: (str,str) = Depends(token_listener),imgobject: UploadFile = None,bgimgobject: UploadFile = None):
    validated,msg = await validate_user(decode_token[1],None,None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    if imgobject:
        filename = imgobject.filename
        new_filename = unique_filename_generator(filename)
        data = imgobject.file._file
        upload3 = await s3_client.upload_fileobj(filename=new_filename, fileobject=data)
        if upload3:
            s3_url = f"https://{s3_client.bucket}.s3.{s3_client.region}.amazonaws.com/{s3_client.key}{new_filename}"
            _,s3_url2 = await recruiter_db.get_img(decode_token[1])
            _, past_img,past_bgimg = await recruiter_db.update_img(s3_url,s3_url2,decode_token[1])
            if past_img:
                status = await s3_client.delete_fileobj(past_img.split('/')[-1])
                if not status:
                    print("Failed to delete old image")
        else:
            raise HTTPException(status_code = 400, detail="Failed to upload")
    if bgimgobject:
        filename2 = bgimgobject.filename
        new_filename2 = unique_filename_generator(filename2)
        data2 = bgimgobject.file._file
        upload32 = await s3_client.upload_fileobj(filename=new_filename2,fileobject=data2)
        if upload32:
            s3_url,_ = await recruiter_db.get_img(decode_token[1])
            s3_url2 = f"https://{s3_client.bucket}.s3.{s3_client.region}.amazonaws.com/{s3_client.key}{new_filename2}"
            _, past_img,past_bgimg = await recruiter_db.update_img(s3_url,s3_url2,decode_token[1])
            if past_bgimg:
                status = await s3_client.delete_fileobj(past_bgimg.split('/0')[-1])
                if not status:
                    print("Failed to delete old backgound")
        else:
            raise HTTPException(status_code = 400, detail="Failed to upload")
    return api_models.Success_Message_Response(
        message = "Images uploaded successfully"
    )
    
#get image/logo
@router.get("/getIMG", response_model = api_models.IMG_Response)
async def getIMG(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1],None,None)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    img_url,bgimg_url = await recruiter_db.get_img(decoded_token[1])
    if not img_url:
        raise HTTPException(status_code=404,detail="image not found")
    if not bgimg_url:
        raise HTTPException(status_code=404, detail="bgimage not found")
    return api_models.IMG_Response(
        img_url = img_url,
        bgimg_url = bgimg_url
    )


#get coins
@router.get("/getCoin", response_model = api_models.Coin)
async def getCoin(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_user(decoded_token[1],None,None)
    if not validated:
        raise HTTPException(status_code=403,detail=msg)
    coins = await recruiter_db.get_coins(decoded_token[1])
    if not coins:
        raise HTTPException(status_code=404,detail="coin not fetched")
    return api_models.Coin(
        coins = coins
    )

#addCoin
@router.post("/addCoin",response_model = api_models.Success_Message_Response)
async def addCoins(decoded_token: (str,str) = Depends(token_listener),amount: str = encrypt('0')):
    validated, msg = await validate_user(decoded_token[1],None,None)
    if not validated:
        raise HTTPException(status_code=403,detail=msg)
    coins = await recruiter_db.get_coins(decoded_token[1])
    if not coins:
        raise HTTPException(status_code=404,detail="coin not fetched")
    amount = int(decrypt(coins)) + int(decrypt(amount))
    coins = encrypt(str(amount))
    _ = await recruiter_db.update_coin(decoded_token[1],coins)
    return api_models.Success_Message_Response(
        message = "Coins added successfully"
    )
