import json
import networkx as nx
import matplotlib.pyplot as plt
import mpld3


def get_network_table(network_json: json):
    try:
        data = json.loads(network_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    if not isinstance(data, dict):
        raise ValueError("JSON data must be a dictionary.")
    try:
        html = ""
        # general details about tne net:
        for key, value in data.items():
            if key == "id":
                html += f"<h3><b>Network {value}</b></h3>"
            if key == "devices":
                break
            html += f"<h4><b>{key}</b> : {value}<h4>\n"
        # table of all the devices
        html += "<table border='1'>\n"
        if "devices" in data and isinstance(data["devices"], list):
            html += "<tr><td colspan='2'><b>Devices</b></td></tr>\n"
            html += "<tr><td colspan='2'><table border='1'>\n"
            html += "<tr><td><b>mac address</b></td><td><b>ip address</b></td><td><b>vendor</b></td><td colspan='2'><b>Target Devices</b></td></tr>\n"
            for device in data["devices"]:
                html += "<tr><td>{}</td>\n".format(device["mac_address"])
                html += "<td>{}</td>\n".format(device["ip_address"])
                html += "<td>{}</td>\n".format(device["vendor"])
                # list ao the mac address that contact with this fevice
                if "target_devices" in device and isinstance(device["target_devices"], list):
                    html += "<td><ul>"
                    for target_device in device["target_devices"]:
                        html += "<li>{}</li>\n".format(target_device["mac_address"])
                html += "</ul> </td></tr>\n"
            html += "</table></td></tr>\n"
        return html
    except Exception as e:
        return f"<h3> faild to load the html table. :( \n{e}</h1>"


def create_device_graph(data):
    # Create an empty graph
    G = nx.Graph()
    # Add nodes for each device and target device
    for device in data['devices']:
        G.add_node(device['mac_address'], label=device['mac_address'])
        for target_device in device['target_devices']:
            G.add_node(target_device['mac_address'], label=target_device['mac_address'])

    # Add edges between devices and their target devices
    for device in data['devices']:
        for target_device in device['target_devices']:
            G.add_edge(device['mac_address'], target_device['mac_address'], protocol=target_device['protocol'])

    return G


def draw_device_graph(graph):
    # Draw the graph using NetworkX and Matplotlib
    pos = nx.spring_layout(graph)
    labels = nx.get_node_attributes(graph, 'label')
    protocols = nx.get_edge_attributes(graph, 'protocol')

    nx.draw(graph, pos, with_labels=True, node_size=5000, node_color='skyblue', font_size=10, font_weight='bold')
    nx.draw_networkx_labels(graph, pos, labels, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=protocols, font_size=8, font_color='red')

    plt.show()


def get_connections_graph(network_json):
    try:
        data = json.loads(network_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    if not isinstance(data, dict):
        raise ValueError("JSON data must be a dictionary.")

    try:
        graph = create_device_graph(data)
        draw_device_graph(graph)
        # Export the plot to an HTML file
        output_html = "./static/device_graph.html"
        mpld3.save_html(plt.gcf(), output_html)
        plt.close()
    except Exception as e:
        print(f"error in teh network visualizaition... \n{e}")



#
# data = {
#     "id": 37,
#     "client_id": 1,
#     "net_location": "\"Beit-Shemesh\"",
#     "production_date": "2023-07-25",
#     "devices": [
#         {
#             "mac_address": "00:25:00:fe:07:c4",
#             "ip_address": "192.168.1.10",
#             "vendor": "Apple, Inc.",
#             "id": None,
#             "network_id": None,
#             "target_devices": [
#                 {
#                     "mac_address": "00:23:69:ad:57:7b",
#                     "ip_address": "4.2.2.1",
#                     "vendor": "Cisco-Linksys, LLC",
#                     "protocol": "UDP"
#                 },
#                 {
#                     "mac_address": "00:23:69:ad:57:7b",
#                     "ip_address": "4.2.2.1",
#                     "vendor": "Cisco-Linksys, LLC",
#                     "protocol": "TCP"
#                 }
#             ]
#         },
#         {
#             "mac_address": "00:23:69:ad:57:7b",
#             "ip_address": "4.2.2.1",
#             "vendor": "Cisco-Linksys, LLC",
#             "id": None,
#             "network_id": None,
#             "target_devices": [
#                 {
#                     "mac_address": "00:25:00:fe:07:c4",
#                     "ip_address": "192.168.1.10",
#                     "vendor": "Apple, Inc.",
#                     "protocol": "UDP"
#                 },
#                 {
#                     "mac_address": "00:25:00:fe:07:c4",
#                     "ip_address": "192.168.1.10",
#                     "vendor": "Apple, Inc.",
#                     "protocol": "TCP"
#                 }
#             ]
#         }
#     ]
# }


