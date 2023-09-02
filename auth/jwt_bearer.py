from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from .jwt_handler import decode_jwt


def verify_jwt(jwtoken: str) -> (bool,str,dict):
    try:
        payload = decode_jwt(jwtoken)
        if payload:
            if payload["expires"] < time.time():
                return False, "Token expired", {}
            else:
                return True, "Token valid", payload
        else:
            return False, "Invalid authentication token", {}
    except:
        return False, "Invalid authentication token", {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication token scheme"
                )
            jwt_verify = verify_jwt(credentials.credentials)
            if not jwt_verify[0]:
                raise HTTPException(
                    status_code=403, detail=jwt_verify[1]
                )
            return credentials.credentials,jwt_verify[2]["user_id"]
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization token")
