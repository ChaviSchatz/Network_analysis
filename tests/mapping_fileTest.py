from file_mangement.mapping_file import map_connections, map_devices
from scapy.all import wrpcap, Ether, IP, UDP


def test_map_connections():
    assert map_connections(r"C:\Users\user\Downloads\evidence01.pcap")


def test_map_devices():
    packet = Ether() / IP(dst="1.2.3.4") / UDP(dport=123)
    wrpcap('foo.pcap', [packet])
    assert map_devices("foo.pcap", 1)
