from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import VALID_TOKENS

auth_scheme = HTTPBearer()

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if credentials.credentials not in VALID_TOKENS:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials.credentials
