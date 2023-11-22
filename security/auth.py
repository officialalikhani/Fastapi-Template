from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from database.main import MongoDb
from models.base_model import *
mg = MongoDb()
SECRET_KEY = "# openssl rand -hex 32"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 525600


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    res = mg.select_user_by(username)
    res = res[f"{username}"]
    return UserInDB(**res)


def add_user(user, hashpass, role):
    mg.user_mongo(user, hashpass, role)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def hash_pass(passwd):
    hashpasswd = get_password_hash(passwd)
    return hashpasswd


def auth_params(token):
    res = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return res


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def has_permission(user=Depends(get_current_user)):
    if user.role != 0:
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "message": "You don't have permission to access this resource",
                "data": "",
            },
        )
    return True
