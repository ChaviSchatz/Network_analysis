from db_management.db_connection import connection
from pymysql import MySQLError
from logger import logger_decorator


@logger_decorator
async def insert_update_to_db(query, data, msg):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, data)
            connection.commit()
            return cursor.lastrowid

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in create function")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception(f"Error in {msg}")


@logger_decorator
async def get_from_db(query, data, msg):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, data)
            connection.commit()
            return cursor.fetchall()

    except MySQLError as ex:
        connection.rollback()
        connection.close()
        raise MySQLError(f"An error {ex} occurred in create function")
    except Exception:
        connection.rollback()
        connection.close()
        raise Exception(f"Error in {msg}")


