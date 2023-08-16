from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt

import database.functions.user as user_db
import convertors.model_convertors as convertors
import api.models.models as api_models


router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def user_login(user_credentials: api_models.UserSignIn = Body(...)):
    user_exists = await user_db.get_user_by_email(user_credentials.username)
    if user_exists:
        password = hash_helper.verify(user_credentials.password, user_exists.password)
        if password:
            return sign_jwt(user_credentials.username)

        raise HTTPException(status_code=403, detail="Incorrect email or password")

    raise HTTPException(status_code=403, detail="Incorrect email or password")


@router.post("/new", response_model=api_models.UserData)
async def user_signup(user:api_models.User = Body(...)):
    user_exists = await user_db.get_user_by_email(user.email)
    if user_exists:
        raise HTTPException(
            status_code=409, detail="User with email supplied already exists"
        )

    user.password = hash_helper.encrypt(user.password)
    
    dbUser = convertors.apiUserToDbUser(user)
    new_user = await user_db.add_user(dbUser)
    new_userData = convertors.dbUserDataToApiUserData(new_user)
    
    return new_userData
