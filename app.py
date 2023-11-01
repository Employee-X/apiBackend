from fastapi import FastAPI,HTTPException, Request,status
from functools import wraps
import time

from config.config import initiate_database

from api.routes.user import router as UserRouter
from api.routes.jobSeeker import router as JSRouter
from api.routes.college import router as CLLGRouter
from api.routes.recruiter import router as RECRouter
from utils.utils import JOB_COUNT_CATEGORY_WISE
import database.models.models as DbUserModels
job_collection = DbUserModels.Job

app = FastAPI()

@app.on_event("startup")
async def start_database():
    await initiate_database()
    jobs = await job_collection.find().to_list()
    if jobs:
        for job in jobs:
            if job.category!=None and job.category in JOB_COUNT_CATEGORY_WISE.keys():
                JOB_COUNT_CATEGORY_WISE[job.category]+=1
 

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello World"}

@app.get("/getOpenings",tags=["Root"])
async def get_openings():
    return JOB_COUNT_CATEGORY_WISE
    

# Authentication Routes
app.include_router(UserRouter, tags=["User"], prefix="/user")

# Post Authentication Profile Routes
app.include_router(JSRouter, tags=["JobSeeker"], prefix="/jobseeker")
app.include_router(CLLGRouter, tags=["College"], prefix="/college")
app.include_router(RECRouter, tags=["Recruiter"], prefix="/recruiter")
