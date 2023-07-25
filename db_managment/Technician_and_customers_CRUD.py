from models.entities import Client, Technician, TargetDevice, Network, Device
import asyncio

import pymysql

from db_managment.db_connection import connection


async def create_client(client: Client):
    try:
        with connection.cursor() as cursor:
            query = """INSERT INTO client (
               fullName)
               VALUES (%s)"""
            data = client.full_name
            cursor.execute(query, data)
            connection.commit()
    except:
        connection.rollback()
    connection.close()


async def create_technician(technician: Technician):
    try:
        with connection.cursor() as cursor:
            query = """INSERT into technician (fullName,hashed_password)
                    values (%s, %s)"""
            val = (technician.full_name, technician.hashed_password)
            cursor.execute(query, val)
            connection.commit()
    except Exception:
        raise Exception("can't insert technician to db")


async def update_client(client: Client):
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE client SET fullName=%s WHERE id=%s"
            val = (client.full_name, client.id)
            cursor.execute(sql, val)
            connection.commit()
    except Exception:
        raise Exception("can't update client to db")


def unique_set_from_list(obj_list):
    unique_dict = {}
    for obj in obj_list:
        key = obj.model_dump_json()  # Convert the Pydantic object to its JSON representation
        unique_dict[key] = obj

    return list(unique_dict.values())


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
            JOIN device AS dst_device ON dst_device.id = connection.dst
            WHERE network.id = %s"""
            val = network_id
            cursor.execute(query, val)
            all_data = cursor.fetchall()
            print(all_data)
            if len(all_data) > 0:
                network_data = all_data[0]
                target_network = Network(id=network_data["network_id"],
                                         client_id=network_data["client_id"],
                                         net_location=network_data["net_location"],
                                         production_date=network_data["production_date"])
                devices = []
                target_devices = {}
                for d in all_data:
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
                devices = unique_set_from_list(devices)
                for d in devices:
                    d.target_devices = target_devices[d.mac_address]
                target_network.devices = devices
                print(target_network)
    except Exception:
        raise Exception("can't insert technician to db")


# data_obj = Technician(fullName="Yoram Levi",
# hashed_password="$2b$12$hNogVM3P4RvKhqzSzC9/uO0f6Uv/USMNqbNgA82TwT80Cu9t7sX3W") asyncio.run(create_technician(
# data_obj))

# data_obj = Client(id=1, full_name="Yoram Levi")
# asyncio.run(create_client(data_obj))
# data_obj = Client(id=1, full_name="Yoram Shalom Levi")
asyncio.run(get_network(1))
# update_costumer(data_obj)
