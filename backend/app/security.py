from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings

password_hash = PasswordHash.recommended()
bearer = HTTPBearer(auto_error=False)

def create_access_token(subject: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode({"sub": subject, "exp": expires}, settings.jwt_secret, algorithm="HS256")

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Autenticação necessária.")
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=["HS256"])
        username = payload.get("sub")
        if not username:
            raise ValueError("missing subject")
        return username
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada.")
