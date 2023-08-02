import asyncio

from db_managment.models.entities import Technician
from db_managment.technician_and_customers_CRUD import create_technician

t = Technician(full_name="Avi", email="avi@gmail.com", hashed_password=f"$2b$12$a9AbkhP1kKgUbLQmR6ElLeprkvChoklTjfBoK7AT14W4Bvo2Usr0i")
asyncio.run(create_technician(t))


