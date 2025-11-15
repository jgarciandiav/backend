from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import bcrypt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # truncar a 72 bytes
    pwd = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(plain, hashed_password.encode("utf-8"))
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)