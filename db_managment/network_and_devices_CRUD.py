from db_managment.db_connection import connection
from db_managment.models.entities import Connection
from typing import List
import asyncio


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


async def main():
    l = [Connection(src=1, dst=2, protocol="tcp/ip"), Connection(src=3, dst=4, protocol="ARP")]
    # d = Device(network_id=1, mac_address="00:1A:2B:3C:4D:5E", ip_address="192.168.0.1", vendor="Cisco")
    # device = [d]
    # await insert_device(device)
    # l=[]
    a = await insert_connections(l)
    print(a)


asyncio.run(main())
