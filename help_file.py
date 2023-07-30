from db_managment.db_connection import connection
from db_managment.models.entities import Technician
from db_managment.technician_and_customers_CRUD import create_technician
import asyncio

tech = Technician(full_name="Yossef Cohen", email="yossef@gmail.com",
                  hashed_password="$2b$12$7Fzyfk.zPU6QYrAoPCK59.zVbFxCE8dEda39BncDAypdvc4erjaba")


def create_con():
    with connection.cursor() as cursor:
        query = """INSERT INTO technician_client (
                       client_id, technician_id)
                       VALUES (%s, %s)"""
        data = (1, 2)
        cursor.execute(query, data)
        connection.commit()


create_con()
