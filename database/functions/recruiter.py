from typing import Union
from beanie import PydanticObjectId
from uuid import uuid1
import database.models.models as DbUserModels
from auth.aes_security import *
from business.policy import REFERRAL_AMOUNT
from fastapi import HTTPException
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

async def update_img(img_url, bgimg_url, userId) -> (DbUserModels.Recruiter, Union[str, None]):
    update_query = {"$set": {
        "img_url": img_url,
        "bgimg_url": bgimg_url
    }}
    to_update_profile = await get_recruiter_profile_by_userId(userId)
    past_img_url = to_update_profile.img_url
    past_bgimg_url = to_update_profile.bgimg_url
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile, past_img_url,past_bgimg_url

async def get_img(userId) -> (Union[str, None]):
    profile = await get_recruiter_profile_by_userId(userId)
    return profile.img_url,profile.bgimg_url


async def get_coins(userId) -> str:
    profile = await get_recruiter_profile_by_userId(userId)
    return profile.coins

async def update_coin(userId,value) -> str:
    update_query = {"$set":{
        "coins": value
    }}
    to_update_profile = await get_recruiter_profile_by_userId(userId)
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile

async def update_free_job(userId,value) -> str:
    update_query = {"$inc": {
        "free_jobs": value
    }}
    to_update_profile = await get_recruiter_profile_by_userId(userId)
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile

async def update_approval_status(userId,status) -> str:
    update_query = {"$set":{
        "approval_status": status
    }}
    to_update_profile = await get_recruiter_profile_by_userId(userId)
    updated_profile = await to_update_profile.update(update_query)
    return updated_profile

async def update_ref_id(userId) -> str:
    ref_id = str(uuid1())
    update_query = {"$set":{
        "referral_id": ref_id
    }}
    to_update_profile = await get_recruiter_profile_by_userId(userId)
    _ = await to_update_profile.update(update_query)
    if _:
        return ref_id
    return None

async def check_referral(referral) -> bool:
    recruiter = await recruiter_collection.find_one({"referral_id": referral})
    if not recruiter:
        return False
    coins = int(decrypt(recruiter.coins)) + REFERRAL_AMOUNT
    # raise HTTPException(status_code=404,detail=str(coins))
    updated_coins = encrypt(str(coins))
    _= await update_coin(recruiter.userId,updated_coins)
    _ = await update_ref_id(recruiter.userId)
    return True