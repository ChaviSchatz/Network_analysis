from fastapi import APIRouter, Depends

from Auth_management.auth import get_current_active_user
from Auth_management.auth_models import User
from logger import logger_decorator


technicians = APIRouter(
    tags=["technicians"],
    responses={404: {"description": "not found"}})


@logger_decorator
@technicians.get("/technicians/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
