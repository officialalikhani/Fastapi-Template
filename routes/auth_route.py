from fastapi import Depends, APIRouter,Response
from security.auth import *
from database.main import MongoDb
from fastapi.security import OAuth2PasswordRequestForm
import traceback
mg = MongoDb()


router = APIRouter(tags=["AUTH"])

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    username = username.lower()
    user = authenticate_user(username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "message": "Incorrect username or password",
                "data": "",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/panel/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/panel/create/", dependencies=[Depends(has_permission)])
def user_create(
    username: str,
    passwd: str,
    role: int,
    response: Response,
    current_user: User = Depends(get_current_active_user),
):
    try:
        hashpass = hash_pass(passwd)
        add_user(username, hashpass, role)
        return {"success": True, "message": "OK", "data": hashpass}
    except Exception:
        err = traceback.format_exc()
        response.status_code = 404
        return {"success": False, "message": "Error", "data": f"{err}"}
