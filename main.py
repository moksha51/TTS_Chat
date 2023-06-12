import requests

import client
import gui_client
import gui_server
import server

SEAHAWK_IP_ADDRESS = '192.168.0.175'


def get_public_ip_address():
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    ip_address = data['ip']
    return ip_address


# # Call the function to get your public IP address
# ip_address = get_public_ip_address()
# print("Your public IP address:", ip_address)

# if get_public_ip_address() == SEAHAWK_IP_ADDRESS:
#     start_gui_server
# else:
#     start_gui_client

server.start_server()
client.connect_to_server()

