from netmiko import ConnectHandler
import time
import re
import requests

ARRAY_LENGTH = 20
# this variable to fine tuning
# for example if value is 2, then last two packet loss then will trigger decision to turn off/on FEC
FINE_TUNE_LAST_COUNT = 2
MAXIMUM_PACKET_LOSS_TO_TRIGGER = 1


def get_fec_status():
    headers = {
        'accept': 'application/json',
    }

    response = requests.get('http://127.0.0.1:8000/info-tunnel', headers=headers)
    response = response.json()
    return response["fec_status"]

def push_conf(command, device_ip, device_username, device_password, device_port):
    device = {
        'device_type': "fortinet",
        'host':   device_ip,
        'username': device_username,
        'password': device_password,
        'port' : device_port,
        'conn_timeout': 100
    }
    net_connect = ConnectHandler(**device)
    try:
        ping_output = net_connect.send_config_set(command,read_timeout=100)
        net_connect.disconnect()
        #Debug
        # print(ping_output)
        
        # Regular expressions to extract the needed data
        packets_regex = r'(\d+) packets transmitted, (\d+) packets received(?:, \d+ duplicates)?, (\d+)% packet loss'
        rtt_regex = r'round-trip min/avg/max = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+) ms'

        # Extracting data using regular expressions
        packets_info = re.search(packets_regex, ping_output)
        rtt_info = re.search(rtt_regex, ping_output)

        # If the information is found, process it into a JSON structure
        if packets_info and rtt_info:
            packets_transmitted, packets_received, packet_loss = packets_info.groups()
            rtt_min, rtt_avg, rtt_max = rtt_info.groups()

            ping_statistics = {
                "packets_transmitted": int(packets_transmitted),
                "packets_received": int(packets_received),
                "packet_loss_percentage": int(packet_loss),
                "round_trip_time": {
                    "min": float(rtt_min),
                    "avg": float(rtt_avg),
                    "max": float(rtt_max)
                }
            }
        else:
            ping_statistics = {"error": "Data extraction failed"}
        return ping_statistics
    except Exception as e:
        return f'{device["host"]} push config fail'

command_sets = []
command = ["execute ping-options adaptive-ping enable","execute ping-options repeat-count 100","execute ping 202.100.200.10"]
creds = ["192.168.93.101","admin","admin","22"]
command_sets.append(command)
command_sets = command_sets + creds

history = []
isFecEnabled = get_fec_status()
isFecLvl2Enabled = False
isFecLvl3Enabled = False
print("current FEC status is Enabled?: ", isFecEnabled)
while True:
    isFecEnabled = get_fec_status()
    def append_with_limit(lst, item, max_length=ARRAY_LENGTH):
        lst.append(item)
        # Remove items from the beginning if the list is longer than max_length
        while len(lst) > max_length:
            lst.pop(0)

    out = push_conf(*command_sets)
    #Debug
    # print(out)
    
    packet_loss = out["packet_loss_percentage"]
    append_with_limit(history, packet_loss)

    def check_last_items_are_zero(lst, n):
        if not lst or n > len(lst) or n <= 0:
            return False
        # Check if the last n items are all zeros
        return all(x == 0 for x in lst[-n:])
    
    def check_more_than_x(lst, last_n, threshold):
        # Check if the list has at least 10 elements
        if len(lst) < 10:
            return False

        # Get the last five elements of the list
        last_five = lst[-last_n:]

        # Check if each element in the last five is greater than two
        return all(x > threshold for x in last_five)
    # threshold_packet_loss = 2
    isLastFiveisZero = check_last_items_are_zero(history, FINE_TUNE_LAST_COUNT)
    isLastFiveGreaterThanThreshold = check_more_than_x(history,FINE_TUNE_LAST_COUNT,MAXIMUM_PACKET_LOSS_TO_TRIGGER)
    print(f'FEC Status:{isFecEnabled} | last packet loss value: {history}')

    # Get the latest 5 data
    latest_five_history = history[-5:]
    # Find the highest number among the latest 5
    highest_packet_loss = max(latest_five_history)
    if isLastFiveGreaterThanThreshold and (isFecEnabled == False):
        import requests

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        json_data = {
            'current_packet_loss': highest_packet_loss,
        }

        response = requests.post('http://127.0.0.1:8000/enable-fec', headers=headers, json=json_data)
        isFecEnabled = True
        print("FEC Enabled with params packet loss: ", highest_packet_loss)
        print(response)
    
    if isLastFiveisZero and (isFecEnabled == True):
        import requests

        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
        }

        response = requests.post('http://127.0.0.1:8000/disable-fec', headers=headers)
        isFecEnabled = False
        isFecLvl2Enabled = False
        isFecLvl3Enabled = False
        print("FEC Disabled")
        print(response)
