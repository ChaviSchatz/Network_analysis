import logging
from typing import Tuple, Any

from pymysql import MySQLError

from db_management.db_connection import connection
from db_management.models.entities import Client, Technician


logging.basicConfig(filename="log_file.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


async def create_client(client: Client) -> None:
    try:
        with connection.cursor() as cursor:
            query = """INSERT INTO client (
               fullName)
               VALUES (%s)"""
            data = client.full_name
            cursor.execute(query, data)
            connection.commit()
            logger.info(f"This client {data} has been created")

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in create_client")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("An error in create_client")


async def create_technician(technician: Technician) -> None:
    try:
        with connection.cursor() as cursor:
            query = """INSERT into technician (full_name,hashed_password, email)
                    values (%s, %s, %s)"""
            data = (technician.full_name, technician.hashed_password, technician.email)
            cursor.execute(query, data)
            connection.commit()
            logger.info(f"This technician {data} has been created")

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in create_technician")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("can't insert technician to db")


async def update_client(client: Client) -> None:
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE client SET full_name=%s WHERE id=%s"
            data = (client.full_name, client.id)
            cursor.execute(sql, data)
            connection.commit()
            logger.info(f"This client {data} has been updated")

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in update_client")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("can't update client to db")


async def update_technician(technician: Technician) -> None:
    try:
        with connection.cursor() as cursor:
            query = "UPDATE technician SET full_name=%s, hashed_password=%s ,email=%s WHERE id=%s"
            data = (technician.full_name, technician.hashed_password, technician.email, technician.id)
            cursor.execute(query, data)
            connection.commit()
            logger.info(f"This technician {data} has been updated")

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in update_technician")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("can't update technician to db")


async def technician_verification(email: str) -> Technician | None:
    # if find - return the technician
    # else return None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM technician WHERE email = %s"
            val = email
            cursor.execute(sql, val)
            result = cursor.fetchall()

            if len(result) > 0:
                logger.info(f"This technician {result}!")
                return result[0]
            logger.info("Dont find the technician...")
            return None

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in technician_verification")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Technician not recognized in the system.")


async def technician_associated_with_client(technician_id: int, client_id: int) -> bool:
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM technician_client WHERE client_id = %s AND technician_id = %s"
            val = (client_id, technician_id)
            cursor.execute(sql, val)
            result = cursor.fetchall()
            if len(result) > 0:
                logger.info("A match was found between the requested technician and the requested client")
                return True
            logger.info("A match was not found between the requested technician and the requested client")
            return False
    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in technician_associated_with_client")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Technician not associated with this client.")


async def authorized_technician(technician_id: int, client_id: int) -> bool:
    # if a technician is authorized to treat the client  - return the true
    # else return false
    try:
        with connection.cursor() as cursor:
            sql = """SELECT * FROM technician_client WHERE technician_id = (%s) And client_id = (%s)"""
            data = (technician_id, client_id)
            cursor.execute(sql, data)
            result = cursor.fetchall()
            if result:
                logger.info("A match was found between the requested technician and the requested client")
                return True
            logger.info("A match was not found between the requested technician and the requested client")
            return False

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in authorized_technician")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Opss, it is an error in authorized_technician")


async def authorized_technician_to_network(technician_email: str, network_id: int) -> bool:
    # if a technician is authorized to treat the client  - return the true
    # else return false
    try:
        with connection.cursor() as cursor:
            sql = """ SELECT * FROM network WHERE id = (%s) """
            data = network_id
            cursor.execute(sql, data)
            network_result = cursor.fetchall()

            sql = """ SELECT * FROM technician WHERE email = (%s) """
            data = technician_email
            cursor.execute(sql, data)
            technician_result = cursor.fetchall()
            if network_result and technician_result:
                sql = """ SELECT * FROM technician_client WHERE client_id = (%s) And technician_id = (%s) """
                data = (network_result[0].get("id"), technician_result[0].get("id"))
                cursor.execute(sql, data)
                result = cursor.fetchall()
                if result:
                    logger.info("A match was found between the requested network and the requested client")
                    return True
            logger.info("A match was found between the requested network and the requested client")
            return False

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in authorized_technician_to_network")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception("Opss, it is an error in authorized_technician_to_network")


