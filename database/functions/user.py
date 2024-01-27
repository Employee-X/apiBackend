import datetime
from typing import Union
from beanie import PydanticObjectId
from pydantic_extra_types.phone_numbers import PhoneNumber
import database.models.models as DbUserModels

user_collection = DbUserModels.User

# --------------------------------------------------------------------------------------------------------


async def add_user(new_user: DbUserModels.User) -> DbUserModels.User:
    user = await new_user.create()
    return user

async def delete_user(user_id: str) -> Union[DbUserModels.User, None]:
    user = await user_collection.delete_one({"_id": PydanticObjectId(user_id)})
    if user:
        return user
    return None

async def get_user_by_id(user_id: str) -> Union[DbUserModels.User, None]:
    user = await user_collection.find_one({"_id": PydanticObjectId(user_id)})
    if user:
        return user
    return None

async def get_user_by_email(email: str) -> Union[dict, None]:
    user = await user_collection.find_one({"email": email})
    if user:
        return user
    return None

async def get_user_by_mobile(mobile: PhoneNumber) -> Union[dict, None]:
    user = await user_collection.find_one({"mobile": mobile})
    if user:
        return user
    return None

async def update_user(user_id: str,email: str,password: str):
    user = await get_user_by_id(user_id)
    update_query = {"$set": {
        "email": email,
        "password": password,
        "email_verified": True,
    }}
    updated_user = await user.update(update_query)
    return updated_user

async def update_otp(user_id: str, otp: int) -> Union[DbUserModels.User, None]:
    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
    resend_time = datetime.datetime.now() + datetime.timedelta(minutes=0.5)
    time_in_str = expiration_time.isoformat()
    update_query = {"$set": {
        "otp": otp,
        "otp_expiration": time_in_str,
        "otp_resend": resend_time.isoformat()
    }}
    user_to_update = await get_user_by_id(user_id)
    updated_user = await user_to_update.update(update_query)
    return updated_user

async def update_phone_verified(user_id: str) -> Union[DbUserModels.User, None]:
    update_query = {"$set": {
        "mobile_verified": True,
    }}
    user_to_update = await get_user_by_id(user_id)
    updated_user = await user_to_update.update(update_query)
    return updated_user

async def update_email_verified(user_id: str) -> Union[DbUserModels.User, None]:
    update_query = {"$set": {
        "email_verified": True,
    }}
    user_to_update = await get_user_by_id(user_id)
    updated_user = await user_to_update.update(update_query)
    return updated_user