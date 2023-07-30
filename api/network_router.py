from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from Auth_management.auth import get_current_active_user, get_permissions
from Auth_management.auth_models import User
from controllers.network_controller import get_network_by_id
from db_managment.models.entities import Network

networks = APIRouter(
    responses={404: {"description": "not found"}})


@networks.get("/networks/{id}", response_model=Network | None)
async def get_network(id: str, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Unauthorized")

    return await get_network_by_id(int(id))

