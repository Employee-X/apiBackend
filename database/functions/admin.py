from typing import Union,List
from beanie import PydanticObjectId
from fastapi import HTTPException

import database.models.models as DbUserModels
from datetime import datetime,timedelta
from config.config import Settings

job_seeker_collection = DbUserModels.Job_Seeker
job_collection = DbUserModels.Job
recruiter_collection = DbUserModels.Recruiter
user_collection = DbUserModels.User
admin_collection = DbUserModels.Admin

adminId = Settings().ADMIN_ID

async def add_admin(new_profile: DbUserModels.Admin) -> DbUserModels.Admin:
    admin = await new_profile.create()
    return admin

async def get_admin_profile_by_adminId(adminId: str) -> Union[DbUserModels.Admin,None]:
    admin = await admin_collection.find_one({"adminId": PydanticObjectId(adminId)})
    if admin:
        return admin
    return None

async def check_time_limit() -> bool:
    admin = await get_admin_profile_by_adminId(adminId)
    day_end_epoch = admin.day_end_epoch
    week_end_epoch = admin.week_end_epoch
    month_end_epoch = admin.month_end_epoch
    now = int(datetime.now().strftime('%s'))
    query = {}
    if now>day_end_epoch:
        updated_bound = (datetime.now()+timedelta(days=1)).strftime('%s')
        query["day_end_epoch"] = updated_bound
        query["last_day_logins"] = admin.day_logins
        query["last_day_new_users"] =  admin.day_new_users
        query["day_logins"] = 0
        query["day_new_users"] = 0
    if now>week_end_epoch:
        updated_bound = (datetime.now()+timedelta(days=7)).strftime('%s')
        query["week_end_epoch"] = updated_bound
        query["last_week_logins"] = admin.week_logins
        query["last_week_new_users"] =  admin.week_new_users
        query["week_logins"] = 0
        query["week_new_users"] = 0
    if now>month_end_epoch:
        updated_bound = (datetime.now()+timedelta(days=30)).strftime('%s')
        query["month_end_epoch"] = updated_bound
        query["last_month_logins"] = admin.month_logins
        query["last_month_new_users"] =  admin.month_new_users
        query["month_logins"] = 0
        query["month_new_users"] = 0
    update_query = {"$set": query}
    updated_admin = await admin.update(update_query)
    return updated_admin


async def incr_login() -> bool:
    _ = await check_time_limit()
    update_query = {"$inc":{
        "day_logins":1,
        "week_logins":1,
        "month_logins":1,
    }}
    admin = await get_admin_profile_by_adminId(adminId)
    updated_admin = await admin.update(update_query)
    return updated_admin

async def incr_signup() -> bool:
    _ = await check_time_limit()
    update_query = {"$inc":{
        "day_new_users":1,
        "week_new_users":1,
        "month_new_users":1,
    }}
    admin = await get_admin_profile_by_adminId(adminId)
    updated_admin = await admin.update(update_query)
    return updated_admin

async def incr_job(amount=0) -> bool:
    if amount==0:
        amount = 1
    update_query = {"$inc":{
        "jobs":amount,
        "active_jobs":amount,
    }}
    admin = await get_admin_profile_by_adminId(adminId)
    updated_admin = await admin.update(update_query)
    return updated_admin

async def decr_jobs() -> bool:
    admin = await get_admin_profile_by_adminId(adminId)
    incr = 0
    if admin.active_jobs>0:
        incr = 1
    update_query = {"$inc":{
        "active_jobs":-incr,
        "inactive_jobs":incr,
    }}
    updated_admin = await admin.update(update_query)
    return updated_admin

async def start_admin(active_jobs,inactive_jobs):
    admin = await get_admin_profile_by_adminId(adminId) 
    update_query = {"$set":{
        "active_jobs": active_jobs,
        "inactive_jobs": inactive_jobs,
        "jobs": active_jobs + inactive_jobs,
    }}
    updated_admin = await admin.update(update_query)
    return updated_admin

async def get_recruiters_list() -> List[DbUserModels.Recruiter]:
    recruiters_list = await recruiter_collection.find().to_list()
    if recruiters_list:
        return recruiters_list
    return []