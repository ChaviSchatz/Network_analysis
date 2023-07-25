import pymysql

from db_managment.db_connection import connection


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


update_costumer({"fullName": "Yosef Cohen", "id": 1})
