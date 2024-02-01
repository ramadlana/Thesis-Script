import re

# Sample ping output
ping_output = """
PING 202.100.100.20 (202.100.100.20): 56 data bytes
64 bytes from 202.100.100.20: icmp_seq=0 ttl=255 time=25.2 ms
64 bytes from 202.100.100.20: icmp_seq=1 ttl=255 time=31.9 ms
64 bytes from 202.100.100.20: icmp_seq=2 ttl=255 time=30.0 ms
64 bytes from 202.100.100.20: icmp_seq=3 ttl=255 time=30.6 ms
64 bytes from 202.100.100.20: icmp_seq=4 ttl=255 time=30.5 ms

--- 202.100.100.20 ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max = 25.2/29.6/31.9 ms
"""

# Regular expressions to extract the needed data
packets_regex = r'(\d+) packets transmitted, (\d+) packets received, (\d+)% packet loss'
rtt_regex = r'round-trip min/avg/max = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)'

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

print(ping_statistics)
