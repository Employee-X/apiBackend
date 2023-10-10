from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.config import initiate_database

from api.routes.user import router as UserRouter
from api.routes.jobSeeker import router as JSRouter
from api.routes.college import router as CLLGRouter
from api.routes.recruiter import router as RECRouter

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://www.employeex.co.in",
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


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello World"}

# Authentication Routes
app.include_router(UserRouter, tags=["User"], prefix="/user")

# Post Authentication Profile Routes
app.include_router(JSRouter, tags=["JobSeeker"], prefix="/jobseeker")
app.include_router(CLLGRouter, tags=["College"], prefix="/college")
app.include_router(RECRouter, tags=["Recruiter"], prefix="/recruiter")
