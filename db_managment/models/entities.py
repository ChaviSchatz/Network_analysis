from pydantic import BaseModel, constr
from pymysql import Date
from typing import Union


class Client(BaseModel):
    id = Union[int, None] = None
    fullName: constr(max_length=40)


class Technician(BaseModel):
    id = Union[int, None] = None
    fullName: constr(max_length=40)
    hashed_password: constr(max_length=100)


class Network(BaseModel):
    id = Union[int, None] = None
    client_id: int
    net_location: constr(max_length=100)
    production_date: Date


class Device(BaseModel):
    id = Union[int, None] = None
    network_id: int
    mac_address: constr(min_length=15, max_length=17)
    ip_address: constr(min_length=15, max_length=39)
    vendor: constr(max_length=32)


class Connection(BaseModel):
    id = Union[int, None] = None
    src: int
    dst: int
    protocol: constr(max_length=15)
