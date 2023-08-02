from fastapi import Request, APIRouter, Depends, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pymysql import Date
from scapy.libs.six import BytesIO
from starlette import status
import json

from Auth_management.auth import get_current_active_user  # , get_permissions
from Auth_management.auth_models import User
from controllers.network_controller import get_network_by_id
from db_managment.models.entities import Network
from file_mangement.network_model import map_file
from visualization.visual_network import get_network_table, get_connections_graph

from logger import logger_decorator

BASEURL = "/networks"
networks = APIRouter(
    responses={404: {"description": "not found"}})

templates = Jinja2Templates(directory="static")


@logger_decorator
@networks.get(BASEURL + "/{id}", response_model=Network | None)
async def get_network(id: str, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Unauthorized")

    return await get_network_by_id(int(id))


@logger_decorator
@networks.get(BASEURL + "/visual/{id}", response_class=HTMLResponse)
async def get_network(id: str, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Unauthorized")
    json_network = await get_network_by_id(int(id))
    return get_network_table(json.dumps(json_network))


@logger_decorator
@networks.get(BASEURL + "/visualCon/{id}", response_class=HTMLResponse)
async def get_network(id: str, request: Request):  # , current_user: User = Depends(get_current_active_user)):
    # import json
    # if not current_user:
    #     return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                          detail="Unauthorized")
    # json_network = await get_network_by_id(int(id))
    json_network = {
        "id": 37,
        "client_id": 1,
        "net_location": "\"Beit-Shemesh\"",
        "production_date": "2023-07-25",
        "devices": [
            {
                "mac_address": "00:25:00:fe:07:c4",
                "ip_address": "192.168.1.10",
                "vendor": "Apple, Inc.",
                "id": None,
                "network_id": None,
                "target_devices": [
                    {
                        "mac_address": "00:23:69:ad:57:7b",
                        "ip_address": "4.2.2.1",
                        "vendor": "Cisco-Linksys, LLC",
                        "protocol": "UDP"
                    },
                    {
                        "mac_address": "00:23:69:ad:57:7b",
                        "ip_address": "4.2.2.1",
                        "vendor": "Cisco-Linksys, LLC",
                        "protocol": "TCP"
                    }
                ]
            },
            {
                "mac_address": "00:23:69:ad:57:7b",
                "ip_address": "4.2.2.1",
                "vendor": "Cisco-Linksys, LLC",
                "id": None,
                "network_id": None,
                "target_devices": [
                    {
                        "mac_address": "00:25:00:fe:07:c4",
                        "ip_address": "192.168.1.10",
                        "vendor": "Apple, Inc.",
                        "protocol": "UDP"
                    },
                    {
                        "mac_address": "00:25:00:fe:07:c4",
                        "ip_address": "192.168.1.10",
                        "vendor": "Apple, Inc.",
                        "protocol": "TCP"
                    }
                ]
            }
        ]
    }
    get_connections_graph(json.dumps(json_network))
    try:
        return templates.TemplateResponse("device_graph.html", {"request": request})
    except:
        return "<center><h4>error in the graph visualization... :(</h4></center>"


@logger_decorator
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
