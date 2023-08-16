from typing import Union
from beanie import PydanticObjectId

import database.models.user as DbUserModels

user_collection = DbUserModels.User

async def add_user(new_user: DbUserModels.User) -> DbUserModels.User:
    user = await new_user.create()
    return user

async def get_user_by_id(user_id: str) -> Union[dict, None]:
    user = await user_collection.find_one({"_id": PydanticObjectId(user_id)})
    if user:
        return user
    return None

async def get_user_by_email(email: str) -> Union[dict, None]:
    user = await user_collection.find_one({"email": email})
    if user:
        return user
    return None
