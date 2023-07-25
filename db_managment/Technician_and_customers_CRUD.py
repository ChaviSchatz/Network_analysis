from db_connection import connection
import asyncio


async def create_client(client):
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


async def update_technician(technician):
    try:
        with connection.cursor() as cursor:
            query = "UPDATE technician SET fullName=%s, hashed_password=%s WHERE id=%s"
            data = (technician["fullName"], technician["hashed_password"], technician["id"])
            print("B")
            cursor.execute(query, data)
            print("c")
            connection.commit()
            print("D")
    except:
        connection.rollback()
    connection.close()


async def create_technician(technician):
    try:
        with connection.cursor() as cursor:
            query = """INSERT into technician (fullName,hashed_password)
                    values (%s, %s)"""
            val = (technician["fullName"], technician["hashed_password"])
            cursor.execute(query, val)
            connection.commit()
    except Exception:
        raise Exception("can't insert technician to db")


async def update_costumer(client):
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE client SET fullName=%s WHERE id=%s VALUES(%s,%s)"
            val = (client["fullName"], client["id"])
            cursor.execute(sql, val)
            connection.commit()
    except Exception:
        raise Exception("can't update client to db")


async def main():
    # update_costumer({"fullName": "Yosef Cohen", "id": 1})
    #  await create_client({"fullName": "Yorram"})
    # await create_technician({"fullName":"Danni", "hashed_password": "$2b$12$.MNAWIkzK6QF11dRVmMxXOzcfxUuRH.Udf7DsQ.27nT0X4FO4qeN."})
    await update_technician({"fullName":"Ron", "hashed_password": "$2b$12$.MNAWIkzK6QF11dRVmMxXOzcfxUuRH.Udf7DsQ.27nT0X4FO4qeN.", "id":1})


asyncio.run(main())
