import asyncio
from typing import List

from pymysql import MySQLError
from logger import logger_decorator
from db_management.db_connection import connection
from db_management.models.entities import Network, Device, Connection, TargetDevice



@logger_decorator
async def create_network(network: Network) -> int:
    try:
        with connection.cursor() as cursor:
            query = """INSERT INTO network (client_id, net_location, production_date)
                            VALUES (%s, %s, %s)"""
            data = (network.client_id, network.net_location, network.production_date)
            cursor.execute(query, data)
            connection.commit()
            network_id = cursor.lastrowid
            return network_id

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in create_network")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Error in create_network")


@logger_decorator
async def insert_devices(device_list: List[Device]) -> None:
    try:
        with connection.cursor() as cursor:
            query = """INSERT INTO device (network_id, mac_address, ip_address, vendor)
                                             VALUES (%s, %s, %s, %s)"""
            for d in device_list:
                data = (d.network_id, d.mac_address, d.ip_address, d.vendor)
                cursor.execute(query, data)
            connection.commit()

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in insert_devices")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Error in insert_network")


@logger_decorator
async def insert_connections(list_of_connections: List[Connection], network_id: int) -> None:
    try:
        with connection.cursor() as cursor:
            sql_get_device_id = """SELECT id FROM device WHERE mac_address = %s AND network_id = %s"""
            sql = """INSERT INTO connection (src, dst, protocol)
                   VALUES (%s,%s,%s)"""
            i = 0
            for con in list_of_connections:
                if i % 100 == 0:
                    print(i)
                cursor.execute(sql_get_device_id, (con.src, network_id))
                src_id = cursor.fetchall()
                cursor.execute(sql_get_device_id, (con.dst, network_id))
                dst_id = cursor.fetchall()
                if src_id and dst_id:
                    val = (src_id[0].get("id"), dst_id[0].get("id"), con.protocol)
                    cursor.execute(sql, val)
                i += 1
            connection.commit()
    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in insert_connections")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Error in insert_connections.")


def unique_set_from_list(obj_list: list) -> list:
    unique_dict = {}
    for obj in obj_list:
        key = obj.model_dump_json()  # Convert the Pydantic object to its JSON representation
        unique_dict[key] = obj

    return list(unique_dict.values())


# The function returns a detailed network model
@logger_decorator
async def get_network(network_id: int) -> Network | None:
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

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in get_network")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("can't get network from db.")


@logger_decorator
async def get_devices_by_one_or_more_filter(network_id: int, the_filter: dict) -> List[Device]:
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
            return result

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in insert_connections")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Opss, it is an error in get_devices_by_one_or_more_filter")


@logger_decorator
async def get_connections_by_protocol_filter(protocol_filter: dict) -> List[Connection]:
    try:
        with connection.cursor() as cursor:
            sql = """SELECT * FROM connection WHERE protocol = (%s)"""
            cursor.execute(sql, protocol_filter)
            result = cursor.fetchall()
            return result

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in insert_connections")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Opss, it is an error in get_connections_by_protocol_filter")


@logger_decorator
async def get_networks_by_client_id(client_id: int) -> List[Network]:
    try:
        with connection.cursor() as cursor:
            sql = """SELECT * FROM network WHERE client_id = (%s)"""
            cursor.execute(sql, client_id)
            result = cursor.fetchall()
            return result

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in insert_connections")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Opss, it is an error in get_network_by_client_id")


def get_network_obj_from_data(data_from_db: list) -> Network | None:
    # The function takes the information from the database and
    # transforms it into a network object after mapping the data
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


# async def main():
#     id = await get_network(1)
#     print("121", )
#
#
# asyncio.run(main())
