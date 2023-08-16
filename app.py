from fastapi import FastAPI

from config.config import initiate_database
from api.routes.user import router as UserRouter
from auth.jwt_bearer import JWTBearer

app = FastAPI()

token_listener = JWTBearer()

@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello World"}

app.include_router(UserRouter, tags=["User"], prefix="/user")
