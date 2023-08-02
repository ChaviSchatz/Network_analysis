import pm as pm
from fastapi import Request, APIRouter, Depends, File, UploadFile, HTTPException, Form
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi import Request, APIRouter, Depends, File, UploadFile, HTTPException, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pymysql import Date
from scapy.libs.six import BytesIO
from starlette import status
from fastapi import File, UploadFile
from starlette.responses import HTMLResponse

from Auth_management.auth import get_current_active_user, get_permissions
from Auth_management.auth_models import User
from controllers.network_controller import get_network_by_id
from db_management.models.entities import Network
from file_management.network_model import map_file
from visualization.visual_network import get_network_table, create_connections_graph_html

BASEURL = "/networks"
networks = APIRouter(
    responses={404: {"description": "not found"}})

templates = Jinja2Templates(directory="static")


@networks.get(BASEURL + "/{id}", response_model=Network | None)
async def get_network(id: str, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Unauthorized")

    return await get_network_by_id(int(id))


# @networks.get(BASEURL + "/visual/{id}", response_class=HTMLResponse)
# async def get_network_visual(id: str, current_user: User = Depends(get_current_active_user)):
#     import json
#     if not current_user:
#         return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                              detail="Unauthorized")
#     if not await get_permissions(str(current_user.email), int(network_id)):
#         return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                              detail="Unauthorized")
#     network: Network = await get_network_by_id(int(id))
#     # network.production_date = str(network.production_date)
#     return get_network_table(network.__dict__)

@networks.get(BASEURL + "/visual/{id}", response_class=HTMLResponse)
async def get_network_visual(id: str):
    network: Network = await get_network_by_id(int(id))
    return get_network_table(network.__dict__)


@networks.get(BASEURL + "/visualCon/{id}", response_class=HTMLResponse)
async def get_network(id: str, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Unauthorized")
    network = await get_network_by_id(int(id))
    a = create_connections_graph_html(network)
    return Response(content=a.getvalue(), media_type="image/png")


    # try:
    #     return templates.TemplateResponse("device_graph.html", {"request": request})
    # except:
    #     return "<center><h4>error in the graph visualization... :(</h4></center>"


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
