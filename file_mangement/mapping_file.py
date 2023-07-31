from typing import List
from scapy.all import rdpcap
from db_managment.models.entities import Device, Connection
import requests

async def map_devices(path, network_id) -> List[Device]:
    # return list of unique devices that connected to the current network
    # gets path to the pcap file
    # gets the network id that this file got and add it to each device
    try:
        scapy_cap = rdpcap(path)
        packets = list(scapy_cap)
        # devices = List[Device]
        devices = list()
        for packet in packets:
            e = packet["Ether"]
            mac_address = e.src
            if not (mac_address in [a.mac_address for a in devices]):
                vendor = await get_vendor(mac_address)
                device = Device(mac_address=mac_address, ip_address=e.dst, vendor=str(vendor), network_id=network_id)
                devices.append(device)
        return devices
    except Exception:
        raise Exception("Failed to read the file")

from db_managment.models.entities import Device, Connection


async def get_vendor(mac_address):
    # We will use an API to get the vendor details
    url = "https://api.macvendors.com/"
    # Use get method to fetch details
    response = requests.get(url + mac_address, verify=False)
    if response.status_code != 200:
        return "None"
        # raise Exception("[!] Invalid MAC Address!")
    # print(response.content.decode())
    return response.content.decode()


async def map_connections(path) -> List[Connection]:
    try:
        scapy_cap = rdpcap(path)
        packets = list(scapy_cap)
        connections = list()
        for packet in packets:
            e = packet["Ether"]
            connect = Connection(src=e.src,dst=e.dst,protocol=get_protocol(e))
            connections.append(connect)
        return connections
    except Exception:
        raise Exception("Failed to read the file")


def get_protocol(packet):
    if 'TCP' in packet:
        protocol = packet['TCP'].name
    elif 'UDP' in packet:
        protocol = packet['UDP'].name
    elif 'ARP' in packet:
        protocol = packet['ARP'].name
    elif 'ICMP' in packet:
        protocol = packet['ICMP'].name
    else:
        protocol = 'Unknown'
    return protocol
