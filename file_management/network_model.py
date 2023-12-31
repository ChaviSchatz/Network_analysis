import asyncio

from scapy.libs.six import BytesIO

from db_management.network_and_devices_CRUD import create_network, insert_connections, insert_devices
from db_management.models.entities import Network
from file_management import mapping_file
from scapy.all import rdpcap


async def map_file(client_id: int, net_location: str, production_date: str, file: BytesIO) -> int:
    network = Network(client_id=client_id, net_location=net_location, production_date=production_date)
    # insert the new network to the db
    network_id = await create_network(network)
    scapy_cap = rdpcap(file)
    devices_mapping_list = await mapping_file.map_devices(scapy_cap, network_id)
    # insert the network's devices to the db
    await insert_devices(devices_mapping_list)
    connections_mapping_list = await mapping_file.map_connections(scapy_cap)
    # insert the connections
    await insert_connections(list(connections_mapping_list), network_id)
    return network_id

