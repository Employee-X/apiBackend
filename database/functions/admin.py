from typing import Union,List
from beanie import PydanticObjectId
from fastapi import HTTPException

import database.models.models as DbUserModels

job_seeker_collection = DbUserModels.Job_Seeker
job_collection = DbUserModels.Job
recruiter_collection = DbUserModels.Recruiter
user_collection = DbUserModels.User
admin_collection = DbUserModels.Admin

async def get_admin_by_id(user_id: str) -> Union[DbUserModels.User, None]:
    admin = await admin_collection.find_one({"_id": PydanticObjectId(user_id)})
    if admin:
        return admin
    return None



async def get_recruiters_list() -> List[DbUserModels.Recruiter]:
    recruiters_list = await recruiter_collection.find().to_list()
    if recruiters_list:
        return recruiters_list
    return []