from typing import List, Union
from beanie import PydanticObjectId
import database.models.models as DbUserModels


job_collection = DbUserModels.Job

# --------------------------------------------------------------------------------------------------------

async def add_job(new_job: DbUserModels.Job) -> DbUserModels.Job:
    job = await new_job.create()
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

async def get_job_by_filter(category: Union[str,None],location: Union[str,None],job_type: Union[str,None]) -> Union[DbUserModels.Job,None]:
    if category == None and location==None and job_type==None:
        jobs = await job_collection.find().to_list()
    elif category == None and location==None:
        jobs = await job_collection.find({"job_type": job_type}).to_list()
    elif category == None and job_type ==None:
        jobs = await job_collection.find({"location": location}).to_list()
    elif location == None and job_type == None:
        jobs = await job_collection.find({"title": category}).to_list()
    elif category == None:
        jobs = await job_collection.find({"job_type": job_type,"location": location}).to_list()
    elif job_type == None:
        jobs = await job_collection.find({"location": location, "title": category}).to_list()
    elif location == None:
        jobs = await job_collection.find({"job_type": job_type, "title": category}).to_list()
    else:
        jobs = await job_collection.find({"job_type": job_type, "title": category, "location": location}).to_list()
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
    job = await get_job_by_id(job_id)
    if job:
        result = await job.delete()
        return True
    else:
        result = None
        return False

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