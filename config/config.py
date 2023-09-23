from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

import database.models as dbModels
from aiobotocore.session import get_session


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None

    # JWT
    secret_key: str = "secret"
    algorithm: str = "HS256"

    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: Optional[str] = None
    S3_Bucket: Optional[str] = None
    S3_Key: Optional[str] = None

    class Config:
        env_file = ".env.dev"
        from_attributes = True


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(), document_models=dbModels.__all__
    )

class S3_SERVICE(object):

    def __init__(self):
        self.aws_access_key_id = Settings().AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = Settings().AWS_SECRET_ACCESS_KEY
        self.region = Settings().AWS_REGION
        self.bucket = Settings().S3_Bucket
        self.key = Settings().S3_Key

    async def upload_fileobj(self, fileobject, filename):
        session = get_session()
        async with session.create_client('s3', region_name=self.region,
                                         aws_secret_access_key=self.aws_secret_access_key,
                                         aws_access_key_id=self.aws_access_key_id) as client:
            file_upload_response = await client.put_object(Bucket=self.bucket,Key = self.key + filename, Body=fileobject)
            if file_upload_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return True
        return False

    async def delete_fileobj(self, filename):
        session = get_session()
        async with session.create_client('s3', region_name=self.region,
                                         aws_secret_access_key=self.aws_secret_access_key,
                                         aws_access_key_id=self.aws_access_key_id) as client:
            file_delete_response = await client.delete_object(Bucket=self.bucket,Key = filename)
            if file_delete_response["ResponseMetadata"]["HTTPStatusCode"] == 204:
                return True
        return False

    async def send_otp_email(self,otp,email):
        session = get_session()
        async with session.create_client('ses', region_name=self.region,
                                         aws_secret_access_key=self.aws_secret_access_key,
                                         aws_access_key_id=self.aws_access_key_id) as client:
            response = await client.send_email(
                Destination={
                    'ToAddresses': [
                        email,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': 'UTF-8',
                            'Data': f'Your OTP for verification on EmployeeX website is {otp}. Do not share this otp and it is valid for 3 minutes only.',
                        },
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': 'EmployeeX: OTP for Verification',
                    },
                },
                Source='EmployeeX <noreply@employeex.co.in>',
            )
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return True
        return False

s3_client = S3_SERVICE()
