import requests
import json
from config.config import Settings
import math, random
from fastapi import HTTPException


OTP_API_KEY = Settings().OTP_API_KEY

def send_otp_phone(otp,phone_number) -> bool:
    formatted_number = phone_convert_string(phone_number)
    base_url = 'https://2factor.in/API/V1/{}/SMS/{}/{}/OTPEMX'.format(OTP_API_KEY,formatted_number,otp)
    # raise HTTPException(status_code=404,detail=str(base_url))
    response = requests.post(base_url)
    response = json.loads(response.text)
    if response:
        return True
    return False

def otp_generator():
    otp = random.randint(100000, 999999)
    return otp

def phone_convert_string(phone_number):
    digits_only = ''.join(filter(str.isdigit, phone_number))
    formatted_number = f"+{digits_only[:2]}{digits_only[2:7]}{digits_only[7:]}"
    return formatted_number