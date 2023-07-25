import asyncio
from typing import List

import pymysql
from db_managment.db_connection import connection
from db_managment.models.entities import Connection
from models.entities import Device

def create_technician(technician):
    try:
        with connection.cursor() as cursor:
            query = """INSERT into technician (fullName,hashed_password)
                    values (%s, %s)"""
            val = (technician["fullName"], technician["hashed_password"])
            cursor.execute(query, val)
            connection.commit()
    except Exception:
        raise Exception("can't insert technician to db")


def update_costumer(client):
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE client SET fullName=%s WHERE id=%s VALUES(%s,%s)"
            val = (client["fullName"], client["id"])
            cursor.execute(sql, val)
            connection.commit()
    except Exception:
        raise Exception("can't update client to db")


# update_costumer({"fullName": "Yosef Cohen", "id": 1})


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



