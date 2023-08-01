from db_managment.network_and_devices_CRUD import get_network_by_client_id, \
    get_devices_by_one_or_more_filter, get_connections_by_protocol_filter, get_network


# async def get_networks_by_client_id(client_id):
#     return await get_network_by_client_id(client_id)


async def get_devices_by_network_id_and_more_filters(network_id, filters):
    return await get_devices_by_one_or_more_filter(network_id, filters)


async def get_connections_by_protocol(protocol_filter):
    return await get_connections_by_protocol_filter(protocol_filter)


async def get_network_by_network_id(network_id):
    return await get_network(network_id)

