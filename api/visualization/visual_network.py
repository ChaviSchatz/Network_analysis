json = {
    "id": 29,
    "client_id": 1,
    "net_location": "\"Beit-Shemesh\"",
    "production_date": "2023-07-25",
    "devices": [
        {
            "mac_address": "00:25:00:fe:07:c4",
            "ip_address": "00:25:00:fe:07:c4",
            "vendor": "Apple, Inc.",
            "id": None,
            "network_id": None,
            "target_devices": [
                {
                    "mac_address": "00:23:69:ad:57:7b",
                    "ip_address": "00:23:69:ad:57:7b",
                    "vendor": "Cisco-Linksys, LLC",
                    "protocol": "UDP"
                },
                {
                    "mac_address": "00:23:69:ad:57:7b",
                    "ip_address": "00:23:69:ad:57:7b",
                    "vendor": "Cisco-Linksys, LLC",
                    "protocol": "TCP"
                }
            ]
        },
        {
            "mac_address": "00:23:69:ad:57:7b",
            "ip_address": "00:23:69:ad:57:7b",
            "vendor": "Cisco-Linksys, LLC",
            "id": None,
            "network_id": None,
            "target_devices": [
                {
                    "mac_address": "00:25:00:fe:07:c4",
                    "ip_address": "00:25:00:fe:07:c4",
                    "vendor": "Apple, Inc.",
                    "protocol": "UDP"
                },
                {
                    "mac_address": "00:25:00:fe:07:c4",
                    "ip_address": "00:25:00:fe:07:c4",
                    "vendor": "Apple, Inc.",
                    "protocol": "TCP"
                }
            ]
        }
    ]
}

def get_visual_connections(network_json) :
    html_content = """
        <html>
            <head>
                <title>Some HTML in here</title>
            </head>
            <body>
                <h1>Look ma! HTML!</h1>
            </body>
        </html>
        """
    return html_content

