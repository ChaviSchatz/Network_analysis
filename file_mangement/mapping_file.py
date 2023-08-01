import re
from typing import List
from db_managment.models.entities import Device, Connection

import requests


async def get_vendor(mac_address: str) -> str:
    # We will use an API to get the vendor details
    url = "https://api.macvendors.com/"
    # Use get method to fetch details
    response = requests.get(url + mac_address, verify=False)
    if response.status_code != 200:
        return "Unknown"
        # raise Exception("[!] Invalid MAC Address!")
    return response.content.decode()


async def map_devices(scapy_cap, network_id: int) -> List[Device]:
    # return list of unique devices that connected to the current network
    # gets path to the pcap file
    # gets the network id that this file got and add it to each device
    try:
        packets = list(scapy_cap)
        # devices = List[Device]
        devices = list()
        pattern = "((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
        for packet in packets:
            e = packet["Ether"]
            mac_address = e.src
            if not (mac_address in [a.mac_address for a in devices]):
                result = re.search(pattern, str(e))
                vendor = await get_vendor(mac_address)
                src_ip = result.group()
                device = Device(mac_address=mac_address, ip_address=src_ip, vendor=str(vendor), network_id=network_id)
                devices.append(device)
        return devices
    except Exception:
        raise Exception("Failed to read the file")


def get_IP_address(packet):
    # declaring the regex pattern for IP addresses
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    ip = pattern.search(packet)
    print(ip)
    return ip


async def map_connections(scapy_cap) -> List[Connection]:
    try:
        packets = list(scapy_cap)
        connections = list()
        for packet in packets:
            e = packet["Ether"]
            connect = Connection(src=e.src, dst=e.dst, protocol=get_protocol(e))
            if connect not in connections:
                connections.append(connect)
        print(connections)
        return list(connections)
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
