import logging
from typing import List
from db_managment.db_connection import connection
from db_managment.models.entities import Network, Device, Connection, TargetDevice

logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


async def create_network(network: Network) -> int:
    try:
        with connection.cursor() as cursor:
            query = """INSERT INTO network (client_id, net_location, production_date)
                            VALUES (%s, %s, %s)"""
            data = (network.client_id, network.net_location, network.production_date)
            cursor.execute(query, data)
            connection.commit()
            logger.info(f"This network {data} has been created")
            network_id = cursor.lastrowid
            return network_id
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Error in create_network")


async def insert_network(device_list: List[Device]):
    try:
        with connection.cursor() as cursor:
            query = """INSERT INTO device (network_id, mac_address, ip_address, vendor)
                                             VALUES (%s, %s, %s, %s)"""
            for d in device_list:
                data = (d.network_id, d.mac_address, d.ip_address, d.vendor)
                cursor.execute(query, data)
            connection.commit()
            logger.info(f"{len(device_list)} devices entered the network")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Error in insert_network")


async def insert_connections(list_of_connections: List[Connection]):
    try:
        with connection.cursor() as cursor:
            sql_get_device_id = """SELECT id FROM device WHERE mac_address = %s"""
            sql = """INSERT INTO connection (src, dst, protocol)
                   VALUES (%s,%s,%s)"""
            i = 0
            for con in list_of_connections:
                if i % 100 == 0:
                    print(i)
                cursor.execute(sql_get_device_id, con.src)
                src_id = cursor.fetchall()
                cursor.execute(sql_get_device_id, con.dst)
                dst_id = cursor.fetchall()
                if src_id and dst_id:
                    val = (src_id[0].get("id"), dst_id[0].get("id"), con.protocol)
                    cursor.execute(sql, val)
                i += 1
            connection.commit()
            logger.info(f"{len(list_of_connections)} connections entered the network")
            print("Done!")
    except Exception:
        connection.close()
        raise Exception("Technician not recognized in the system.")


def unique_set_from_list(obj_list):
    unique_dict = {}
    for obj in obj_list:
        key = obj.model_dump_json()  # Convert the Pydantic object to its JSON representation
        unique_dict[key] = obj

    return list(unique_dict.values())


# The function returns a detailed network model
async def get_network(network_id):
    try:
        with connection.cursor() as cursor:
            query = """SELECT network.id AS network_id, network.client_id,
            network.net_location, network.production_date,
            src_device.mac_address, src_device.ip_address, src_device.vendor,
            connection.protocol, dst_device.mac_address AS dst_mac_address,
            dst_device.ip_address AS dst_ip_address,
            dst_device.vendor AS dst_vendor
            FROM network
            JOIN device AS src_device ON src_device.network_id = network.id
            JOIN connection ON connection.src = src_device.id
            JOIN device AS dst_device ON dst_device.id = connection.dst WHERE network.id = %s"""

            val = network_id
            cursor.execute(query, val)
            all_data = cursor.fetchall()
            tech = get_network_obj_from_data(all_data)
            return tech
    except Exception:
        raise Exception("can't get network from db")


async def get_devices_by_one_or_more_filter(network_id, the_filter):
    try:
        with connection.cursor() as cursor:
            sql = """SELECT * FROM device WHERE network_id = (%s) """
            params = [network_id]
            # counter = 0
            for key, value in the_filter.items():
                sql += """ AND (%s) = (%s)"""
                params.append(key)
                params.append(value)
            cursor.execute(sql, params)
            result = cursor.fetchall()
            logger.info(f"there are {len(result)} network(s) with the required filters")
            return result
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Opss, it is an error in get_devices_by_one_or_more_filter")


async def get_connections_by_protocol_filter(protocol_filter) -> List[Connection]:
    try:
        with connection.cursor() as cursor:
            sql = """SELECT * FROM connection WHERE protocol = (%s)"""
            cursor.execute(sql, protocol_filter)
            result = cursor.fetchall()
            logger.info(f"There are {len(result)} connections with the required protocol filter")
            return result
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Opss, it is an error in get_connections_by_protocol_filter")


async def get_network_by_client_id(client_id) -> Network:
    try:
        with connection.cursor() as cursor:
            sql = """SELECT * FROM network WHERE client_id = (%s)"""
            cursor.execute(sql, client_id)
            result = cursor.fetchall()
            logger.info(f"There are {len(result)} networks to client ID {client_id}")
            return result
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Opss, it is an error in get_network_by_client_id")


# The function takes the information from the database and
# transforms it into a network object after mapping the data
def get_network_obj_from_data(data_from_db):
    if len(data_from_db) == 0:
        return None
    # create the network obj
    network_data = data_from_db[0]
    target_network = Network(id=network_data["network_id"],
                             client_id=network_data["client_id"],
                             net_location=network_data["net_location"],
                             production_date=network_data["production_date"])
    # find all the devices and into list
    # and all the target_devices into dict with mac_address of the device is the key
    devices = []
    target_devices = {}
    for d in data_from_db:
        current_device = Device(mac_address=d["mac_address"],
                                ip_address=d["ip_address"],
                                vendor=d["vendor"],
                                )
        current_target_device = TargetDevice(mac_address=d["dst_mac_address"],
                                             ip_address=d["dst_ip_address"],
                                             vendor=d["dst_vendor"],
                                             protocol=d["protocol"])
        if target_devices.get(current_device.mac_address):
            target_devices[current_device.mac_address].append(current_target_device)
        else:
            target_devices[current_device.mac_address] = [current_target_device]
        devices.append(current_device)
    # get all the uniq devices
    devices = unique_set_from_list(devices)
    # give to each device list of its target_devices from the dict we create before
    for d in devices:
        d.target_devices = target_devices[d.mac_address]
    # give the network the devices
    target_network.devices = devices
    return target_network
