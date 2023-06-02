import json
import re
from typing import List

import folium
from geolite2 import geolite2
import subprocess


def geolocate_ip(ip_address):
    reader = geolite2.reader()
    location = reader.get(ip_address)
    if location is not None:
        return location['location']


def plot_route(ip_addresses):
    m = folium.Map(location=[0, 0], zoom_start=2)  # Create a map

    # Plot IP addresses and connect them with routes
    for i in range(len(ip_addresses) - 1):
        start_ip = ip_addresses[i]
        end_ip = ip_addresses[i + 1]

        start_location = geolocate_ip(start_ip)
        end_location = geolocate_ip(end_ip)

        if start_location and end_location:
            start_lat, start_lon = start_location['latitude'], start_location['longitude']
            end_lat, end_lon = end_location['latitude'], end_location['longitude']

            # Add markers for start and end points
            folium.Marker([start_lat, start_lon], popup=start_ip).add_to(m)
            folium.Marker([end_lat, end_lon], popup=end_ip).add_to(m)

            # Add a line connecting the markers
            folium.PolyLine([(start_lat, start_lon), (end_lat, end_lon)], color='blue', weight=2.5, opacity=1).add_to(m)

    return m


def get_ip_list(url: str) -> List[str]:
    command = f"traceroute -n {url}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    ip_addresses = []

    stars_max = 5
    stars_counter = 0

    for line in iter(process.stdout.readline, b''):
        line = line.decode('utf-8').strip()

        print(line)  # Print real-time output

        if "traceroute" in line:
            continue

        ip_address = None
        line_parts = line.split()

        if "* * *" in line:
            stars_counter += 1
            if stars_counter == stars_max:
                break

        for part in line_parts:
            ip_match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", part)
            if ip_match:
                ip_address = part
                break

        if not ip_address:
            continue

        ip_addresses.append(ip_address)
        stars_counter = 0

    process.stdout.close()
    process.wait()

    return ip_addresses


def main(url: str):
    # ip_addresses = get_ip_list(url)

    ip_addresses = [
        "192.168.1.1",
        "192.168.0.1",
        "84.116.254.69",
        "84.116.253.93",
        "84.116.138.85",
        "193.59.202.57",
        "194.181.92.97"
    ]

    print(f"Found IPs: {json.dumps(ip_addresses, indent=4)}")

    map_with_routes = plot_route(ip_addresses)
    map_with_routes.save(f"map_with_routes_for {url}.html")


if __name__ == '__main__':
    main('gosuslugi.ru')
