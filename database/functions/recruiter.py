from typing import Union
from beanie import PydanticObjectId

import database.models.models as DbUserModels


recruiter_collection = DbUserModels.Recruiter

# --------------------------------------------------------------------------------------------------------

async def add_recruiter(new_profile: DbUserModels.Recruiter) -> DbUserModels.Recruiter:
    company = await new_profile.create()
    return company

async def update_profile(new_profile, userId) -> DbUserModels.Recruiter:
    req = {k: v for k, v in new_profile.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in req.items()
    }}
    to_update_profile = await get_recruiter_profile_by_userId(userId)
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile

async def get_recruiter_profile_by_userId(userId: str) -> Union[DbUserModels.Recruiter, None]:
    recruiter = await recruiter_collection.find_one({"userId": PydanticObjectId(userId)})
    if recruiter:
        return recruiter
    return None

async def get_recruiter_by_email(email: str) -> Union[dict, None]:
    company = await recruiter_collection.find_one({"email": email})
    if company:
        return company
    return None
