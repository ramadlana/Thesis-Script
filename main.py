
from fastapi import FastAPI
from netmiko import ConnectHandler
import time
import re
from pydantic import BaseModel
app = FastAPI()

devices_list = [
        ["192.168.93.101","admin","admin","22"],
        ["192.168.93.102","admin","admin","22"]
    ]
#controls sleep reset after change VPN_FEC 
sleep_control = 5 

# Command reset VPN
reset_vpn_tunnel = [
        "diagnose vpn ike gateway clear name Binus-tunnel",
        "diagnose vpn tunnel down Binus-tunnel", 
        "diagnose vpn tunnel up Binus-tunnel"
        ]
# Command show status
show_status_vpn_tunnel = ["sh vpn ipsec phase1-interface "]

def push_conf(command, device_ip, device_username, device_password, device_port):
    device = {
        'device_type': "fortinet",
        'host':   device_ip,
        'username': device_username,
        'password': device_password,
        'port' : device_port,
        'conn_timeout': 15
    }
    net_connect = ConnectHandler(**device)
    time.sleep(1)
    try:
        out = net_connect.send_config_set(command, delay_factor=2)
        net_connect.disconnect()
        return f'{device["host"]} successfully configured'
    except:
        return f'{device["host"]} push config fail'

def reestablish_vpn(command, device_ip, device_username, device_password, device_port):
    device = {
        'device_type': "fortinet",
        'host':   device_ip,
        'username': device_username,
        'password': device_password,
        'port' : device_port,
        'conn_timeout': 15
    }
    net_connect = ConnectHandler(**device)
    time.sleep(1)
    try:
        out = net_connect.send_config_set(command, delay_factor=2)
        net_connect.disconnect()
        return f'{device["host"]} successfully re-establish VPN IPsec TUnnel'
    except:
        return f'{device["host"]} re-establish VPN IPsec TUnnel fail'

def get_config(command, device_ip, device_username, device_password, device_port):
    device = {
        'device_type': "fortinet",
        'host':   device_ip,
        'username': device_username,
        'password': device_password,
        'port' : device_port,
        'conn_timeout': 15
    }
    net_connect = ConnectHandler(**device)
    time.sleep(1)
    try:
        out = net_connect.send_config_set(command, delay_factor=2)
        net_connect.disconnect()
        return out
    except:
        return f'{device["host"]} push config fail'


# Define your data model
class FecParams(BaseModel):
    current_packet_loss: int

@app.get("/info-tunnel")
async def homepage():
    global fec_status
    fec_status = False
    append_output_status = []
    for device in devices_list:
        output_device = get_config(show_status_vpn_tunnel, *device)
        # Regular expression to find the fec-base and fec-redundant values
        regex = r"set fec-(base|redundant) (\d+)"
        # Function to find fec-base and fec-redundant values
        def find_fec_values(text):
            global fec_status
            matches = re.findall(regex, text)
            if matches:
                values = {f'fec-{match[0]}': int(match[1]) for match in matches}
                fec_status = True
                return values
            else:
                fec_status = False
                return "fec not enabled"
        # Find values in both texts
        result1 = find_fec_values(output_device)
        append_output_status.append(result1)
    return {"message": append_output_status, "fec_status": fec_status}
    

@app.post("/disable-fec")
async def disable_fec():
    command_set = [
        "config vpn ipsec phase1-interface",
        "edit Binus-tunnel",
        "set fec-egress disable",
        "set fec-ingress disable",
        "next",
        "end",
        "diagnose vpn ike gateway clear name Binus-tunnel", 
        "diagnose vpn tunnel down Binus-tunnel"
        ]
    append_output=[]
    append_output_reset=[]
    for device in devices_list:
        output_device = push_conf(command_set, *device)
        append_output.append(output_device)
    time.sleep(sleep_control)
    for device in devices_list:
        output_device = reestablish_vpn(reset_vpn_tunnel, *device)
        append_output_reset.append(output_device)
    return {"message": "FEC Disabled", "detail": {"config status": append_output, "re-establish status": append_output_reset}}

@app.post("/enable-fec")
async def enable_fec(data: FecParams):
    fec_base = 40
    fec_redundant = 4
    # Get data from request body
    current_packet_loss = data.current_packet_loss
    if current_packet_loss > 5 and current_packet_loss < 20:
        fec_redundant = fec_redundant * 1
    if current_packet_loss >= 20 and current_packet_loss < 30:
        fec_redundant = fec_redundant * 2 
    if current_packet_loss >= 30:
        fec_redundant = fec_redundant * 3
    command_set = [
        "config vpn ipsec phase1-interface",
        "edit Binus-tunnel","set fec-egress enable",
        "set fec-ingress enable",
        f'set fec-base {fec_base}',
        f"set fec-redundant {fec_redundant}",
        "set fec-send-timeout 8",
        "set fec-receive-timeout 5000",
        "next",
        "end",
        "diagnose vpn ike gateway clear name Binus-tunnel", 
        "diagnose vpn tunnel down Binus-tunnel"
    ]
    append_output=[]
    append_output_reset=[]
    for device in devices_list:
        output_device = push_conf(command_set, *device)
        append_output.append(output_device)
    time.sleep(sleep_control)
    for device in devices_list:
        output_device = reestablish_vpn(reset_vpn_tunnel, *device)
        append_output_reset.append(output_device)
    return {"message": f"FEC Enabled and Tailored for: Under 10% packet loss, your last packet loss is {current_packet_loss}", "params" : f"fec_base: {fec_base} fec_redundant: {fec_redundant}", "detail": append_output, "detail": {"config status": append_output, "re-establish status": append_output_reset}}