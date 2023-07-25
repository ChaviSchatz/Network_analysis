from db_connection import connection
from models.entities import Client, Technician
import asyncio

import pymysql

from db_managment.db_connection import connection


async def create_client(client: Client):
    try:
        with connection.cursor() as cursor:
            query = """INSERT INTO client (
               fullName)
               VALUES (%s)"""
            data = (client["fullName"])
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
            val = (technician.fullName, technician.hashed_password)
            cursor.execute(query, val)
            connection.commit()
    except Exception:
        raise Exception("can't insert technician to db")


async def update_client(client: Client):
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE client SET fullName=%s WHERE id=%s VALUES(%s,%s)"
            val = (client.fullName, client.id)
            cursor.execute(sql, val)
            connection.commit()
    except Exception:
        raise Exception("can't update client to db")


# data_obj = Technician(fullName="Yoram Levi",
# hashed_password="$2b$12$hNogVM3P4RvKhqzSzC9/uO0f6Uv/USMNqbNgA82TwT80Cu9t7sX3W") asyncio.run(create_technician(
# data_obj))

data_obj = Client(id=1, fullName="Yoram Levi")
asyncio.run(update_client(data_obj))
# update_costumer(data_obj)
