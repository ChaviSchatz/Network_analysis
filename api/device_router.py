from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from Auth_management.auth import get_current_active_user
from Auth_management.auth_models import User
from controllers.device_controller import get_devices_by_network_id
from db_managment.models.entities import Network, Device

BASEURL = "/devices"
devices = APIRouter(
    responses={404: {"description": "not found"}})


@devices.get(BASEURL + "/{network_id}", response_model=List[Device] | None)
async def get_devices(network_id: str, mac: str | None = None, vendor: str | None = None,
                      current_user: User = Depends(get_current_active_user)):
    filters = {}
    if mac:
        filters["mac"] = mac
    if vendor:
        filters["vendor"] = vendor
    if not current_user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Unauthorized")
    res = await get_devices_by_network_id(int(network_id), filters)
    return res
