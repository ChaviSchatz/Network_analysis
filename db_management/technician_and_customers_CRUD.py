from db_management.models.entities import Client, Technician

from db_access import get_from_db, insert_update_to_db
from network_and_devices_CRUD import get_network


async def create_client(client: Client) -> None:
    query = """INSERT INTO client (
               fullName)
               VALUES (%s)"""
    data = client.full_name
    await insert_update_to_db(query, data, "create_client")


async def create_technician(technician: Technician) -> None:
    query = """INSERT into technician (full_name,hashed_password, email)
                    values (%s, %s, %s)"""
    data = (technician.full_name, technician.hashed_password, technician.email)
    await insert_update_to_db(query, data, "create_technician")


async def update_client(client: Client) -> None:
    query = "UPDATE client SET full_name=%s WHERE id=%s"
    data = (client.full_name, client.id)
    await insert_update_to_db(query, data, "update_client")


async def update_technician(technician: Technician) -> None:
    query = "UPDATE technician SET full_name=%s, hashed_password=%s ,email=%s WHERE id=%s"
    data = (technician.full_name, technician.hashed_password, technician.email, technician.id)
    await insert_update_to_db(query, data, "update_technician")


async def technician_verification(email: str) -> Technician | None:
    # if find - return the technician
    # else return None
    query = "SELECT * FROM technician WHERE email = %s"
    data = email
    result = await get_from_db(query, data, "technician_verification")
    if len(result) > 0:
        return result[0]
    return None


async def technician_associated_with_client(technician_id: int, client_id: int) -> bool:
    query = "SELECT * FROM technician_client WHERE client_id = %s AND technician_id = %s"
    data = (client_id, technician_id)
    result = await get_from_db(query, data, "technician_associated_with_client")
    if len(result) > 0:
        return True
    return False


async def authorized_technician(technician_id: int, client_id: int) -> bool:
    query = "SELECT * FROM technician_client WHERE client_id = %s AND technician_id = %s"
    data = (client_id, technician_id)
    result = await get_from_db(query, data, "authorized_technician")
    if len(result) > 0:
        return True
    return False


async def authorized_technician_to_network(technician_email: str, network_id: int) -> bool:
    # if a technician is authorized to treat the client  - return the true
    # else return false
    network_result = await get_network(network_id)
    query = """ SELECT * FROM technician WHERE email = (%s) """
    data = technician_email
    technician_result = await get_from_db(query, data, "get technician in authorized_technician_to_network")
    if network_result and technician_result:
        query = """ SELECT * FROM technician_client WHERE client_id = (%s) And technician_id = (%s) """
        data = (network_result[0].get("id"), technician_result[0].get("id"))
        result = get_from_db(query, data, "authorized_technician_to_network")
        if result:
            return True
    return False
