from pydantic import BaseModel, constr
from pymysql import Date

class Client(BaseModel):
    id: int
    fullName: constr(max_length=40)


class Technician(BaseModel):
    id: int
    fullName: constr(max_length=40)
    hashed_password: constr(max_length=100)


class Network(BaseModel):
    id: int
    client_id: int
    net_location: constr(max_length=100)
    production_date: Date


class Device(BaseModel):
    id: int
    network_id: int
    mac_address: constr(min_length=15, max_length=17)
    ip_address: constr(min_length=15, max_length=39)
    vendor: constr(max_length=32)


class Connection(BaseModel):
    id: int
    src: int
    dst: int
    protocol: constr(max_length=15)

