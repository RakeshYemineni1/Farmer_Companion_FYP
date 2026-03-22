from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.core.security import decode_token
from jose import JWTError

bearer = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    try:
        payload = decode_token(credentials.credentials)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
