import json


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

