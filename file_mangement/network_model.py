import mapping_file
import asyncio
from db_managment.network_and_devices_CRUD import insert_network, create_network, insert_connections
from db_managment.models.entities import Network, Device, Connection


async def map_file(client_id, net_location, production_date, path):
    network = Network(client_id=client_id, net_location=net_location, production_date=production_date)
    network_id = await create_network(network)
    devices_mapping_list: list[Device] = mapping_file.map_devices(path, network_id)
    # await insert_network(devices_mapping_list)
    connections_mapping_list: list[Connection] = mapping_file.map_connections(path)
    # await insert_connections(connections_mapping_list)
    await asyncio.gather(insert_network(devices_mapping_list), insert_connections(connections_mapping_list))
