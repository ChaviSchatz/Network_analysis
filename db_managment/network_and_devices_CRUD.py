from db_connection import connection
import asyncio
from models.entities import Network, Device, Connection
from typing import List


async def create_network(network: Network):
    try:
        with connection.cursor() as cursor:
            query = """INSERT INTO network (client_id, net_location, production_date)
                            VALUES (%s, %s, %s)"""
            data = (network["client_id"], network["net_location"], network["production_date"])
            cursor.execute(query, data)
            connection.commit()
            network_id = cursor.lastrowid
            return network_id
    except:
        connection.rollback()
    connection.close()


async def insert_network(device_list: List[Device]):
    try:
        with connection.cursor() as cursor:
            query = """INSERT INTO device (network_id, mac_address, ip_address, vendor)
                                             VALUES (%s, %s, %s, %s)"""
            for d in device_list:
                data = (d.network_id, d.mac_address, d.ip_address, d.vendor)
                print("data", data)
                cursor.execute(query, data)
            connection.commit()
    except Exception:
        connection.rollback()
    connection.close()


async def insert_connections(list_of_connections: List[Connection]):
    try:
        with connection.cursor() as cursor:
            sql = """INSERT INTO connection (src, dst, protocol)
                   VALUES (%s, %s, %s)"""
            for con in list_of_connections:
                val = (con.src, con.dst, con.protocol)
                print("data", val)
                cursor.execute(sql, val)
                print(4)
            # val = list_of_connections
            # cursor.execute(sql, val)
            connection.commit()
    except Exception:
        raise Exception("Technician not recognized in the system.")


async def get_device_by_filter(network_id, the_filter):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM device WHERE network_id = %s"
            params = [network_id]
            for key, value in the_filter.items():
                sql += " AND %s = %s"
                params.append(key)
                params.append(value)
            print(params)
            print(sql)
            cursor.execute(sql, params)
            result = cursor.fetchall()
            connection.close()
            return result
    except Exception:
        connection.rollback()

# finally:
# connection.close()


async def main():
    # id = await create_network({"client_id": 1, "net_location": "Haifa", "production_date": "2023-07-25"})
    # print("ID:", id)
    # d = Device(network_id=1, mac_address="00:1A:2B:3C:4D:5E", ip_address="192.168.0.1", vendor="Cisco")
    # list_of_devices = [d]
    # await insert_network(list_of_devices)
    # l = [Connection(src=1, dst=1, protocol="tcp/ip")]
    # a = await insert_connections(l)
    # print(a)
    filter_conditions = {"vendor": "Cisco"}
    devices = await get_device_by_filter(1, filter_conditions)
    print(devices)


asyncio.run(main())
