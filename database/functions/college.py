from typing import Union
from beanie import PydanticObjectId

import database.models.models as DbUserModels


college_collection = DbUserModels.College

# --------------------------------------------------------------------------------------------------------

async def add_college(new_user: DbUserModels.College) -> DbUserModels.College:
    college = await new_user.create()
    return college

async def get_college_by_id(user_id: str) -> Union[dict, None]:
    college = await college_collection.find_one({"_id": PydanticObjectId(user_id)})
    if college:
        return college
    return None

async def get_college_by_email(email: str) -> Union[dict, None]:
    college = await college_collection.find_one({"email": email})
    if college:
        return college
    return None
