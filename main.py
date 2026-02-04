import argparse
import ipaddress
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from typing import List

import folium

TRACEROUTE_TIMEOUT = 120  # seconds
GEOIP_API_URL = "http://ip-api.com/json/{}?fields=status,lat,lon"


def geolocate_ip(ip_address):
    try:
        with urllib.request.urlopen(GEOIP_API_URL.format(ip_address), timeout=5) as resp:
            data = json.loads(resp.read())
            if data.get("status") == "success":
                return {"latitude": data["lat"], "longitude": data["lon"]}
    except (urllib.error.URLError, json.JSONDecodeError, KeyError):
        pass
    return None


def plot_route(ip_addresses):
    m = folium.Map(location=[0, 0], zoom_start=2)

    all_coordinates = []
    unique_locations = []
    step = 0

    for ip_address in ip_addresses:
        location = geolocate_ip(ip_address)
        if not location:
            continue
        coord = (location['latitude'], location['longitude'])
        all_coordinates.append(coord)
        if location not in unique_locations:
            step += 1
            unique_locations.append(location)
            folium.Marker(list(coord), popup=f"{ip_address}", tooltip=f"Step {step}").add_to(m)

    if all_coordinates:
        folium.PolyLine(all_coordinates, color='blue', weight=2.5, opacity=1).add_to(m)

    return m


def is_private_ip(ip_str: str) -> bool:
    try:
        return ipaddress.IPv4Address(ip_str).is_private
    except ipaddress.AddressValueError:
        return False


def is_valid_ipv4(ip_str: str) -> bool:
    try:
        ipaddress.IPv4Address(ip_str)
        return True
    except ipaddress.AddressValueError:
        return False


def get_ip_list(url: str) -> List[str]:
    if not shutil.which('traceroute'):
        print("Error: 'traceroute' command not found. Install it and try again.", file=sys.stderr)
        sys.exit(1)

    process = subprocess.Popen(
        ['traceroute', '-n', url],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    ip_addresses = []

    stars_max = 5
    stars_counter = 0

    try:
        for line in iter(process.stdout.readline, b''):
            line = line.decode('utf-8').strip()

            print(line)

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
                if ip_match and is_valid_ipv4(part) and not is_private_ip(part):
                    ip_address = part
                    break

            if not ip_address:
                continue

            ip_addresses.append(ip_address)
            stars_counter = 0

    finally:
        process.stdout.close()
        try:
            process.wait(timeout=TRACEROUTE_TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            print("Warning: traceroute timed out", file=sys.stderr)

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
