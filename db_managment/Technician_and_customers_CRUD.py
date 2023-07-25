from db_connection import connection
import asyncio
from models.entities import Client, Technician





async def create_client(client: Client):
    try:
        with connection.cursor() as cursor:
            query = """INSERT INTO client (
               full_name)
               VALUES (%s)"""
            data = (client["full_name"])
            cursor.execute(query, data)
            connection.commit()
    except:
        connection.rollback()
    connection.close()


async def update_technician(technician: Technician):
    try:
        with connection.cursor() as cursor:
            query = "UPDATE technician SET full_name=%s, hashed_password=%s WHERE id=%s"
            data = (technician["full_name"], technician["hashed_password"], technician["id"])
            cursor.execute(query, data)
            connection.commit()
    except:
        connection.rollback()
    connection.close()


async def create_technician(technician):
    try:
        with connection.cursor() as cursor:
            query = """INSERT into technician (full_name,hashed_password)
                    values (%s, %s)"""
            val = (technician["full_name"], technician["hashed_password"])
            cursor.execute(query, val)
            connection.commit()
    except Exception:
        raise Exception("can't insert technician to db")


async def update_costumer(client):
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE client SET full_name=%s WHERE id=%s VALUES(%s,%s)"
            val = (client["full_name"], client["id"])
            cursor.execute(sql, val)
            connection.commit()
    except Exception:
        raise Exception("can't update client to db")


async def main():
    # update_costumer({"full_name": "Yosef Cohen", "id": 1})
    #  await create_client({"full_name": "Yorram"})
    # await create_technician({"full_name":"Danni", "hashed_password": "$2b$12$.MNAWIkzK6QF11dRVmMxXOzcfxUuRH.Udf7DsQ.27nT0X4FO4qeN."})
    await update_technician({"full_name": "Ron", "hashed_password": "$2b$12$.MNAWIkzK6QF11dRVmMxXOzcfxUuRH.Udf7DsQ.27nT0X4FO4qeN.", "id":1})


asyncio.run(main())
