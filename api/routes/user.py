from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt
from utils.email import send_email
import database.functions.user as user_db
import database.functions.jobSeeker as job_seeker_db
import database.functions.recruiter as recruiter_db
import database.functions.college as college_db
import database.functions.admin as admin_db

import convertors.model_convertors as convertors
import api.models.models as api_models
import database.models.models as db_models

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

# -----------------------------------------JOB SEEKER-------------------------------------------------

@router.post("/login",response_model=api_models.User_SignIn_Response)
async def user_login(user_credentials: api_models.User_SignIn = Body(...)):
    user_exists = await user_db.get_user_by_email(user_credentials.username)
    if user_exists:
        password = hash_helper.verify(user_credentials.password, user_exists.password)
        if password:
            token = sign_jwt(str(user_exists.id))
            _ = await admin_db.incr_login()
            return api_models.User_SignIn_Response(
                access_token = token,
                roles = user_exists.roles,
                email_verified=user_exists.email_verified,
                mobile_verified=user_exists.mobile_verified,
            )

        raise HTTPException(status_code=403, detail = "Incorrect email or password")
    
    raise HTTPException(status_code=403, detail = "Incorrect email or password")


@router.post("/signup",response_model=api_models.User_SignIn_Response)
async def user_signup(user: api_models.User_SignUp = Body(...)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=403, detail="Passwords entered do not match")
    user_exists = await user_db.get_user_by_email(user.email)
    if user_exists:
        raise HTTPException(
            status_code=409, detail = "User with email supplied already exists"
        )
    user_exists = await user_db.get_user_by_mobile(user.phone_number)
    if user_exists:
        raise HTTPException(
            status_code=409, detail = "User with mobile supplied already exists"
        )
    
    user.password = hash_helper.encrypt(user.password)
    referral = user.referral
    if referral:
        rec = await recruiter_db.check_referral(referral)
        raise HTTPException(status_code=404,detail=referral+" "+str(rec))
        if not rec: 
            raise HTTPException(status_code=404,detail="referral expired")
    dbUser =  convertors.apiUserToDbUser(user)
    
           
    if dbUser.roles == "job_seeker":
        new_profile = api_models.Job_Seeker_Profile(email = dbUser.email, phone_number = user.phone_number)
        new_user = await user_db.add_user(dbUser)
        db_profile = convertors.apiJobSeekerProfileToDbJobSeekerProfile(new_profile, new_user.id)
        new_profile = await job_seeker_db.add_job_seeker(db_profile)
    elif dbUser.roles == "recruiter":
        new_profile = api_models.Recruiter_Profile(email = dbUser.email, phone_number = user.phone_number)
        new_user = await user_db.add_user(dbUser)
        db_profile = convertors.apiRecruiterProfileToDbRecruiterProfile(new_profile, new_user.id)
        new_profile = await recruiter_db.add_recruiter(db_profile)
    elif dbUser.roles == "college":
        new_profile = api_models.College_Profile(email = dbUser.email, phone_number = user.phone_number)
        new_user = await user_db.add_user(dbUser)
        db_profile = convertors.apiCollegeProfileToDbCollegeProfile(new_profile, new_user.id)
        new_profile = await college_db.add_college(db_profile)
    elif dbUser.roles == "admin":
        new_user = await user_db.add_user(dbUser)
        db_profile = db_models.Admin(adminId=new_user.id)
        new_profile = await admin_db.add_admin(db_profile)
    else:
        raise HTTPException(status_code=403, detail="Invalid user roles")
    # return user created successfully
    user_exists = await user_db.get_user_by_email(user.email)
    token = sign_jwt(str(user_exists.id))
    _ = await admin_db.incr_signup()
    return api_models.User_SignIn_Response(
        access_token = token,
        roles = user_exists.roles,
        email_verified=user_exists.email_verified,
        mobile_verified=user_exists.mobile_verified
    )

@router.post("/sendEmail",response_model=api_models.Success_Message_Response)
def sendEmail(reciever_email: str,message: str):
    res = send_email(to_email=reciever_email,body=message + '\n' + "hui hui hui")
    return api_models.Success_Message_Response(
        message="Mail sent successfully"
    )