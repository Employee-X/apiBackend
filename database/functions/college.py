from typing import Union
from beanie import PydanticObjectId

import database.models.models as DbUserModels


college_collection = DbUserModels.College

# --------------------------------------------------------------------------------------------------------

async def add_college(new_profile: DbUserModels.College) -> DbUserModels.College:
    college = await new_profile.create()
    return college

async def update_profile(new_profile, userId) -> DbUserModels.College:
    req = {k: v for k, v in new_profile.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in req.items()
    }}
    to_update_profile = await get_college_profile_by_userId(userId)
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile

async def get_college_profile_by_userId(userId: str) -> Union[DbUserModels.College, None]:
    college = await college_collection.find_one({"userId": PydanticObjectId(userId)})
    if college:
        return college
    return None

async def get_college_by_email(email: str) -> Union[dict, None]:
    college = await college_collection.find_one({"email": email})
    if college:
        return college
    return None
