from netmiko import ConnectHandler
import time



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
        out = net_connect.send_config_set(command, delay_factor=1)
        net_connect.disconnect()
        return f'{device["host"]} successfully configured'
    except:
        return f'{device["host"]} push config fail'

command_disable_fec = ["config vpn ipsec phase1-interface","edit Binus-tunnel","set fec-egress disable","set fec-ingress disable","set fec-base 10","set fec-redundant 2","set fec-send-timeout 8","set fec-receive-timeout 5000","next","end","diagnose vpn ike gateway clear name Binus-tunnel"]

push_conf(command_disable_fec,"192.168.93.101","admin","admin","22")
push_conf(command_disable_fec,"192.168.93.102","admin","admin","22")

print("FEC Disabled")
