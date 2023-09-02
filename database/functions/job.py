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

async def get_job_by_id(job_id: str) -> Union[DbUserModels.Job, None]:
    job = await job_collection.find_one({"_id": PydanticObjectId(job_id)})
    if job:
        return job
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
