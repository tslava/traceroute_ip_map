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


def main(url: str):
    command = f"traceroute -n {url}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    ip_addresses = []
    for line in iter(process.stdout.readline, b''):
        line = line.decode('utf-8').strip()
        print(line)  # Print real-time output

        if ' ' in line:
            line_parts = line.split()
            ip_address = line_parts[line_parts.index(' ') + 1]
            ip_addresses.append(ip_address)

    process.stdout.close()
    process.wait()

    map_with_routes = plot_route(ip_addresses)
    map_with_routes.save("map_with_routes.html")


if __name__ == '__main__':
    main('ya.ru')
