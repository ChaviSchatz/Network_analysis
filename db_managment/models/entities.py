from typing import Union, List
from pydantic import BaseModel, constr
from pymysql import Date

from Auth_management.auth_models import User


class Client(BaseModel):
    id: Union[int, None] = None
    full_name: constr(max_length=40)


class Technician(User):
    id: Union[int, None] = None
    hashed_password: constr(max_length=100)


class BaseDevice(BaseModel):
    mac_address: constr(min_length=15, max_length=17)
    ip_address: constr(min_length=7, max_length=39)
    vendor: constr(max_length=32)

    def __eq__(self, other):
        return self.mac_address == other.mac_address


class TargetDevice(BaseDevice):
    protocol: constr(max_length=15)


class Device(BaseDevice):
    id: Union[int, None] = None
    network_id: Union[int, None] = None
    target_devices: Union[List[TargetDevice], None] = None


class Network(BaseModel):
    id: Union[int, None] = None
    client_id: int
    net_location: constr(max_length=100)
    production_date: Date


class Connection(BaseModel):
    id: Union[int, None] = None
    src: constr(max_length=40)
    dst: constr(max_length=40)
    protocol: constr(max_length=15)
