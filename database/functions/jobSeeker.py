from typing import Union
from beanie import PydanticObjectId
from fastapi import HTTPException
from pydantic_extra_types.phone_numbers import PhoneNumber
import database.models.models as DbUserModels

job_seeker_collection = DbUserModels.Job_Seeker

# --------------------------------------------------------------------------------------------------------

async def add_job_seeker(new_profile: DbUserModels.Job_Seeker) -> DbUserModels.Job_Seeker:
    job_seeker = await new_profile.create()
    return job_seeker

async def update_profile(new_profile, userId: str) -> DbUserModels.Job_Seeker:
    req = {k: v for k, v in new_profile.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in req.items()
    }}
    to_update_profile = await get_job_seeker_profile_by_userId(userId)
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile

async def update_email(email: str,mobile: PhoneNumber) -> DbUserModels.Job_Seeker:
    update_query = {"$set":{
        "email": email
    }}
    to_update_profile = await get_job_seeker_by_mobile(mobile)
    # raise HTTPException(status_code=404,detail=str(to_update_profile))
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile

async def update_cv(cv_url,verification_url, userId) -> (DbUserModels.Job_Seeker, Union[str, None], Union[str, None]):
    update_query = {"$set": {
        "cv_url": cv_url,
        "verification_doc_url": verification_url,
        "cv_verified_status": False,
        "cv_uploaded": True,
    }}
    to_update_profile = await get_job_seeker_profile_by_userId(userId)
    past_url = to_update_profile.cv_url
    past_verification_url = to_update_profile.verification_doc_url
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile, past_url, past_verification_url

async def apply_job(jobId: str, userId: str):
    update_query = {"$set": {
        f"jobs_applied.{PydanticObjectId(jobId)}":"applied",
    }}
    to_update_profile = await get_job_seeker_profile_by_userId(userId)
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile

async def get_cv(userId) -> (Union[str, None], Union[str, None], bool):
    profile = await get_job_seeker_profile_by_userId(userId)
    return profile.cv_url, profile.verification_doc_url, profile.cv_verified_status,profile.cv_uploaded


async def get_job_seeker_by_mobile(mobile: PhoneNumber) -> Union[dict, None]:
    user = await job_seeker_collection.find_one({"phone_number": mobile})
    if user:
        return user
    return None

async def get_job_seeker_profile_by_userId(userId: str) -> Union[DbUserModels.Job_Seeker, None]:
    job_seeker = await job_seeker_collection.find_one({"userId": PydanticObjectId(userId)})
    if job_seeker:
        return job_seeker
    return None

async def get_job_seeker_by_email(email: str) -> Union[dict, None]:
    job_seeker = await job_seeker_collection.find_one({"email": email})
    if job_seeker:
        return job_seeker
    return None


async def update_img(img_url, userId) -> (DbUserModels.Recruiter, Union[str, None]):
    update_query = {"$set": {
        "img_url": img_url,
        "bgimg_url": ""
    }}
    to_update_profile = await get_job_seeker_profile_by_userId(userId)
    past_img_url = to_update_profile.img_url
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile, past_img_url

async def get_img(userId) -> (Union[str, None]):
    profile = await get_job_seeker_profile_by_userId(userId)
    return profile.img_url

# for deletion of job from list of jobseeker
async def update_job_rejection(jobId: str,userId: str) -> bool:
    update_query = {"$set": {
        f"jobs_applied.{PydanticObjectId(jobId)}":"rejected",
    }}
    to_update_profile = await get_job_seeker_profile_by_userId(PydanticObjectId(userId))
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile
