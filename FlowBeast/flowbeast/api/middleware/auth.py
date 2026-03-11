from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Dict
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def create_access_token(data: Dict, expires_delta: timedelta = timedelta(days=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        tier: str = payload.get("tier", "developer")
        if sub is None:
            raise HTTPException(status_code=401, detail="无效凭证")
        return {"sub": sub, "tier": tier}
    except JWTError:
        raise HTTPException(status_code=401, detail="凭证过期")
