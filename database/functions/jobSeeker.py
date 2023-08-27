from typing import Union
from beanie import PydanticObjectId

import database.models.models as DbUserModels

job_seeker_collection = DbUserModels.Job_Seeker

# --------------------------------------------------------------------------------------------------------


async def add_job_seeker(new_user: DbUserModels.Job_Seeker) -> DbUserModels.Job_Seeker:
    job_seeker = await new_user.create()
    return job_seeker

async def get_job_seeker_by_id(user_id: str) -> Union[dict, None]:
    job_seeker = await job_seeker_collection.find_one({"_id": PydanticObjectId(user_id)})
    if job_seeker:
        return job_seeker
    return None

async def get_job_seeker_by_email(email: str) -> Union[dict, None]:
    job_seeker = await job_seeker_collection.find_one({"email": email})
    if job_seeker:
        return job_seeker
    return None
