from fastapi import FastAPI

from config.config import initiate_database
from api.routes.jobSeeker import router as JSRouter
from api.routes.college import router as CLLGRouter
from api.routes.recruiter import router as RECRouter
from auth.jwt_bearer import JWTBearer

app = FastAPI()

token_listener = JWTBearer()

@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello World"}

app.include_router(JSRouter, tags=["JobSeeker"], prefix="/jobseeker")
app.include_router(CLLGRouter, tags=["College"], prefix="/college")
app.include_router(RECRouter, tags=["Recruiter"], prefix="/recruiter")
