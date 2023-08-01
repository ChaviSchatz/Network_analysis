import asyncio
from db_managment.network_and_devices_CRUD import insert_network, create_network, insert_connections
from db_managment.models.entities import Network
from file_mangement import mapping_file
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
    # await asyncio.gather(insert_network(devices_mapping_list), insert_connections(connections_mapping_list))
    return network_id


async def main():
    r = await map_file(2, "NYC", "2023-05-12", r"C:\Users\user\Downloads\evidence01.pcap")
    print(r)


asyncio.run(main())
