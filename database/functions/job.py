from typing import List, Union
from beanie import PydanticObjectId
import database.models.models as DbUserModels
from utils.utils import JOB_COUNT_CATEGORY_WISE

job_collection = DbUserModels.Job

# --------------------------------------------------------------------------------------------------------

async def add_job(new_job: DbUserModels.Job) -> DbUserModels.Job:
    job = await new_job.create()
    JOB_COUNT_CATEGORY_WISE[new_job.category] += 1
    return job

async def get_jobs_by_recruiter_id(recruiter_id: str) -> List[DbUserModels.Job]:
    jobs = await job_collection.find({"recruiterId": PydanticObjectId(recruiter_id)}).to_list()
    if jobs:
        return jobs
    return []

async def get_all_jobs() -> List[DbUserModels.Job]:
    jobs = await job_collection.find().to_list()
    if jobs:
        return jobs
    return []

async def get_job_by_id(job_id: str) -> Union[DbUserModels.Job, None]:
    job = await job_collection.find_one({"_id": PydanticObjectId(job_id)})
    if job:
        return job
    return None

async def get_job_by_filter(category: Union[str,None],location: Union[str,None],job_type: Union[str,None],job_role: Union[str,None]) -> Union[DbUserModels.Job,None]:
    if category == None and location==None and job_type==None:
        jobs = await job_collection.find().to_list()
        return jobs
    query = {}
    if location is not None:
        query["location"] = location
    if job_type is not None: 
        query["job_type"] = job_type
    if category is not None:
        query["category"] = category
    if job_role is not None:
        query["title"] = job_role
    jobs = await job_collection.find(query).to_list()
    if jobs:
        return jobs
    return None


async def update_job(new_job, job_id: str) -> DbUserModels.Job:
    req = {k: v for k, v in new_job.dict().items() if v is not None}
    req.pop("recruiterId", None)
    update_query = {"$set": {
        field: value for field, value in req.items()
    }}
    to_update_job = await get_job_by_id(job_id)
    updated_job = await to_update_job.update(update_query)
    return updated_job

async def delete_job(job_id: str) -> bool:
    update_query = {"$set":{
        "status": "inactive"
    }}
    job = await get_job_by_id(job_id)
    if JOB_COUNT_CATEGORY_WISE[job.category]>0:
        JOB_COUNT_CATEGORY_WISE[job.category] -= 1
    updated_job = await job.update(update_query)
    return updated_job

async def apply_job(jobId: str, userId: str) -> bool:
    update_query = {"$set": {
        f"applicants.{PydanticObjectId(userId)}":False,
    },
    "$inc":{
        "no_of_applicants": 1
    }}
    to_update_job = await get_job_by_id(jobId)
    updated_job = await to_update_job.update(update_query)
    return updated_job

async def update_coin(jobId: str,new_value: str) -> bool:
    update_query = {"$set":{
        "coins": new_value
    }}
    to_update_job = await get_job_by_id(jobId)
    updated_job = await to_update_job.update(update_query)
    return updated_job

async def mark_visited_applicant(jobId: str,userId: str) -> bool:
    update_query = {"$set":{
        f"applicants.{PydanticObjectId(userId)}":True
    }}
    to_update_job = await get_job_by_id(jobId)
    updated_job = await to_update_job.update(update_query)
    return updated_job

async def update_applicant_list(jobId: str,userId: str) -> bool:
    update_query = {"$unset":{
        f"applicants.{PydanticObjectId(userId)}":""
    },
    "$inc": {
        "no_of_applicants": -1
    }}
    to_update_job = await get_job_by_id(jobId)
    updated_job = await to_update_job.update(update_query)
    return updated_job
