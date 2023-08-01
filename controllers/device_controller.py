from network_analysis.network_analysis import get_devices_by_network_id_and_more_filters


async def get_devices_by_network_id(network_id, filters):
    return await get_devices_by_network_id_and_more_filters(network_id, filters)
