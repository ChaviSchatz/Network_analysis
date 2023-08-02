from fastapi import APIRouter
from datetime import timedelta

from fastapi import Depends, HTTPException, status, Response, encoders
from fastapi.security import OAuth2PasswordRequestForm

from Auth_management.auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user
from Auth_management.auth_models import Token, User
from db_managment.models.entities import Technician

auth_router = APIRouter(
    responses={404: {"description": "not authenticate"}},)


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user: Technician = await authenticate_user(form_data.email, form_data.password, int(form_data.client_id))
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="Authorization", value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
