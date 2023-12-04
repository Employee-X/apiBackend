from fastapi import FastAPI

from config.config import initiate_database
from fastapi.middleware.cors import CORSMiddleware

from api.routes.user import router as UserRouter
from api.routes.jobSeeker import router as JSRouter
from api.routes.college import router as CLLGRouter
from api.routes.recruiter import router as RECRouter
from api.routes.admin import router as ADMRouter
from utils.utils import JOB_COUNT_CATEGORY_WISE
import database.models.models as DbUserModels
import database.functions.job as job_db
from beanie import PydanticObjectId
import database.functions.admin as admin_db
job_collection = DbUserModels.Job
recruiter_collection = DbUserModels.Recruiter
job_seeker_collection = DbUserModels.Job_Seeker

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://www.employeex.co.in",
    "https://www.employeex.co.in",
    "http://frontend-test-env.eba-qubingfp.ap-south-1.elasticbeanstalk.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_database():
    await initiate_database()
    jobs = await job_collection.find().to_list()
    active_jobs = 0
    inactive_jobs = 0
    if jobs:
        for job in jobs:
            if job.category!=None and job.category in JOB_COUNT_CATEGORY_WISE.keys():
                JOB_COUNT_CATEGORY_WISE[job.category]+=1
            if job.status == "active":
                active_jobs+=1
            elif job.status == "inactive":
                inactive_jobs+=1
    _ = await admin_db.start_admin(active_jobs,inactive_jobs)
    # await update()
    

 

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
app.include_router(ADMRouter, tags=["Admin"], prefix="/admin")


# async def update():
#     job_seekers = await job_seeker_collection.find().to_list()
#     for job_seeker in job_seekers:
#         # if not job_seeker.cv_uploaded:
#         cv_uploaded = False
#         if job_seeker.cv_url!=None:
#             cv_uploaded = True
#         update_query = {"$set":{
#             "cv_uploaded": cv_uploaded
#         }}
#         _ = await job_seeker.update(update_query)