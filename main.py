import argparse
import json
import re
import subprocess
from typing import List

import folium
from geolite2 import geolite2


def geolocate_ip(ip_address):
    reader = geolite2.reader()
    location = reader.get(ip_address)
    if location is not None:
        return location['location']


def plot_route(ip_addresses):
    m = folium.Map(location=[0, 0], zoom_start=2)  # Create a map

    locations = []
    steps = 0
    # Plot IP addresses and connect them with routes
    for i, ip_address in enumerate(ip_addresses):
        location = geolocate_ip(ip_address)
        if location:
            if location not in locations:
                steps += 1
                locations.append(location)
                lat, lon = location['latitude'], location['longitude']
                folium.Marker([lat, lon], popup=f"{ip_address}", tooltip=f"Step {steps+1}").add_to(m)
            else:
                print(f"Skip location for IP {ip_address}")

    # Add lines connecting the markers
    locations = [geolocate_ip(ip) for ip in ip_addresses]
    valid_locations = [loc for loc in locations if loc is not None]
    coordinates = [(loc['latitude'], loc['longitude']) for loc in valid_locations]
    folium.PolyLine(coordinates, color='blue', weight=2.5, opacity=1).add_to(m)

    return m


def get_ip_list(url: str) -> List[str]:
    process = subprocess.Popen(
        ['traceroute', '-n', url],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

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
                if part not in ["192.168.1.1", "192.168.0.1"]:
                    ip_address = part
                    break

        if not ip_address:
            continue

        ip_addresses.append(ip_address)
        stars_counter = 0

    process.stdout.close()
    process.wait()

    return ip_addresses


def main(url: str, output_path: str = None):
    ip_addresses = get_ip_list(url)

    if not ip_addresses:
        print("No IP addresses found in traceroute")
        return

    print(f"Found IPs: {json.dumps(ip_addresses, indent=4)}")

    map_with_routes = plot_route(ip_addresses)

    if output_path is None:
        output_path = f"map_{url.replace('/', '_')}.html"

    map_with_routes.save(output_path)
    print(f"Map saved to: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Trace route to a domain and visualize the path on an interactive map'
    )
    parser.add_argument('domain', help='Domain or IP address to trace')
    parser.add_argument(
        '-o', '--output',
        help='Output HTML file path (default: map_<domain>.html)'
    )
    args = parser.parse_args()

    main(args.domain, args.output)
