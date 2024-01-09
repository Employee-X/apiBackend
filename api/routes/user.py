from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext
from typing import Optional
import datetime
from auth.jwt_handler import sign_jwt
from utils.email import send_email
import database.functions.user as user_db
import database.functions.jobSeeker as job_seeker_db
import database.functions.recruiter as recruiter_db
import database.functions.college as college_db
import database.functions.admin as admin_db
from auth.otp import otp_generator,send_otp_phone
import convertors.model_convertors as convertors
import api.models.models as api_models
import database.models.models as db_models
from business.policy import VERIFIED_RECRUITER_COINS

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


async def validate_user_before_verify(email_id: Optional[str], mobile: Optional[str]):
    user = await user_db.get_user_by_email(email_id)
    # user = await user_db.get_user_by_id(user_id)
    if user:
        if email_id:
            if user.email != email_id:
                return False, "Email does not match"
        if mobile:
            if user.mobile != mobile:
                return False, "Mobile does not match"
        return True, ""
    return False, "Unauthorized Access"

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
    if user.roles == "recruiter":
        referral = user.referral
        if referral:
            rec = await recruiter_db.check_referral(referral,user.email)
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
        _ = await recruiter_db.add_mssg(db_profile.userId,VERIFIED_RECRUITER_COINS,"signup_bonus")
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
    # return api_models.Success_Message_Response(
    #     message="Account created successfully"
    # )
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
    res = send_email(to_email=reciever_email,body=message)
    return api_models.Success_Message_Response(
        message="Mail sent successfully"
    )

@router.post("/generateOtp", response_model=api_models.Success_Message_Response)
async def generate_otp(email_input: api_models.SendOtp = Body(...)):
    validated, msg = await validate_user_before_verify(email_id=email_input.email,mobile=email_input.phone_number)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    user = await user_db.get_user_by_email(email=email_input.email)
    current_time = datetime.datetime.now()
    expiration_tim_str = user.otp_expiration
    if expiration_tim_str:
        expiration_time = datetime.datetime.fromisoformat(expiration_tim_str)
        # if otp already exists and is not expired
        if user.otp and user.otp_expiration and current_time < expiration_time:
            time_remaining = expiration_time - current_time
            time_instring = int(time_remaining.total_seconds())
            raise HTTPException(status_code=403, detail=f"OTP already sent and is not expired. Try again in {time_instring} seconds")
    otp = otp_generator()
    _ = send_otp_phone(otp,email_input.phone_number)
    res = await user_db.update_otp(user.id,otp)
    return api_models.Success_Message_Response(
        message = "OTP sent successfully"
    )

@router.post("/verifyOtp", response_model=api_models.User_SignIn_Response)
async def verify_otp(otp_input: api_models.RecvOtp = Body(...)):
    validated, msg = await validate_user_before_verify(email_id=otp_input.email,mobile=otp_input.phone_number)
    if not validated:
        raise HTTPException(status_code=403, detail=msg)
    user = await user_db.get_user_by_email(email=otp_input.email)
    current_time = datetime.datetime.now()
    expiration_tim_str = user.otp_expiration
    if expiration_tim_str:
        expiration_time = datetime.datetime.fromisoformat(expiration_tim_str)
        if user.otp and user.otp_expiration and current_time < expiration_time and user.otp == otp_input.otp:
            user = await user_db.update_email_verified(user.id)    
            # user_exists = await user_db.get_user_by_email(otp_input.email)
            # if user_exists:
            token = sign_jwt(str(user.id))
            _ = await admin_db.incr_login()
            return api_models.User_SignIn_Response(
                access_token = token,
                roles = user.roles,
                email_verified=user.email_verified,
                mobile_verified=user.mobile_verified,
                )
    raise HTTPException(status_code=403, detail="OTP is invalid or expired")
