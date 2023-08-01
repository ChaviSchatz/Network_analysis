import asyncio
from db_managment.network_and_devices_CRUD import insert_network, create_network, insert_connections
from db_managment.models.entities import Network, Device, Connection
from file_mangement import mapping_file
from scapy.all import rdpcap


async def map_file(client_id, net_location, production_date, path):
    network = Network(client_id=client_id, net_location=net_location, production_date=production_date)
    # insert the new network to the db
    network_id = await create_network(network)
    scapy_cap = rdpcap(path)
    devices_mapping_list = await mapping_file.map_devices(scapy_cap, network_id)
    # insert the network's devices to the db
    await insert_network(devices_mapping_list)
    connections_mapping_list = await mapping_file.map_connections(scapy_cap)
    # insert the connections
    await insert_connections(list(connections_mapping_list))
    # await asyncio.gather(insert_network(devices_mapping_list), insert_connections(connections_mapping_list))

