import json
from typing import io
import networkx as nx
import matplotlib.pyplot as plt
import mpld3

from db_managment.models.entities import Network


def get_network_table(data: dict):
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
                html += "<tr><td>{}</td>\n".format(device.mac_address)
                html += "<td>{}</td>\n".format(device.ip_address)
                html += "<td>{}</td>\n".format(device.vendor)
                # list ao the mac address that contact with this device
                if device.target_devices:
                    html += "<td><ul>"
                    for target_device in device.target_devices:
                        html += "<li>{}</li>\n".format(target_device.mac_address)
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
        G.add_node(device['mac_address'], label=device['ip_address'])
        for target_device in device['target_devices']:
            G.add_node(target_device['mac_address'], label=target_device['mac_address'])

    # Add edges between devices and their target devices
    for device in data['devices']:
        protocols = []
        for target_device in device['target_devices']:
            protocols.append(target_device["protocol"])
            G.add_edge(device['mac_address'], target_device['mac_address'], protocol=str(protocols))

    return G


def draw_device_graph(graph):
    # Draw the graph using NetworkX and Matplotlib
    pos = nx.spring_layout(graph)
    labels = nx.get_node_attributes(graph, 'label')
    protocols = nx.get_edge_attributes(graph, 'protocol')

    nx.draw(graph, pos, with_labels=True, node_size=5000, node_color='skyblue', font_size=10, font_weight='bold')
    nx.draw_networkx_labels(graph, pos, labels, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=protocols, font_size=8, font_color='red')
    # plt.show()


def create_connections_graph_html(network: Network):

    try:
        for d in network.devices:
            d.target_devices = [td.__dict__ for td in d.target_devices]
        network.devices = [d.__dict__ for d in network.devices]
        graph = create_device_graph(network.__dict__)
        draw_device_graph(graph)
        # Export the plot to an HTML file
        # output_html = "./static/device_graph.html"
        # mpld3.save_html(plt.gcf(), output_html)
        # plt.close()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.show()
        # Clear the plot
        plt.clf()
        return buffer
    except Exception as e:
        print(f"error in teh network visualization... \n{e}")


