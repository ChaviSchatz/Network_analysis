from file_mangement.mapping_file import map_connections, map_devices


def test_map_connections():
    assert map_connections(r"C:\Users\This User\Downloads\evidence01.pcap")


def test_map_devices():
    # # assert map_devices(r"C:\Users\This User\Downloads\evidence01.pcap", 1)
    # # with open("myfile.txt", "w") as f:
    # #     f.write("line1\nline2\nline3")
    # # assert map_devices(f, 1) == ["line1\n", "line2\n", "line3"]
    #
    #
    # cap = sniff(timeout=5)
    #
    # # save to pcap file
    # wrpcap('test-std.pcap', cap)
    #
    # # save to buffer
    #
    # with open('test-mem.pcap', 'wb') as fp:
    #     fp.write(buf.read())
    assert map_devices(r"C:\Users\This User\Downloads\evidence01.pcap", 1)
