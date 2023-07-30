from db_managment.models.entities import Network
from db_managment.network_and_devices_CRUD import get_network


async def get_network_by_id(id: int):
    network: Network = await get_network(id)
    return network


