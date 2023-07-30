from fastapi import APIRouter, Depends

from Auth_management.auth import get_current_active_user
from Auth_management.auth_models import User
from db_managment.models.entities import Network

networks = APIRouter(
    tags=["technicians"],
    responses={404: {"description": "not found"}})


# @networks.get("/technicians/{id}", response_model=Network)
# async def read_users_me(id: str, current_user: User = Depends(get_current_active_user)):
