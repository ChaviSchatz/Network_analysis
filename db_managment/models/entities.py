from typing import Union, List

from pydantic import BaseModel, constr
from pymysql import Date


class Client(BaseModel):
    id: Union[int, None] = None
    full_name: constr(max_length=40)


class Technician(BaseModel):
    id: Union[int, None] = None
    full_name: constr(max_length=40)
    hashed_password: constr(max_length=100)


class BaseDevice(BaseModel):
    mac_address: constr(min_length=15, max_length=17)
    ip_address: constr(min_length=7, max_length=39)
    vendor: constr(max_length=32)


class TargetDevice(BaseDevice):
    protocol: constr(max_length=15)


class Device(BaseDevice):
    id: int
    network_id: int
    target_devices: Union[List[TargetDevice], None] = None


class Network(BaseModel):
    id: Union[int, None] = None
    client_id: int
    net_location: constr(max_length=100)
    production_date: Date
    devices: Union[List[Device], None] = None


class Connection(BaseModel):
    id: Union[int, None] = None
    src: int
    dst: int
    protocol: constr(max_length=15)
