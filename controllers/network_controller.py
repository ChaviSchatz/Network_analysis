from scapy.libs.six import BytesIO

from db_management.models.entities import Network
from file_management.network_model import map_file
from network_analysis.network_analysis import get_network_by_network_id


async def get_network_by_id(id: int):
    network: Network = await get_network_by_network_id(id)
    return network


async def map_cap_file(client_id: str, net_location: str, production_date:str, file: BytesIO):
    return map_file(client_id, net_location, production_date, file)
