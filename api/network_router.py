from fastapi import APIRouter, Depends, HTTPException, Form
from pymysql import Date
from scapy.libs.six import BytesIO
from starlette import status
from fastapi import File, UploadFile

from Auth_management.auth import get_current_active_user
from Auth_management.auth_models import User
from controllers.network_controller import get_network_by_id
from db_managment.models.entities import Network
from file_mangement.network_model import map_file

BASEURL = "/networks"
networks = APIRouter(
    responses={404: {"description": "not found"}})


@networks.get(BASEURL + "/{id}", response_model=Network | None)
async def get_network(id: str, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Unauthorized")

    return await get_network_by_id(int(id))


@networks.post(BASEURL)
async def create_network_model_from_file(file: UploadFile = File(...), client_id: int = Form(...),
                                         net_location: str = Form(...),
                                         production_date: Date = Form(...),
                                         current_user: User = Depends(get_current_active_user)):
    # check technician auth
    if not current_user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Unauthorized")
    # valid file type
    if not valid_file_type(file):
        raise HTTPException(status_code=400, detail="Invalid file type")
    file_content = await file.read()
    file_for_map = BytesIO(file_content)
    return await map_file(client_id, net_location, production_date, file_for_map)


def valid_file_type(file):
    content_type = file.content_type
    types = [f".pcap", f".cap", f".pcapng"]
    b = False
    for t in types:
        if t in content_type:
            b = True
    return b
