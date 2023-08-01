from typing import Tuple, Any
from db_connection import connection
from models.entities import Client, Technician


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
            query = """INSERT into technician (full_name,hashed_password, user_name)
                    values (%s, %s, %s)"""
            val = (technician.full_name, technician.hashed_password, technician.user_name)
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
            query = "UPDATE technician SET full_name=%s, hashed_password=%s ,user_name=%s WHERE id=%s"
            data = (technician.full_name, technician.hashed_password, technician.user_name, technician.id)
            cursor.execute(query, data)
            connection.commit()

    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Error in update_technician")


async def technician_verification(user_name) -> Technician | None:
    # if find - return the technician
    # else return None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM technician WHERE user_name = %s"
            val = user_name
            cursor.execute(sql, val)
            result = cursor.fetchall()
            if len(result) > 0:
                return result
            return None
    except Exception:
        raise Exception("Technician not recognized in the system.")


async def technician_associated_with_client(technician_id, client_id):
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


# async def authorized_technician_for_network()

