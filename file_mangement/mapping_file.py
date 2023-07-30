from typing import List
from scapy.all import rdpcap
from db_managment.models.entities import Device, Connection
from mac_vendor_lookup import MacLookup


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
            if not(mac_address in [a.mac_address for a in devices]):
                vendor = "MacLookup().lookup(mac_address)"
                device = Device(mac_address=mac_address, ip_address=e.dst, vendor=str(vendor), network_id=network_id)
                devices.append(device)
        return devices
    except Exception:
        raise Exception("Failed to read the file")


def map_connections(path, network_id) -> List[Connection]:
    pass


print(map_devices(r"C:\Users\user\Downloads\evidence01.pcap", 1))
