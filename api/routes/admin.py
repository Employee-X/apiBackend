from typing import Optional
from fastapi import Body, APIRouter, HTTPException, Depends, UploadFile, File, logger
from passlib.context import CryptContext
from beanie import PydanticObjectId

from auth.jwt_handler import sign_jwt

import api.models.models as apiModels
import database.functions.user as user_db
import database.functions.admin as admin_db
import database.functions.job as job_db
import database.functions.recruiter as recruiter_db
import convertors.model_convertors as convertors
from auth.jwt_bearer import JWTBearer
from utils.utils import unique_filename_generator,Recruiter_Status,Job_Approval_Status,JOB_COUNT_CATEGORY_WISE


token_listener = JWTBearer()

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

async def validate_admin(user_id: str, email_id: Optional[str], mobile: Optional[str]):
    user = await user_db.get_user_by_id(user_id)
    if user and user.roles == "admin" and user.email_verified and user.mobile_verified:
        if email_id:
            if user.email != email_id:
                return False, "Email does not match"
        if mobile:
            if user.mobile != mobile:
                return False, "Mobile does not match"
        return True, ""
    return False, "Unauthorized Access"

@router.get("/recruiterlist",response_model=apiModels.Recriters_with_approval_status_list)
async def get_recruiters_list(decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_admin(decoded_token[1],None,None)
    if not validated:
        raise HTTPException(status_code=403,detail=msg)
    recruiters = await admin_db.get_recruiters_list()
    # raise HTTPException(status_code=205,detail=str(type(recruiters)))
    api_recruiters = []
    for recruiter in recruiters:
        api_recruiters.append(convertors.dbRecruiterToApiAdmin(recruiter))
    return apiModels.Recriters_with_approval_status_list(
        recruiters = api_recruiters
    )

@router.get("/getJobs/{recruiterId}",response_model=apiModels.Job_with_approval_status_list)
async def get_job_recruiterId(recruiterId: str,decoded_token: (str,str) =  Depends(token_listener)):
    validated, msg = await validate_admin(decoded_token[1],None,None)
    if not validated:
        raise HTTPException(status_code=403,detail=msg)
    jobs = await job_db.get_jobs_by_recruiter_id(recruiterId)
    apiJobs = []
    for job in jobs:
        apiJobs.append(convertors.dbJobToApiAdminJob(job))
    return apiModels.Job_with_approval_status_list(
        jobs=apiJobs
    )

@router.post("/approveRecruiter/{recruiterId}",response_model=apiModels.Success_Message_Response)
async def approveRecruiter(status: Recruiter_Status,recruiterId: str,decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_admin(decoded_token[1],None,None)
    if not validated:
        raise HTTPException(status_code=403,detail=msg)
    _ = await recruiter_db.update_approval_status(recruiterId,status)
    if not _:
        raise HTTPException(status_code=404,detail="recruiter approval status not updated")
    return apiModels.Success_Message_Response(
        message="Approval Status Changed to {}".format(status)
    )

@router.post("/approveJob/{jobId}",response_model=apiModels.Success_Message_Response)
async def approveJob(status: Job_Approval_Status,jobId: str,decoded_token: (str,str) = Depends(token_listener)):
    validated, msg = await validate_admin(decoded_token[1],None,None)
    if not validated:
        raise HTTPException(status_code=403,detail=msg)
    job = await job_db.get_job_by_id(jobId)
    _ = await job_db.update_job_approval(jobId,status)
    if not _:
        raise HTTPException(status_code=404,detail="job approval status not updated")
    updated_job = await job_db.get_job_by_id(jobId)
    if job.job_approval_status=="hold" and updated_job.job_approval_status=="unhold":
        JOB_COUNT_CATEGORY_WISE[job.category]+=1
    elif job.job_approval_status=="unhold" and updated_job.job_approval_status=="hold":
        JOB_COUNT_CATEGORY_WISE[job.category]-=1
    return apiModels.Success_Message_Response(
        message="Approval Status Changed to {}".format(status)
    )

@router.get("/user_stat",response_model=apiModels.admin_log)
async def user_stat(decoded_token: (str,str) = Depends(token_listener)) -> apiModels.admin_log:
    validated, msg = await validate_admin(decoded_token[1],None,None)
    if not validated:
        raise HTTPException(status_code=403,detail=msg)
    admin = await admin_db.get_admin_profile_by_adminId(decoded_token[1])
    if not admin:
        raise HTTPException(status_code=404,detail="Admin not found")
    return convertors.dbAdminToApiAdmin(admin)