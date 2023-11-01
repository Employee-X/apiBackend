from fastapi import FastAPI,HTTPException, Request,status
from functools import wraps
import time

from config.config import initiate_database

from api.routes.user import router as UserRouter
from api.routes.jobSeeker import router as JSRouter
from api.routes.college import router as CLLGRouter
from api.routes.recruiter import router as RECRouter
from utils.utils import JOB_COUNT_CATEGORY_WISE

app = FastAPI()

@app.on_event("startup")
async def start_database():
    await initiate_database()

def rate_limit(max_call: int, time_frame: int):
    def decorator(func):
        calls = []
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            now = time.time()
            calls_in_time_frame = [call for call in calls if call >= now-time_frame]
            if len(calls_in_time_frame) >= max_call:
                raise HTTPException(status_code = status.HTTP_429_TOO_MANY_REQUESTS,detail="Rate limit exceeded.")
            calls.append(now)
            return await func(request,*args,**kwargs)
        return wrapper
    return decorator
 

@app.get("/", tags=["Root"])
@rate_limit(max_call=5,time_frame=5)
async def read_root(request: Request):
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
