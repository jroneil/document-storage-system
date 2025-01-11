from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Add your authentication logic here (e.g., validate JWT)
    if token != "valid-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token