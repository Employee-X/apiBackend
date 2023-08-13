from fastapi import FastAPI

from config.config import initiate_database

app = FastAPI()

@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello World"}