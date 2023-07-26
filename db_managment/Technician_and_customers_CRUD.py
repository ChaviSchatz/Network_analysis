import asyncio
from typing import List

import pymysql

from db_managment.db_connection import connection
from db_managment.models.entities import Client, Technician

from db_connection import connection
from models.entities import Connection, Client, Technician, TargetDevice, Network
from models.entities import Device

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
            sql = "UPDATE client SET full_name=%s WHERE id=%s"
            val = (client.full_name, client.id)
            cursor.execute(sql, val)
            connection.commit()
    except Exception:
        raise Exception("can't update client to db")


async def update_technician(technician: Technician):
    try:
        with connection.cursor() as cursor:
            query = "UPDATE technician SET full_name=%s, hashed_password=%s WHERE id=%s"
            data = (technician.full_name, technician.hashed_password, technician.id)
            cursor.execute(query, data)
            connection.commit()

    except:
        connection.rollback()
    connection.close()


def unique_set_from_list(obj_list):
    unique_dict = {}
    for obj in obj_list:
        key = obj.model_dump_json()  # Convert the Pydantic object to its JSON representation
        unique_dict[key] = obj

    return list(unique_dict.values())


async def technician_verification(name, password):
    # if find - return the technician's id
    # else return 0
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM technician WHERE full_Name = %s AND hashed_password = %s"
            val = (name, password)
            cursor.execute(sql, val)
            result = cursor.fetchall()
            if len(result) > 0:
                return result[0]['id']
            return 0
    except Exception:
        raise Exception("Technician not recognized in the system.")


async def technician_associated_with_Client(technician_id, client_id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM technician_client WHERE client_id = %s AND technician_id = %s"
            val = (client_id, technician_id)
            cursor.execute(sql, val)
            result = cursor.fetchall()
            if len(result) > 0:
                return True
            return False
    except Exception:
        raise Exception("Technician not associated with this client.")


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
            JOIN device AS dst_device ON dst_device.id = connection.dst
            WHERE network.id = %s"""
            val = network_id
            cursor.execute(query, val)
            all_data = cursor.fetchall()
            return get_network_obj_from_data(all_data)
    except Exception:
        raise Exception("can't insert technician to db")


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
