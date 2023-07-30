import asyncio
from typing import List

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


async def technician_verification(name: str) -> Technician:
    # if find - return the technician's id
    # else return 0
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM technician WHERE full_Name = %s AND hashed_password = %s"
            val = (name)
            cursor.execute(sql, val)
            result = cursor.fetchall()
            if len(result) > 0:
                return result[0]['id']
            return 0
    except Exception:
        raise Exception("Technician not recognized in the system.")


async def technician_associated_with_client(technician_id: str, client_id: str):
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
