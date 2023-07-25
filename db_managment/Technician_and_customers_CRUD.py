from db_connection import connection


async def insert_client(client):
    try:
        client_insert = """INSERT INTO tbl_client (
           fullName)
           VALUES (%s)"""

        data = [
        ]

        connection.execute(client_insert, data)
        connection.commit()
        print('Record inserted successfully...')
    except:
        connection.rollback()
    connection.close()



