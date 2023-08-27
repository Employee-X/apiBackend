from typing import Union
from beanie import PydanticObjectId

import database.models.models as DbUserModels


recruiter_collection = DbUserModels.Recruiter

# --------------------------------------------------------------------------------------------------------

async def add_recruiter(new_user: DbUserModels.Recruiter) -> DbUserModels.Recruiter:
    company = await new_user.create()
    return company

async def get_recruiter_by_id(user_id: str) -> Union[dict, None]:
    company = await recruiter_collection.find_one({"_id": PydanticObjectId(user_id)})
    if company:
        return company
    return None

async def get_recruiter_by_email(email: str) -> Union[dict, None]:
    company = await recruiter_collection.find_one({"email": email})
    if company:
        return company
    return None
