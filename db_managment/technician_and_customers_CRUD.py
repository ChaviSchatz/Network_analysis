from typing import Tuple, Any

from db_managment.db_connection import connection
from db_managment.models.entities import Client, Technician


async def create_client(client: Client):
    try:
        with connection.cursor() as cursor:
            query = """INSERT INTO client (
               fullName)
               VALUES (%s)"""
            data = client.full_name
            cursor.execute(query, data)
            connection.commit()
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("An error in create_client")


async def create_technician(technician: Technician):
    try:
        with connection.cursor() as cursor:
            query = """INSERT into technician (full_name,hashed_password, email)
                    values (%s, %s, %s)"""
            val = (technician.full_name, technician.hashed_password, technician.email)
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
            query = "UPDATE technician SET full_name=%s, hashed_password=%s ,email=%s WHERE id=%s"
            data = (technician.full_name, technician.hashed_password, technician.email, technician.id)
            cursor.execute(query, data)
            connection.commit()

    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Error in update_technician")


async def technician_verification(email):
    # if find - return the technician
    # else return None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM technician WHERE email = %s"
            val = email
            cursor.execute(sql, val)
            result = cursor.fetchall()
            if len(result) > 0:
                return result[0]
            return None
    except Exception:
        raise Exception("Technician not recognized in the system.")


async def technician_associated_with_client(technician_id: str, client_id: str) -> bool:
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
        connection.rollback()
        connection.close()
        raise Exception("Technician not associated with this client.")


async def authorized_technician(technician_id, client_id) -> bool:
    try:
        with connection.cursor() as cursor:
            sql = """SELECT * FROM technician_client WHERE technician_id = (%s) And client_id = (%s)"""
            data = (technician_id, client_id)
            cursor.execute(sql, data)
            result = cursor.fetchall()
            # if result.get("technician_id") == technician_id:
            #     return True
            # return False
            if result:
                return True
            return False
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Opss, it is an error in authorized_technician")




